import dash
from dash import dcc, html, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from auth import login
from data import (
    get_overview_for_role, get_dept_for_role,
    AGE, INCOME, SATISFACTION
)

# ── App init ────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True
)
server = app.server

# ── Chart config — removes zoom/pan toolbar ─────────────
CHART_CONFIG = {
    "displayModeBar"  : False,
    "staticPlot"      : False,
    "scrollZoom"      : False,
}

# ── Theme colors ─────────────────────────────────────────
LIGHT = {"bg": "#F8F9FA", "card": "#FFFFFF", "text": "#212529", "border": "#DEE2E6"}
DARK  = {"bg": "#1A1A2E", "card": "#16213E", "text": "#E0E0E0", "border": "#2D2D44"}

# ── Root layout ──────────────────────────────────────────
app.layout = html.Div([
    dcc.Store(id="user-store",  storage_type="session"),
    dcc.Store(id="theme-store", data="light"),
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# ── Login page ───────────────────────────────────────────
def login_layout():
    return html.Div([
        html.Div([
            # IBM logo
            html.Div("IBM", style={
                "background"   : "#1F70C1",
                "color"        : "#fff",
                "padding"      : "8px 20px",
                "borderRadius" : "6px",
                "fontSize"     : "22px",
                "fontWeight"   : "bold",
                "display"      : "inline-block",
                "marginBottom" : "12px",
                "letterSpacing": "3px"
            }),
            html.H4("HR Attrition Intelligence",
                    style={"fontWeight": "600", "marginBottom": "4px"}),
            html.P("Sign in to your account",
                   style={"color": "#6C757D", "marginBottom": "28px"}),

            # Email field
            dbc.Label("Email address", style={"fontWeight": "500"}),
            dbc.Input(
                id          = "login-email",
                type        = "email",
                placeholder = "Enter your email",
                className   = "mb-3"
            ),

            # Password field with show/hide toggle
            dbc.Label("Password", style={"fontWeight": "500"}),
            html.Div([
                dbc.Input(
                    id          = "login-password",
                    type        = "password",
                    placeholder = "Enter your password",
                    style       = {"paddingRight": "45px"}
                ),
                html.I(
                    id        = "toggle-password",
                    className = "bi bi-eye",
                    style     = {
                        "position"  : "absolute",
                        "right"     : "12px",
                        "top"       : "50%",
                        "transform" : "translateY(-50%)",
                        "cursor"    : "pointer",
                        "color"     : "#6C757D",
                        "fontSize"  : "18px",
                        "zIndex"    : "10"
                    }
                )
            ], style={"position": "relative", "marginBottom": "20px"}),

            # Error message
            html.Div(id="login-error",
                     style={"color": "#DC3545", "marginBottom": "12px",
                            "fontSize": "14px", "textAlign": "center"}),

            # Sign in button
            dbc.Button(
                "Sign In",
                id        = "login-btn",
                color     = "primary",
                className = "w-100 mb-4",
                style     = {"padding": "10px", "fontWeight": "500"}
            ),

            html.Hr(),

            # Demo credentials
            html.P("Demo Credentials",
                   style={"fontWeight": "600", "marginBottom": "10px",
                          "color": "#495057", "fontSize": "14px"}),
            html.Div([
                html.Div([
                    dbc.Badge("Admin",   color="danger",  className="me-2"),
                    html.Small("admin@hrapp.com / Admin@123")
                ], className="mb-2"),
                html.Div([
                    dbc.Badge("Manager", color="success", className="me-2"),
                    html.Small("manager@hrapp.com / Manager@123")
                ], className="mb-2"),
                html.Div([
                    dbc.Badge("Analyst", color="warning", className="me-2"),
                    html.Small("analyst@hrapp.com / Analyst@123")
                ]),
            ], style={
                "background"   : "#F8F9FA",
                "padding"      : "14px",
                "borderRadius" : "8px",
                "textAlign"    : "left"
            }),

        ], style={
            "maxWidth"     : "420px",
            "margin"       : "60px auto",
            "padding"      : "40px",
            "borderRadius" : "16px",
            "boxShadow"    : "0 4px 24px rgba(0,0,0,0.10)",
            "background"   : "#FFFFFF",
            "textAlign"    : "center"
        })
    ], style={"background": "#F0F4F8", "minHeight": "100vh"})


# ── Dashboard layout ─────────────────────────────────────
def dashboard_layout(user, theme="light"):
    role  = user["role"]
    name  = user["name"]
    dept  = user["dept"]
    t     = DARK if theme == "dark" else LIGHT

    overview = get_overview_for_role(role, dept)
    dept_df  = get_dept_for_role(role, dept)

    show_salary = role in ["Admin", "Manager"]

    # ── KPI cards ────────────────────────────────────────
    kpi_style = {
        "background"   : t["card"],
        "border"       : f"1px solid {t['border']}",
        "borderRadius" : "12px",
        "padding"      : "20px",
        "textAlign"    : "center",
        "color"        : t["text"]
    }

    kpi_cards = dbc.Row([
        dbc.Col(html.Div([
            html.P("Total Employees",
                   style={"color": "#6C757D", "fontSize": "13px", "marginBottom": "6px"}),
            html.H3(f"{int(overview['total_employees'].iloc[0]):,}",
                    style={"fontWeight": "700", "color": "#1F70C1"}),
            html.Small("Full workforce", style={"color": "#6C757D"})
        ], style=kpi_style), width=3),

        dbc.Col(html.Div([
            html.P("Attrition Rate",
                   style={"color": "#6C757D", "fontSize": "13px", "marginBottom": "6px"}),
            html.H3(f"{overview['attrition_rate'].iloc[0]}%",
                    style={"fontWeight": "700", "color": "#D85A30"}),
            html.Small(f"{int(overview['total_attrition'].iloc[0])} employees left"
                       if "total_attrition" in overview.columns else "dept rate",
                       style={"color": "#6C757D"})
        ], style=kpi_style), width=3),

        dbc.Col(html.Div([
            html.P("Avg Monthly Income",
                   style={"color": "#6C757D", "fontSize": "13px", "marginBottom": "6px"}),
            html.H3(
                f"${int(overview['avg_monthly_income'].iloc[0]):,}"
                if show_salary else "🔒 Restricted",
                style={"fontWeight": "700",
                       "color": "#1D9E75" if show_salary else "#6C757D"}
            ),
            html.Small("Across all roles" if show_salary else "Analyst role only",
                       style={"color": "#6C757D"})
        ], style=kpi_style), width=3),

        dbc.Col(html.Div([
            html.P("Avg Tenure",
                   style={"color": "#6C757D", "fontSize": "13px", "marginBottom": "6px"}),
            html.H3(f"{overview['avg_tenure_years'].iloc[0]} yrs",
                    style={"fontWeight": "700", "color": "#534AB7"}),
            html.Small("Years at company", style={"color": "#6C757D"})
        ], style=kpi_style), width=3),
    ], className="mb-4 g-3")

    # ── Charts ───────────────────────────────────────────
    # Chart 1 — Dept: Horizontal bar
    fig_dept = px.bar(
        dept_df.sort_values("attrition_rate"),
        x           = "attrition_rate",
        y           = "department",
        orientation = "h",
        title       = "Attrition Rate by Department",
        labels      = {"attrition_rate": "Attrition %", "department": ""},
        color       = "attrition_rate",
        color_continuous_scale = "Reds",
        text        = "attrition_rate"
    )
    fig_dept.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_dept.update_layout(
        plot_bgcolor  = t["card"],
        paper_bgcolor = t["card"],
        font_color    = t["text"],
        showlegend    = False,
        coloraxis_showscale = False,
        margin        = dict(l=10, r=30, t=40, b=10)
    )

    # Chart 2 — Age: Funnel chart
    fig_age = go.Figure(go.Funnel(
        y      = AGE["age_group"],
        x      = AGE["attrition_rate"],
        textinfo = "label+value+percent initial",
        marker = {"color": ["#534AB7","#7F77DD","#AFA9EC","#CECBF6","#E8E6FB"]}
    ))
    fig_age.update_layout(
        title         = "Attrition Rate by Age Group",
        plot_bgcolor  = t["card"],
        paper_bgcolor = t["card"],
        font_color    = t["text"],
        margin        = dict(l=10, r=10, t=40, b=10)
    )

    # Chart 3 — Income: Pie chart
    fig_income = px.pie(
        INCOME,
        names  = "income_band",
        values = "attrition_count",
        title  = "Attrition Count by Income Band",
        color_discrete_sequence = px.colors.sequential.Blues_r,
        hole   = 0.4
    )
    fig_income.update_traces(
        textposition = "inside",
        textinfo     = "percent+label"
    )
    fig_income.update_layout(
        plot_bgcolor  = t["card"],
        paper_bgcolor = t["card"],
        font_color    = t["text"],
        margin        = dict(l=10, r=10, t=40, b=10)
    )

    # Chart 4 — Satisfaction: Grouped bar
    fig_sat = px.bar(
        SATISFACTION,
        x     = "satisfaction_label",
        y     = ["total_employees", "attrition_count"],
        title = "Job Satisfaction vs Attrition",
        labels = {"value": "Count", "satisfaction_label": "Satisfaction Level",
                  "variable": "Metric"},
        barmode = "group",
        color_discrete_map = {
            "total_employees" : "#1F70C1",
            "attrition_count" : "#D85A30"
        }
    )
    fig_sat.update_layout(
        plot_bgcolor  = t["card"],
        paper_bgcolor = t["card"],
        font_color    = t["text"],
        margin        = dict(l=10, r=10, t=40, b=10),
        legend        = dict(orientation="h", y=-0.2)
    )

    chart_card_style = {
        "background"   : t["card"],
        "borderRadius" : "12px",
        "padding"      : "16px",
        "border"       : f"1px solid {t['border']}",
        "cursor"       : "pointer"
    }

    charts = dbc.Row([
        dbc.Col(html.Div(
            dcc.Graph(id="chart-dept", figure=fig_dept, config=CHART_CONFIG),
            style=chart_card_style, id="card-dept"
        ), width=6),
        dbc.Col(html.Div(
            dcc.Graph(id="chart-age", figure=fig_age, config=CHART_CONFIG),
            style=chart_card_style, id="card-age"
        ), width=6),
        dbc.Col(html.Div(
            dcc.Graph(id="chart-income", figure=fig_income, config=CHART_CONFIG),
            style=chart_card_style, id="card-income"
        ), width=6, className="mt-3"),
        dbc.Col(html.Div(
            dcc.Graph(id="chart-sat", figure=fig_sat, config=CHART_CONFIG),
            style=chart_card_style, id="card-sat"
        ), width=6, className="mt-3"),
    ])

    # ── Modal popup for charts ────────────────────────────
    modal = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
        dbc.ModalBody(dcc.Graph(id="modal-chart", config=CHART_CONFIG)),
    ], id="chart-modal", size="xl", is_open=False)

    # ── Role badge color ─────────────────────────────────
    role_color = {"Admin": "danger", "Manager": "success", "Analyst": "warning"}

    return html.Div([
        # Navbar
        dbc.Navbar(dbc.Container([
            # Left — IBM branding
            html.Div([
                html.Span("IBM", style={
                    "background"   : "#1F70C1",
                    "color"        : "#fff",
                    "padding"      : "4px 12px",
                    "borderRadius" : "4px",
                    "fontWeight"   : "bold",
                    "marginRight"  : "10px",
                    "letterSpacing": "2px"
                }),
                html.Span("HR Attrition Intelligence",
                          style={"fontWeight": "600", "fontSize": "16px",
                                 "color": t["text"]}),
            ], style={"display": "flex", "alignItems": "center"}),

            # Right — role, theme toggle, logout
            html.Div([
                dbc.Badge(role, color=role_color.get(role, "primary"),
                          className="me-3 p-2"),
                html.Span(f"👤 {name}",
                          style={"fontSize": "13px", "marginRight": "16px",
                                 "color": t["text"]}),
                dbc.Switch(
                    id        = "theme-toggle",
                    label     = "🌙 Dark",
                    value     = theme == "dark",
                    className = "me-3"
                ),
                dbc.Button("Logout", id="logout-btn",
                           size="sm", color="outline-secondary"),
            ], style={"display": "flex", "alignItems": "center"}),
        ], fluid=True),
        color  = t["card"],
        dark   = False,
        className = "mb-4 shadow-sm",
        style  = {"borderBottom": f"1px solid {t['border']}"}),

        # Manager restriction banner
        dbc.Alert([
            html.I(className="bi bi-info-circle me-2"),
            f"You are viewing {dept} department data only. "
            f"Contact Admin for full access."
        ], color="warning", className="mx-3 mb-3") if role == "Manager" else html.Div(),

        # Main content
        dbc.Container([
            # Description for non-technical users
            dbc.Alert([
                html.Strong("About this dashboard: "),
                "This app analyses employee attrition patterns across the organisation. "
                "Use the charts below to understand why employees leave, "
                "which departments are most affected, and where to focus retention efforts."
            ], color="info", className="mb-4"),

            kpi_cards,
            charts,
            modal,

            # Hidden div for logout redirect
            html.Div(id="logout-redirect")
        ], fluid=True)
    ], style={"background": t["bg"], "minHeight": "100vh"})


