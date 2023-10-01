def row_remove_cr(row):
    return tuple([(value.replace('\n', ' ') if isinstance(value, str) else value) for value in row])


def rows_remove_cr(rows):
    return tuple([row_remove_cr(row) for row in rows])


if __name__ == '__main__':
    rows = (('header',), ('row1\nciao', True))
    cr = rows_remove_cr(rows)
    print(cr)
