import dash
from dash import dcc, html, dash_table, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import io

# ------------------------------------------------------------------------------
# 1. DATA LOADING (EMBEDDED DIRECTLY)
# ------------------------------------------------------------------------------

RAW_CSV_DATA = """Section,West Tanna,South West Tanna,Central Tanna,Anietyum,Varsu,Nguna,Vermali,Emae,Central Malekula,North West Malekula,South west Malekula,Paama,North Ambrym,South East Ambrym,Cp1,CP2,South Pentecost,North Maewo,South santo,West Malo,North west Santo,Pelvus,Bigbay coast,West Gaua,Ureparapara,West Vanua Lava,Mota Lava
Does the community have a disaster plan,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Year disaster plan developed,1,0.75,0.75,0,0,0,0.5,0,0.5,0.25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC contribute to development of Disaster Plan,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCC have an evacuation center,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCC have a management plan for the evacuation center,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Is there a set of preparatory activities prior to disaster,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC have a set of post disaster assessment activities,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC have a set of climate change adaptation activities for water security,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC have a set of climate change adaptation activities for food security,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC have a set of climate change adaptation activities for improved livelihood,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC have a set of climate change adaptation activities for addressing land erosion,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC have a set of planned activities target women and children,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC have a set of planned activities targeting youth,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Does the CDCCC have a set of planned activities targeting any other specific areas,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Is the community currently implementing the plan,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Community chiefs and village council,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Women representatives,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Youth Representatives,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Disability representatives,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Provincial Disaster officer,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
whole community to be part of,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Area Administrator,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
NGO nor project officer,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Does the CDCCC have a budget for implementing the plan,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Does the CDCCC participate in developing a budget,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Is the CDCCC able to access funding for implementing the plan,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Community fund raising,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Area Council Support,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Provincial Government support,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
National Government support,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
NGO support,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Does the plan have a timeframe,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
What is the expiry date of the plan,0,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Does the plan reflect a vulnerability assessment,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Risks from tsunami,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Risks from earthquack,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Risks from Climate change,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Risks from volcanic activities,1,1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Risks from floods,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
tropical cyclone,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Risks from droughts,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Risks from heatwaves,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Risks from sea level rise,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Risks from change in ecosystem,0,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC well updated on early warning prior to disaster,0,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC receive disaster warning through mobile phones,1,1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC receive disaster warning through Area Administrator,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC receive disaster warning through provincial disaster officer,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC receive disaster warning through friends and relatives,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC receive Early warning through Facebook or Sociial Media,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC receive disaster warning through radio vanuatu and FM radios,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC receive disaster warning through traditional knowledge,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Public annoucement through a hailer,0,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Passing of information by door to door method,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Informs Vulnerable People eg People With Disability,1,1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Visit Areas Which are high risk to disasters yes,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Remind people to prepare enough food and water during disaster,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Remind people to check their House,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
To put animals and other things like boat solar panel safe,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Remind to trim plants in the garden before disaster like cyclone,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC encourage the movement of vulnrable household during evacuation,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC makes assesment on affected household and population and provides other information,1,1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCC do not use other form,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC use other form provided by NDMO or NGO to assses the impact of disaster on people and evacuation center,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC help to make a displacement cluster assesment to talk about the status of people on evacuation center,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC do not know what kind of assesmnet they use,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC have a copy of post disaster assesment with them,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCC provide assesment result to the province,1,1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCC provide assesment result to the Area councils,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Provide Assesment result to the NGO or Project Staff,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC not sure on who take the assesment result,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC provide assesmnet resutl to the national government staff,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC work closely with Area secretary and Area Administrator,1,1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCC Work with Area Council Somethimes,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC work with Area Administrator and Area Secretary sometimes and not often,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC do not have a working relationship with Area Council,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Total population of househols statistics,1,1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Gender break down of men and women inplace,1,1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Age break down statistics of different age group that are already inplace,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC does not have an accurate statistics of the community,0,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Estimate Number of People With Disability,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCC do not have an assesment form to use,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC do not receive training on how to use the assesment forms,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC don’t know who to share the assesment results with,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Hard to diseminate assesmnet afta a disaster,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Communication problem such as difficult to access internet,1,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
No other challenge to report,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC or Community engage in any community profiling activities,0,1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC or community engage on any vulnerability and needs assesment,0,1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Community has any copy of the final report of the community profiling or assesment,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC have a storage room or bulding,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
CDCCC have any resource to do the work,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Mobile Phone Tablet Printer,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Mini projector HI-Vis vest stationary,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Claw hammer spade Shovel,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Hoe Hand Saw Machete,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Tire Wire tin Snips Metal Brush,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Tarpoline 5x5m plastic Box 100I Radio,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Loud Heiler Wistle Rain Coat,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
"""