# ── Callbacks ────────────────────────────────────────────

# Page router
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    State("user-store", "data"),
    State("theme-store", "data")
)
def render_page(pathname, user, theme):
    if user:
        return dashboard_layout(user, theme or "light")
    return login_layout()

# Login handler
@app.callback(
    Output("user-store",    "data"),
    Output("login-error",   "children"),
    Output("url",           "pathname"),
    Input("login-btn",      "n_clicks"),
    State("login-email",    "value"),
    State("login-password", "value"),
    prevent_initial_call=True
)
def handle_login(n_clicks, email, password):
    if not email or not password:
        return None, "Please enter email and password.", "/"
    user = login(email, password)
    if user:
        return user, "", "/dashboard"
    return None, "Invalid email or password. Please try again.", "/"

# Password show/hide toggle
@app.callback(
    Output("login-password", "type"),
    Output("toggle-password", "className"),
    Input("toggle-password", "n_clicks"),
    State("login-password", "type"),
    prevent_initial_call=True
)
def toggle_password(n, current_type):
    if current_type == "password":
        return "text", "bi bi-eye-slash"
    return "password", "bi bi-eye"

# Logout handler
@app.callback(
    Output("user-store", "data",     allow_duplicate=True),
    Output("url",        "pathname", allow_duplicate=True),
    Input("logout-btn",  "n_clicks"),
    prevent_initial_call=True
)
def handle_logout(n):
    return None, "/"

