import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from auth import login

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
server = app.server

app.layout = html.Div([
    dcc.Store(id="user-store", storage_type="session"),
    dcc.Store(id="theme-store", data="light"),
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# ── Login page ──────────────────────────────────────────
def login_layout():
    return dbc.Container([
        dbc.Row(dbc.Col([
            html.Div([
                html.Div("IBM", style={
                    "background":"#1F70C1","color":"#fff",
                    "padding":"6px 16px","borderRadius":"6px",
                    "display":"inline-block","fontSize":"20px",
                    "fontWeight":"bold","marginBottom":"12px"
                }),
                html.H4("HR Attrition Intelligence", className="mb-1"),
                html.P("Sign in to continue", className="text-muted mb-4"),
                dbc.Input(id="login-email",    placeholder="Email",    type="email",    className="mb-3"),
                dbc.Input(id="login-password", placeholder="Password", type="password", className="mb-3"),
                dbc.Button("Sign In", id="login-btn", color="primary", className="w-100 mb-3"),
                html.Div(id="login-error", className="text-danger text-center"),
                html.Hr(),
                html.Small("Demo credentials", className="text-muted d-block text-center mb-2"),
                html.Small("Admin: admin@hrapp.com / Admin@123",   className="text-muted d-block text-center"),
                html.Small("Manager: manager@hrapp.com / Manager@123", className="text-muted d-block text-center"),
                html.Small("Analyst: analyst@hrapp.com / Analyst@123", className="text-muted d-block text-center"),
            ], style={
                "maxWidth":"400px","margin":"80px auto",
                "padding":"40px","borderRadius":"12px",
                "boxShadow":"0 2px 16px rgba(0,0,0,0.1)",
                "textAlign":"center"
            })
        ]))
    ], fluid=True)

# ── Dashboard layout ─────────────────────────────────────
def dashboard_layout(user):
    role = user["role"]
    name = user["name"]
    dept = user["dept"]

    try:
        overview     = pd.DataFrame([{"total_employees":1470,"total_attrition":237,"attrition_rate":16.1,"avg_age":36.9,"avg_monthly_income":6503,"avg_tenure_years":7.0}])
        dept_df      = pd.DataFrame([{"department":"Sales","attrition_rate":20.6},{"department":"Human Resources","attrition_rate":19.0},{"department":"Research & Development","attrition_rate":13.8}])
        age_df       = pd.DataFrame([{"age_group":"18-25","attrition_rate":38.4},{"age_group":"26-35","attrition_rate":19.7},{"age_group":"36-45","attrition_rate":12.1},{"age_group":"46-55","attrition_rate":10.9},{"age_group":"55+","attrition_rate":8.7}])
        income_df    = pd.DataFrame([{"income_band":"1k-3k","attrition_rate":29.8},{"income_band":"3k-6k","attrition_rate":14.2},{"income_band":"6k-10k","attrition_rate":9.1},{"income_band":"10k+","attrition_rate":6.3}])
        sat_df       = pd.DataFrame([{"satisfaction_label":"Low","attrition_rate":22.8},{"satisfaction_label":"Medium","attrition_rate":16.4},{"satisfaction_label":"High","attrition_rate":14.4},{"satisfaction_label":"Very High","attrition_rate":11.3}])
    except:
        pass

    if role == "Manager":
        dept_df  = dept_df[dept_df["department"].str.contains(dept, case=False)]

    show_salary = role in ["Admin", "Analyst"]

    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([
            html.P("Total Employees", className="text-muted small mb-1"),
            html.H3(f"{overview['total_employees'].iloc[0]:,}"),
        ])]), width=3),
        dbc.Col(dbc.Card([dbc.CardBody([
            html.P("Attrition Rate", className="text-muted small mb-1"),
            html.H3(f"{overview['attrition_rate'].iloc[0]}%", style={"color":"#D85A30"}),
        ])]), width=3),
        dbc.Col(dbc.Card([dbc.CardBody([
            html.P("Avg Monthly Income", className="text-muted small mb-1"),
            html.H3(f"${overview['avg_monthly_income'].iloc[0]:,}" if show_salary else "🔒 Hidden"),
        ])]), width=3),
        dbc.Col(dbc.Card([dbc.CardBody([
            html.P("Avg Tenure", className="text-muted small mb-1"),
            html.H3(f"{overview['avg_tenure_years'].iloc[0]} yrs"),
        ])]), width=3),
    ], className="mb-4")

    charts = dbc.Row([
        dbc.Col(dcc.Graph(figure=px.bar(
            dept_df, x="department", y="attrition_rate",
            title="Attrition by Department",
            labels={"attrition_rate":"Attrition %","department":"Department"},
            color="attrition_rate", color_continuous_scale="Reds"
        )), width=6),
        dbc.Col(dcc.Graph(figure=px.bar(
            age_df, x="age_group", y="attrition_rate",
            title="Attrition by Age Group",
            labels={"attrition_rate":"Attrition %","age_group":"Age Group"},
            color="attrition_rate", color_continuous_scale="Purples"
        )), width=6),
        dbc.Col(dcc.Graph(figure=px.bar(
            income_df, x="income_band", y="attrition_rate",
            title="Attrition by Income Band",
            labels={"attrition_rate":"Attrition %","income_band":"Income Band"},
            color="attrition_rate", color_continuous_scale="Blues"
        )), width=6),
        dbc.Col(dcc.Graph(figure=px.bar(
            sat_df, x="satisfaction_label", y="attrition_rate",
            title="Attrition by Job Satisfaction",
            labels={"attrition_rate":"Attrition %","satisfaction_label":"Satisfaction"},
            color="attrition_rate", color_continuous_scale="Greens"
        )), width=6),
    ])

    return dbc.Container([
        # Navbar
        dbc.Navbar(dbc.Container([
            html.Div([
                html.Span("IBM", style={"background":"#1F70C1","color":"#fff","padding":"4px 10px","borderRadius":"4px","fontWeight":"bold","marginRight":"10px"}),
                html.Span("HR Attrition Intelligence", style={"fontWeight":"500"}),
            ]),
            html.Div([
                dbc.Badge(role, color="primary", className="me-2"),
                html.Span(f"👤 {name}", className="me-3 small"),
                dbc.Button("Logout", id="logout-btn", size="sm", color="outline-secondary"),
            ], style={"display":"flex","alignItems":"center"})
        ]), color="white", dark=False, className="mb-4 shadow-sm"),

        # Restricted banner for Manager
        dbc.Alert(f"You are viewing {dept} department data only.", color="warning", className="mb-3") if role == "Manager" else html.Div(),

        kpi_cards,
        charts,
        html.Div(id="logout-redirect")
    ], fluid=True)

# ── Callbacks ────────────────────────────────────────────
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    State("user-store", "data")
)
def render_page(pathname, user):
    if user:
        return dashboard_layout(user)
    return login_layout()

@app.callback(
    Output("user-store",  "data"),
    Output("login-error", "children"),
    Output("url",         "pathname"),
    Input("login-btn",    "n_clicks"),
    State("login-email",    "value"),
    State("login-password", "value"),
    prevent_initial_call=True
)
def handle_login(n_clicks, email, password):
    if not email or not password:
        return None, "Please enter email and password", "/"
    user = login(email, password)
    if user:
        return user, "", "/dashboard"
    return None, "Invalid email or password", "/"

@app.callback(
    Output("user-store",     "data",    allow_duplicate=True),
    Output("url",            "pathname", allow_duplicate=True),
    Input("logout-btn",      "n_clicks"),
    prevent_initial_call=True
)
def handle_logout(n):
    return None, "/"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