def load_data_from_string():
    df_raw = pd.read_csv(io.StringIO(RAW_CSV_DATA))
    district_columns = [c for c in df_raw.columns if c != "Section"]
    data_list = []
    for index, row in df_raw.iterrows():
        indicator = str(row['Section']).strip()
        category = "Other"
        if any(x in indicator.lower() for x in ['plan', 'evacuation', 'adaptation', 'women', 'children', 'resource', 'statistics']):
            category = "Readiness and Gaps"
        elif any(x in indicator.lower() for x in ['risk', 'warning', 'alert', 'radio', 'facebook']):
            category = "Early Warning and Response"
        elif any(x in indicator.lower() for x in ['challenge', 'budget', 'fund', 'hard to', 'problem']):
            category = "Bottlenecks"
            
        for district in district_columns:
            try:
                val = row[district]
                val = float(val) if (pd.notna(val) and val != '') else 0
            except:
                val = 0
            
            province = "Unknown"
            d_lower = district.lower()
            if "tanna" in d_lower or "anietyum" in d_lower: province = "Tafea"
            elif "malekula" in d_lower or "paama" in d_lower or "ambrym" in d_lower: province = "Malampa"
            elif "santo" in d_lower or "malo" in d_lower or "bigbay" in d_lower: province = "Sanma"
            elif "pentecost" in d_lower or "maewo" in d_lower: province = "Penama"
            elif "gaua" in d_lower or "vanua" in d_lower or "mota" in d_lower or "ureparapara" in d_lower or "torba" in d_lower: province = "Torba"
            elif "emae" in d_lower or "nguna" in d_lower or "varsu" in d_lower or "vermali" in d_lower or "shefa" in d_lower: province = "Shefa"
            
            data_list.append({'Province': province, 'District': district, 'Indicator': indicator, 'Value': val, 'Category': category})
            
    return pd.DataFrame(data_list)

df = load_data_from_string()

# ------------------------------------------------------------------------------
# 2. DASHBOARD SETUP
# ------------------------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server
app.title = "National Disaster Resilience Tracker"

