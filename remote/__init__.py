import asyncio

from js import document
from wwwpy.remote.hotkey import HotkeyWindow

from remote.bootstrap import setup_bootstrap
from remote.bootstrap.navbar_widget import NavbarWidget
from remote.menu_item import MenuItem
from remote.components.tree_widget import TreeWidget
from remote.ui import spinner, toast
from remote.welcome_widget import WelcomeWidget


async def main():
    HotkeyWindow.enable_log = True
    setup_bootstrap()
    document.body.innerHTML = ''
    navbar_widget = NavbarWidget().append_to(document.body)
    ui.set_navbar_widget(navbar_widget)

    navbar_widget.show_main(WelcomeWidget())
    spinner.append_to(document.body)

    menu_root = build_menu(navbar_widget)
    navbar_widget.offcanvas.show(wrap_in_tree(menu_root, navbar_widget))


def spinner_seconds(delay_secs):
    async def wait():
        await asyncio.sleep(delay_secs)

    spinner.spinner_async(wait)


def build_menu(navbar: NavbarWidget) -> MenuItem:
    def show_calculator():
        from remote.calculator_widget import CalculatorWidget
        navbar.show_main(CalculatorWidget())

    def show_bluetooth():
        from remote.bluetooth import BluetoothWidget
        navbar.show_main(BluetoothWidget())

    def show_sql_editor():
        from remote.execute_sql_widget import ExecuteSqlWidget
        navbar.show_main(ExecuteSqlWidget())

    def show_filesystem():
        from wwwpy.remote.widgets.filesystem_tree_widget import FilesystemTreeWidget
        navbar.show_main(FilesystemTreeWidget())

    root = MenuItem('_root')
    base = root.new_child('Development')
    base.new_child('Calculator', show_calculator)
    base.new_child('Blueetooth', show_bluetooth)
    base.new_child('Sql Editor', show_sql_editor)
    base.new_child('Filesystem', show_filesystem)
    second = root.new_child('Misceleanous')
    second.new_child('Spinner for 3 seconds', lambda: spinner_seconds(3))
    second.new_child('Show some toast', lambda: toast.showToast('Hello wwwpy!'))
    second.new_child('Nested').new_child('Do we need this?', lambda: navbar.toast.showToast('Maybe!'))

    return root


def wrap_in_tree(root: MenuItem, navbar) -> TreeWidget:
    def item_click(item: MenuItem):
        navbar.toggle()
        if item.action is not None:
            item.action()
        else:
            print(f'action not define for item `{item.caption}`')

    menu = TreeWidget()

    menu.on_get_children = lambda i: root.children if i is None else i.children
    menu.on_get_caption = lambda i: i.caption
    menu.on_cell_render = lambda i: None if i.depth == 0 else i.cell.classList.add("py-1")
    menu.on_item_click = item_click
    return menu


