from js import HTMLTableElement
from wwwpy.remote.widget import Widget

from remote.grid import Grid


class GridWidget(Widget, Grid):
    def __init__(self):
        Widget.__init__(self, html)
        Grid.__init__(self)
        self.id_table: HTMLTableElement = self

    def after_render(self):
        self.setup(self.id_table)


html = """
<div class="table-responsive table-hover">
    <table id='id_table' class='table' ></table>
</div>
"""
