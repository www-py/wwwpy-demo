from js import HTMLButtonElement
from wwwpy.remote.widget import Widget


class ButtonWidget(Widget):
    def __init__(self, text: str = 'no-text-specified'):
        # language=html
        html = f"""<button id="btn" class="btn btn-primary">{text}<i class= aria-hidden="true"></i></button>"""
        super().__init__(html)
        self.btn: HTMLButtonElement = self
