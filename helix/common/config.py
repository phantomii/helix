#!/usr/bin/env python
# Copyright (c) 2014 Eugene Frolov <efrolov@mirantis.com>
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

import sys

from oslo_config import cfg

from helix import version


common_cli_opts = [
    cfg.BoolOpt('debug',
                short='d',
                default=False,
                help=('Print debugging output (set logging level to '
                      'DEBUG instead of default WARNING level).')),
    cfg.BoolOpt('verbose',
                short='v',
                default=False,
                help=('Print more verbose output (set logging level to '
                      'INFO instead of default WARNING level).'))
]


# Register the configuration options
cfg.CONF.register_cli_opts(common_cli_opts)


def parse(args):
    cfg.CONF(args=args, project='helix',
             version='%%prog %s' % version.version_info.release_string())
    return cfg.CONF.config_file


class ConfigFileIsntDefined(Exception):
    pass


def parse_or_die(args=[]):
    if not parse(args):
        raise ConfigFileIsntDefined()


def parse_sys_args_or_die():
    return parse_or_die(sys.argv[1:])
