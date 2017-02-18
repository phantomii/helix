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


class PositionResult(object):

    def __init__(self, buy_order_position, sell_order_position):
        super(PositionResult, self).__init__()
        self._buy_order_position = buy_order_position
        self._sell_order_position = sell_order_position

    @property
    def instrument(self):
        return self._buy_order_position.order.instrument

    @property
    def open_price(self):
        return self._open_price

    @property
    def close_price(self):
        return self._close_price

    def get_profit_loss_in_pips(self):
        raise NotImplementedError()


class Position(object):

    def __init__(self, instrument):
        super(Position, self).__init__()
        self._instrument = instrument
        self._sell_positions = []
        self._buy_positions = []
        self._current_price = 0

    @property
    def open_price(self):
        return self._open_price

    @property
    def current_price(self):
        return self._current_price

    @property
    def amount(self):
        return len(self._buy_positions) - len(self._sell_positions)

    def add_position(self, order_position):
        if order_position.amount == 1:
            self._buy_positions.append(order_position)
        elif order_position.amount == -1:
            self._sell_positions.append(order_position)
        else:
            raise ValueError("Invalid order position amount. Amount is %d",
                             order_position.amount)


class PositionManager(object):

    def __init__(self, event_bus, instruments):
        super(PositionManager, self).__init__()
        self._event_bus = event_bus
        self._positions = {i.name: Position(i) for i in instruments}

    def on_tick(self, tick):
        pass

    def add_filled_positions(self, order_positions):
        for order_position in order_positions:
            instrument_name = order_position.order.instrument.name
            self._positions[instrument_name].add_position(
                order_position=order_position)
