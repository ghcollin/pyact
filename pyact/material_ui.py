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

from .html import svg
from .component import state, callback, combine_callbacks, basic_element, create_namespace_element

from typing import Optional, Dict
from .context import Component, ChildList

MATERIAL_UI_CDN = "https://unpkg.com/@material-ui/core@latest/umd/material-ui.production.min.js"
MATERIAL_ICONS_CSS_CDN = "https://fonts.googleapis.com/icon?family=Material+Icons"

el, void = create_namespace_element('MaterialUI.')

def CssBaseline() -> Component:
    return basic_element('MaterialUI.CssBaseline', None, None, None, None)

def Icon(name: str, id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, **kw_args) -> Component:
    return basic_element('MaterialUI.Icon', id, key, props, children=[name], **kw_args)

def SvgIcon(d: str, id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, **kw_args) -> Component:
    return basic_element('MaterialUI.SvgIcon', id, key, props, children=[
        svg(props={'d': d})
    ], **kw_args)

def Typography(text: str, id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, **kw_args) -> Component:
    return basic_element('MaterialUI.Typography', id, key, props, children=[text], **kw_args)

FormControlLabel = void('FormControlLabel')
Switch = void('Switch')
Divider = void('Divider')

__getattr__ = el

TextField = el('TextField')

async def controlled_text_field(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, **kw_args) -> Dict:
    value, set_value = await state('value', "")
    async def onChange(value):
        set_value(value)
    props = combine_callbacks({**kw_args, **props} if props else kw_args, 'onChange', callback(onChange, ['e.target.value']))
    return await TextField(id, key, {**props, 'value': value})
