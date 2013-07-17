from ..printer import printer
from . import ApiCommand, ParameterAction, namespace_to_dict, rname


class Set(ApiCommand):

    help = 'set zone parameters'

    def prepare(self):
        self.add_arg('--refresh', '-r', type=int)
        self.add_arg('--retry', '-y', type=int)
        self.add_arg('--expire', '-e', type=int)
        self.add_arg('--minimum', '-m', type=int)
        self.add_arg('--rname', '-n', type=rname,
                     help='Set zone admin email address')
        self.add_arg('--primary-ns', '-p', help='Set the primary name server')
        self.add_arg('name', metavar='zone-name', help='Name of zone to modify')

    def api_run(self, args, config):
        zones, ans = self.get('/zones')
        for zone in zones['zones']:
            if zone['name'] == args.name:
                break
        else:
            printer.p('Unknown zone with this name')
        query_data = namespace_to_dict(args, ['refresh', 'retry', 'expire',
                                              'minimum', 'rname', 'primary_ns'])
        data, ans = self.put(zone['url'], data=query_data)
        if ans.ok:
            printer.p('Zone has been updated!')
        else:
            printer.p('Error %s' % data)


class RSet(ApiCommand):

    help = 'set record parameters'

    def prepare(self):
        self.add_arg('--name', '-n', help='Set record name')
        self.add_arg('--type', '-t', help='Set record type')
        self.add_arg('zone_name', metavar='zone-name',
                     help='Name of zone of which to modify the record')
        self.add_arg('record_uuid', metavar='record-uuid',
                     help='Identity of the record to modify')
        self.add_arg('parameters', metavar='param=value', nargs='*',
                     action=ParameterAction,
                     help='Parameters of the record. You can see all available '
                          'types and theirs parameters using the `types` '
                          'command')

    def api_run(self, args, config):
        zones, ans = self.get('/zones')
        for zone in zones['zones']:
            if zone['name'] == args.zone_name:
                break
        else:
            printer.p('Unknown zone with this name')
            return
        records, ans = self.get(zone['records_url'])
        for record in records['records']:
            if record['uuid'] == args.record_uuid:
                break
        else:
            printer.p('Unknown record with provided id')
            return
        query_data = namespace_to_dict(args, ['type', 'parameters'])
        data, ans = self.put(record['url'], data=query_data)
        if ans.ok:
            printer.p('Record has been updated!')
        else:
            printer.p('Error %s' % data)
