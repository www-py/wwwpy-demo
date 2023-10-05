from js import HTMLInputElement
from wwwpy.remote.widget import Widget

from remote import toast
from server import rpc


class CalculatorWidget(Widget):
    def __init__(self):
        super().__init__(_html)
        self.inputA: HTMLInputElement = self
        self.inputB: HTMLInputElement = self
        self.inputResult: HTMLInputElement = self

    def after_render(self):
        self.inputA.oninput = self._calculate
        self.inputB.oninput = self._calculate

    async def _calculate(self, event):
        def to_num(num_str):
            return int(num_str) if len(num_str.strip()) > 0 else None

        try:
            a = to_num(self.inputA.value)
            b = to_num(self.inputB.value)
        except ValueError as e:
            self.inputResult.value = f'Integer expected. Exception=`{e}`'
            return

        if a is None or b is None:
            self.inputResult.value = ''
        else:
            try:
                self.inputResult.value = await rpc.add(a, b)
            except Exception as e:
                self.inputResult.value = f'RPC Exception!'
                toast.showToast(f'RPC Exception! {e}')


# language=html
_html = """
<div class="input-group mb-3">
    <span class="input-group-text">A</span>
    <input id='inputA' type="text" class="form-control"
           placeholder="an integer A">
</div>

<div class="input-group mb-3">
    <span class="input-group-text">B</span>
    <input id='inputB' type="text" class="form-control"
           placeholder="an integer B">
</div>

<div class="form-floating mb-3">
    <input id='inputResult' type="text" class="form-control">
    <label for="inputResult">A + B =</label>
</div>


<div class="card" >
    <div class="card-body">
        <h5 class="card-title">Good to know!</h5>
        <p class="card-text">When the sum is greater than 42, the server will raise an exception.</p>
        <p>Just for fun!</p>
    </div>
</div>
"""
