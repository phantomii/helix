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
import uuid

import six

from helix.market import events


BUY = "BUY"
SELL = "SELL"


@six.add_metaclass(abc.ABCMeta)
class AbstractOrderPosition(object):

    def __init__(self, price, order=None):
        super(AbstractOrderPosition, self).__init__()
        self._order = order
        self._price = price
        self._contractor = None

    @property
    def order(self):
        return self._order

    @property
    def price(self):
        return self._price

    @property
    def contractor(self):
        return self._contractor

    @abc.abstractproperty
    def amount(self):
        raise NotImplementedError()

    def set_contragent(self, position, price):
        self._contractor = position
        self._price = price


class SellOrderPosition(AbstractOrderPosition):

    @property
    def amount(self):
        return -1


class BuyOrderPosition(AbstractOrderPosition):

    @property
    def amount(self):
        return 1


@six.add_metaclass(abc.ABCMeta)
class AbstractOrder(object):

    CREATED = 'CREATED'
    SUBMITTED = 'SUBMITTED'
    PARTIALLY_FILLED = 'PARTIALLY FILLED'
    FILLED = 'FILLED'
    CANCELED = 'CANCELED'
    REJECTED = 'REJECTED'

    def __init__(self, account, instrument, price, amount):
        super(AbstractOrder, self).__init__()
        self._order_id = uuid.uuid4()
        self._account = account
        self._instrument = instrument
        self._price = price
        self._amount = amount
        self._submited_order_positions = []
        self._canceled_order_positions = []
        self._rejected_reason = None

        event_bus = self._account.get_engine().get_event_bus()
        event_bus.subscribe(events.OnOrderPositionSubmitted,
                            self._on_order_position_handler)
        event_bus.subscribe(events.OnOrderPositionFilled,
                            self._on_order_position_handler)

        order_positions = self._gen_order_positions()

        self._account.submit_order_positions(instrument=self._instrument,
                                             positions=order_positions)

    def _on_order_position_handler(self, event):
        order_position = event.order_position
        if order_position.order == self:
            if order_position not in self._submited_order_positions:
                self._submited_order_positions.append(order_position)

    @property
    def account(self):
        return self._account

    @property
    def instrument(self):
        return self._instrument

    @property
    def price(self):
        price = 0
        positions = self._submited_order_positions[:]
        if positions:
            for position in positions:
                price += position.price
            return price / len(positions)
        return self._price

    def get_reject_reason(self):
        return self._rejected_reason

    def get_status(self):
        if self._rejected_reason:
            return AbstractOrder.REJECTED
        elif (len(self._submited_order_positions +
                  self._canceled_order_positions) < self._amount):
            return AbstractOrder.CREATED
        elif self._canceled_order_positions:
            return AbstractOrder.CANCELED
        else:
            without_contractor = len(filter(lambda p: p.contractor is None,
                                            self._submited_order_positions))
            if without_contractor == self._amount:
                return AbstractOrder.SUBMITTED
            elif without_contractor == 0:
                return AbstractOrder.FILLED
            else:
                return AbstractOrder.PARTIALLY_FILLED

    @abc.abstractproperty
    def __ORDER_POSITION_CLASS__(self):
        raise NotImplementedError()

    def _gen_order_positions(self):
        return [self.__ORDER_POSITION_CLASS__(
            price=self._price,
            order=self) for x in xrange(self._amount)]


class BuyLimitOrder(AbstractOrder):

    __ORDER_POSITION_CLASS__ = BuyOrderPosition


class SellLimitOrder(AbstractOrder):

    __ORDER_POSITION_CLASS__ = SellOrderPosition


__ALL__ = [BuyLimitOrder, SellLimitOrder]
