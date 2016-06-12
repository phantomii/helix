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

encoding_opts = [
    cfg.StrOpt('system-encoding', default='utf-8',
               help="Default encoding for all strings")
]


CONF = cfg.CONF
CONF.register_opts(encoding_opts)


def set_default_encoding_from_config():
    # NOTE(Eugene Frolov): setdefaultencoding function is only
    # available at Python start-up time, when Python scans the
    # environment. It has to be called in a system-wide module,
    # after this module has been evaluated, the
    # setdefaultencoding() function is removed from the sys module.
    # see bellow articles for more information
    # http://www.ianbicking.org/illusive-setdefaultencoding.html
    # http://stackoverflow.com/questions/3828723/why-we-need-sys-
    # setdefaultencodingutf-8-in-a-py-script
    reload(sys)
    sys.setdefaultencoding(CONF.system_encoding)
