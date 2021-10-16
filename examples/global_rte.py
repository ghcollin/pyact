"""
Copyright (c) 2021 ghcollin
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pyact
import uvicorn # type: ignore

async def app():
    from pyact.html import Div
    from pyact import callback, element

    async def editor():
        value, set_value = await pyact.state('value', "")

        return await Div(children=[ 
            element("ReactSimpleWysiwyg.DefaultEditor", None, None, None, None, value=value, onChange=callback(set_value, ["e.target.value"]))
        ])

    global_editor = await editor()

    async def root():
        return await Div(children=[global_editor])

    return root

if __name__ == "__main__":
    address = '127.0.0.1'
    port = 8000

    index_html = pyact.index_html(
        "ws://{}:{}".format(address, port),
        title="Global react-rte component",
        crossorigin_scripts=[
            "https://unpkg.com/react-simple-wysiwyg@1.0.2/lib/umd/index.umd.min.js"
        ],
        style_urls=[
        ]
    )

    server_app = pyact.starlette.create_app(app, index_html)

    uvicorn.run(server_app, host=address, port=port)
