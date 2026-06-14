from flask import session
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, no_update, ctx, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from auth import login
from data import get_data_for_role, GOLD_OVERVIEW, AGE_GROUPS

CFG = {"displayModeBar": False, "scrollZoom": False}

THEMES = {
    "light": {
        "bg"    : "#F0F4F8",
        "card"  : "#FFFFFF",
        "text"  : "#212529",
        "border": "#DEE2E6",
        "muted" : "#6C757D",
        "navbar": "#FFFFFF",
    },
    "dark": {
        "bg"    : "#0D1117",
        "card"  : "#161B22",
        "text"  : "#E6EDF3",
        "border": "#30363D",
        "muted" : "#8B949E",
        "navbar": "#161B22",
    }
}

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="IBM HR Attrition Intelligence"
)
server = app.server

server.secret_key = "hr-attrition-intelligence-secret-key"

app.layout = html.Div([
    dcc.Store(id="user-store",        storage_type="session"),
    dcc.Store(id="theme-store",       storage_type="session", data="light"),
    dcc.Store(id="age-filter-store",  storage_type="session", data="All"),
    dcc.Store(id="dept-filter-store", storage_type="session", data="All"),
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])


# ════════════════════════════════════════════════════════
# LANDING PAGE
# ════════════════════════════════════════════════════════
def landing_layout(theme="light"):
    t = THEMES[theme]

    def stat_card(value, label, color):
        return html.Div([
            html.H4(value, style={"color": color, "fontWeight": "700"}),
            html.P(label,  style={"color": t["muted"], "margin": 0})
        ], style={
            "background"  : t["card"], "borderRadius": "12px",
            "padding"     : "24px",    "textAlign": "center",
            "border"      : f"1px solid {t['border']}"
        })

    return html.Div([
        html.Div([
            html.Div("IBM", style={
                "background": "#1F70C1", "color": "#FFFFFF",
                "padding": "8px 24px", "borderRadius": "6px",
                "fontSize": "28px", "fontWeight": "900",
                "letterSpacing": "4px", "display": "inline-block",
                "marginBottom": "20px",
            }),
            html.H1("HR Attrition Intelligence Portal", style={
                "textAlign": "center", "fontWeight": "700",
                "fontSize": "32px", "color": t["text"], "marginBottom": "4px",
            }),
            html.P("IBM Employee Attrition Dataset", style={
                "textAlign": "center", "color": "#1F70C1",
                "fontWeight": "600", "marginBottom": "12px"
            }),
            html.P(
                "An interactive analytics platform to understand employee "
                "attrition patterns, workforce trends, and department-level "
                "insights using IBM HR data.",
                style={
                    "textAlign": "center", "color": t["muted"],
                    "fontSize": "16px", "maxWidth": "600px",
                    "margin": "0 auto 32px auto", "lineHeight": "1.7",
                }
            ),
            html.Div([
                dbc.Button([html.I(className="bi bi-lock-fill me-2"), "Login"],
                           href="/login", color="primary", size="lg",
                           className="me-3",
                           style={"padding": "12px 32px", "fontWeight": "600"}),
                dbc.Button([html.I(className="bi bi-info-circle me-2"), "About Dataset"],
                           id="about-btn", color="outline-secondary", size="lg",
                           style={"padding": "12px 32px"}),
            ], style={"textAlign": "center", "marginBottom": "48px"}),

            dbc.Row([
                dbc.Col(stat_card("1,470", "Total Employees",   "#1F70C1"), width=3),
                dbc.Col(stat_card("35",    "Data Attributes",   "#1D9E75"), width=3),
                dbc.Col(stat_card("3",     "Departments",       "#D85A30"), width=3),
                dbc.Col(stat_card("16.1%", "Overall Attrition", "#534AB7"), width=3),
            ], className="g-3 justify-content-center mb-4"),

            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("About IBM HR Analytics Dataset")),
                dbc.ModalBody([
                    html.P([html.Strong("Dataset: "),
                            "IBM HR Analytics Employee Attrition & Performance"]),
                    html.P([html.Strong("Source: "),
                            "Kaggle — IBM HR Analytics Employee Attrition Dataset"]),
                    html.P([html.Strong("Purpose: "),
                            "Created by IBM data scientists to understand what "
                            "factors lead to employee attrition."]),
                    html.P([html.Strong("Size: "), "1,470 employees × 35 attributes"]),
                    html.P(html.Strong("Key Columns:")),
                    html.Ul([
                        html.Li("Age — how old the employee is"),
                        html.Li("Department — Sales, Human Resources, or Research & Development"),
                        html.Li("Monthly Income — how much the employee earns per month in USD"),
                        html.Li("Job Satisfaction — how happy the employee is at work, rated 1 (Low) to 4 (Very High)"),
                        html.Li("Years at Company — how long the employee has been working here"),
                        html.Li([
                            html.Strong("Attrition — "),
                            html.Span("Yes", style={"color": "#D85A30", "fontWeight": "600"}),
                            " means the employee has LEFT the company. ",
                            html.Span("No", style={"color": "#1D9E75", "fontWeight": "600"}),
                            " means the employee is STILL working here. "
                            "This is the most important column — it tells us who left and who stayed."
                        ]),
                    ]),
                    dbc.Alert(
                        "Dataset Source: IBM HR Analytics Employee Attrition Dataset",
                        color="info"
                    )
                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-about", className="ms-auto")
                )
            ], id="about-modal", is_open=False),

        ], style={
            "maxWidth": "900px", "margin": "0 auto",
            "padding": "60px 20px", "textAlign": "center"
        }),

        html.Footer(html.P(
            "Dataset Source: IBM HR Analytics Employee Attrition Dataset | "
            "Built on Databricks Medallion Architecture",
            style={"textAlign": "center", "color": t["muted"],
                   "fontSize": "13px", "padding": "20px",
                   "borderTop": f"1px solid {t['border']}"}
        ))
    ], style={"background": t["bg"], "minHeight": "100vh"})


