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

from helix.dm import events as dm_events
from helix.market import events as market_events
from helix.market import positions


class Account(object):

    def __init__(self, engine, deposit, leverage=1):
        super(Account, self).__init__()
        self._engine = engine
        self._deposit = deposit
        self._leverage = leverage
        self._positions = positions.PositionManager(
            instruments=engine.get_instruments())
        self._engine.subscribe(dm_events.OnTickEvent, self._on_tick_handler)

    def get_engine(self):
        return self._engine

    def _on_tick_handler(self, engine, event):
        tick = event.get_tick()
        self._positions.on_tick(tick=tick)

    def submit_order_positions(self, instrument, positions):
        # TODO(efrolov): Should check margin level here
        processed_positions = instrument.submit_order_positions(
            positions=positions)
        if processed_positions.submitted_positions:
            self._engine.fire(market_events.OnOrderPositionsSubmitted(
                order_positions=processed_positions.submitted_positions))
        if processed_positions.filled_positions:
            # self._positions.add_filled_positions(
            #     order_positions=processed_positions.filled_positions)
            self._engine.fire(market_events.OnOrderPositionsFilled(
                order_positions=processed_positions.filled_positions))
