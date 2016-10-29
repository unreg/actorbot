import datetime


def print_date(unix):
        """
        """
        return '.'.join([
            datetime.datetime.fromtimestamp(
                int(unix)/1000).strftime('%Y-%d-%m %H:%M:%S'),
            '%d' % (int(unix) % 1000)])
