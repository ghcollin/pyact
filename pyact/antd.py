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

from .component import create_namespace_element, state, callback, basic_element, combine_callbacks

from typing import Optional, Dict, Callable, Union, Tuple, List
from .context import Component, ChildList

ANTD_CDN = "https://unpkg.com/antd@latest/dist/antd.min.js"
ANTD_CSS_CDN = "https://unpkg.com/antd@latest/dist/antd.min.css"
ANTD_ICONS_CDN = "https://unpkg.com/@ant-design/icons@4.7.0/dist/index.umd.min.js"

el, void = create_namespace_element('antd.')

Header = el('Layout.Header')
Sider = el('Layout.Sider')
Content = el('Layout.Content')
Footer = el('Layout.Footer')

SubMenu = el('Menu.SubMenu')
MenuItem = el('Menu.Item')

TabPane = el('Tabs.TabPane')
SelectOption = el('Select.Option')
RadioGroup = el('Radio.Group')
BreadcrumbItem = el('Breadcrumb.Item')

Input = void('Input')
InputNumber = void('InputNumber')

def Icon(name: str, id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, **kw_args) -> Component:
    return basic_element('icons.' + name, id, key, props, None, **kw_args)

__getattr__ = el

## Custom elements

Tabs = el('Tabs')
Radio = el('Radio')

async def controlled_input(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, on_change: Optional[Callable[[str], str]] = None, **kw_args) -> Dict:
    value, set_value = await state('value', "")
    async def onChange(value):
        set_value(on_change(value) if on_change else value)
    props = combine_callbacks({**kw_args, **props} if props else kw_args, 'onChange', callback(onChange, ['e.target.value']))
    return await Input(id, key, {**props, 'value': value})

def make_tabs(panes: List[Tuple[str, Union[str, ChildList]]], default_key: str,
    id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, **kw_args):
    pane = lambda key, c: TabPane(key=key, tab=key, children=[c] if isinstance(c, str) else c)
    return Tabs(id, key, props, defaultActiveKey=default_key, children=[
        pane(*k) for k in panes
    ], **kw_args)

def make_radios(panes: List[Tuple[str, Union[str, ChildList]]], default_value: Optional[str],
    id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, **kw_args):
    button = lambda value, c: Radio(value=value, children=[c] if isinstance(c, str) else c)
    return RadioGroup(id, key, props, **({'defaultValue':default_value} if default_value else {}), children=[
        button(*k) for k in panes
    ], **kw_args)
