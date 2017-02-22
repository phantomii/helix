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

import logging

from helix.dm import events as dm_events
from helix.market import events as market_events
from helix.market import positions


LOG = logging.getLogger(__name__)


class Account(object):

    def __init__(self, engine, deposit, leverage=1):
        super(Account, self).__init__()
        self._engine = engine
        self._event_bus = engine.get_event_bus()
        self._deposit = deposit
        self._leverage = leverage
        self._positions = positions.PositionManager(
            event_bus=self._event_bus,
            instruments=engine.get_instruments())
        self._event_bus.subscribe(dm_events.OnTickEvent, self._on_tick_handler)
        self._event_bus.subscribe(market_events.OnOrderPositionFilled,
                                  self._on_filled_position_handler)
        self._event_bus.subscribe(market_events.OnTradeResult,
                                  self._on_trade_result_handler)

    def get_engine(self):
        return self._engine

    def get_deposit(self):
        return self._deposit

    def get_profit_loss(self):
        return self._positions.get_profit_loss()

    def get_equity(self):
        return self._deposit + self._positions.get_profit_loss()

    def get_margin(self):
        return 0

    def _on_filled_position_handler(self, event):
        order_position = event.order_position
        order = order_position.order
        if order is not None and order_position.order.account == self:
            self._positions.process_filled_order_position(order_position)

    def _on_tick_handler(self, event):
        # TODO(efrolov): Should check margin level here
        tick = event.get_tick()
        self._positions.on_tick(tick)

    def _on_trade_result_handler(self, event):
        trade = event.trade_result
        self._deposit += trade.get_profit_loss()
        LOG.info("Trade: %s", event.trade_result)

    def submit_order_positions(self, instrument, positions):
        # TODO(efrolov): Should check margin level here
        instrument.submit_order_positions(positions=positions)

    def __str__(self):
        return ("Account: Deposit: %.2f, Profit: %.2f, Equity: %.2f, "
                "Margin: %.2f" % (self.get_deposit(), self.get_profit_loss(),
                                  self.get_equity(), self.get_margin()))
