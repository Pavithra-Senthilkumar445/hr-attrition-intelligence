from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from utils.auth import authenticate_user
from pages import admin, manager, employee

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="session"),

    html.Div(id="page-content")
])

# LOGIN + ROUTING
@app.callback(
    Output("session", "data"),
    Input("login-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def login(n, u, p):
    return authenticate_user(u, p)

@app.callback(
    Output("page-content", "children"),
    Input("session", "data")
)
def route(session):
    if not session:
        return employee.login_layout()

    role = session.get("role")

    if role == "admin":
        return admin.layout()
    elif role == "manager":
        return manager.layout()
    else:
        return employee.layout()

if __name__ == "__main__":
    app.run_server(debug=True)
