from js import console, HTMLTableElement, HTMLTextAreaElement, HTMLButtonElement
from wwwpy.remote.hotkey import Hotkey
from wwwpy.remote.widget import Widget

from remote import spinner
from remote.asyncjs import set_timeout
from remote.excel import download_rows
from remote.grid_widget import GridWidget
from server.rpc import server_execute_sql


class ExecuteSqlWidget(Widget):
    def __init__(self):
        super().__init__(html)
        self.id_sql: HTMLTextAreaElement = self
        self.id_btn: HTMLButtonElement = self
        self.id_xls: HTMLButtonElement = self
        self.id_table: HTMLTableElement = self
        self.rows = None
        self.grid = self(lambda: GridWidget())

    async def _download_rows(self, *args):
        await download_rows(self.rows)

    def after_render(self):
        self.id_sql.value = 'select * from person'
        self.id_btn.onclick = self._execute_sql
        self.id_xls.onclick = self._download_rows
        self.id_btn.click()

        # self.grid = Grid(self.id_table)

        def ctrl_e(ev):
            set_timeout(self._execute_sql)
            return True

        Hotkey(self.container).add('CTRL-E', ctrl_e)

    async def _execute_sql(self, *args):
        console.log(self.id_sql.value)
        self.grid.render_rows((('loading...',),))
        async with spinner.context():
            rows = await server_execute_sql(self.id_sql.value, header=True, exception_as_result=True)
            self.rows = rows
        self.grid.render_rows(rows)


# language=html
html = """
<h1>sql</h1>
<textarea id='id_sql' rows='6' style='width: 100%'></textarea>
<br>
<button id='id_btn'>execute</button>
<button id='id_xls'>excel</button>
<div id='grid'></div>
"""

