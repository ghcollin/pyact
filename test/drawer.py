import pyact
import uvicorn # type: ignore

import pyact.material_ui as mui

globaltext = mui.LiveTextField(props=dict(label="Live text input"))

@pyact.state
def layout(state, ctx, appbar_contents, drawer_contents, main_contents):
    state.add_listener(ctx)
    opendraw, setOpendraw = state.create('open', True)

    drawerWidth = 240
    barStyle = {
        'width': f'calc(100% - {drawerWidth}px)',
        'marginLeft': drawerWidth
    } if opendraw else {}
    drawerStyle = {'width': drawerWidth, 'flexShrink': 0}
    contentStyle = {'marginLeft': 0, 'marginTop': 80, 'padding': 20} if opendraw else {'flexGrow': 1, 'marginLeft': -drawerWidth, 'marginTop': 80, 'padding': 20}

    return pyact.html.Div(props=dict(style={'display': 'flex'}), children=[
        mui.AppBar(props=dict(position='fixed', style=barStyle), children=[
            mui.Toolbar(children=[
                mui.IconButton(props=dict(
                        color='inherit',
                        onClick = ctx.event_callback(lambda: setOpendraw(not opendraw)),
                        edge='start',
                        style={'marginRight': 10}
                    ),
                    children=[ mui.Icon('menu') ]
                )
            ] + appbar_contents)
        ]),
        mui.Drawer(props=dict(variant='persistent', anchor='left', open=opendraw, style=drawerStyle, PaperProps={'style':{'width': drawerWidth}}), children=drawer_contents),
        pyact.html.Main(props=dict(style=contentStyle), children=main_contents)
    ])

def app():
    return pyact.html.Div(children=[
            mui.CssBaseline(),
            layout([
                mui.Typography("Drawer Test App", props=dict(variant='h6', noWrap=True))
            ], [
                
            ] + [
                mui.ListItem(props=dict(button=True), children=[
                    mui.ListItemText(props=dict(primary=text))
                ])
                for text in ['Item 1', 'Item 2', 'Item 3']
            ], [
                mui.Typography("""
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
          ut labore et dolore magna aliqua. Rhoncus dolor purus non enim praesent elementum
          facilisis leo vel. Risus at ultrices mi tempus imperdiet. Semper risus in hendrerit
          gravida rutrum quisque non tellus. Convallis convallis tellus id interdum velit laoreet id
          donec ultrices. Odio morbi quis commodo odio aenean sed adipiscing. Amet nisl suscipit
          adipiscing bibendum est ultricies integer quis. Cursus euismod quis viverra nibh cras.
          Metus vulputate eu scelerisque felis imperdiet proin fermentum leo. Mauris commodo quis
          imperdiet massa tincidunt. Cras tincidunt lobortis feugiat vivamus at augue. At augue eget
          arcu dictum varius duis at consectetur lorem. Velit sed ullamcorper morbi tincidunt. Lorem
          donec massa sapien faucibus et molestie ac.
                """, props=dict(paragraph=True)),
                globaltext
            ])
        ])

if __name__ == "__main__":
    address = '127.0.0.1'
    port = 8000

    index_html = pyact.index_html(
        "ws://{}:{}".format(address, port),
        title="Drawer test",
        crossorigin_scripts=[mui.MATERIAL_UI_CDN],
        style_urls=[
            "https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap",
            "https://fonts.googleapis.com/icon?family=Material+Icons"
        ]
    )

    server_app = pyact.starlette.create_app(app(), index_html)

    uvicorn.run(server_app, host=address, port=port)
