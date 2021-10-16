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
    from pyact.antd import Layout, Header, Sider, Content, Footer, Menu, SubMenu, MenuItem, Icon, make_tabs, make_radios, Select, Breadcrumb, BreadcrumbItem, InputNumber
    from pyact.html import div
    from pyact import callback, javascript_fn
    
    #globaltext = await LiveInput(props=dict(label="Live text input"))

    async def math_acos():
        value, set_value = await pyact.state('acos', 0)

        return await div(children=[ 
            "acos(",
            InputNumber(value=value, onChange=callback(set_value, ['val'])),
            ") =",
            InputNumber(value=javascript_fn("Math.acos", value), disabled=True)
        ])

    async def inner_pane(nav_item, visible):
        with await pyact.scope(str(nav_item)):
            menu_item, set_menu_item = await pyact.state('nav', 1)

            return await Layout(style={} if visible else {'display': "none"}, children=[ 
                Sider(width=200, children=[ 
                    Menu(mode='inline', defaultSelectedKeys=['1'], defaultOpenKeys=['sub1'], style={'height': '100%'}, children=[ 
                        SubMenu(key='sub1', icon=Icon("UserOutlined"), title='subnav 1', children=[
                            MenuItem(key=n, children=["nav " + n], onClick=(lambda x: callback(lambda: set_menu_item(int(x))))(n))
                        for n in map(str, range(1, 5))]),
                        SubMenu(key='sub2', icon=Icon("LaptopOutlined"), title='subnav 2', children=[
                            MenuItem(key=n, children=["nav " + n], onClick=(lambda x: callback(lambda: set_menu_item(int(x))))(n))
                        for n in map(str, range(5, 10))]),
                        SubMenu(key='sub3', icon=Icon("NotificationOutlined"), title='subnav 3', children=[
                            MenuItem(key=n, children=["nav " + n], onClick=(lambda x: callback(lambda: set_menu_item(int(x))))(n))
                        for n in map(str, range(10, 15))])
                    ])
                ]),
                Content(style={'padding': '0 50px'}, children=[
                    Breadcrumb(style={'margin': '16px 0'}, children=[ 
                        BreadcrumbItem(children=["Nav " + str(nav_item)]),
                        BreadcrumbItem(children=["Menu " + str(menu_item)])
                    ]),
                    div(style={'padding': '24px', 'background': '#fff'}, children=[
                        make_tabs([
                            ("Radio buttons", [ 
                                make_radios([
                                    (str(i), "Option " + str(i)) for i in range(1,6)
                                ], None)
                            ]),
                            ("Selection", [
                                Select(style={'width': '120px'}, options=[dict(label="Selection " + str(i), value=str(i)) for i in range(1, 11)])
                            ]),
                            ("Maths", [ 
                                math_acos()
                            ])
                        ], "Radio buttons")
                ])
                ])
            ])

    async def outer_pane():
        nav_item, set_nav_item = await pyact.state('nav', 2)

        return await Layout(key='outer', style={'min-height': '100vh'}, children=[
            Header(children=[
                div(className='logo'),
                Menu(theme='dark', mode='horizontal', defaultSelectedKeys=['2'], children=[
                    (lambda x: MenuItem(key=n, children=["nav " + n], onClick=callback(lambda: set_nav_item(int(x)))))(n)
                for n in map(str, range(1, 10))])
            ]),
            Content(children=[
                inner_pane(i, i == nav_item) for i in range(1, 10)
            ]),
            Footer(style={'textAlign': 'center'}, children=["Copyright"])
        ])

    return outer_pane

if __name__ == "__main__":
    address = '127.0.0.1'
    port = 8000

    index_html = pyact.index_html(
        "ws://{}:{}".format(address, port),
        title="ANTD Admin pane",
        crossorigin_scripts=[
            pyact.antd.ANTD_CDN,
            pyact.antd.ANTD_ICONS_CDN
        ],
        style_urls=[
            pyact.antd.ANTD_CSS_CDN
        ]
    )

    server_app = pyact.starlette.create_app(app, index_html)

    uvicorn.run(server_app, host=address, port=port)
