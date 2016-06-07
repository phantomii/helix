# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2016 Eugene Frolov <eugene@frolov.net.ru>
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

import uuid

import sqlalchemy as sa
from sqlalchemy.ext import declarative
from sqlalchemy import orm


Base = declarative.declarative_base()


class Broker(Base):
    __tablename__ = 'brokers'

    uuid = sa.Column(sa.String(36), primary_key=True,
                     default=lambda: uuid.uuid4())
    name = sa.Column(sa.String(72), index=True, nullable=False, unique=True)

    def __init__(self, name):
        super(Broker, self).__init__()
        self.name = name


class Instrument(Base):
    __tablename__ = 'instruments'

    uuid = sa.Column(sa.String(36), primary_key=True,
                     default=lambda: uuid.uuid4())
    _broker_uuid = sa.Column(sa.String(36), sa.ForeignKey(Broker.uuid),
                             nullable=False)
    broker = orm.relationship(Broker)
    name = sa.Column(sa.String(25), nullable=False, unique=False)
    ticker_symbol = sa.Column(sa.String(10), nullable=False, unique=False,
                              index=True)
    digits = sa.Column(sa.Integer, nullable=False)

    __table_args__ = (
        sa.UniqueConstraint('uuid', 'ticker_symbol'),)

    def __init__(self, broker, ticker_symbol, name, digits):
        super(Instrument, self).__init__()
        self.broker = broker
        self.ticker_symbol = ticker_symbol
        self.name = name
        self.digits = digits


class Tick(Base):
    __tablename__ = 'ticks'

    uuid = sa.Column(sa.String(36), primary_key=True,
                     default=lambda: uuid.uuid4())
    timestamp = sa.Column(sa.REAL, nullable=False, index=True)
    _instrument_uuid = sa.Column(sa.String(36), sa.ForeignKey(Instrument.uuid),
                                 nullable=False)
    instrument = orm.relationship(Instrument)
    ask = sa.Column(sa.Float, nullable=False, index=True)
    bid = sa.Column(sa.Float, nullable=False, index=True)
    ask_volume = sa.Column(sa.Float)
    bid_volume = sa.Column(sa.Float)

    def __init__(self, instrument, timestamp, ask, bid, ask_volume=None,
                 bid_volume=None):
        super(Tick, self).__init__()
        self.timestamp = timestamp
        self.instrument = instrument
        self.ask = ask
        self.bid = bid
        self.ask_volume = ask_volume
        self.bid_volume = bid_volume
