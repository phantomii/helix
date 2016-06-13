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

from oslo_config import cfg
from tavrida import client
from tavrida import config
from tavrida import discovery
from tavrida import entry_point


connection_group = cfg.OptGroup(
    name='amqp',
    title='General RabbitMQ connection config')


connection_opts = [
    cfg.StrOpt('host', help='RabbitMQ host', required=True),
    cfg.StrOpt('username', help='RabbitMQ username', required=True),
    cfg.StrOpt('password', help='RabbitMQ password', required=True),
    cfg.IntOpt('port', help='RabbitMQ port', required=True, default=5672),
    cfg.StrOpt('virtual_host', help='RabbitMQ virtual host', required=True,
               default="/"),
    cfg.IntOpt('heartbeat_interval', help='RabbitMQ heartbeat interval (secs)',
               required=True,
               default=10),
    cfg.IntOpt('connection_attempts',
               help='RabbitMQ connection attempts number', required=True,
               default=3),
    cfg.IntOpt('channel_max', help='RabbitMQ maximum channel count value'),
    cfg.IntOpt('frame_max', help='The maximum byte size for an AMQP frame'),
    cfg.FloatOpt('retry_delay', help='RabbitMQ connection retry delay',
                 required=True, default=1.0),
    cfg.FloatOpt('socket_timeout', help='RabbitMQ socket timeout',
                 required=True, default=3.0),
    cfg.StrOpt('locale', help='RabbitMQ locale value'),
    cfg.BoolOpt('backpressure_detection', help='Toggle RabbitMQ backpressure '
                                               'detection'),
    cfg.IntOpt('reconnect_attempts', help='Attempts to reconnect to RabbitMQ',
               required=True, default=-1),
    cfg.BoolOpt('async_engine', help='Use async server engine', required=True,
                default=False)
]


helix_api_opts = [
    cfg.StrOpt("service_name", default="api",
               help="Service name in AMQP messages"),
    cfg.StrOpt("notification_exchange", default="api_notifications",
               help=("An exchange for notifications from API to "
                     "another services"))
]


CONF = cfg.CONF

CONF.register_group(connection_group)
CONF.register_opts(connection_opts, connection_group)
CONF.register_opts(helix_api_opts, 'api')


_amqp_client = {}


def factory_amqp_client(event_name):

    credentials = config.Credentials(username=CONF.amqp.username,
                                     password=CONF.amqp.password)

    source = entry_point.Source(service_name=CONF.api.service_name,
                                method_name=event_name)

    disc = discovery.LocalDiscovery()
    disc.register_local_publisher(service_name=CONF.api.service_name,
                                  exchange_name=CONF.api.notification_exchange)

    conn_conf = config.ConnectionConfig(
        host=CONF.amqp.host,
        credentials=credentials,
        port=CONF.amqp.port,
        virtual_host=CONF.amqp.virtual_host,
        channel_max=CONF.amqp.channel_max,
        frame_max=CONF.amqp.frame_max,
        heartbeat_interval=CONF.amqp.heartbeat_interval,
        ssl=False,
        ssl_options=None,
        connection_attempts=CONF.amqp.connection_attempts,
        retry_delay=CONF.amqp.retry_delay,
        socket_timeout=CONF.amqp.socket_timeout,
        locale=CONF.amqp.locale,
        backpressure_detection=CONF.amqp.backpressure_detection,
        reconnect_attempts=CONF.amqp.reconnect_attempts,
        async_engine=CONF.amqp.async_engine
    )

    cli = client.RPCClient(config=conn_conf, discovery=disc, source=source)
    return cli


def get_client_by_event(event_name):
    if event_name not in _amqp_client:
        _amqp_client[event_name] = factory_amqp_client(event_name)
    return _amqp_client[event_name]