# ------------------------------------------------------------------------------
# 3. LAYOUT
# ------------------------------------------------------------------------------
app.layout = dbc.Container([
    
    dbc.NavbarSimple(
        brand="National Disaster Resilience Tracker",
        brand_href="#",
        color="primary",
        dark=True,
        className="mb-4"
    ),

    dcc.Tabs([
        # --- TAB 1: SUMMARY ---
        dcc.Tab(label='Executive Summary', children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Geographic Hierarchy"),
                            dbc.CardBody([
                                html.P("Click Center for Country, Ring for Province, Outer for District.", className="text-muted small"),
                                dcc.Graph(id='hierarchy-sunburst', style={'height': '500px'})
                            ])
                        ])
                    ], md=6),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(id='drill-through-title', children="Selection Details"),
                            dbc.CardBody([
                                html.H5("Readiness Score:", className="mb-3"),
                                html.H2(id='drill-score', className="text-primary text-center mb-4"),
                                html.Hr(),
                                html.H5("Detailed Indicators in Scope:"),
                                # REPLACED BAR CHART WITH READABLE TABLE
                                dash_table.DataTable(
                                    id='drill-table',
                                    style_table={'height': '300px', 'overflowY': 'auto'},
                                    style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'sans-serif'},
                                    style_header={'fontWeight': 'bold', 'backgroundColor': 'rgb(230, 230, 230)'},
                                    style_data_conditional=[
                                        {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
                                    ]
                                )
                            ])
                        ], className="h-100")
                    ], md=6)
                ])
            ], fluid=True, className="p-4")
        ]),

        # --- TAB 2: COMPARISONS (NEW!) ---
        dcc.Tab(label='Comparisons', children=[
            dbc.Container([
                html.H3("Regional & Council Comparison", className="text-center my-4"),
                
                # Controls
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Comparison Level:"),
                        dcc.RadioItems(
                            id='comp-level-radio',
                            options=[{'label': ' Province vs Province', 'value': 'Province'}, 
                                     {'label': ' Council vs Council', 'value': 'District'}],
                            value='Province',
                            inline=True,
                            className="mb-3"
                        ),
                    ], width=12),
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Select Entity A:"),
                        dcc.Dropdown(id='comp-dropdown-a', clearable=False)
                    ], md=5),
                    dbc.Col([html.H4("VS", className="text-center mt-4")], md=2),
                    dbc.Col([
                        dbc.Label("Select Entity B:"),
                        dcc.Dropdown(id='comp-dropdown-b', clearable=False)
                    ], md=5),
                ], className="mb-4"),
                
                # Results
                dbc.Row([
                    # Readiness Comparison
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Readiness Score Comparison"),
                            dbc.CardBody(dcc.Graph(id='comp-readiness-bar'))
                        ])
                    ], md=6),
                    
                    # Risk Profile Comparison
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Risk Profile Comparison"),
                            dbc.CardBody(dcc.Graph(id='comp-risk-radar'))
                        ])
                    ], md=6),
                ])

            ], fluid=True, className="p-4")
        ]),

        # --- TAB 3: METRICS ---
        dcc.Tab(label='Detailed Metrics', children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Select District:"),
                        dcc.Dropdown(
                            id='district-dropdown',
                            options=[{'label': d, 'value': d} for d in df['District'].unique()],
                            value=df['District'].unique()[0],
                            clearable=False
                        )
                    ], width=6, className="my-3")
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='readiness-gauge'), md=4),
                    dbc.Col(dcc.Graph(id='risk-radar'), md=4),
                    dbc.Col(dcc.Graph(id='budget-gauge'), md=4),
                ])
            ], fluid=True)
        ])
    ])
], fluid=True)

# ------------------------------------------------------------------------------
# 4. CALLBACKS
# ------------------------------------------------------------------------------

# TAB 1: SUNBURST & READABLE TABLE
@callback(
    [Output('hierarchy-sunburst', 'figure'),
     Output('drill-through-title', 'children'),
     Output('drill-score', 'children'),
     Output('drill-table', 'data'), 
     Output('drill-table', 'columns')],
    [Input('hierarchy-sunburst', 'clickData')]
)
def update_executive_summary(clickData):
    ctx_df = df.copy()
    scope_name = "National Overview"
    
    if clickData:
        clicked_point = clickData['points'][0]
        clicked_label = clicked_point.get('label')
        clicked_parent = clicked_point.get('parent')
        if clicked_parent == "": scope_name = "National Overview"
        elif clicked_parent == "Total": 
            scope_name = f"Province: {clicked_label}"
            ctx_df = df[df['Province'] == clicked_label]
        else:
            scope_name = f"District: {clicked_label}"
            ctx_df = df[df['District'] == clicked_label]

    # Sunburst
    sunburst_df = df[df['Category'] == 'Readiness and Gaps'].groupby(['Province', 'District'])['Value'].sum().reset_index()
    sunburst_df['Country'] = 'Total' 
    fig_sun = px.sunburst(sunburst_df, path=['Country', 'Province', 'District'], values='Value', color='Value', 
                          color_continuous_scale='RdBu', title="Hierarchy")
    fig_sun.update_layout(margin=dict(t=30, l=0, r=0, b=0))

    # Metrics
    readiness_score = ctx_df[ctx_df['Category'] == 'Readiness and Gaps']['Value'].mean() * 100
    score_text = f"{readiness_score:.1f}%"
    
    # TABLE DATA (Aggregated by Indicator)
    table_df = ctx_df.groupby('Indicator')['Value'].mean().reset_index()
    table_df['Value'] = (table_df['Value'] * 100).round(1).astype(str) + '%'
    table_df = table_df.sort_values('Value', ascending=False)
    
    columns = [{"name": i, "id": i} for i in table_df.columns]
    data = table_df.to_dict('records')

    return fig_sun, scope_name, score_text, data, columns

