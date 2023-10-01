from functools import partial

from typing import Callable

from js import HTMLTableElement, HTMLTableCellElement, document, KeyboardEvent, HTMLTableRowElement, Range, window, \
    console, MouseEvent

from common.datatable import Row, Datatable
from remote.asyncjs import set_timeout
from wwwpy.remote.hotkey import Hotkey
from pyodide.ffi import create_proxy


class Grid:

    def __init__(self, table: HTMLTableElement = None) -> None:
        if table is not None:
            self.setup(table)
        self.onclick: Callable[[Row], None] = None

    def render_table(self, table: Datatable):
        self.render_rows([table.header] + table.rows)

    def render_rows(self, rows, has_header: bool = True):
        t = self.table
        t.innerHTML = ''
        body = t.createTBody()

        if has_header:
            r = body.insertRow(-1)
            for value in rows[0]:
                c = document.createElement('th')
                r.append(c)
                if value is not None:
                    c.innerHTML = value
        start_data = 1 if has_header else 0
        for row in rows[start_data:]:
            r = body.insertRow(-1)
            r.onclick = self._row_click(row)
            for value in row:
                c = r.insertCell()
                c.tabIndex = 0
                if value is not None:
                    c.innerHTML = value

    def _row_click(self, row):
        def click(event):
            c = self.onclick
            if c is not None:
                import inspect
                if inspect.iscoroutinefunction(c):
                    print('detect coroutine')

                    async def cb():
                        await c(row)

                    set_timeout(cb)
                else:
                    print('detect NO coroutine')
                    c(row)

        return click

    def setup(self, table: HTMLTableElement):
        _grid_add_css()
        table.className = ''
        table.classList.add('grid')
        self.table = table
        prev_val = ''

        def current_cell() -> HTMLTableCellElement:
            return document.activeElement

        def pageup_pagedown_keydown(direction, event: KeyboardEvent):
            if in_edit():
                return False
            cell = current_cell()
            tr: HTMLTableRowElement = cell.closest('tr')
            index = tr.rowIndex
            if (index == 1 and direction == -1) or (index == (table.rows.length - 1) and direction == 1):
                return False  # let the event bubble up

            y = index + (10 * direction)
            if y < 1:
                y = 1
            if y > table.rows.length:
                y = table.rows.length - 1

            x = cell.cellIndex
            new_row: HTMLTableRowElement = table.rows[y]
            if x >= new_row.cells.length:
                x = new_row.cells.length - 1
            new_row.cells[x].focus()
            event.stopPropagation()
            event.preventDefault()

        def home_end_keydown(index, event: KeyboardEvent):
            if in_edit():
                return False
            event.stopPropagation()
            event.preventDefault()
            cell = current_cell()
            tr: HTMLTableRowElement = cell.closest('tr')
            tr.cells[index].focus()

            cell = current_cell()
            tr: HTMLTableRowElement = cell.closest('tr')
            tr.cells[index].focus()
            event.stopPropagation()
            event.preventDefault()

        def arrows(xy, event: KeyboardEvent):
            xdelta, ydelta = xy
            cell = current_cell()
            if ydelta == 0 and in_edit():  # in edit left right arrow
                return False  # let the event bubble up
            accept_edit()
            tr: HTMLTableRowElement = cell.closest('tr')
            x = cell.cellIndex + xdelta
            y = tr.rowIndex + ydelta
            if x < 0 or y < 1:
                return False
            if y >= table.rows.length:
                return False

            new_row: HTMLTableRowElement = table.rows[y]
            if x >= new_row.cells.length:
                return False
            new_cell: HTMLTableCellElement = new_row.cells[x]
            new_cell.focus()

            event.stopPropagation()
            event.preventDefault()

        def in_edit() -> bool:
            return current_cell().contentEditable == 'true'

        def start_edit():
            cell = current_cell()
            cell.contentEditable = 'true'
            nonlocal prev_val
            prev_val = cell.innerHTML

        def accept_edit():
            if in_edit():
                current_cell().contentEditable = 'false'

        def starts_edit_select_all(event: KeyboardEvent):
            if not in_edit():
                start_edit()
                select_all()
            return False

        def on_keydown(event: KeyboardEvent):
            if not Hotkey.keyboard_event(event):
                return False
            if len(event.key) != 1 or event.altKey or event.ctrlKey or event.metaKey:
                return False  # non printable (you wish!)
            if not in_edit():
                start_edit()
                select_all()
            return False

        def f2_keydown(event: KeyboardEvent):
            # console.log('editable()')
            start_edit()
            current_cell().focus()
            caret_at_end()

        def caret_at_end():
            select_all().collapse(False)

        def caret_at_start():
            select_all().collapse(True)

        def select_all() -> Range:
            cell = current_cell()
            rangex = document.createRange()
            selection = window.getSelection()

            rangex.selectNodeContents(cell)
            selection.removeAllRanges()
            selection.addRange(rangex)
            return rangex

        def cancel_edit():
            cell = current_cell()
            cell.contentEditable = 'false'
            nonlocal prev_val
            cell.innerHTML = prev_val
            prev_val = ''

        def enter_keydown(event: KeyboardEvent):
            if in_edit():
                accept_edit()
            else:
                start_edit()
                select_all()

        def escape_keydown(event: KeyboardEvent):
            cell = current_cell()
            if in_edit():
                event.stopPropagation()
                event.preventDefault()
                console.log('contentEditable', cell.contentEditable, cell)
                cancel_edit()
            else:
                console.log('contentEditable false')
                return False  # let the event bubble up

        def on_mousedown(event: MouseEvent):

            if event.detail == 2 and not in_edit():
                start_edit()
                select_all()
                event.preventDefault()
                event.stopPropagation()

            return False

        self.table.addEventListener('mousedown', create_proxy(on_mousedown))
        self.table.addEventListener('keydown', create_proxy(on_keydown))
        hotkey = Hotkey(self.table)
        hotkey.add('F2', f2_keydown)
        hotkey.add('Escape', escape_keydown)
        hotkey.add('Enter', enter_keydown)
        hotkey.add('Backspace', starts_edit_select_all)
        hotkey.add('Delete', starts_edit_select_all)
        hotkey.add('Home', partial(home_end_keydown, 0))
        hotkey.add('End', partial(home_end_keydown, -1))
        hotkey.add('PageUp', partial(pageup_pagedown_keydown, -1))
        hotkey.add('PageDown', partial(pageup_pagedown_keydown, 1))
        fun = {'ArrowUp': (0, -1), 'ArrowDown': (0, 1), 'ArrowLeft': (-1, 0), 'ArrowRight': (1, 0), }
        for (key, xy) in fun.items():
            hotkey.add(key, partial(arrows, xy))


_once = False


def _grid_add_css():
    global _once
    if _once:
        return
    document.head.insertAdjacentHTML('beforeend', _grid_css)


# language=html
_grid_css = """
<style>

    table.grid {
        border-collapse: collapse;
        border: 1px solid #ccc;

    }

    table.grid > tbody > tr {
        background: #fff;
    }

    table.grid > tbody > tr > td {
        border: 1px solid #ccc;
        padding: 2px 10px;
    }
    table.grid > tbody > tr > th {
        border: 1px solid #ccc;
        padding: 2px 10px;
    }

    table.grid > tbody > tr > td:focus {
        /* box-shadow: inset 0 0 0 2px #4B89FF; */
        outline: 2px solid #4B89FF;;
    }

</style>
    """
