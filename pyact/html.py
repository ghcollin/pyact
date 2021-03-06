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

from typing import Optional, Dict, List, Any
from .context import Component, ChildList
from .component import basic_element, create_namespace_element

# def Div(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None, **kw_args) -> Component:
#     return basic_element('div', id, key, props, children, **kw_args)
    
# def B(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None, **kw_args) -> Component:
#     return basic_element('b', id, key, props, children, **kw_args)

# def Svg(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, **kw_args) -> Component:
#     return basic_element('svg', id, key, props, None, **kw_args)

# def Main(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None, **kw_args) -> Component:
#     return basic_element('main', id, key, props, children, **kw_args)

# def Header(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None, **kw_args) -> Component:
#     return basic_element('header', id, key, props, children, **kw_args)


__getattr__, void = create_namespace_element('')

# #div = el('div')
# b = el('b')
# main = el('main')
# header = el('header')

svg = void('svg')

# def __getattr__(name: str):
#     return el(name)