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

# import system modules
import re
import json
import time
import logging
import requests

# import pdberest modules
from .config import (default_url, api_endpoints, http_status_codes,
                     user_agent, content_type)
from .exceptions import RestError, RestRateLimitError, RestServiceUnavailable

# Logger instance
logger = logging.getLogger(__name__)

__version__ = "0.1.0"


# PDBe REST API object
class pyPDBeREST(object):
    # class initialisation function
    def __init__(self, **kwargs):
        # read args variable into object as session_args
        self.session_args = kwargs or {}

        # In order to rate limiting the requests
        self.reqs_per_sec = 15
        self.req_count = 0
        self.last_req = 0
        # request response object
        self.response = None

        # initialise default values
        default_base_url = default_url
        default_headers = user_agent
        default_content_type = content_type
        default_proxies = {}
        default_method = 'GET'
        default_pretty_json = True

        # make these attributes public
        self.version = __version__
        self.base_url = default_url
        self.pretty_json = default_pretty_json

        # set default values if not client arguments
        if 'base_url' not in self.session_args:
            self.session_args['base_url'] = default_base_url
        if 'headers' not in self.session_args:
            self.session_args['headers'] = default_headers
        elif 'User-Agent' not in self.session_args['headers']:
            self.session_args['headers'].update(default_headers)
        elif 'Content-Type' not in self.session_args['headers']:
            self.session_args['headers'].update(default_content_type)
        if 'proxies' not in self.session_args:
            self.session_args['proxies'] = default_proxies
        if 'method' not in self.session_args:
            self.session_args['method'] = default_method
        if 'pretty_json' not in self.session_args:
            self.session_args['pretty_json'] = default_pretty_json

        # setup requests session
        self.session = requests.Session()

        # update requests client with arguments
        client_args_copy = self.session_args.copy()
        for key, val in client_args_copy.items():
            if key in ('base_url', 'proxies', 'method', 'pretty_json'):
                # update session
                setattr(self.session, key, val)
                self.session_args.pop(key)
                # update self
                setattr(self, key, val)

        # update headers as already exist within client
        self.session.headers.update(self.session_args.pop('headers'))

        # store the name of all available top level endpoints
        self.values = [n for n in api_endpoints.keys()]

        # iterate over api_endpoints keys and add key to class namespace
        for top_name in api_endpoints.keys():
            # generate a new class object for each top level endpoint
            values = [n for n in api_endpoints[top_name].keys()]
            subclass = type(top_name, (object,), {'endpoints': _get_endpoints,
                                                  'values': values})
            # initiate the new subclass
            subclass = subclass()
            # populate it into the baseclass
            self.__dict__[top_name] = subclass
            self.__dict__[top_name].__name__ = top_name

            for fun_name in api_endpoints[top_name].keys():
                # setattr(self, key, self.register_api_func(key))
                # not as a class attribute, but a class method
                subclass.__dict__[fun_name] = self.register_api_func(top_name, fun_name)

                # add function name to the class methods
                subclass.__dict__[fun_name].__name__ = fun_name

                # set __doc__ for generic class method
                if "doc" in api_endpoints[top_name][fun_name]:
                    subclass.__dict__[fun_name].__doc__ = api_endpoints[top_name][fun_name]["doc"]

                # add special attributes - access to full func record
                subclass.__dict__[fun_name].__full__ = api_endpoints[top_name][fun_name]

                if "url" in api_endpoints[top_name][fun_name]:
                    subclass.__dict__[fun_name].url = api_endpoints[top_name][fun_name]['url']
                if "method" in api_endpoints[top_name][fun_name]:
                    subclass.__dict__[fun_name].method = api_endpoints[top_name][fun_name]['method']
                if "doc" in api_endpoints[top_name][fun_name]:
                    subclass.__dict__[fun_name].doc = api_endpoints[top_name][fun_name]['doc']
                if "var" in api_endpoints[top_name][fun_name]:
                    subclass.__dict__[fun_name].var = api_endpoints[top_name][fun_name]['var']
                if "content_type" in api_endpoints[top_name][fun_name]:
                    subclass.__dict__[fun_name].content_type = api_endpoints[top_name][fun_name]['content_type']

    # gets the available endpoints implemented in the PDBe REST API
    def endpoints(self):
        return _get_endpoints(self)

    # dynamic api registration function
    def register_api_func(self, top_name, fun_name):
        return lambda **kwargs: self.call_api_func(top_name, fun_name, **kwargs)

    # dynamic api call function
    def call_api_func(self, top_name, fun_name, **kwargs):

        # variables
        data = ''

        # overriding general request method if it is specified in the function call
        if 'method' in kwargs:
            self.session.method = (kwargs['method']).upper()
        else:
            self.session.method = 'GET'

        # build url from api_endpoint kwargs
        func = api_endpoints[top_name][fun_name]

        # verify required variables and raise an Exception if needed
        mandatory_params = re.findall('\{\{(?P<m>[a-zA-Z_]+)\}\}', func['url'])

        # check up mandatory parameters
        for param in mandatory_params:
            if param not in kwargs:
                logger.debug("'%s' param not specified. Mandatory params are %s"
                             % (param, mandatory_params))
                raise Exception("mandatory param '%s' not specified" % param)

        # also check for unrecognised parameters
        for param in kwargs:
            # skip the parameter 'method'
            if param not in mandatory_params and param != 'method':
                logger.debug("'%s' param not recognised. Mandatory params are %s"
                             % (param, mandatory_params))
                raise Exception("mandatory param '%s' not specified" % param)

        # get formatted urls
        if self.session.method == 'GET':
            url = re.sub('\{\{(?P<m>[a-zA-Z_]+)\}\}', lambda m: "%s" % kwargs.get(m.group(1)),
                         self.session.base_url + func['url'])
        elif self.session.method == 'POST':
            url = re.sub('\{\{(?P<m>[a-zA-Z_]+)\}\}', '', self.session.base_url + func['url'])

            # hard-coding here that the data for all post requets are given through the
            # pdbid or compid attribute
            for key in kwargs:
                if key in ('pdbid', 'compid'):
                    data = kwargs[key]
        else:
            raise NotImplementedError("Method '%s' not yet implemented. Available methods are: '%s'"
                                      % (self.session.method, "', '".join(func['method'])))

        # logging url
        logger.info("Resolved url: '%s'" % url)

        # now remove mandatory params from kwargs (because of get requests)
        # the url is already constructed and we don't need them in **kwargs
        for param in mandatory_params:
            del (kwargs[param])

        # evaluating the number of request in a second (according to EnsEMBL rest specification)
        if self.req_count >= self.reqs_per_sec:
            delta = time.time() - self.last_req
            if delta < 1:
                time.sleep(1 - delta)
            self.last_req = time.time()
            self.req_count = 0

        # check the request type (GET or POST)
        if self.session.method in func['method'] and self.session.method == 'GET':
            logger.info("Submitting a GET request. url = '%s', headers = %s, params = %s" % (
                url, {"Content-Type": func['content_type']}, kwargs))
            # do get request
            try:
                resp = self.session.get(url, headers={"Content-Type": func['content_type']}, params=kwargs)
            except requests.ConnectionError:
                # making fake 500 status response
                resp = type('resp', (object,), {'status_code': 500})
                resp = resp()

        elif self.session.method in func['method'] and self.session.method == 'POST':
            logger.info("Submitting a POST request. url = '%s', data = '%s', headers = %s, params = %s" % (
                url, data, {"Content-Type": func['content_type']}, kwargs))
            # do post the request
            try:
                resp = self.session.post(url, headers={"Content-Type": func['content_type']}, data=data)
            except requests.ConnectionError:
                # making fake 500 status response
                resp = type('resp', (object,), {'status_code': 500})
                resp = resp()
        else:
            raise NotImplementedError("Method '%s' not yet implemented. Available methods are: '%s'"
                                      % (self.session.method, "', '".join(func['method'])))

        # update response attribute
        self.response = resp

        # increment the request counter to rate limit requests
        self.req_count += 1

        # parse status codes
        if resp.status_code > 304:
            ExceptionType = RestError
            if resp.status_code == 429:
                ExceptionType = RestRateLimitError
            elif resp.status_code > 500:
                ExceptionType = RestServiceUnavailable

            # if the the error code is not yet documented in http_status_code
            try:
                doc = http_status_codes[resp.status_code][1]
            except KeyError:
                # gets a status based on the preceding value i.e. 405 codes assume message of 400
                if resp.status_code < 500:
                    doc = http_status_codes[400][1]
                else:
                    doc = http_status_codes[500][1]
            raise ExceptionType(doc, error_code=resp.status_code)

        if self.session.pretty_json:
            content = json.dumps(resp.json(), sort_keys=False, indent=4)
        else:
            content = resp.json()
        return content


def _get_endpoints(base):
    # print out formatted list of available endpoints
    return ('The following endpoints are available:\n    %s'
            % '\n    '.join(base.values))
