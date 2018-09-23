class PrettyDict:
    def __init__(self, v):
        self.v = v

    def _format_value(self, v, indent, comma, tab):
        if type(v) == tuple:
            v = str(v)

        if type(v) == list:
            return ''.join([self._format_value(item, indent, comma, tab) for item in v])

        elif type(v) == dict:
            res = ' : {\n'
            res += self.format(v, tab, indent)
            res += (" " * tab * (indent - 1)) + '}' + comma + '\n'
            return res

        else:
            return (' : "%s"' % (v)) + comma + "\n"

    def format(self, d, tab=4, indent=0):
        """
        Performs dict formatting to human-readable string

        :param d: dictionary to format
        :param tab: tab identation length
        :param indent: initial identation to use for formatting
        :rtype: str
        """
        i = 0
        l = len(d)
        res = ''
        comma = ','

        for key in d:
            i += 1

            if i == l:
                comma = ''

            res += (" " * tab * indent) + ('"%s"' % key)
            res += self._format_value(d[key], indent + 1, comma, tab)

        return res

    def __str__(self):
        return self.format(self.v)
