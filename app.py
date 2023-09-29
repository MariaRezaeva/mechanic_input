import dash
import dash_auth
from dash import dcc
from dash import Input, Output, html
import dash_bootstrap_components as dbc
import repair, reserve
from flask import request

#This password for enter to app
VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world',
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


content = html.Div(
    id="page-content",
    className='content_style',)

name = 'Семендяев'
app.layout = html.Div([
        dcc.Location(id="url"),
        html.Div([
            html.Div(className='greeting', id='username'),
            html.Div([dbc.Nav([
                dbc.NavItem(dbc.NavLink("Ремонты", href="repair")),
                dbc.NavItem(dbc.NavLink("Склад и заявки", href="reserve")),
            ], pills=True, fill=True),
            html.Div(id="hidden_div", style={"display": "none"}),
                    ], className='menu'),
        ], className='user', id = 'error'),
        content,
    ], className="wrapper", id='exit')


#style={"background":"#F3F3F9"}


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):

    if pathname == "/repair":
        return repair.repair_layout
    elif pathname == "/reserve":
        return reserve.reserve_layout
    else:
        return repair.repair_layout

        # If the user tries to reach a different page, return a 404 message
@app.callback(Output("username", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    return f"Добро пожаловать, господин {request.authorization['username']}"

if __name__ == "__main__":
    #app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=False, port = 8050)