# ════════════════════════════════════════════════════════
# LOGIN PAGE
# ════════════════════════════════════════════════════════
def login_layout(theme="light"):
    t = THEMES[theme]

    def cred_row(role, color, cred):
        return html.Div([
            dbc.Badge(role, color=color, className="me-2"),
            html.Small(cred, style={"color": t["muted"]})
        ], className="mb-2")

    return html.Div([
        html.Div([
            html.A([html.I(className="bi bi-arrow-left me-2"), "Back to Home"],
                   href="/", style={
                       "color": t["muted"], "textDecoration": "none",
                       "fontSize": "14px", "display": "block",
                       "marginBottom": "24px"
                   }),
            html.Div("IBM", style={
                "background": "#1F70C1", "color": "#FFFFFF",
                "padding": "6px 18px", "borderRadius": "6px",
                "fontSize": "20px", "fontWeight": "900",
                "letterSpacing": "3px", "display": "inline-block",
                "marginBottom": "12px",
            }),
            html.H4("HR Attrition Intelligence Portal",
                    style={"fontWeight": "600", "color": t["text"],
                           "marginBottom": "4px"}),
            html.P("IBM Employee Attrition Dataset",
                   style={"color": "#1F70C1", "fontWeight": "500",
                          "marginBottom": "28px", "fontSize": "14px"}),

            dbc.Label("Email Address",
                      style={"fontWeight": "500", "color": t["text"]}),
            dbc.Input(id="login-email", type="email",
                      placeholder="Enter your email", className="mb-3",
                      style={"background": t["card"], "color": t["text"]}),

            dbc.Label("Password",
                      style={"fontWeight": "500", "color": t["text"]}),
            html.Div([
                dbc.Input(id="login-password", type="password",
                          placeholder="Enter your password",
                          style={"paddingRight": "48px",
                                 "background": t["card"],
                                 "color": t["text"]}),
                html.I(id="toggle-pwd", className="bi bi-eye",
                       n_clicks=0, style={
                           "position": "absolute", "right": "14px",
                           "top": "50%", "transform": "translateY(-50%)",
                           "cursor": "pointer", "color": t["muted"],
                           "fontSize": "18px", "zIndex": "10",
                       }),
            ], style={"position": "relative", "marginBottom": "8px"}),

            html.Div(id="login-error",
                     style={"color": "#DC3545", "fontSize": "13px",
                            "marginBottom": "16px", "minHeight": "20px"}),

            dbc.Button(
                [html.I(className="bi bi-box-arrow-in-right me-2"), "Sign In"],
                id="login-btn", color="primary", className="w-100 mb-4",
                style={"padding": "10px", "fontWeight": "600"}
            ),

            html.Hr(style={"borderColor": t["border"]}),

            html.P("Demo Credentials",
                   style={"fontWeight": "600", "color": t["text"],
                          "fontSize": "14px", "marginBottom": "10px"}),
            html.Div([
                cred_row("HR Admin",      "danger",  "admin@hrapp.com / Admin@123"),
                cred_row("HR Manager",    "warning", "hr@hrapp.com / HR@123"),
                cred_row("Sales Manager", "success", "sales@hrapp.com / Sales@123"),
                cred_row("R&D Manager",   "primary", "rd@hrapp.com / RnD@123"),
            ], style={
                "background": t["bg"], "padding": "14px",
                "borderRadius": "8px", "border": f"1px solid {t['border']}"
            }),

            html.P(
                "Dataset Source: IBM HR Analytics Employee Attrition Dataset",
                style={"textAlign": "center", "color": t["muted"],
                       "fontSize": "12px", "marginTop": "20px"}
            )
        ], style={
            "maxWidth": "420px", "margin": "40px auto",
            "padding": "40px", "background": t["card"],
            "borderRadius": "16px",
            "boxShadow": "0 4px 24px rgba(0,0,0,0.10)",
            "textAlign": "center",
        })
    ], style={"background": t["bg"], "minHeight": "100vh"})


