import os

from ..printer import printer
from . import Command


DEFAULT_CONFIG = '''# Restdns-cli configuration file

base_url = "{base_url}"

'''


class Config(Command):

    """ Create and edit the configuration file.
    """

    help = 'create and edit the configuration file'

    def run(self, args, config):
        if not os.path.isfile(args.config):
            printer.p('Configuration file cannot be found!')
            if printer.ask('Would you like to create configuration?', default=True):
                env = {}
                env['base_url'] = printer.input('What is the base url to your Restdns instance')
                with open(args.config, 'w') as fconfig:
                    fconfig.write(DEFAULT_CONFIG.format(**env))
                printer.p('Call again this command to edit the config file')
        else:
            with open(args.config, 'r+') as fconfig:
                config = printer.edit(fconfig.read())
                fconfig.seek(0)
                fconfig.truncate()
                fconfig.write(config)
            printer.p('Saved.')
