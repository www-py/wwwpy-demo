from __future__ import annotations

import asyncio
from typing import Callable, Awaitable

from js import window, console
from pyodide.ffi import create_once_callable

AwaitableCallback = Callable[[], Awaitable[any]]


async def wait_animation_frame():
    event = asyncio.Event()

    def callback(*args):
        console.log('waitAnimationFrame callback!')
        console.log(args)
        event.set()

    window.requestAnimationFrame(create_once_callable(callback))
    await event.wait()
    console.log('waitAnimationFrame done')


def set_timeout(callback: AwaitableCallback, timeout: int | None = 0):
    window.setTimeout(create_once_callable(callback), timeout)
