import prettytable

from ..printer import printer
from . import ApiCommand


def format_parameters(params):
    return '; '.join([('%s: %s' % x) for x in params.iteritems()])


class Show(ApiCommand):

    help = 'show zones'

    def prepare(self):
        self.add_arg('name', metavar='zone-name', nargs='?',
                     help='Name of zone to show')

    def api_run(self, args, config):
        zones, ans = self.get('/zones')

        if not args.name:  # No zone provided, showing zone listing
            printer.table(['name', 'serial', 'primary nameserver'],
                          [(x['name'], x['serial'], x['primary_ns']) for x in zones['zones']])
        else:
            # Search zone with the specified name:
            for zone in zones['zones']:
                if zone['name'] == args.name:
                    break
            else:
                printer.p('Unknown zone with this name')

            printer.p('ZONE DETAILS:')
            zone_data = [(x, zone[x]) for x in ('name', 'primary_ns', 'rname', 'refresh', 'retry', 'expire', 'minimum', 'serial')]
            printer.table(['a', 'b'], zone_data, header=False, hrules=prettytable.ALL)

            printer.p()

            # Get zone records:
            printer.p('RECORD LIST:')
            records, ans = self.get(zone['records_url'])
            printer.table(['uuid', 'name', 'type', 'parameters'],
                          [(x['uuid'], x['name'], x['type'].upper(),
                            format_parameters(x['parameters'])) for x in records['records']])