# Theme toggle
@app.callback(
    Output("theme-store",  "data"),
    Output("page-content", "children", allow_duplicate=True),
    Input("theme-toggle",  "value"),
    State("user-store",    "data"),
    prevent_initial_call=True
)
def toggle_theme(is_dark, user):
    theme = "dark" if is_dark else "light"
    if user:
        return theme, dashboard_layout(user, theme)
    return theme, no_update

# Chart modal popup — dept
@app.callback(
    Output("chart-modal", "is_open"),
    Output("modal-title", "children"),
    Output("modal-chart", "figure"),
    Input("chart-dept",   "clickData"),
    Input("chart-age",    "clickData"),
    Input("chart-income", "clickData"),
    Input("chart-sat",    "clickData"),
    State("chart-modal",  "is_open"),
    State("theme-store",  "data"),
    prevent_initial_call=True
)
def open_modal(dept_click, age_click, income_click, sat_click, is_open, theme):
    from dash import ctx
    t = DARK if theme == "dark" else LIGHT

    triggered = ctx.triggered_id

    if triggered == "chart-dept" and dept_click:
        from data import DEPT
        fig = px.bar(
            DEPT.sort_values("attrition_rate"),
            x="attrition_rate", y="department",
            orientation="h",
            color="attrition_rate",
            text="attrition_rate",
            color_continuous_scale="Reds",
            labels={"attrition_rate":"Attrition %","department":""}
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(plot_bgcolor=t["card"], paper_bgcolor=t["card"],
                          font_color=t["text"], coloraxis_showscale=False)
        return True, "Attrition by Department — Detail", fig

    if triggered == "chart-age" and age_click:
        fig = px.bar(
            AGE, x="age_group", y="attrition_rate",
            color="attrition_rate", text="attrition_rate",
            color_continuous_scale="Purples",
            labels={"attrition_rate":"Attrition %","age_group":"Age Group"}
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(plot_bgcolor=t["card"], paper_bgcolor=t["card"],
                          font_color=t["text"], coloraxis_showscale=False)
        return True, "Attrition by Age Group — Detail", fig

    if triggered == "chart-income" and income_click:
        fig = px.bar(
            INCOME, x="income_band", y="attrition_rate",
            color="attrition_rate", text="attrition_rate",
            color_continuous_scale="Blues",
            labels={"attrition_rate":"Attrition %","income_band":"Income Band"}
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(plot_bgcolor=t["card"], paper_bgcolor=t["card"],
                          font_color=t["text"], coloraxis_showscale=False)
        return True, "Attrition by Income Band — Detail", fig

    if triggered == "chart-sat" and sat_click:
        fig = px.bar(
            SATISFACTION, x="satisfaction_label",
            y=["total_employees","attrition_count"],
            barmode="group",
            color_discrete_map={
                "total_employees":"#1F70C1",
                "attrition_count":"#D85A30"
            },
            labels={"value":"Count","satisfaction_label":"Satisfaction"}
        )
        fig.update_layout(plot_bgcolor=t["card"], paper_bgcolor=t["card"],
                          font_color=t["text"])
        return True, "Job Satisfaction vs Attrition — Detail", fig

    return False, no_update, no_update


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
