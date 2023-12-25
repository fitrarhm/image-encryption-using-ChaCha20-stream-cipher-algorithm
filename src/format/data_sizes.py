UNITS = {1000: ['KB', 'MB', 'GB'],
         1024: ['KiB', 'MiB', 'GiB']}


def approximate_size(size, flag_1024_or_1000=True):
    mult = 1024 if flag_1024_or_1000 else 1000
    for unit in UNITS[mult]:
        size = size / mult
        if size < mult:
            return '{0:.3f} {1}'.format(size, unit)

# approximate_size(2123, False)


# def convert_bytes(size):
#     for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
#         if size < 1024.0:
#             return "%3.1f %s" % (size, x)
#         size /= 1024.0

#     return size
