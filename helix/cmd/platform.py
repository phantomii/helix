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
import sys
import time

from helix import accounts
from helix.common import config
from helix.common import log as helix_logging
from helix.dm.backtest import instruments
from helix import engines
from helix.events import bus
from helix.strategies import helix_v1


def main():
    if not config.parse(sys.argv[1:]):
        logging.warning("Unable to find configuration file via the"
                        " default search paths (~/.helix/, ~/, /etc/helix/,"
                        " /etc/) and the '--config-file' option!")
    helix_logging.configure()
    log = logging.getLogger(__name__)

    event_bus = bus.Eventbus()

    eurusd = instruments.EURUSD(
        file_path="data/EURUSD_UTC_Ticks_Bid_2013.01.01_2017.01.01.csv",
        event_bus=event_bus)

    instruments_list = engines.GroupOfHistoricalInstruments(
        instruments=[eurusd])

    engine = engines.EventEngine(event_bus=event_bus,
                                 instruments=instruments_list)

    account = accounts.Account(engine, 1000, leverage=100)
    helix_v1.HelixStrategy(account=account)

    engine.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        engine.stop()
        engine.join()
        log.info("Good bay!!!")
