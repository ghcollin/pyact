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

styles = dict(
    done = dict(
        textDecoration= "line-through",
        opacity= ".5",
        display= "flex",
        width= "100%"
    ),
    header = dict(
        justifyContent= "center",
        display= "flex",
        flexDirection= "row",
        alignItems= "center"
    ),
    main = dict(
        width= "100%",
        maxWidth= "400px",
        margin= "20px auto"
    ),
    card = dict(
        padding= "20px",
        margin= "20px 0"
    ),
    todo = dict(
        position= "relative",
        display= "flex",
        flexFow= "row",
        alignContent= "space-between"
    ),
    label = dict(
        display= "flex",
        width= "100%"
    ),
    divider = dict(
        position= "absolute",
        width= "100%",
        top= 0
    )
)

async def app():
    from pyact.material_ui import TextField, Button, Card, FormGroup, Divider, FormControlLabel, Switch, Tooltip, IconButton, Icon
    from pyact.html import Div, Header
    from pyact import callback

    async def task(index, value, enabled, update_task):
        def toggle():
            update_task(index, (value, not enabled))
        def delete():
            update_task(index, None)
        return await Div(key=index, style=styles['todo'], children=[ 
            Divider(style=styles['divider']) if index > 0 else None,
            FormControlLabel(label=value, style=styles['label' if enabled else 'done'],
                control=Switch(color='primary', checked=enabled, onChange=callback(toggle))),
            Tooltip(title="Delete task", placement='top', children=
                IconButton(props={'aria-label': 'delete'}, onClick=callback(delete), children=[ 
                    Icon("delete")
                ])
            )
        ])

    async def todo():
        new_task, set_new_task = await pyact.state('new_task', "")

        tasks, set_tasks = await pyact.state('tasks', [])
        def add_task():
            set_tasks(tasks + [(new_task, True)])
            set_new_task("")

        def update_task(index, update):
            new_tasks = tasks.copy()
            if update:
                new_tasks[index] = update
            else:
                new_tasks.pop(index)
            set_tasks(new_tasks)

        return await Div(style=styles['main'], children=[ 
            Header(style=styles['header'], children=[ 
                TextField(label="Add new task", value=new_task, onChange=callback(set_new_task, ['e.target.value'])),
                Button(variant='raised', color='primary', disabled=(len(new_task) == 0), onClick=callback(add_task), children=["Add"])
            ]),
            Card(style=styles['card'], children=[ 
                FormGroup(children=[ 
                   task(index, value, enabled, update_task) for index, (value, enabled) in enumerate(tasks) 
                ])
            ]) if len(tasks) > 0 else None
        ])

    return todo

if __name__ == "__main__":
    address = '127.0.0.1'
    port = 8000

    index_html = pyact.index_html(
        "ws://{}:{}".format(address, port),
        title="Material UI todo",
        crossorigin_scripts=[
            #pyact.material_ui.MATERIAL_UI_CDN
            "https://unpkg.com/@material-ui/core@4.12.3/umd/material-ui.development.js"
        ],
        style_urls=[
            pyact.material_ui.MATERIAL_ICONS_CSS_CDN
        ]
    )

    server_app = pyact.starlette.create_app(app, index_html)

    uvicorn.run(server_app, host=address, port=port)
