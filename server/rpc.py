async def add(a, b) -> int:
    result = a + b
    if result > 42:
        raise ValueError(f'The result is {result}. It is greater than 42. So it is not allowed.')
    return result


async def server_execute_sql(sql: str,
                             params: dict = None,
                             header: bool = False,
                             print_result: bool = False,
                             exception_as_result: bool = False):
    tab = _sqlalchemy_error(header)
    if tab is not None:
        return tab
    from server.database import execute_sql
    return execute_sql(sql, params, header, print_result, exception_as_result)


def _sqlalchemy_error(header):
    try:
        import sqlalchemy
        return None
    except ImportError:
        print('sqlalchemy not installed')
        head_row = (('exception',),)
        tab = (('sqlalchemy not installed! ',)
               , ('Please, install it with `pip install sqlalchemy`',),)
        if header:
            tab = head_row + tab
        return tab