# ════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════
def dashboard_layout(
    user        : dict,
    theme       : str = "light",
    age_filter  : str = "All",
    active_dept : str = "All"
) -> html.Div:
    t    = THEMES[theme]
    role = user["role"]
    dept = user["department"]
    name = user["name"]

    data    = get_data_for_role(role, dept, age_filter, active_dept)
    plot_bg = {
        "plot_bgcolor" : t["card"],
        "paper_bgcolor": t["card"],
        "font"         : {"color": t["text"]}
    }

    # ── KPI cards ────────────────────────────────────────
    def kpi(label, value, sub, color):
        return html.Div([
            html.P(label,  style={"color": t["muted"], "fontSize": "13px",
                                  "marginBottom": "6px", "fontWeight": "500"}),
            html.H3(value, style={"fontWeight": "700", "color": color,
                                  "margin": "0 0 4px 0"}),
            html.Small(sub, style={"color": t["muted"]})
        ], style={
            "background": t["card"], "borderRadius": "12px",
            "padding": "20px 24px", "textAlign": "center",
            "border": f"1px solid {t['border']}"
        })

    kpi_row = dbc.Row([
        dbc.Col(kpi(
            "Total Employees",
            f"{data['total_employees']:,}",
            f"{dept} workforce" if dept != "All" else "Full workforce",
            "#1F70C1"
        ), width=3),
        dbc.Col(kpi(
            "Overall Attrition Rate",
            f"{data['attrition_rate']}%",
            f"{data['total_attrition']} employees left",
            "#D85A30"
        ), width=3),
        dbc.Col(kpi(
            "Avg Monthly Income",
            f"${int(data['avg_monthly_income']):,}",
            "Across selected scope",
            "#1D9E75"
        ), width=3),
        dbc.Col(kpi(
            "Avg Tenure",
            f"{data['avg_tenure']} yrs",
            f"Avg age: {data['avg_age']}",
            "#534AB7"
        ), width=3),
    ], className="mb-4 g-3")

    # ── Filters ──────────────────────────────────────────
    dept_pills = html.Div() if dept != "All" else html.Div([
        html.Span("Department: ",
                  style={"fontWeight": "500", "color": t["muted"],
                         "fontSize": "13px", "marginRight": "8px"}),
        *[dbc.Button(
            d,
            id       = {"type": "dept-pill", "index": d},
            size     = "sm",
            color    = "primary" if d == active_dept else "outline-secondary",
            className= "me-2",
            n_clicks = 0,
            style    = {"borderRadius": "20px", "marginBottom": "4px"}
        ) for d in ["All", "Sales", "Human Resources", "Research & Development"]]
    ], className="mb-2")

    age_pills = html.Div([
        html.Span("Age Group: ",
                  style={"fontWeight": "500", "color": t["muted"],
                         "fontSize": "13px", "marginRight": "8px"}),
        *[dbc.Button(
            a,
            id       = {"type": "age-pill", "index": a},
            size     = "sm",
            color    = "primary" if a == age_filter else "outline-secondary",
            className= "me-2",
            n_clicks = 0,
            style    = {"borderRadius": "20px", "marginBottom": "4px"}
        ) for a in ["All"] + AGE_GROUPS]
    ], className="mb-2")

    filter_section = html.Div([
        dept_pills,
        age_pills,
    ], style={
        "background": t["card"], "padding": "16px 20px",
        "borderRadius": "10px", "border": f"1px solid {t['border']}",
        "marginBottom": "20px"
    })

    # ── Charts ───────────────────────────────────────────
    dept_df = data["dept_analysis"]
    age_df  = data["age_analysis"]
    inc_df  = data["income_analysis"]
    sat_df  = data["sat_analysis"]

    # Chart 1 — Dept horizontal bar
    fig_dept = px.bar(
        dept_df.sort_values("attrition_rate") if len(dept_df) > 0 else dept_df,
        x="attrition_rate", y="department", orientation="h",
        title="Attrition Rate by Department",
        color="attrition_rate", color_continuous_scale="Reds",
        text="attrition_rate",
        labels={"attrition_rate": "Attrition Rate (%)", "department": "Department"}
    )
    fig_dept.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_dept.update_layout(
        **plot_bg,
        coloraxis_showscale = False,
        xaxis_title         = "Attrition Rate (%)",
        yaxis_title         = "Department",
        xaxis_range         = [0, 30],
        height              = 450,
        margin              = dict(l=10, r=80, t=40, b=10)
    )

    # Chart 2 — Age funnel
    fig_age = go.Figure(go.Funnel(
        y        = age_df["age_group"].astype(str) if len(age_df) > 0 else [],
        x        = age_df["attrition_rate"]        if len(age_df) > 0 else [],
        textinfo = "label+value+percent initial",
        marker   = {"color": ["#534AB7","#7F77DD","#AFA9EC","#CECBF6","#E8E6FB"]}
    ))
    fig_age.update_layout(
        title       = "Attrition Rate (%) by Age Group",
        **plot_bg,
        xaxis_title = "Attrition Rate (%)",
        yaxis_title = "Age Group",
        margin      = dict(l=10, r=10, t=40, b=10)
    )

    # Chart 3 — Income donut
    fig_income = px.pie(
        inc_df if len(inc_df) > 0 else pd.DataFrame(
            {"income_band": [], "attrition_count": []}),
        names="income_band", values="attrition_count",
        title="Attrition Count by Monthly Income Band (USD)",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.45
    )
    fig_income.update_traces(textposition="inside", textinfo="percent+label")
    fig_income.update_layout(**plot_bg, margin=dict(l=10, r=10, t=40, b=10))

    # Chart 4 — Satisfaction grouped bar
    fig_sat = px.bar(
        sat_df if len(sat_df) > 0 else pd.DataFrame(),
        x="satisfaction_label",
        y=["total_employees", "attrition_count"],
        title="Job Satisfaction Level vs Number of Employees",
        barmode="group",
        labels={
            "value"              : "Number of Employees",
            "satisfaction_label" : "Job Satisfaction Level",
            "variable"           : "Metric"
        },
        color_discrete_map={
            "total_employees": "#1F70C1",
            "attrition_count": "#D85A30"
        }
    )
    fig_sat.update_layout(
        **plot_bg,
        xaxis_title = "Job Satisfaction Level",
        yaxis_title = "Number of Employees",
        margin      = dict(l=10, r=10, t=40, b=10),
        legend      = dict(orientation="h", y=-0.25)
    )

    card_s = {
        "background"  : t["card"], "borderRadius": "12px",
        "padding"     : "16px",    "border": f"1px solid {t['border']}",
        "cursor"      : "pointer", "marginBottom": "16px"
    }

    charts_row = dbc.Row([
        dbc.Col(html.Div(
            dcc.Graph(id="chart-dept",   figure=fig_dept,   config=CFG),
            style=card_s
        ), width=6),
        dbc.Col(html.Div(
            dcc.Graph(id="chart-age",    figure=fig_age,    config=CFG),
            style=card_s
        ), width=6),
        dbc.Col(html.Div(
            dcc.Graph(id="chart-income", figure=fig_income, config=CFG),
            style=card_s
        ), width=6),
        dbc.Col(html.Div(
            dcc.Graph(id="chart-sat",    figure=fig_sat,    config=CFG),
            style=card_s
        ), width=6),
    ], className="g-3")

    # ── Insights ─────────────────────────────────────────
    insights_section = html.Div([
        html.H5([
            html.I(className="bi bi-lightbulb-fill me-2",
                   style={"color": "#F0A500"}),
            "Key Insights"
        ], style={"fontWeight": "600", "color": t["text"], "marginBottom": "12px"}),
        *[dbc.Alert(i, color="light", className="mb-2",
                    style={"border": f"1px solid {t['border']}",
                           "color": t["text"], "background": t["card"],
                           "lineHeight": "1.6"})
          for i in data["insights"]]
    ], style={
        "background": t["card"], "borderRadius": "12px",
        "padding": "20px", "border": f"1px solid {t['border']}",
        "marginTop": "8px"
    })

    # ── Modal ────────────────────────────────────────────
    modal = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
        dbc.ModalBody(dcc.Graph(id="modal-chart", config=CFG,
                                style={"height": "500px"})),
    ], id="chart-modal", size="xl", is_open=False)

    return html.Div([
        # Navbar
        html.Div([
            dbc.Container([
                html.Div([
                    html.Div([
                        html.Span("IBM", style={
                            "background": "#1F70C1", "color": "#FFFFFF",
                            "padding": "4px 12px", "borderRadius": "4px",
                            "fontWeight": "900", "letterSpacing": "2px",
                            "marginRight": "10px", "fontSize": "16px"
                        }),
                        html.Span("HR Attrition Intelligence Portal",
                                  style={"fontWeight": "600", "color": t["text"],
                                         "fontSize": "15px"}),
                    ], style={"display": "flex", "alignItems": "center"}),

                    html.Div([
                        html.Span([
                            html.I(className="bi bi-person-circle me-2",
                                   style={"fontSize": "18px",
                                          "color": t["text"]}),
                            html.Strong(role, style={"color": t["text"],
                                                     "fontSize": "14px"})
                        ], style={"marginRight": "16px"}),

                        dbc.Switch(
                            id="theme-toggle",
                            label="🌙 Dark",
                            value=theme == "dark",
                            className="me-3 mt-1",
                            style={"color": t["text"]}
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-box-arrow-right me-1"),
                             "Logout"],
                            id="logout-btn", size="sm",
                            color="outline-secondary"
                        ),
                    ], style={"display": "flex", "alignItems": "center"}),
                ], style={
                    "display": "flex", "justifyContent": "space-between",
                    "alignItems": "center", "width": "100%"
                })
            ], fluid=True)
        ], style={
            "background": t["navbar"],
            "borderBottom": f"1px solid {t['border']}",
            "padding": "12px 0", "marginBottom": "24px",
            "boxShadow": "0 1px 4px rgba(0,0,0,0.06)"
        }),

        dbc.Container([
            dbc.Alert([
                html.I(className="bi bi-funnel-fill me-2"),
                f"Viewing {dept} department — "
                f"{data['total_employees']} employees in scope."
            ], color="warning", className="mb-3") if dept != "All" else html.Div(),

            dbc.Alert([
                html.Strong("IBM HR Attrition Intelligence Portal  |  "),
                html.Em("Dataset: IBM HR Analytics Employee Attrition Dataset")
            ], color="info", className="mb-4"),

            kpi_row,
            filter_section,
            charts_row,
            html.Br(),
            insights_section,
            modal,

            html.Footer(html.P(
                "Dataset Source: IBM HR Analytics Employee Attrition Dataset | "
                "Built on Databricks Medallion Architecture (Bronze → Silver → Gold)",
                style={"textAlign": "center", "color": t["muted"],
                       "fontSize": "12px", "padding": "24px 0 8px 0"}
            )),
            html.Div(id="logout-redirect")
        ], fluid=True)
    ], style={"background": t["bg"], "minHeight": "100vh"})


