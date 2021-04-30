from typing import Optional, Dict

from .types import PyactApp, ChildList

def basic_element(el: str, id: Optional[str], key: Optional[str], props: Optional[Dict], children: Optional[ChildList]) -> PyactApp:
    return lambda ctx: {
        'el': "{}#{}".format(el, id) if id else el,
        'props' : {
            **(props if props else {}),
            'key': key if key else ctx.next_key()
        },
        'children': [ c(ctx) if callable(c) else c for c in children ] if children else []
    }

def Div(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('div', id, key, props, children)
    
def B(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('b', id, key, props, children)

def Svg(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None) -> PyactApp:
    return basic_element('svg', id, key, props, None)

def Main(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None) -> PyactApp:
    return basic_element('main', id, key, props, children)