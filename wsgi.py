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
import logging
import sys

from helix.api import app
from helix.common import config
from helix.common import encoding
from helix.common import log as helix_logging


if not config.parse(sys.argv[1:]):
        logging.warning("Unable to find configuration file via the"
                        " default search paths (~/.helix/, ~/, /etc/helix/,"
                        " /etc/) and the '--config-file' option!")
helix_logging.configure()
log = logging.getLogger(__name__)
encoding.set_default_encoding_from_config()

application = app.build_wsgi_application()
