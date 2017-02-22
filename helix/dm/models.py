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
from datetime import datetime

import six

from helix.market import order_books


@six.add_metaclass(abc.ABCMeta)
class Instrument(object):

    def __init__(self, event_bus, name):
        self._name = name
        self._event_bus = event_bus
        self._order_book = order_books.OrderBook(event_bus=event_bus)

    @property
    def name(self):
        return self._name

    def get_last_tick(self):
        ask = self._order_book.get_ask(default=float("inf"))
        bid = self._order_book.get_bid(default=0)
        ask_volume = len(self._order_book.get_ask_positions(ask))
        bid_volume = len(self._order_book.get_bid_positions(bid))
        return Tick(instrument=self,
                    timestamp=self.get_instrument_timestamp(),
                    ask=ask,
                    bid=bid,
                    ask_volume=ask_volume,
                    bid_volume=bid_volume)

    def submit_order_positions(self, positions):
        return self._order_book.add(positions=positions)

    @abc.abstractmethod
    def get_instrument_timestamp(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def on_loop(self, engine):
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate_profit_loss(self, points, amount=1):
        raise NotImplementedError()

    def __str__(self):
        return "Instrument: %s" % self.name


class Tick(object):

    def __init__(self, instrument, timestamp, ask,
                 bid, ask_volume, bid_volume):
        self._instrument = instrument
        self._timestamp = timestamp
        self._ask = ask
        self._bid = bid
        self._ask_volume = ask_volume
        self._bid_volume = bid_volume

    @property
    def instrument(self):
        return self._instrument

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def ask(self):
        return self._ask

    @property
    def bid(self):
        return self._bid

    @property
    def ask_volume(self):
        return self._ask_volume

    @property
    def bid_volume(self):
        return self._bid_volume

    @property
    def datetime(self):
        return datetime.utcfromtimestamp(self.timestamp)

    def __str__(self):
        return "Tick: dt=%s, ask=%.5f(%d), bid=%.5f(%d)" % (
            self.datetime.strftime('%Y-%m-%d %H:%M:%S'), self.ask,
            self.ask_volume, self.bid, self.bid_volume)


SUPER_HIGHT_TICK = Tick(instrument=None, timestamp=0,
                        ask=float("inf"), bid=float("inf"),
                        ask_volume=0, bid_volume=0)
SUPER_LOW_TICK = Tick(instrument=None, timestamp=0,
                      ask=float("-inf"), bid=float("-inf"),
                      ask_volume=0, bid_volume=0)


class Bar(object):

    def __init__(self, ticks, period):
        if len(ticks) < 1:
            raise ValueError("Count of ticks should be greater than zero")
        self._open = ticks[0]
        self._close = ticks[-1]
        self._hight = SUPER_LOW_TICK
        self._low = SUPER_HIGHT_TICK

        self._instrument = ticks[0].instrument
        self._period = period

        for tick in ticks:
            if self._instrument != tick.instrument:
                raise ValueError("Invalid instrument %s value on tick %s. "
                                 "Should be %s" % (
                                     tick.instrument, tick, self._instrument))
            if tick.ask > self._hight.ask:
                self._hight = tick
            if tick.bid < self._low.bid:
                self._low = tick

    @property
    def instrument(self):
        self._instrument

    @property
    def open(self):
        return self._open

    @property
    def close(self):
        return self._close

    @property
    def hight(self):
        return self._hight

    @property
    def low(self):
        return self._low

    @property
    def period(self):
        return self._period
