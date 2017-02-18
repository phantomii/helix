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

from helix.dm import events
from helix.dm import instruments
from helix.events import base
from helix.market import orders
from helix.streams import csvs


class EURUSD(instruments.EURUSD):

    def __init__(self, event_bus, file_path, default_volume=100):
        super(EURUSD, self).__init__(event_bus=event_bus)
        self._stream_reader = csvs.TickStreamReader(file_path=file_path)
        self._tick_generator = self._stream_reader.stream()
        self._last_time_stamp = 0
        self._tick_info = next(self._tick_generator)
        self._default_volume = default_volume
        self._bid_order_positions = []
        self._ask_order_positions = []
        self._load_next_tick()

    def get_instrument_timestamp(self):
        return self._last_time_stamp

    def get_next_tick_info(self):
        return self._tick_info

    def _load_next_tick(self):
        self._last_time_stamp = self._tick_info.timestamp

        self._order_book.remove(self._bid_order_positions)
        self._order_book.remove(self._ask_order_positions)

        self._bid_order_positions = [
            orders.BuyOrderPosition(price=self._tick_info.bid)
            for i in xrange(self._default_volume)]
        self._ask_order_positions = [
            orders.SellOrderPosition(price=self._tick_info.ask)
            for i in xrange(self._default_volume)]

        self._order_book.add(positions=self._bid_order_positions)
        self._order_book.add(positions=self._ask_order_positions)

        self._tick_info = next(self._tick_generator)

        return self.get_last_tick()

    def on_loop(self):
        try:
            tick = self._load_next_tick()
            self._event_bus.fire(events.OnTickEvent(tick=tick))
        except StopIteration:
            self._stream_reader.close()
            self._event_bus.fire(base.OnStopEngine())
