# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2015 Eugene Frolov <eugene@frolov.net.ru>
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

import copy


class HelixBaseException(Exception):
    _msg_template = "Unknown error"

    def __init__(self, **kwargs):
        super(HelixBaseException, self).__init__()
        self._kwargs = kwargs

    def __str__(self):
        return self._msg_template % self._kwargs

    @property
    def message_template(self):
        return self._msg_template

    @property
    def kwargs(self):
        return copy.deepcopy(self._kwargs)
