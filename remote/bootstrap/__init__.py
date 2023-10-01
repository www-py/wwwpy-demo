from pathlib import Path

from js import document

parent = Path(__file__).parent


def setup_bootstrap():
    document.head.insertAdjacentHTML('beforeend', (parent / 'index_head.html').read_text())

    # dynamically load a script tag to load the bootstrap js
    element = document.createElement('script')
    element.setAttribute('src', 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js')
    document.body.append(element)
