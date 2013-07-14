import re
import json
import argparse

import requests

from ..exceptions import RestdnsCliRuntimeError


class Command(object):

    """ Base class for all commands.

    :cvar help: the help for the command
    """

    help = ''

    def __init__(self, name, aparser_subs):
        self._aparser = aparser_subs.add_parser(name, help=self.help)
        self._aparser.set_defaults(command=self.run, command_name=name)

    def add_arg(self, *args, **kwargs):
        """ Add an argument to the command argument parser.
        """

        self._aparser.add_argument(*args, **kwargs)

    def prepare(self):
        """ Method to override, executed before to parse arguments from command
            line. This is a good place to call :meth:`add_arg`.
        """
        pass

    def run(self, args, config):
        """ Method to override, executed if command has been selected.

        :param args: parsed arguments
        :param config: parsed configuration
        """
        pass


class ApiCommand(Command):

    """ Base class for all commands interacting with Restdns API.
    """

    def run(self, args, config):
        self._base_url = config.get('base_url').rstrip('/')
        self.api_run(args, config)

    def request(self, resource, method='GET', data=None):
        """ Do a request on the API on the specified resource.
        """
        headers = {}
        if data is not None:
            data = json.dumps(data)
            headers['content-type'] = 'application/json'
        resource = self._base_url + resource
        ans = requests.request(method, resource, data=data, headers=headers)
        try:
            content = ans.json()
        except ValueError:
            content = ans.text
        if not ans.ok:
            raise RestdnsCliRuntimeError(content)
        return content, ans

    def get(self, *args, **kwargs):
        kwargs['method'] = 'GET'
        return self.request(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs['method'] = 'POST'
        return self.request(*args, **kwargs)

    def put(self, *args, **kwargs):
        kwargs['method'] = 'PUT'
        return self.request(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs['method'] = 'DELETE'
        return self.request(*args, **kwargs)


class ParameterAction(argparse.Action):

    """ Argparse action able to parse parameters (key=value).
    """

    RE_PARAM = re.compile('^([a-z0-9_.]+)=(.+|["][^"]*["])$')

    def __call__(self, parser, namespace, values, option_string=None):
        params = {}
        for value in values:
            match = self.RE_PARAM.match(value)
            if match is None:
                parser.error('Bad parameter format near of %r' % value)
            else:
                key_string, value = match.groups()
                keys = key_string.split('.')
                last_params = params
                for key in keys[0:-1]:
                    if key in last_params and not isinstance(last_params[key], dict):
                        parser.error('Already defined argument %r' % key_string)
                    elif key not in last_params:
                        last_params[key] = {}
                    last_params = last_params[key]
                if keys[-1] in last_params:
                    parser.error('Already defined argument %r' % key_string)
                else:
                    last_params[keys[-1]] = value
        setattr(namespace, self.dest, params)


def namespace_to_dict(namespace, args=()):
    """ Export provided args of namespace to a dict.
    """
    params = {}
    for name in args:
        value = getattr(namespace, name, None)
        if value is not None:
            params[name] = value
    return params


def rname(value):
    """ Convert string to rname.
    """
    return str(value).replace('@', '.')