# ════════════════════════════════════════════════════════
# CALLBACKS
# ════════════════════════════════════════════════════════

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    Input("theme-store", "data"),
    Input("age-filter-store", "data"),
    Input("dept-filter-store", "data"),
    Input("user-store", "data"),
)
def render_page(pathname, theme, age_f, dept_f, user):
    theme = theme or "light"
    age_f = age_f or "All"
    dept_f = dept_f or "All"

    saved_user = user or session.get("user")

    if pathname == "/login":
        return login_layout(theme)

    if pathname == "/dashboard":
        if saved_user:
            return dashboard_layout(
                saved_user,
                theme,
                age_filter=age_f,
                active_dept=dept_f
            )

        if ctx.triggered_id in ["theme-store", "age-filter-store", "dept-filter-store"]:
            return no_update

        return login_layout(theme)

    return landing_layout(theme)

@app.callback(
    Output("user-store", "data"),
    Output("login-error", "children"),
    Output("url", "pathname"),
    Input("login-btn", "n_clicks"),
    State("login-email", "value"),
    State("login-password", "value"),
    prevent_initial_call=True
)
def handle_login(n, email, password):
    if not email or not password:
        return no_update, "Please enter email and password.", no_update

    user = login(email, password)

    if user:
        session["user"] = user
        return user, "", "/dashboard"

    return no_update, "Invalid email or password.", no_update


