from ..printer import printer
from . import ApiCommand, ParameterAction, namespace_to_dict, rname


class Create(ApiCommand):

    help = 'create a zone'

    def prepare(self):
        self.add_arg('--refresh', '-r', type=int)
        self.add_arg('--retry', '-y', type=int)
        self.add_arg('--expire', '-e', type=int)
        self.add_arg('--minimum', '-m', type=int)
        self.add_arg('name', metavar='zone-name', help='Name of zone to create')
        self.add_arg('primary_ns', metavar='primary-ns',
                     help='Primary name server of zone to create')
        self.add_arg('rname', type=rname, help='Email address of zone admin')

    def api_run(self, args, config):
        query_data = namespace_to_dict(args, ['name', 'primary_ns', 'rname',
                                              'refresh', 'retry', 'expire',
                                              'minimum'])
        data, ans = self.post('/zones', data=query_data)
        if ans.ok:
            printer.p('Zone has been created!')
        else:
            printer.p('Error %s' % data)


class RCreate(ApiCommand):

    help = 'create a record'

    def prepare(self):
        self.add_arg('zone_name', metavar='zone-name',
                     help='Name of zone on which create the record')
        self.add_arg('name', metavar='record-name',
                     help='Name of the record to create')
        self.add_arg('type', help='Type of the record to create')
        self.add_arg('parameters', metavar='param=value', nargs='+',
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
        query_data = namespace_to_dict(args, ['name', 'type', 'parameters'])
        data, ans = self.post(zone['records_url'], data=query_data)
        if ans.ok:
            printer.p('Record has been created!')
        else:
            printer.p('Error %s' % data)
