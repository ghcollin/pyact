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

from typing import List, Optional

template = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>{title}</title>
  </head>
  <body>
    {styles}
    <style>
    {style}
    </style>
    <div id="root"></div>
    {scripts}
    <script type="text/javascript">
//<![CDATA[
'use strict';
{javascript_head}
{javascript}
//]]>
    </script>
  </body>
</html>
"""

websocket_javascript = """
'use strict';

const h = React.createElement;

function get_component(name) {
    let c = name.split('.').reduce((o,i)=>o[i], window)
    return c ? c : name;
}

function obj_map(obj, callback) {
    var result = {};
    Object.keys(obj).forEach(function (key) {
        result[key] = callback.call(obj, obj[key], key, obj);
    });
    return result;
}

function ary_to_dict_map(ary, callback) {
    var result = {};
    ary.map(v => result[v] = callback.call(ary, v, ary));
    return result;
}

var connection = new WebSocket(serverUrl, "json");

function to_callback(json) {
    return (e) => {
        json['cbs'].map(cb => connection.send(JSON.stringify({
            key: cb["key"],
            values: ary_to_dict_map( cb["values"], val => val.split('.').reduce((o,i)=>o[i], e) )
        })))
    }
}

function RecursiveRender(json) {
    return h(
        get_component(json.el),
        obj_map(json.props, v => 
            typeof v === "object" && "__is_callback" in v ? to_callback(v) : v)
        ,
        "children" in json ? json.children.map(child =>
            typeof child === "string" ? child :
            RecursiveRender(child)
        ) : []
    )
}

const domContainer = document.querySelector('#root');

connection.onmessage = function(evt) {
    var msg = JSON.parse(evt.data);

    ReactDOM.render(RecursiveRender(msg), domContainer);
};

window.addEventListener("unload", function () {
    if(connection.readyState == WebSocket.OPEN)
    connection.close();
});
"""

REACT_CDNS= [
    "https://unpkg.com/react@17/umd/react.production.min.js",
    "https://unpkg.com/react-dom@17/umd/react-dom.production.min.js"
]

def index_html(server_url:str, 
        title: Optional[str] = None, 
        crossorigin_scripts: Optional[List[str]] = None, 
        scripts: Optional[List[str]] = None, 
        react_urls: Optional[List[str]] = None, 
        style_urls: Optional[List[str]] = None, 
        style: Optional[str] = None) -> str:
    title = title if title else ""
    crossorigin_scripts = crossorigin_scripts if crossorigin_scripts else []
    scripts = scripts if scripts else []
    react_urls = react_urls if react_urls else REACT_CDNS
    style_urls = style_urls if style_urls else []
    style = style if style else ""
    return template.format(
        title = title,
        scripts = "\n".join([
            '<script crossorigin src="{}"></script>'.format(url) for url in react_urls + crossorigin_scripts
        ] + [
            '<script src="{}"></script>'.format(url) for url in scripts
        ]),
        styles = "\n".join([
            '<link rel="stylesheet" href="{}" />'.format(url) for url in style_urls
        ]),
        style = style,
        javascript_head = 'var serverUrl = "{serverUrl}/ws";'.format(serverUrl = server_url),
        javascript = websocket_javascript
    )