@app.callback(
    Output("login-password", "type"),
    Output("toggle-pwd",     "className"),
    Input("toggle-pwd",      "n_clicks"),
    State("login-password",  "type"),
    prevent_initial_call=True
)
def toggle_password(n, current):
    if current == "password":
        return "text", "bi bi-eye-slash"
    return "password", "bi bi-eye"


@app.callback(
    Output("user-store", "data", allow_duplicate=True),
    Output("url", "pathname", allow_duplicate=True),
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True
)
def logout(n):
    if not n:
        return no_update, no_update

    return None, "/"


@app.callback(
    Output("theme-store",  "data"),
    Input("theme-toggle",  "value"),
    prevent_initial_call=True
)
def toggle_theme(is_dark):
    return "dark" if is_dark else "light"


@app.callback(
    Output("age-filter-store", "data"),
    Input({"type": "age-pill", "index": ALL}, "n_clicks_timestamp"),
    State({"type": "age-pill", "index": ALL}, "id"),
    prevent_initial_call=True
)
def apply_age_filter(timestamps, ids):
    if not timestamps or not ids:
        return no_update

    clicked = [
        (timestamp, button_id)
        for timestamp, button_id in zip(timestamps, ids)
        if timestamp and timestamp > 0
    ]

    if not clicked:
        return no_update

    latest = max(clicked, key=lambda item: item[0])[1]
    return latest["index"]


