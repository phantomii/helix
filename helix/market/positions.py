# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2017 Eugene Frolov <eugene@frolov.net.ru>
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc
import logging

import six

from helix.market import events


LOG = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class AbstractTradeResult(object):

    def __init__(self, open_price, close_price, instrument):
        super(AbstractTradeResult, self).__init__()
        self._open_price = open_price
        self._close_price = close_price
        self._instrument = instrument

    @property
    def instrument(self):
        return self._instrument

    @property
    def open_price(self):
        return self._open_price

    @property
    def close_price(self):
        return self._close_price

    @abc.abstractmethod
    def get_profit_loss_in_points(self):
        raise NotImplementedError()

    def get_profit_loss(self):
        return self._instrument.calculate_profit_loss(
            self.get_profit_loss_in_points())

    def __str__(self):
        return "%s: op: %.5f, cp: %.5f, profit: %.2f" % (
            type(self).__name__,
            self.open_price,
            self.close_price,
            self.get_profit_loss())


class SellTradeResult(AbstractTradeResult):

    def get_profit_loss_in_points(self):
        return self._open_price - self._close_price


class BuyTradeResult(AbstractTradeResult):

    def get_profit_loss_in_points(self):
        return self._close_price - self._open_price


class Position(object):

    def __init__(self, event_bus, instrument):
        super(Position, self).__init__()
        self._event_bus = event_bus
        self._instrument = instrument
        self._open_price = 0
        self._amount = 0
        self._current_price = 0

    @property
    def open_price(self):
        if self.amount == 0:
            return 0
        return self._open_price

    @property
    def current_price(self):
        return self._current_price

    @property
    def amount(self):
        return self._amount

    def _calculate_new_current_price(self, price):
        return ((self.open_price * self.amount) + (price)) / (
            self._amount + 1)

    def _process_sell_order_position(self, order_position):
        if self.amount < 0:
            new_price = self._calculate_new_current_price(order_position.price)
            self._open_price = new_price
            self._amount -= 1
        elif self.amount > 0:
            self._event_bus.fire(events.OnTradeResult(
                BuyTradeResult(open_price=self._open_price,
                               close_price=order_position.price,
                               instrument=self._instrument)))
            self._amount -= 1
        else:
            ValueError("Invalid position amount. Amount is %d. Should not be "
                       "0.", order_position.amount)

    def _process_buy_order_position(self, order_position):
        if self.amount > 0:
            new_price = self._calculate_new_current_price(order_position.price)
            self._open_price = new_price
            self._amount += 1
        elif self.amount < 0:
            self._event_bus.fire(events.OnTradeResult(
                SellTradeResult(open_price=self._open_price,
                                close_price=order_position.price,
                                instrument=self._instrument)))
            self._amount += 1
        else:
            ValueError("Invalid position amount. Amount is %d. Should not be "
                       "0.", order_position.amount)

    def process_order_position(self, order_position):
        if self.amount == 0:
            self._open_price = order_position.price
            self._amount = order_position.amount
        elif order_position.amount == 1:
            self._process_buy_order_position(order_position)
        elif order_position.amount == -1:
            self._process_sell_order_position(order_position)
        else:
            raise ValueError("Invalid order position amount. Amount is %d",
                             order_position.amount)

    def on_tick(self, tick):
        if self.amount > 0:
            self._current_price = tick.bid
        else:
            self._current_price = tick.ask

    def get_profit_loss(self):
        return self._instrument.calculate_profit_loss(
            points=self._current_price - self._open_price,
            amount=self.amount)


class PositionManager(object):

    def __init__(self, event_bus, instruments):
        super(PositionManager, self).__init__()
        self._event_bus = event_bus
        self._positions = {i.name: Position(event_bus, i) for i in instruments}

    def on_tick(self, tick):
        instrument = tick.instrument
        self._positions[instrument.name].on_tick(tick)

    def process_filled_order_position(self, order_position):
        instrument = order_position.order.instrument
        self._positions[instrument.name].process_order_position(order_position)

    def get_profit_loss(self):
        profit = 0
        for position in self._positions.values():
            profit += position.get_profit_loss()
        return profit
