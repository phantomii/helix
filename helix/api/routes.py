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

from restalchemy.api import routes

from helix.api import controllers


class Tick(routes.Route):
    __controller__ = controllers.Tick
    __allow_methods__ = [routes.GET, routes.CREATE]


class Instrument(routes.Route):
    __controller__ = controllers.Instrument
    __allow_methods__ = [routes.CREATE, routes.GET, routes.FILTER,
                         routes.DELETE]

    ticks = routes.route(Tick, resource_route=True)


class Broker(routes.Route):
    __controller__ = controllers.Broker
    __allow_methods__ = [routes.CREATE, routes.GET, routes.FILTER,
                         routes.DELETE, routes.UPDATE]

    instruments = routes.route(Instrument, resource_route=True)


class V1(routes.Route):
    __controller__ = controllers.Collection
    __allow_methods__ = [routes.FILTER]

    brokers = routes.route(Broker)
