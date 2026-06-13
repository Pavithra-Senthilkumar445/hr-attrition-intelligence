from dash import html

def login_layout():
    return html.Div([
        html.H2("Login Page"),
        html.Input(id="username", placeholder="Username"),
        html.Br(),
        html.Input(id="password", type="password", placeholder="Password"),
        html.Br(),
        html.Button("Login", id="login-btn")
    ])

def layout():
    return html.Div([
        html.H2("Employee Dashboard"),
        html.P("Welcome to HR Analytics Portal")
    ])
