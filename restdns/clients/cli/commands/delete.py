from ..printer import printer
from . import ApiCommand


class Delete(ApiCommand):

    help = 'delete a zone'

    def prepare(self):
        self.add_arg('name', metavar='zone-name', help='Name of zone to delete')

    def api_run(self, args, config):
        zones, ans = self.get('/zones')
        for zone in zones['zones']:
            if zone['name'] == args.name:
                break
        else:
            printer.p('Unknown zone with this name')
            return
        data, ans = self.delete(zone['url'])
        if ans.ok:
            printer.p('Zone has been deleted!')
        else:
            printer.p('Error %s' % data)


class RDelete(ApiCommand):

    help = 'delete a record'

    def prepare(self):
        self.add_arg('zone_name', metavar='zone-name',
                     help='Name of zone of which to delete the record')
        self.add_arg('record_id', metavar='record-id', type=int,
                     help='Identity of the record to delete')

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
            if record['id'] == args.record_id:
                break
        else:
            printer.p('Unknown record with provided id')
            return
        data, ans = self.delete(record['url'])
        if ans.ok:
            printer.p('Record has been deleted!')
        else:
            printer.p('Error %s' % data)
