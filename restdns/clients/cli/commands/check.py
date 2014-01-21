import socket

import prettytable
import dns.query
import dns.message
import dns.exception

from ..printer import printer
from . import ApiCommand


def format_parameters(params):
    return '; '.join([('%s: %s' % x) for x in params.iteritems()])


def state(serial, serial_by_ns):
    """ Compute a global status depending on status of each nameserver.
    """
    up_to_date_ns = len([k for k, v in serial_by_ns.iteritems() if v >= serial])
    if up_to_date_ns == 0:
        status = 'None'
    elif up_to_date_ns == len(serial_by_ns):
        status = 'OK'
    else:
        status = 'Partial'
    return status


def do_query(query, name):
    """ Do the query on the DNS server, trying each address returned by getaddrinfo.
    """
    try:
        addr_info = socket.getaddrinfo(name, 53, 0, 0, socket.SOL_UDP)
    except socket.gaierror:
        raise
        return None
    for host in addr_info:
        try:
            answer = dns.query.udp(query, host[4][0], timeout=5)
        except (socket.error, dns.exception.Timeout):
            continue
        else:
            return answer
    else:
        return None


class Check(ApiCommand):

    help = 'check zone deployment'

    def prepare(self):
        self.add_arg('name', metavar='zone-name', nargs='?',
                     help='Name of zone to check')

    def api_run(self, args, config):
        zones, ans = self.get('/zones')

        if not args.name:  # No zone provided, showing zone listing
            states = []
            for zone in zones['zones']:
                ns_serial = self._do_check(zone['name'], zone['records_url'])
                states.append((zone['name'], zone['serial'], state(zone['serial'], ns_serial), format_parameters(ns_serial)))
            printer.table(['zone', 'serial', 'state', 'nameservers'], states)
        else:
            # Search zone with the specified name:
            for zone in zones['zones']:
                if zone['name'] == args.name:
                    break
            else:
                printer.p('Unknown zone with this name')

            ns_serial = self._do_check(zone['name'], zone['records_url'])

            printer.p('ZONE STATUS:')
            zone_status = [('Zone', zone['name']),
                           ('Current serial', zone['serial']),
                           ('Status', state(zone['serial'], ns_serial))]
            printer.table(['Name', 'Value'], zone_status, header=False, hrules=prettytable.ALL)

            printer.p()

            # Get zone records:
            printer.p('NAMESERVER DETAILS:')
            printer.table(['Nameserver', 'Serial'],
                          [(k, v) for k, v in ns_serial.iteritems()])

    def _do_check(self, zone, records_url):
        """ Do the query on each ns of the zone and return serial of each ns.
        """
        ns_serial = {}
        query = dns.message.make_query(zone, 'SOA')
        records, ans = self.get(records_url)
        for record in records['records']:
            if not record['name'] and record['type'] == 'ns':
                answer = do_query(query, record['parameters']['name'])
                if answer is None:
                    serial = -1
                else:
                    if len(answer.answer):
                        serial = answer.answer[0][0].serial
                    else:
                        serial = -1
                ns_serial[record['parameters']['name']] = serial

        return ns_serial
