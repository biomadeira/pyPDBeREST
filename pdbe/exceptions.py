#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    pyPDBeREST: A wrapper for the PDBe REST API.
    Copyright (C) 2015  Fábio Madeira

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from config import ensembl_http_status_codes


class EnsemblRestError(Exception):
    """
        Generic error class, catch-all for most EnsemblRest issues.
        Special cases are handled by EnsemblRestRateLimitError and EnsemblRestServiceUnavailable.
    """

    def __init__(self, msg, error_code=None, rate_reset=None, rate_limit=None, rate_remaining=None):
        self.error_code = error_code

        if error_code is not None and error_code in ensembl_http_status_codes:
            msg = 'EnsEMBL REST API returned a %s (%s), %s' % \
                  (error_code, ensembl_http_status_codes[error_code][0], msg)

        super(EnsemblRestError, self).__init__(msg)

    @property
    def msg(self):
        return self.args[0]


class EnsemblRestRateLimitError(EnsemblRestError):
    """
        Raised when you've hit a rate limit.
        The amount of seconds to retry your request in will be appended to the message.
    """

    def __init__(self, msg, error_code, rate_reset=None, rate_limit=None, rate_remaining=None):
        if isinstance(rate_limit, int):
            msg = '%s (Rate limit hit:  %d seconds)' % (msg, rate_reset, rate_limit, rate_remaining)
        EnsemblRestError.__init__(self, msg, error_code=error_code)


class EnsemblRestServiceUnavailable(EnsemblRestError):
    """
        Raised when the service is down.
    """
    pass