@app.callback(
    Output("dept-filter-store", "data"),
    Input({"type": "dept-pill", "index": ALL}, "n_clicks_timestamp"),
    State({"type": "dept-pill", "index": ALL}, "id"),
    prevent_initial_call=True
)
def apply_dept_filter(timestamps, ids):
    if not timestamps or not ids:
        return no_update

    clicked = [
        (timestamp, button_id)
        for timestamp, button_id in zip(timestamps, ids)
        if timestamp and timestamp > 0
    ]

    if not clicked:
        return no_update

    latest = max(clicked, key=lambda item: item[0])[1]
    return latest["index"]


@app.callback(
    Output("chart-modal", "is_open"),
    Output("modal-title", "children"),
    Output("modal-chart", "figure"),
    Input("chart-dept",   "clickData"),
    Input("chart-age",    "clickData"),
    Input("chart-income", "clickData"),
    Input("chart-sat",    "clickData"),
    State("chart-modal",  "is_open"),
    State("user-store",   "data"),
    State("theme-store",  "data"),
    State("age-filter-store",  "data"),
    State("dept-filter-store", "data"),
    prevent_initial_call=True
)
def open_modal(d_c, a_c, i_c, s_c, is_open, user, theme, age_f, dept_f):
    if not user:
        return False, no_update, no_update
    theme     = theme or "light"
    t         = THEMES[theme]
    plot_bg   = {"plot_bgcolor": t["card"], "paper_bgcolor": t["card"],
                 "font": {"color": t["text"]}}
    triggered = ctx.triggered_id
    data      = get_data_for_role(
        user["role"], user["department"],
        age_f or "All", dept_f or "All"
    )

    if triggered == "chart-dept" and d_c:
        df  = data["dept_analysis"]
        fig = px.bar(
            df.sort_values("attrition_rate"),
            x="attrition_rate", y="department", orientation="h",
            color="attrition_rate", text="attrition_rate",
            color_continuous_scale="Reds",
            labels={"attrition_rate": "Attrition Rate (%)",
                    "department": "Department"}
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(**plot_bg, coloraxis_showscale=False,
                          xaxis_range=[0, 30],
                          xaxis_title="Attrition Rate (%)",
                          yaxis_title="Department")
        return True, "Attrition Rate by Department — Full Detail", fig

    if triggered == "chart-age" and a_c:
        df  = data["age_analysis"]
        fig = px.bar(
            df, x="age_group", y="attrition_rate",
            color="attrition_rate", text="attrition_rate",
            color_continuous_scale="Purples",
            labels={"attrition_rate": "Attrition Rate (%)",
                    "age_group": "Age Group"}
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(**plot_bg, coloraxis_showscale=False,
                          xaxis_title="Age Group",
                          yaxis_title="Attrition Rate (%)")
        return True, "Attrition Rate by Age Group — Full Detail", fig

    if triggered == "chart-income" and i_c:
        df  = data["income_analysis"]
        fig = px.bar(
            df, x="income_band", y="attrition_rate",
            color="attrition_rate", text="attrition_rate",
            color_continuous_scale="Blues",
            labels={"attrition_rate": "Attrition Rate (%)",
                    "income_band": "Monthly Income Band (USD)"}
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(**plot_bg, coloraxis_showscale=False,
                          xaxis_title="Monthly Income Band (USD)",
                          yaxis_title="Attrition Rate (%)")
        return True, "Attrition by Income Band — Full Detail", fig

    if triggered == "chart-sat" and s_c:
        df  = data["sat_analysis"]
        fig = px.bar(
            df, x="satisfaction_label",
            y=["total_employees", "attrition_count"],
            barmode="group",
            color_discrete_map={
                "total_employees": "#1F70C1",
                "attrition_count": "#D85A30"
            },
            labels={"value": "Number of Employees",
                    "satisfaction_label": "Job Satisfaction Level",
                    "variable": "Metric"}
        )
        fig.update_layout(**plot_bg,
                          xaxis_title="Job Satisfaction Level",
                          yaxis_title="Number of Employees")
        return True, "Job Satisfaction vs Attrition — Full Detail", fig

    return False, no_update, no_update


@app.callback(
    Output("about-modal", "is_open"),
    Input("about-btn",    "n_clicks"),
    Input("close-about",  "n_clicks"),
    State("about-modal",  "is_open"),
    prevent_initial_call=True
)
def toggle_about(n1, n2, is_open):
    return not is_open


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
