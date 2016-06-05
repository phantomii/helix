# Copyright (c) 2014
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import logging.config
import yaml

from oslo_config import cfg


DEFAULT_CONFIG = {
    'version': 1,
    'formatters': {
        'precise': {
            'datefmt': '%Y-%m-%d,%H:%M:%S',
            'format': '%(levelname)-7s %(asctime)15s '
                      '%(name)s:%(lineno)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'precise',
            'stream': 'ext://sys.stderr'
        },
    },
    'loggers': {
        'helix': {},
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
}


logging_opts = [
    cfg.StrOpt('config', default='logging.yaml',
               help="Logging subsystem configuration YAML file")
]

cfg.CONF.register_cli_opts(logging_opts, 'logging')


class ConfigNotFound(Exception):
    pass


def configure():
    config = cfg.CONF.logging.config
    config_file = cfg.CONF.find_file(config)

    if config_file is None:
        config_data = DEFAULT_CONFIG
    else:
        with open(config_file) as f:
            config_data = yaml.load(f)

    logging.config.dictConfig(config_data)

    if config_data == DEFAULT_CONFIG:
        logging.getLogger(__name__).warning(
            'Logging configuration %s not found - using defaults',
            config)
