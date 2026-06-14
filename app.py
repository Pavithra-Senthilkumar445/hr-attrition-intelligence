# app.py
# IBM HR Attrition Intelligence Portal
# Role based access: HR Admin, Sales Manager, R&D Manager
# Real data from Unity Catalog Volume via Databricks SDK

import dash
from dash import dcc, html, Input, Output, State, no_update, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from auth import login
from data import get_data_for_role, GOLD_OVERVIEW

# ── Chart toolbar config — removes zoom/pan ──────────────
CFG = {"displayModeBar": False, "scrollZoom": False}

# ── Theme ────────────────────────────────────────────────
THEMES = {
    "light": {
        "bg"     : "#F0F4F8",
        "card"   : "#FFFFFF",
        "text"   : "#212529",
        "border" : "#DEE2E6",
        "navbar" : "#FFFFFF",
        "muted"  : "#6C757D",
    },
    "dark": {
        "bg"     : "#0D1117",
        "card"   : "#161B22",
        "text"   : "#E6EDF3",
        "border" : "#30363D",
        "navbar" : "#161B22",
        "muted"  : "#8B949E",
    }
}

# ── App init ─────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP
    ],
    suppress_callback_exceptions=True,
    title="IBM HR Attrition Intelligence"
)
server = app.server

# ── Root layout ──────────────────────────────────────────
app.layout = html.Div([
    dcc.Store(id="user-store",  storage_type="session"),
    dcc.Store(id="theme-store", data="light",  storage_type="session"),
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])


