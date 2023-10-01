import datetime
from pathlib import Path

import xlsxwriter


def rows_to_excel(rows, path: Path):
    if path.exists():
        raise Exception(f'Path should not exists: {path}')
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    for x, value in enumerate(rows[0]):
        worksheet.write(0, x, value, bold)
    format2 = workbook.add_format({'num_format': 'dd/mm/yyyy'})

    for y, row in enumerate(rows[1:]):
        for x, value in enumerate(row):
            if value is not None:
                if isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
                    worksheet.write_datetime(y + 1, x, value, format2)
                else:
                    worksheet.write(y + 1, x, value)
    worksheet.autofit()
    workbook.close()
