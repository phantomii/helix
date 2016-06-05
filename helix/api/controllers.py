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

from restalchemy.api import controllers
from restalchemy.api import resources

from helix.dm import models
from helix import version


class Controller(controllers.Controller):

    def _add_filter_to_query(self, query, model, kwargs):
        if kwargs:
            for name, value in kwargs.items():
                attr = getattr(model, name, None)
                if attr:
                    query = query.filter(attr == value)
        return query


class Version(controllers.Controller):
    """This controller which handles "/" url."""

    def filter(self):
        return [version.API_VERSION]


class Collection(controllers.Controller):
    """This controller which handles "/v1/" url."""

    def filter(self):
        return ['brokers', 'quotas']


class Broker(Controller):
    __resource__ = resources.ResourceBySAModel(models.Broker)

    def create(self, **kwargs):
        ctx = self.get_context()
        broker = self.model(**kwargs)
        ctx.session.add(broker)
        ctx.session.commit()
        return broker

    def filter(self, **kwargs):
        ctx = self.get_context()
        query = ctx.session.query(self.model)
        query = self._add_filter_to_query(query, self.model, kwargs)
        brokers = query.all()
        return brokers

    def get(self, uuid):
        ctx = self.get_context()
        broker = ctx.session.query(self.model).filter(
            self.model.uuid == uuid).one()
        return broker

    def delete(self, uuid):
        ctx = self.get_context()
        broker = self.get(uuid)
        ctx.session.delete(broker)
        ctx.session.commit()

    def update(self, uuid, name):
        ctx = self.get_context()
        broker = self.get(uuid)
        broker.name = name
        ctx.session.commit()
        return broker


class Instrument(Controller):
    __resource__ = resources.ResourceBySAModel(models.Instrument)

    def create(self, parent_resource, **kwargs):
        ctx = self.get_context()
        instrument = self.model(broker=parent_resource, **kwargs)
        ctx.session.add(instrument)
        ctx.session.commit()
        return instrument

    def get(self, parent_resource, uuid):
        ctx = self.get_context()
        instrument = ctx.session.query(self.model).filter(
            self.model.uuid == uuid,
            self.model.broker == parent_resource).one()
        return instrument

    def filter(self, parent_resource, **kwargs):
        ctx = self.get_context()
        query = ctx.session.query(self.model)
        query = self._add_filter_to_query(query, self.model, kwargs)
        instruments = query.all()
        return instruments

    def delete(self, uuid):
        ctx = self.get_context()
        instrument = self.get(uuid)
        ctx.session.delete(instrument)
        ctx.session.commit()


class Tick(controllers.Controller):
    __resource__ = resources.ResourceBySAModel(models.Tick)

    def create(self, parent_resource, **kwargs):
        ctx = self.get_context()
        tick = self.model(instrument=parent_resource, **kwargs)
        ctx.session.add(tick)
        ctx.session.commit()
        return tick

    def get(self, parent_resource, uuid):
        ctx = self.get_context()
        tick = ctx.session.query(self.model).filter(
            self.model.uuid == uuid,
            self.model.instrument == parent_resource).one()
        return tick
