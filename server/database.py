import decimal
import traceback
from pathlib import Path

from sqlalchemy import create_engine, text


def map_data(row):
    def convert_value(value):
        if isinstance(value, decimal.Decimal):
            value = float(value)
        return value

    return tuple(map(convert_value, row))


def new_connection():
    path = (Path(__file__).parent / 'database.db').absolute()
    exists = path.exists()
    connection_string = f'sqlite:////{path}'
    engine = create_engine(connection_string)

    if not exists:
        create = engine.connect()
        print('creating database')
        with open(Path(__file__).parent / 'database.sql', 'r') as f:
            sqls = f.read().split('\nGO\n')
        for sql in sqls:
            print(f'executing: ```{sql}```')
            create.execute(text(sql))
        create.commit()
        create.close()
    return engine.connect()


def result_to_rows(result):
    return tuple(map_data(row._data) for row in result)


def result_to_header(result):
    return tuple(result.keys()._keys)


def execute_sql(sql: str, params: dict = None, header: bool = False, print_result: bool = False,
                exception_as_result: bool = False):
    try:
        with new_connection() as connection:
            result = connection.execute(text(sql), params)
            if result.returns_rows:
                head_row = (result_to_header(result),)
                tab = result_to_rows(result)
            else:
                head_row = (('rowcount',),)
                tab = ((result.rowcount,),)
                connection.commit()
    except Exception as ex:
        if not exception_as_result:
            raise
        else:
            head_row = (('exception',),)
            tab = ((traceback.format_exc(),),)
    if header:
        tab = head_row + tab
    if print_result:
        for row in tab:
            print(row)
    return tab


def execute_queryweb(queryweb_id: int, params: dict = None):
    rows = execute_sql(f'select dssql from sqlquery where id=:id', {'id': queryweb_id}, header=False)
    row = rows[0]
    sql = row[0]
    if sql != '':
        return execute_sql(sql, params, header=True, exception_as_result=True)
    return ()


if __name__ == '__main__':
    # res = execute_sql('select max(id) from sqlquery')
    # execute_sql("update sqlquery set dssql='' where id=-1", print_result=True, header=True)
    new_connection()
