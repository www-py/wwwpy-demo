from __future__ import annotations

from datetime import datetime
from pathlib import Path

from remote import piplib, spinner
from wwwpy.common.files import download_path as _download_path


async def download_rows(rows, with_filename: str = ''):
    if with_filename == '':
        with_filename = f'export-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
    async with spinner.context():
        await _excel(rows, with_filename)


async def _excel(rows, with_filename: str):
    await piplib.install('xlsxwriter')
    from common.excel import rows_to_excel
    path = Path('export.xlsx')
    if path.exists():
        path.unlink()
    rows_to_excel(rows, path)
    mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    _download_path(with_filename, path, mimetype)
