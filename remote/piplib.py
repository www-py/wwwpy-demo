
async def install(package):
    import pyodide_js
    await pyodide_js.loadPackage('micropip')
    import micropip
    await micropip.install([package])
