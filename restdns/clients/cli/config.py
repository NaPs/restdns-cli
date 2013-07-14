""" restdns-cli configuration parsers.
"""

from dotconf import Dotconf
from dotconf.schema.containers import Section, Value
from dotconf.schema.types import Url


class RootRestdnsCliConfig(Section):

    base_url = Value(Url())


def parse_config(filename):
    conf = Dotconf.from_filename(filename, schema=RootRestdnsCliConfig())
    return conf.parse()