# ════════════════════════════════════════════════════════
# SCREEN 1 — LANDING PAGE
# ════════════════════════════════════════════════════════
def landing_layout(theme="light"):
    t = THEMES[theme]
    return html.Div([
        # Hero section
        html.Div([
            # IBM badge
            html.Div([
                html.Span("IBM", style={
                    "background"    : "#1F70C1",
                    "color"         : "#FFFFFF",
                    "padding"       : "8px 24px",
                    "borderRadius"  : "6px",
                    "fontSize"      : "28px",
                    "fontWeight"    : "900",
                    "letterSpacing" : "4px",
                    "display"       : "inline-block",
                    "marginBottom"  : "20px",
                }),
            ], style={"textAlign": "center"}),

            html.H1(
                "HR Attrition Intelligence Portal",
                style={
                    "textAlign"   : "center",
                    "fontWeight"  : "700",
                    "fontSize"    : "32px",
                    "color"       : t["text"],
                    "marginBottom": "12px",
                }
            ),

            html.P(
                "An interactive analytics platform to understand employee "
                "attrition patterns, workforce trends, and department-level "
                "insights using IBM HR data.",
                style={
                    "textAlign"    : "center",
                    "color"        : t["muted"],
                    "fontSize"     : "16px",
                    "maxWidth"     : "600px",
                    "margin"       : "0 auto 32px auto",
                    "lineHeight"   : "1.7",
                }
            ),

            # Buttons
            html.Div([
                dbc.Button([
                    html.I(className="bi bi-lock-fill me-2"),
                    "Login"
                ],
                    id       = "landing-login-btn",
                    color    = "primary",
                    size     = "lg",
                    className= "me-3",
                    href     = "/login",
                    style    = {"padding": "12px 32px", "fontWeight": "600"}
                ),
                dbc.Button([
                    html.I(className="bi bi-info-circle me-2"),
                    "About Dataset"
                ],
                    id        = "about-btn",
                    color     = "outline-secondary",
                    size      = "lg",
                    style     = {"padding": "12px 32px"}
                ),
            ], style={"textAlign": "center", "marginBottom": "48px"}),

            # Dataset info cards
            dbc.Row([
                dbc.Col(html.Div([
                    html.H4("1,470", style={"color": "#1F70C1", "fontWeight": "700"}),
                    html.P("Total Employees", style={"color": t["muted"], "margin": 0})
                ], style={
                    "background"   : t["card"],
                    "borderRadius" : "12px",
                    "padding"      : "24px",
                    "textAlign"    : "center",
                    "border"       : f"1px solid {t['border']}"
                }), width=3),

                dbc.Col(html.Div([
                    html.H4("35", style={"color": "#1D9E75", "fontWeight": "700"}),
                    html.P("Data Attributes", style={"color": t["muted"], "margin": 0})
                ], style={
                    "background"   : t["card"],
                    "borderRadius" : "12px",
                    "padding"      : "24px",
                    "textAlign"    : "center",
                    "border"       : f"1px solid {t['border']}"
                }), width=3),

                dbc.Col(html.Div([
                    html.H4("3", style={"color": "#D85A30", "fontWeight": "700"}),
                    html.P("Departments", style={"color": t["muted"], "margin": 0})
                ], style={
                    "background"   : t["card"],
                    "borderRadius" : "12px",
                    "padding"      : "24px",
                    "textAlign"    : "center",
                    "border"       : f"1px solid {t['border']}"
                }), width=3),

                dbc.Col(html.Div([
                    html.H4("16.1%", style={"color": "#534AB7", "fontWeight": "700"}),
                    html.P("Overall Attrition", style={"color": t["muted"], "margin": 0})
                ], style={
                    "background"   : t["card"],
                    "borderRadius" : "12px",
                    "padding"      : "24px",
                    "textAlign"    : "center",
                    "border"       : f"1px solid {t['border']}"
                }), width=3),
            ], className="g-3 justify-content-center mb-4"),

            # About Dataset modal trigger
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("About IBM HR Analytics Dataset")),
                dbc.ModalBody([
                    html.P([
                        html.Strong("Dataset: "),
                        "IBM HR Analytics Employee Attrition & Performance"
                    ]),
                    html.P([
                        html.Strong("Source: "),
                        "Kaggle — IBM HR Analytics Employee Attrition Dataset"
                    ]),
                    html.P([
                        html.Strong("Purpose: "),
                        "This dataset was created by IBM data scientists to understand "
                        "what factors lead to employee attrition."
                    ]),
                    html.P([
                        html.Strong("Size: "),
                        "1,470 employees × 35 attributes"
                    ]),
                    html.P([
                        html.Strong("Key columns: "),
                        "Age, Department, Monthly Income, Job Satisfaction, "
                        "Years at Company, Attrition (Yes/No)"
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
            "maxWidth" : "900px",
            "margin"   : "0 auto",
            "padding"  : "60px 20px",
        }),

        # Footer
        html.Footer([
            html.P(
                "Dataset Source: IBM HR Analytics Employee Attrition Dataset | "
                "Built on Databricks Medallion Architecture",
                style={
                    "textAlign"  : "center",
                    "color"      : t["muted"],
                    "fontSize"   : "13px",
                    "padding"    : "20px",
                    "borderTop"  : f"1px solid {t['border']}",
                }
            )
        ])
    ], style={"background": t["bg"], "minHeight": "100vh"})


# ════════════════════════════════════════════════════════
# SCREEN 2 — LOGIN PAGE
# ════════════════════════════════════════════════════════
def login_layout(theme="light"):
    t = THEMES[theme]
    return html.Div([
        html.Div([
            # Back to home
            html.A([
                html.I(className="bi bi-arrow-left me-2"),
                "Back to Home"
            ], href="/", style={
                "color"          : t["muted"],
                "textDecoration" : "none",
                "fontSize"       : "14px",
                "display"        : "block",
                "marginBottom"   : "24px"
            }),

            # IBM badge
            html.Div("IBM", style={
                "background"    : "#1F70C1",
                "color"         : "#FFFFFF",
                "padding"       : "6px 18px",
                "borderRadius"  : "6px",
                "fontSize"      : "20px",
                "fontWeight"    : "900",
                "letterSpacing" : "3px",
                "display"       : "inline-block",
                "marginBottom"  : "12px",
            }),

            html.H4(
                "HR Attrition Intelligence Portal",
                style={"fontWeight": "600", "marginBottom": "4px", "color": t["text"]}
            ),
            html.P(
                "IBM Employee Attrition Dataset",
                style={"color": t["muted"], "marginBottom": "28px", "fontSize": "14px"}
            ),

            # Email
            dbc.Label("Email Address", style={"fontWeight": "500", "color": t["text"]}),
            dbc.Input(
                id          = "login-email",
                type        = "email",
                placeholder = "Enter your email",
                className   = "mb-3",
                style       = {"background": t["card"], "color": t["text"]}
            ),

            # Password with show/hide
            dbc.Label("Password", style={"fontWeight": "500", "color": t["text"]}),
            html.Div([
                dbc.Input(
                    id          = "login-password",
                    type        = "password",
                    placeholder = "Enter your password",
                    style       = {
                        "paddingRight" : "48px",
                        "background"   : t["card"],
                        "color"        : t["text"]
                    }
                ),
                html.I(
                    id        = "toggle-pwd",
                    className = "bi bi-eye",
                    n_clicks  = 0,
                    style     = {
                        "position"  : "absolute",
                        "right"     : "14px",
                        "top"       : "50%",
                        "transform" : "translateY(-50%)",
                        "cursor"    : "pointer",
                        "color"     : t["muted"],
                        "fontSize"  : "18px",
                        "zIndex"    : "10",
                    }
                ),
            ], style={"position": "relative", "marginBottom": "8px"}),

            # Error
            html.Div(
                id    = "login-error",
                style = {
                    "color"        : "#DC3545",
                    "fontSize"     : "13px",
                    "marginBottom" : "16px",
                    "minHeight"    : "20px"
                }
            ),

            # Login button
            dbc.Button(
                [html.I(className="bi bi-box-arrow-in-right me-2"), "Sign In"],
                id        = "login-btn",
                color     = "primary",
                className = "w-100 mb-4",
                style     = {"padding": "10px", "fontWeight": "600"}
            ),

            html.Hr(style={"borderColor": t["border"]}),

            # Demo credentials
            html.P(
                "Demo Credentials",
                style={"fontWeight": "600", "color": t["text"],
                       "fontSize": "14px", "marginBottom": "10px"}
            ),
            html.Div([
                html.Div([
                    dbc.Badge("HR Admin",      color="danger",  className="me-2"),
                    html.Small("admin@hrapp.com / Admin@123",
                               style={"color": t["muted"]})
                ], className="mb-2"),
                html.Div([
                    dbc.Badge("Sales Manager", color="success", className="me-2"),
                    html.Small("sales@hrapp.com / Sales@123",
                               style={"color": t["muted"]})
                ], className="mb-2"),
                html.Div([
                    dbc.Badge("R&D Manager",   color="primary", className="me-2"),
                    html.Small("rd@hrapp.com / RnD@123",
                               style={"color": t["muted"]})
                ]),
            ], style={
                "background"   : t["bg"],
                "padding"      : "14px",
                "borderRadius" : "8px",
                "border"       : f"1px solid {t['border']}"
            }),

            # Footer note
            html.P(
                "Dataset Source: IBM HR Analytics Employee Attrition Dataset",
                style={
                    "textAlign"  : "center",
                    "color"      : t["muted"],
                    "fontSize"   : "12px",
                    "marginTop"  : "20px"
                }
            )

        ], style={
            "maxWidth"     : "420px",
            "margin"       : "40px auto",
            "padding"      : "40px",
            "background"   : t["card"],
            "borderRadius" : "16px",
            "boxShadow"    : "0 4px 24px rgba(0,0,0,0.10)",
            "textAlign"    : "center",
        })
    ], style={"background": t["bg"], "minHeight": "100vh"})


# ════════════════════════════════════════════════════════
# SCREEN 3 — DASHBOARD
# ════════════════════════════════════════════════════════
def dashboard_layout(user: dict, theme: str = "light") -> html.Div:
    t    = THEMES[theme]
    role = user["role"]
    dept = user["department"]
    name = user["name"]

    # Get real filtered data from Silver + Gold
    data = get_data_for_role(role, dept)

    role_colors = {
        "HR Admin"     : "danger",
        "Sales Manager": "success",
        "R&D Manager"  : "primary"
    }

    # ── KPI cards ────────────────────────────────────────
    def kpi_card(label, value, sub, color):
        return html.Div([
            html.P(label, style={
                "color"        : t["muted"],
                "fontSize"     : "13px",
                "marginBottom" : "6px",
                "fontWeight"   : "500"
            }),
            html.H3(value, style={
                "fontWeight" : "700",
                "color"      : color,
                "margin"     : "0 0 4px 0"
            }),
            html.Small(sub, style={"color": t["muted"]})
        ], style={
            "background"   : t["card"],
            "borderRadius" : "12px",
            "padding"      : "20px 24px",
            "border"       : f"1px solid {t['border']}",
            "textAlign"    : "center"
        })

    kpi_row = dbc.Row([
        dbc.Col(kpi_card(
            "Total Employees",
            f"{data['total_employees']:,}",
            f"{dept} workforce" if dept != "All" else "Full workforce",
            "#1F70C1"
        ), width=3),
        dbc.Col(kpi_card(
            "Overall Attrition Rate (IBM HR Dataset Snapshot)",
            f"{data['attrition_rate']}%",
            f"{data['total_attrition']} employees left",
            "#D85A30"
        ), width=3),
        dbc.Col(kpi_card(
            "Avg Monthly Income",
            f"${int(data['avg_monthly_income']):,}",
            "Across selected scope",
            "#1D9E75"
        ), width=3),
        dbc.Col(kpi_card(
            "Avg Tenure",
            f"{data['avg_tenure']} yrs",
            f"Avg age: {data['avg_age']}",
            "#534AB7"
        ), width=3),
    ], className="mb-4 g-3")

    # ── Chart helpers ────────────────────────────────────
    plot_bg = {"plot_bgcolor": t["card"], "paper_bgcolor": t["card"],
               "font": {"color": t["text"]}}

    # Chart 1 — Dept: Horizontal bar
    dept_df  = data["dept_analysis"]
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
        **plot_bg,
        coloraxis_showscale = False,
        margin = dict(l=10, r=40, t=40, b=10)
    )

    # Chart 2 — Age: Funnel
    age_df  = data["age_analysis"]
    fig_age = go.Figure(go.Funnel(
        y        = age_df["age_group"].astype(str),
        x        = age_df["attrition_rate"],
        textinfo = "label+value+percent initial",
        marker   = {"color": ["#534AB7","#7F77DD","#AFA9EC","#CECBF6","#E8E6FB"]}
    ))
    fig_age.update_layout(
        title  = "Attrition Rate by Age Group",
        **plot_bg,
        margin = dict(l=10, r=10, t=40, b=10)
    )

    # Chart 3 — Income: Donut
    inc_df     = data["income_analysis"]
    fig_income = px.pie(
        inc_df,
        names  = "income_band",
        values = "attrition_count",
        title  = "Attrition Count by Income Band",
        color_discrete_sequence = px.colors.sequential.Blues_r,
        hole   = 0.45
    )
    fig_income.update_traces(
        textposition = "inside",
        textinfo     = "percent+label"
    )
    fig_income.update_layout(
        **plot_bg,
        margin = dict(l=10, r=10, t=40, b=10)
    )

    # Chart 4 — Satisfaction: Grouped bar
    sat_df  = data["sat_analysis"]
    fig_sat = px.bar(
        sat_df,
        x       = "satisfaction_label",
        y       = ["total_employees", "attrition_count"],
        title   = "Job Satisfaction vs Attrition Count",
        barmode = "group",
        labels  = {
            "value"              : "Count",
            "satisfaction_label" : "Satisfaction Level",
            "variable"           : "Metric"
        },
        color_discrete_map = {
            "total_employees" : "#1F70C1",
            "attrition_count" : "#D85A30"
        }
    )
    fig_sat.update_layout(
        **plot_bg,
        margin = dict(l=10, r=10, t=40, b=10),
        legend = dict(orientation="h", y=-0.25)
    )

    card_style = {
        "background"   : t["card"],
        "borderRadius" : "12px",
        "padding"      : "16px",
        "border"       : f"1px solid {t['border']}",
        "cursor"       : "pointer",
        "marginBottom" : "16px"
    }

    charts_row = dbc.Row([
        dbc.Col(html.Div(
            dcc.Graph(id="chart-dept",   figure=fig_dept,   config=CFG),
            style=card_style, id="wrap-dept"
        ), width=6),
        dbc.Col(html.Div(
            dcc.Graph(id="chart-age",    figure=fig_age,    config=CFG),
            style=card_style, id="wrap-age"
        ), width=6),
        dbc.Col(html.Div(
            dcc.Graph(id="chart-income", figure=fig_income, config=CFG),
            style=card_style, id="wrap-income"
        ), width=6),
        dbc.Col(html.Div(
            dcc.Graph(id="chart-sat",    figure=fig_sat,    config=CFG),
            style=card_style, id="wrap-sat"
        ), width=6),
    ], className="g-3")

    # ── Insights section ─────────────────────────────────
    insights_section = html.Div([
        html.H5([
            html.I(className="bi bi-lightbulb-fill me-2",
                   style={"color": "#F0A500"}),
            "Key Insights"
        ], style={"fontWeight": "600", "color": t["text"], "marginBottom": "12px"}),
        html.Div([
            dbc.Alert(insight, color="light", className="mb-2",
                      style={
                          "border"     : f"1px solid {t['border']}",
                          "color"      : t["text"],
                          "background" : t["card"]
                      })
            for insight in data["insights"]
        ])
    ], style={
        "background"   : t["card"],
        "borderRadius" : "12px",
        "padding"      : "20px",
        "border"       : f"1px solid {t['border']}",
        "marginTop"    : "8px"
    })

    # ── Modal for chart popup ─────────────────────────────
    modal = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
        dbc.ModalBody(
            dcc.Graph(id="modal-chart", config=CFG,
                      style={"height": "500px"})
        ),
    ], id="chart-modal", size="xl", is_open=False)

    return html.Div([
        # ── Navbar ───────────────────────────────────────
        html.Div([
            dbc.Container([
                html.Div([
                    # Left — IBM branding
                    html.Div([
                        html.Span("IBM", style={
                            "background"    : "#1F70C1",
                            "color"         : "#FFFFFF",
                            "padding"       : "4px 12px",
                            "borderRadius"  : "4px",
                            "fontWeight"    : "900",
                            "letterSpacing" : "2px",
                            "marginRight"   : "10px",
                            "fontSize"      : "16px"
                        }),
                        html.Span(
                            "HR Attrition Intelligence Portal",
                            style={"fontWeight": "600", "color": t["text"],
                                   "fontSize": "15px"}
                        ),
                    ], style={"display": "flex", "alignItems": "center"}),

                    # Right — role, theme, logout
                    html.Div([
                        dbc.Badge(
                            role,
                            color     = role_colors.get(role, "secondary"),
                            className = "me-3 p-2"
                        ),
                        html.Span(
                            f"👤 {name}",
                            style={"fontSize": "13px", "marginRight": "16px",
                                   "color": t["text"]}
                        ),
                        dbc.Switch(
                            id        = "theme-toggle",
                            label     = "🌙 Dark",
                            value     = theme == "dark",
                            className = "me-3 mt-1"
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-box-arrow-right me-1"), "Logout"],
                            id    = "logout-btn",
                            size  = "sm",
                            color = "outline-secondary"
                        ),
                    ], style={"display": "flex", "alignItems": "center"}),
                ], style={
                    "display"        : "flex",
                    "justifyContent" : "space-between",
                    "alignItems"     : "center",
                    "width"          : "100%"
                })
            ], fluid=True)
        ], style={
            "background"   : t["navbar"],
            "borderBottom" : f"1px solid {t['border']}",
            "padding"      : "12px 0",
            "marginBottom" : "24px",
            "boxShadow"    : "0 1px 4px rgba(0,0,0,0.06)"
        }),

        # ── Main content ──────────────────────────────────
        dbc.Container([
            # Restriction banner for managers
            dbc.Alert([
                html.I(className="bi bi-funnel-fill me-2"),
                f"Viewing {dept} department data only — "
                f"{data['total_employees']} employees in scope."
            ], color="warning", className="mb-3") if dept != "All" else html.Div(),

            # About banner
            dbc.Alert([
                html.Strong("IBM HR Attrition Intelligence Portal  |  "),
                html.Span("IBM Employee Attrition Dataset  |  "),
                html.Em("Dataset Source: IBM HR Analytics Employee Attrition Dataset")
            ], color="info", className="mb-4"),

            kpi_row,
            charts_row,

            html.Br(),
            insights_section,
            modal,

            # Footer
            html.Footer(
                html.P(
                    "Dataset Source: IBM HR Analytics Employee Attrition Dataset | "
                    "Built on Databricks Medallion Architecture (Bronze → Silver → Gold)",
                    style={
                        "textAlign"  : "center",
                        "color"      : t["muted"],
                        "fontSize"   : "12px",
                        "padding"    : "24px 0 8px 0",
                    }
                )
            )
        ], fluid=True),

        html.Div(id="logout-redirect")
    ], style={"background": t["bg"], "minHeight": "100vh"})


