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

from sqlachemy import orm as sa_orm
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Broker(Base):
    __tablename__ = "brokers"

    uuid = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(128), index=True, unique=True)


class Instrument(Base):
    __tablename__ = 'instruments'

    uuid = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(max_size=128), index=True)
    brocker_uuid = sa.Column(sa.String(36), index=True)

    __table_args__ = (sa.UniqueConstraint('name', 'brocker_uuid'),)


class Tick(Base):
    __tablename__ = 'ticks'

    timestamp = sa.Column(sa.Float, primary_key=True)
    instrument_uuid = sa.Column(sa.String(max_size=36),
                                sa.ForeignKey(Instrument.uuid))
    ask = sa.Column(sa.Float, index=True)
    bid = sa.Column(sa.Float, index=True)
    ask_volume = sa.Column(sa.Float)
    bid_volume = sa.Column(sa.Float)

    instrument = sa_orm.relationship(Instrument)


class Bar(Base):
    __tablename__ = 'bars'

    open_tick_ts = sa.Column(sa.Float, sa.ForeignKey(Tick.timestamp))
    high_tick = sa.Column(sa.Float, sa.ForeignKey(Tick.timestamp))
    low_tick = sa.Column(sa.Float, sa.ForeignKey(Tick.timestamp))
    close_tick = sa.Column(sa.Float, sa.ForeignKey(Tick.timestamp))
