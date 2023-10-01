from js import HTMLInputElement
from wwwpy.remote.widget import Widget


class InputWidget(Widget):
    counter = 0

    def __init__(self, label: str, input_type: str = 'input', input_id: str = None):
        # language=html
        if input_id is None:
            input_id = self.next_id()
        self.input_id = input_id
        html = f"""
<div class="form-group">
    <label for="{input_id}">{label}</label>
    <input type='{input_type}' class="form-control" id='{input_id}'>
</div>    
"""
        super().__init__(html)

    @property
    def input(self) -> HTMLInputElement:
        selector = self.container.querySelector(f'#{self.input_id}')
        if selector is None:
            raise Exception(f'id not found {self.input_id}')
        return selector

    @staticmethod
    def next_id() -> str:
        InputWidget.counter += 1
        return f'inputLabelWidget_{InputWidget.counter}'