# ════════════════════════════════════════════════════════
# CALLBACKS
# ════════════════════════════════════════════════════════

# Page router
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    State("user-store",  "data"),
    State("theme-store", "data"),
)
def render_page(pathname, user, theme):
    theme = theme or "light"
    if pathname == "/login":
        return login_layout(theme)
    if pathname == "/dashboard" and user:
        return dashboard_layout(user, theme)
    if pathname == "/dashboard" and not user:
        return login_layout(theme)
    return landing_layout(theme)


# Login
@app.callback(
    Output("user-store",    "data"),
    Output("login-error",   "children"),
    Output("url",           "pathname"),
    Input("login-btn",      "n_clicks"),
    State("login-email",    "value"),
    State("login-password", "value"),
    prevent_initial_call=True
)
def handle_login(n, email, password):
    if not email or not password:
        return no_update, "Please enter email and password.", no_update
    user = login(email, password)
    if user:
        return user, "", "/dashboard"
    return no_update, "Invalid email or password. Please try again.", no_update


# Password toggle
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


# Logout
@app.callback(
    Output("user-store", "data",     allow_duplicate=True),
    Output("url",        "pathname", allow_duplicate=True),
    Input("logout-btn",  "n_clicks"),
    prevent_initial_call=True
)
def logout(n):
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


