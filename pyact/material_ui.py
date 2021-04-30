from .html import basic_element, Svg
from .component import state, combine_callbacks

from typing import Optional, Dict
from .types import PyactApp, ChildList

MATERIAL_UI_CDN = "https://unpkg.com/@material-ui/core@latest/umd/material-ui.production.min.js"

def TextField(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('MaterialUI.TextField', id, key, props, children)

def Button(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('MaterialUI.Button', id, key, props, children)

def AppBar(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('MaterialUI.AppBar', id, key, props, children)

def Toolbar(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('MaterialUI.Toolbar', id, key, props, children)

def CssBaseline() -> PyactApp:
    return basic_element('MaterialUI.CssBaseline', None, None, None, None)

def Drawer(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('MaterialUI.Drawer', id, key, props, children)

def List(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('MaterialUI.List', id, key, props, children)

def ListItem(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('MaterialUI.ListItem', id, key, props, children)

def ListItemIcon(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('MaterialUI.ListItemIcon', id, key, props, children)

def ListItemText(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('MaterialUI.ListItemText', id, key, props, children)

def IconButton(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('MaterialUI.IconButton', id, key, props, children)

def Icon(name: str, id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None) -> PyactApp:
    return basic_element('MaterialUI.Icon', id, key, props, children=[name])

def SvgIcon(d: str, id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None) -> PyactApp:
    return basic_element('MaterialUI.SvgIcon', id, key, props, children=[
        Svg(props={'d': d})
    ])

def Typography(text: str, id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None) -> PyactApp:
    return basic_element('MaterialUI.Typography', id, key, props, children=[text])

@state
def LiveTextField(state, ctx, id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None) -> PyactApp:
    state.add_listener(ctx)
    value, set_value = state.create('value', "")
    async def onChange(values):
        set_value(values['target.value'])
    props = combine_callbacks(props, 'onChange', ctx.event_callback(onChange, ['target.value']))
    return TextField(id, key, {**props, 'value': value})