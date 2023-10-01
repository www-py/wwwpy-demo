from js import document, console, Object
from pyodide.ffi import to_js
from wwwpy.remote.widget import Widget

from remote import toast


async def go_bluetooth():
    document.body.innerHTML = 'loading widget...'
    BluetoothWidget().append_to(document.body)


class BluetoothWidget(Widget):

    def __init__(self):
        super().__init__(
            #     language=html
            """
            <button id='btn1' class="btn btn-primary">bluetooth device request dialog</button>
            """
        )

    async def btn1__click(self, event):
        console.log('going to requestDevice')
        try:
            from js import navigator
            opt = Object.fromEntries(to_js({'acceptAllDevices': True}))
            device = await navigator.bluetooth.requestDevice(opt)
            console.log(device.name)
            toast.showToast(f'You selected the device `{device.name}`')

        except Exception as e:
            import traceback
            exc = traceback.format_exc().replace('\n', '<br>')
            toast.showToast(f'Exception! {exc}')