# TAB 2: COMPARISON LOGIC
@callback(
    [Output('comp-dropdown-a', 'options'),
     Output('comp-dropdown-a', 'value'),
     Output('comp-dropdown-b', 'options'),
     Output('comp-dropdown-b', 'value')],
    [Input('comp-level-radio', 'value')]
)
def set_compare_options(level):
    if level == 'Province':
        opts = [{'label': i, 'value': i} for i in df['Province'].unique() if i != "Unknown"]
    else:
        opts = [{'label': i, 'value': i} for i in df['District'].unique()]
    
    val_a = opts[0]['value'] if opts else None
    val_b = opts[1]['value'] if len(opts) > 1 else val_a
    return opts, val_a, opts, val_b

@callback(
    [Output('comp-readiness-bar', 'figure'),
     Output('comp-risk-radar', 'figure')],
    [Input('comp-level-radio', 'value'),
     Input('comp-dropdown-a', 'value'),
     Input('comp-dropdown-b', 'value')]
)
def update_comparison(level, entity_a, entity_b):
    col = 'Province' if level == 'Province' else 'District'
    
    # Filter Data for A and B
    df_a = df[df[col] == entity_a]
    df_b = df[df[col] == entity_b]
    
    # 1. Readiness Bar Chart
    score_a = df_a[df_a['Category'] == 'Readiness and Gaps']['Value'].mean() * 100
    score_b = df_b[df_b['Category'] == 'Readiness and Gaps']['Value'].mean() * 100
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=[entity_a, entity_b], y=[score_a, score_b], marker_color=['#1f77b4', '#ff7f0e']))
    fig_bar.update_layout(title="Readiness Score Comparison", yaxis_title="Score (%)", yaxis_range=[0, 100])
    
    # 2. Risk Radar
    risk_a = df_a[(df_a['Category'] == 'Early Warning and Response') & (df_a['Indicator'].str.contains("Risks"))].groupby('Indicator')['Value'].mean().reset_index()
    risk_b = df_b[(df_b['Category'] == 'Early Warning and Response') & (df_b['Indicator'].str.contains("Risks"))].groupby('Indicator')['Value'].mean().reset_index()
    
    # Clean Indicator names for Radar
    risk_a['Indicator'] = risk_a['Indicator'].str.replace("Risks from ", "")
    risk_b['Indicator'] = risk_b['Indicator'].str.replace("Risks from ", "")

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=risk_a['Value'], theta=risk_a['Indicator'], fill='toself', name=entity_a))
    fig_radar.add_trace(go.Scatterpolar(r=risk_b['Value'], theta=risk_b['Indicator'], fill='toself', name=entity_b))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), title="Risk Vulnerability Comparison")
    
    return fig_bar, fig_radar

# TAB 3: METRICS LOGIC
@callback(
    [Output('readiness-gauge', 'figure'),
     Output('risk-radar', 'figure'),
     Output('budget-gauge', 'figure')],
    [Input('district-dropdown', 'value')]
)
def update_details(district):
    dff = df[df['District'] == district]
    val = dff[dff['Category'] == 'Readiness and Gaps']['Value'].mean() * 100
    fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=val, title={'text': "Readiness"}))
    
    risk_df = dff[(dff['Category'] == 'Early Warning and Response') & (dff['Indicator'].str.contains("Risks"))]
    fig_radar = px.line_polar(risk_df, r='Value', theta='Indicator', line_close=True, title="Risk Profile")
    
    b_val = dff[dff['Category'] == 'Bottlenecks']['Value'].sum()
    fig_budget = go.Figure(go.Indicator(mode="gauge+number", value=b_val, title={'text': "Budget Issues"}, gauge={'bar': {'color': 'red'}}))
    
    return fig_gauge, fig_radar, fig_budget

if __name__ == '__main__':
    app.run(debug=True)
