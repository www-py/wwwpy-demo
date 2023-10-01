from js import HTMLTableElement, HTMLElement, HTMLAnchorElement, MouseEvent
from wwwpy.remote.widget import Widget


class ContainerWidget(Widget):
    def __init__(self, title: str, content: str = ''):
        # language=html
        html = f"""
        <h2 id="titolo" class="text-center">{title}</h2>
        <div id="root">
            {content}
        </div>"""

        super().__init__(html)
        self.titolo: HTMLElement = self
        self.root: HTMLElement = self
