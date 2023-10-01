from dataclasses import dataclass
from typing import Callable

from js import HTMLTableElement, HTMLTableCellElement, HTMLElement
from wwwpy.remote.widget import Widget
from pyodide.ffi import create_proxy


class TreeWidget(Widget):
    def __init__(self):
        super().__init__(_html)
        self.idTable: HTMLTableElement = self
        self.on_get_children = lambda parent_item: []
        self.on_get_caption = lambda item: str(item)
        self.on_item_click = lambda item: print(f'item clicked: {self.on_get_caption(item)}')
        self.on_cell_render: Callable[[CellRender], None] = lambda item: print(f'item cell render: {item}')
        self.bind_self_elements()
        self._tbody = self.idTable.tBodies[0]

    def append_to(self, element: HTMLElement):
        self._tbody.innerHTML = ''
        self._append_item(None, 0)
        return super().append_to(element)

    def _append_item(self, parent, depth: int):
        children = self.on_get_children(parent)
        for item in children:
            tr = self._tbody.insertRow(-1)
            tr.setAttribute('w-depth', str(depth))
            tr.setAttribute('w-item', str(item))
            tr.addEventListener('click', self.capture_item(item))

            td = tr.insertCell(-1)
            td.innerHTML = '&nbsp;' * 8 * depth + self.on_get_caption(item)
            self.on_cell_render(CellRender(item, td, depth))
            self._append_item(item, depth + 1)

    def capture_item(self, item):
        return create_proxy(lambda evt: self.on_item_click(item))


@dataclass(frozen=True)
class CellRender:
    item: any
    cell: HTMLTableCellElement
    depth: int


# language=HTML
_html = """
<table class="table table-hover" id='idTable'>
    <tbody></tbody>
</table>
"""
