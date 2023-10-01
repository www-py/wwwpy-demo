from typing import Union

from remote import NavbarWidget
from remote.components.spinner_widget import SpinnerWidget

spinner = SpinnerWidget()

_navbar: Union[NavbarWidget, None] = None


def set_navbar_widget(navbar_widget):
    global _navbar
    _navbar = navbar_widget


class ToastWrapper:

    @staticmethod
    def showToast(message):
        _navbar.toast.showToast(message)


toast = ToastWrapper()
