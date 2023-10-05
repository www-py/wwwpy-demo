import decimal
import traceback
from pathlib import Path
import sqlite3
from datetime import datetime


def map_data(row):
    def convert_value(value):
        if isinstance(value, decimal.Decimal):
            value = float(value)
        return value

    return tuple(map(convert_value, row))


def new_connection():
    path = (Path(__file__).parent / 'database.db').absolute()
    exists = path.exists()
    connection = sqlite3.connect(str(path))

    if not exists:
        print('creating database')
        with open(Path(__file__).parent / 'database.sql', 'r') as f:
            sqls = f.read().split('\nGO\n')
        cursor = connection.cursor()
        for sql in sqls:
            print(f'executing: ```{sql}```')
            cursor.execute(sql)
        connection.commit()
        cursor.close()
    return connection


def result_to_rows(cursor):
    return tuple(map(map_data, cursor.fetchall()))


def result_to_header(cursor):
    return tuple(column[0] for column in cursor.description)


def execute_sql(sql: str, params: dict = None, header: bool = False, print_result: bool = False,
                exception_as_result: bool = False):
    try:
        with new_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params if params else {})
            if cursor.description:  # If the query returns rows
                head_row = (result_to_header(cursor),)
                tab = result_to_rows(cursor)
            else:
                head_row = (('rowcount',),)
                tab = ((cursor.rowcount,),)
                connection.commit()
    except sqlite3.Error as ex:
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
    rows = execute_sql('select dssql from sqlquery where id=?', (queryweb_id,), header=False)
    row = rows[0]
    sql = row[0]
    if sql:
        return execute_sql(sql, params, header=True, exception_as_result=True)
    return ()


def save_pie_to_database(name: str, flavor: str, pie_date: datetime = None) -> int:
    sql = 'INSERT INTO pie (name, flavor, date) VALUES (?, ?, ?)'
    date_str = pie_date.isoformat() if pie_date else None
    with new_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, (name, flavor, date_str))
        row_id = cursor.lastrowid
        connection.commit()
        cursor.close()
    return row_id


if __name__ == '__main__':
    # res = execute_sql('select max(id) from sqlquery')
    # execute_sql("update sqlquery set dssql='' where id=-1", print_result=True, header=True)
    # new_connection()
    assigned_id = save_pie_to_database("Sample Pie", "Sample Flavor", datetime.now())
    print(f"Assigned ID for the pie: {assigned_id}")
    execute_sql('select * from pie', print_result=True, header=True)
