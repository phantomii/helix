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
import traceback

from restalchemy.api import middlewares
import six

from helix import contexts
from helix import security


class HelixContextMiddleware(middlewares.ContextMiddleware):

    def process_request(self, req):
        ctx = contexts.Context()
        req.context = ctx
        result = req.get_response(self.application)
        ctx.release()
        return result


class LoggingMiddleware(middlewares.Middleware):
    """API logging middleware."""

    def __init__(self, application, logger_name=__name__):
        super(LoggingMiddleware, self).__init__(application)
        self.logger = logging.getLogger(logger_name)

    def process_request(self, req):
        req_chunk = self._request_chunk(req)
        headers = security.make_secure_headers(dict(req.headers))
        self.logger.info('API > %s %s %s',
                         req_chunk,
                         self._headers_chunk(headers),
                         req.body)
        try:
            res = req.get_response(self.application)
            # XXX(Eugeny Flolov):
            # :py:method:`middlewares.ContextMiddleware#process_response`
            # unreachable if
            # :py:method:`middlewares.ContextMiddleware#process_request`
            # returns response.
            self.logger.info('API < %s %s %s %s',
                             res.status_code,
                             self._request_chunk(req),
                             self._headers_chunk(res.headers),
                             res.body)
            return res
        except Exception:
            e_type, e_value, e_tb = sys.exc_info()
            e_file, e_lineno, e_fn, e_line = traceback.extract_tb(e_tb)[-1]
            self.logger.error('API Error %s %s %s %s:%s:%s> %s',
                              req_chunk,
                              e_type,
                              e_value,
                              e_file, e_lineno, e_fn, e_line)
            six.reraise(e_type, e_value, e_tb)

    @staticmethod
    def _request_chunk(req):
        return '%s %s' % (req.method, req.url)

    @staticmethod
    def _headers_chunk(headers):
        return ['%s: %s' % (h, headers[h]) for h in headers]


# class ErrorHandlingMiddleware(middlewares.Middleware):

#     def process_request(self, req):
#         try:
#             return req.get_response(self.application)
#         except Exception as e:
#             LOG.exception("An exception %(exc_module)s.%(exc_class)s "
#                           "occurred",
#                           {"exc_module": type(e).__module__,
#                            "exc_class": type(e).__name__})
#             status, body, content_type = exceptions.get_api_representation(
#                 e, i18n.get_locale_from_request(req))
#             return req.ResponseClass(status=status, body=body,
#                                      content_type=content_type)
