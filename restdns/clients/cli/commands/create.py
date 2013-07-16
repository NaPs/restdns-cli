import dns.reversename

from ..printer import printer
from ..exceptions import RestdnsCliRuntimeError
from . import ApiCommand, ParameterAction, namespace_to_dict, rname


class Create(ApiCommand):

    help = 'create a zone'

    def prepare(self):
        self.add_arg('--refresh', '-r', type=int)
        self.add_arg('--retry', '-y', type=int)
        self.add_arg('--expire', '-e', type=int)
        self.add_arg('--minimum', '-m', type=int)
        self.add_arg('--reverse', action='store_true', default=False)
        self.add_arg('--reverse-length', type=int, default=1)
        self.add_arg('name', metavar='zone-name', help='Name of zone to create')
        self.add_arg('primary_ns', metavar='primary-ns',
                     help='Primary name server of zone to create')
        self.add_arg('rname', type=rname, help='Email address of zone admin')

    def api_run(self, args, config):
        # Handle reverse zones:
        if args.reverse:
            try:
                rev = dns.reversename.from_address(args.name)
            except dns.exception.SyntaxError:
                raise RestdnsCliRuntimeError('Name must be an IP address with `--reverse`')
            # Validate length:
            if args.reverse_length < 0 or args.reverse_length > len(rev) - 2:
                raise RestdnsCliRuntimeError('Bad reverse length value for provided IP version')
            for __ in xrange(args.reverse_length):
                rev = rev.parent()
            args.name = str(rev)

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


class RRCreate(ApiCommand):

    help = 'create a reverse record'

    def prepare(self):
        self.add_arg('ipaddr', metavar='ip-address',
                     help='IP of the reverse record')
        self.add_arg('ptr_name', metavar='ptr-name')

    def api_run(self, args, config):
        rev = dns.reversename.from_address(args.ipaddr)
        zones, ans = self.get('/zones')
        for zone in sorted(zones['zones'], key=lambda x:len(x['name']), reverse=True):
            zone_name = dns.name.from_text(zone['name'])
            if rev.is_subdomain(zone_name):
                break
        else:
            raise RestdnsCliRuntimeError(['No zone can be found for the provided IP.',
                                          'Use the `create --reverse` command to create a new reverse zone'])

        query_data = {'name': str(rev.relativize(zone_name)),
                      'type': 'ptr',
                      'parameters': {'name': args.ptr_name}}
        data, ans = self.post(zone['records_url'], data=query_data)
        if ans.ok:
            printer.p('Record has been created!')
        else:
            printer.p('Error %s' % data)
