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

import copy

import sortedcontainers

from helix.market import events


class NoQuotas(Exception):
    pass


class OrderBook(object):

    def __init__(self, event_bus):
        super(OrderBook, self).__init__()
        self._event_bus = event_bus
        self._ask_positions = sortedcontainers.SortedDict()
        self._bid_positions = sortedcontainers.SortedDict()

    def get_ask(self, default=None):
        try:
            return self._ask_positions.iloc[0]
        except IndexError:
            if default is None:
                raise NoQuotas()
            return default

    def get_bid(self, default=None):
        try:
            return self._bid_positions.iloc[-1]
        except IndexError:
            if default is None:
                raise NoQuotas()
            return default

    def add(self, positions):
        for position in positions:
            if position.amount < 0:
                bid_price = self.get_bid(default=0)
                if position.price > bid_price:
                    try:
                        self._ask_positions[position.price].append(position)
                    except KeyError:
                        self._ask_positions[position.price] = [position]
                    self._event_bus.fire(events.OnOrderPositionSubmitted(
                        order_position=position))
                else:
                    bid_position = self._bid_positions[bid_price].pop(0)
                    position.set_contragent(bid_position, price=bid_price)
                    bid_position.set_contragent(position, price=bid_price)
                    self._event_bus.fire(events.OnOrderPositionFilled(
                        order_position=bid_position))
                    self._event_bus.fire(events.OnOrderPositionFilled(
                        order_position=position))
                    if len(self._bid_positions[bid_price]) == 0:
                        del self._bid_positions[bid_price]
            else:
                ask_price = self.get_ask(default=float("inf"))
                if position.price < ask_price:
                    try:
                        self._bid_positions[position.price].append(position)
                    except KeyError:
                        self._bid_positions[position.price] = [position]
                    self._event_bus.fire(events.OnOrderPositionSubmitted(
                        order_position=position))
                else:
                    ask_position = self._ask_positions[ask_price].pop(0)
                    position.set_contragent(ask_position, price=ask_price)
                    ask_position.set_contragent(position, price=ask_price)
                    self._event_bus.fire(events.OnOrderPositionFilled(
                        order_position=ask_position))
                    self._event_bus.fire(events.OnOrderPositionFilled(
                        order_position=position))
                    if len(self._ask_positions[ask_price]) == 0:
                        del self._ask_positions[ask_price]

    def remove(self, positions):
        result = []
        for position in positions:
            selected = (self._bid_positions if position.amount > 0 else
                        self._ask_positions)
            try:
                selected[position.price].remove(position)
                if len(selected[position.price]) == 0:
                    del selected[position.price]
            except (KeyError, ValueError):
                result.append(position)
        return result

    def get_ask_positions(self, price):
        return copy.copy(self._ask_positions.get(price, []))

    def get_bid_positions(self, price):
        return copy.copy(self._bid_positions.get(price, []))
