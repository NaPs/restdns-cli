def format_struct(node, level=0):
    if isinstance(node, basestring):
        return ' ' * level * 4 + node + '\n'
    elif isinstance(node, list):
        return '\n'.join([format_struct(x, level) for x in node])
    elif isinstance(node, dict):
        return '\n'.join(['%s= %s:\n%s' % (' ' * level * 4, k.title(), format_struct(v, level + 1)) for k, v in node.iteritems()])


class RestdnsCliRuntimeError(RuntimeError):

    """ Error raised on a restdns-cli runtime error.
    """

    def as_text(self):
        return format_struct(self.message)
