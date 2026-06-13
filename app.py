import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# ---------------- DATA ----------------
df = pd.read_csv("data.csv")

if "Attrition" in df.columns:
    df["Attrition_Flag"] = df["Attrition"].map({"Yes": 1, "No": 0})

# ---------------- USERS ----------------
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "manager": {"password": "manager123", "role": "manager"},
    "employee": {"password": "emp123", "role": "employee"}
}

# ---------------- APP ----------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Store(id="session"),
    html.Div(id="page-content")
])

# ---------------- LOGIN ----------------
def login_page():
    return dbc.Container([
        html.H2("HR Dashboard Login", className="text-center mt-5"),

        dbc.Row([
            dbc.Col([
                dbc.Input(id="username", placeholder="Username"),
                html.Br(),
                dbc.Input(id="password", type="password", placeholder="Password"),
                html.Br(),
                dbc.Button("Login", id="login-btn"),
                html.Div(id="msg", className="text-danger")
            ], width=4)
        ], justify="center")
    ])

# ---------------- DASHBOARDS ----------------
def admin_dashboard():
    fig = px.histogram(df, x="Age", title="Age Distribution")
    return html.Div([html.H2("Admin Dashboard"), dcc.Graph(figure=fig)])

def manager_dashboard():
    fig = px.pie(df, names="Attrition_Flag", title="Attrition Rate")
    return html.Div([html.H2("Manager Dashboard"), dcc.Graph(figure=fig)])

def employee_dashboard():
    return html.Div([html.H2("Employee Dashboard"), html.P("Welcome!")])

# ---------------- ROUTING ----------------
@app.callback(
    Output("page-content", "children"),
    Input("session", "data")
)
def route(session):
    if not session:
        return login_page()

    role = session.get("role")

    if role == "admin":
        return admin_dashboard()
    elif role == "manager":
        return manager_dashboard()
    else:
        return employee_dashboard()

# ---------------- LOGIN LOGIC ----------------
@app.callback(
    Output("session", "data"),
    Output("msg", "children"),
    Input("login-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def login(n, u, p):
    if u in users and users[u]["password"] == p:
        return {"role": users[u]["role"]}, ""
    return None, "Invalid login"

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=False)
