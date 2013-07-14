from ..printer import printer
from . import ApiCommand


class Types(ApiCommand):

    help = 'show available record types'

    def api_run(self, args, config):
        record_types, ans = self.get('/record/types')
        rows = [(k.upper(), '; '.join(v['parameters'])) for k, v in record_types.iteritems()]
        printer.table(['type', 'parameters'], rows)
