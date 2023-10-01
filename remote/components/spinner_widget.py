import contextlib

from js import HTMLElement, console
from wwwpy.remote.widget import Widget

from remote.asyncjs import wait_animation_frame, AwaitableCallback, set_timeout


class SpinnerWidget(Widget):
    def __init__(self):
        super().__init__(html)
        self.div_loader: HTMLElement = self
        self.counter = 0
        self.bind_self_elements()

    async def spinnerSuspend(self, function: AwaitableCallback):
        await self.show_spinner()
        console.log(f"after increment {self.counter}")
        await wait_animation_frame()
        try:
            await function()
        finally:
            await self.hide_spinner()

    async def hide_spinner(self):
        self.counter -= 1
        console.log(f"after increment {self.counter}")
        if self.counter == 0:
            await self.visible(False)

    async def show_spinner(self):
        if self.counter == 0:
            await self.visible(True)
        self.counter += 1

    @contextlib.asynccontextmanager
    async def context(self):
        await self.show_spinner()
        try:
            yield
        finally:
            await self.hide_spinner()

    async def visible(self, want_visible: bool):
        self.div_loader.style.display = '' if want_visible else 'none'
        await wait_animation_frame()

    def spinner_async(self, callback: AwaitableCallback):
        async def fun():
            async with self.context():
                await callback()

        set_timeout(fun)


# language=html
html = """<style>
    .spinner_base {
        border: 4px solid #f3f3f3; /* Light grey */
        border-top: 4px solid #3498db; /* Blue */
        border-radius: 50%;
        position: fixed;
        width: 30px;
        height: 30px;
        animation: spin 0.5s linear infinite;
    }

    #div_loader2 {
        left: 0px;
        top: 0px;
    }

    #div_loader {
        bottom: 0;
        right: 0;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
</style>
<div id="div_loader" class="spinner_base" style="display: none"></div>

    
"""
