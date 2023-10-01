from pathlib import Path
from typing import Union
from pyodide.ffi import create_proxy, to_js

import js
from js import HTMLElement, HTMLButtonElement, Event
from wwwpy.remote.hotkey import HotkeyWindow
from wwwpy.remote.widget import Widget, HolderWidget

parent = Path(__file__).parent


class NavbarWidget(Widget):
    def __init__(self):
        super().__init__((parent / 'navbar_widget.html').read_text())
        self.main_content = self(lambda: HolderWidget())
        self.offcanvas = self(lambda: HolderWidget())
        self.toast = self(lambda: ToastsWidget())
        self.navbarSideCollapse: HTMLElement = self
        self.btnToggle: HTMLButtonElement = self
        self.offcanvasScrollingLabel: HTMLElement = self

    def after_render(self):
        HotkeyWindow.add("META-Escape", self.toggle)

    def navbarSideCollapse__click(self, evt: Event):
        evt.stopPropagation()
        evt.preventDefault()
        self.toggle()

    def toggle(self, *args):
        self.btnToggle.click()

    def show_main(self, widget: Widget):
        self.main_content.show(widget)


class ToastWidget(Widget):
    def __init__(self):
        super().__init__(  # language=HTML
            """
<div id="liveToast" class="toast hide" role="alert" aria-live="assertive" aria-atomic="true">
    <div class="toast-header">
        <img src="" class="rounded me-2" alt="">
        <strong class="me-auto">Information</strong>
        <small>0 secs ago</small>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    
    <div class="toast-body" id="idBody">
    
    </div>
</div>
""")
        self.idBody: HTMLElement = self
        self.liveToast: HTMLElement = self
        self.bsToast = None
        self.bind_self_elements()
        #  skip idBody

    def show(self):
        if self.bsToast is None:
            self.bsToast = js.eval("(e) => bootstrap.Toast.getOrCreateInstance(e)")(self.liveToast)
        self.bsToast.show()
        self.liveToast.addEventListener("hidden.bs.toast", create_proxy(lambda evt: self.container.remove()))


class ToastsWidget(Widget):
    def __init__(self):
        super().__init__('')

    def after_render(self):
        self.container.className = 'toast-container position-fixed bottom-0 end-0 p-3'
        self.container.style.zIndex = "2000"

    def showToast(self, toast: Union[ToastWidget, str]):
        if isinstance(toast, str):
            tw = ToastWidget()
            tw.idBody.innerHTML = toast
            self.showToast(tw)
        else:
            self.container.append(toast.container)
            toast.show()
