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

from helix.market import orders
from helix.strategies import base


LOG = logging.getLogger(__name__)


class HelixStrategy(base.Strategy):

    def on_start(self):
        LOG.debug("Helix strategy started")
        LOG.info("Submit Limit Orders")
        instrument = self._engine.get_instrument(name="EUR/USD")
        self.buy = orders.BuyLimitOrder(account=self._account,
                                        instrument=instrument,
                                        price=1.32,
                                        amount=1)
        self.sell = orders.SellLimitOrder(account=self._account,
                                          instrument=instrument,
                                          price=1.32114,
                                          amount=1)

    def on_stop(self):
        LOG.debug("Helix strategy stopped")

    def on_tick(self, tick):
        LOG.debug("Tick received %s", tick)
        LOG.info("BuyLimitOrder status is %s, price is %.5f",
                 self.buy.get_status(), self.buy.price)
        LOG.info("SellLimitOrder status is %s, price is %.5f",
                 self.sell.get_status(), self.sell.price)