# Chart modal popup
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
    prevent_initial_call=True
)
def open_modal(d_click, a_click, i_click, s_click, is_open, user, theme):
    if not user:
        return False, no_update, no_update

    theme    = theme or "light"
    t        = THEMES[theme]
    plot_bg  = {"plot_bgcolor": t["card"], "paper_bgcolor": t["card"],
                "font": {"color": t["text"]}}
    triggered = ctx.triggered_id
    data      = get_data_for_role(user["role"], user["department"])

    if triggered == "chart-dept" and d_click:
        df  = data["dept_analysis"]
        fig = px.bar(
            df.sort_values("attrition_rate"),
            x="attrition_rate", y="department",
            orientation="h", color="attrition_rate",
            text="attrition_rate",
            color_continuous_scale="Reds",
            labels={"attrition_rate": "Attrition %", "department": ""}
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(**plot_bg, coloraxis_showscale=False)
        return True, "Attrition by Department — Full Detail", fig

    if triggered == "chart-age" and a_click:
        df  = data["age_analysis"]
        fig = px.bar(
            df, x="age_group", y="attrition_rate",
            color="attrition_rate", text="attrition_rate",
            color_continuous_scale="Purples",
            labels={"attrition_rate": "Attrition %", "age_group": "Age Group"}
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(**plot_bg, coloraxis_showscale=False)
        return True, "Attrition by Age Group — Full Detail", fig

    if triggered == "chart-income" and i_click:
        df  = data["income_analysis"]
        fig = px.bar(
            df, x="income_band", y="attrition_rate",
            color="attrition_rate", text="attrition_rate",
            color_continuous_scale="Blues",
            labels={"attrition_rate": "Attrition %", "income_band": "Income Band"}
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(**plot_bg, coloraxis_showscale=False)
        return True, "Attrition by Income Band — Full Detail", fig

    if triggered == "chart-sat" and s_click:
        df  = data["sat_analysis"]
        fig = px.bar(
            df, x="satisfaction_label",
            y=["total_employees", "attrition_count"],
            barmode="group",
            color_discrete_map={
                "total_employees": "#1F70C1",
                "attrition_count": "#D85A30"
            },
            labels={"value": "Count", "satisfaction_label": "Satisfaction"}
        )
        fig.update_layout(**plot_bg)
        return True, "Job Satisfaction vs Attrition — Full Detail", fig

    return False, no_update, no_update


# About modal
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
