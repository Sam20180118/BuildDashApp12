import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np

# for visualization
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import matplotlib.pyplot as plt

import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "notebook_connected"
pio.renderers.default = 'iframe'

plt.rcParams.update({'font.family':'Modern Sans'})

# ========================================
jwork = pd.read_csv('jdat-prob-by-IADL.csv')
jwork.shape

# button1 = 'Standing balance'
button1 = jwork['button1'].unique()
button1

my_slider = jwork['my_slider'].unique()
my_slider

jwork[np.isin(jwork['button1'], button1) & np.isin(jwork['my_slider'], my_slider)]

def control1(button1, my_slider):
    slider_avg_risk = round(jwork[np.isin(jwork['button1'], button1) &
                                  np.isin(jwork['my_slider'], my_slider)]['value'], 4).mean()

    avg_risk_plt = go.Figure(go.Indicator(
        mode="gauge+number",
        value=slider_avg_risk,
        number={
            # "suffix": "%",
            'font_color': 'red',
            "valueformat": ".1%", },
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [0, 1]}},
        # title = {'text': "average risk of admission twice in one year"}
    ))

    avg_risk_plt.add_annotation(
        x=0.5,
        y=0.35,
        text='Expected risk prevalence <br> if interventions effective',
        font=dict(
            size=12,
            # color = 'darkred'
        ), showarrow=True)

    avg_risk_plt.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="center", x=0.5),
        margin=dict(b=0, t=0, l=0, r=0),
        template='ggplot2',
        height=200
    )
    return avg_risk_plt


# Start Dashboard
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout section
app.layout = html.Div([
    html.Div([html.H2('Frequent Flyer Risk Prediction Tool (Management View)',
                      style={'marginLeft': 20, 'color': 'white'})],
             style={'borderBottom': 'thin black solid',
                    'backgroundColor': '#24a0ed',
                    'padding': '10px 5px'}),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    html.Div([
                        dcc.Dropdown(id='dp7',
                                     multi=False,
                                     value='Standing balance',
                                     options=[{'label': x, 'value': x} for x in button1],
                                     style={"textTransform": "uppercase",
                                            'border-color': '#b3dad7',
                                            'background-color': 'white',
                                            'text-color': 'white',
                                            # 'textAlign': 'center',
                                            'margin': '5px',
                                            # 'width': '100%',
                                            # 'height': '600px',
                                            'height': '10px', 'width': '400px',
                                            'font-size': '100%'},
                                     className="dropdown open"), ]),
                    width={"size": 4}
                ),
                dbc.Col([
                    html.Div(['Decision Direction'],
                             style={
                                 'font-size': 25,
                                 'margin-right': '2px',
                                 'margin-left': '2px'
                             }), ]),

            ], className="g-0"),
            dbc.Row([
                dbc.Col([html.Div("Current risk prevalence of Dependent group",
                                  style={'font-weight': 'bold',
                                         'font-size': 15,
                                         # 'marginBottom': '0px',
                                         # 'marginTop': '10px',
                                         # 'margin': '1px',
                                         }),
                         html.Div(
                             id='avg_risk',
                             style={
                                 # 'font-weight': 'bold',
                                 'font-size': 60,
                                 'color': 'blue',
                             }),
                         ], width={"size": 4}),
                dbc.Col([html.Div("VS",
                                  style={'font-weight': 'bold',
                                         'padding': '45px 0px',
                                         'font-size': 60})], width={"size": 2}),

                dbc.Col([html.Div(["Current risk prevalence of Full sample"],
                                  style={'font-weight': 'bold',
                                         'font-size': 15,
                                         # 'marginBottom': '0px',
                                         # 'marginTop': '10px',
                                         # 'margin': '1px',
                                         }),
                         html.Div('15.8%',
                                  style={
                                      # 'font-weight': 'bold',
                                      'font-size': 60,
                                      'color': 'green', }),
                         ], width={"size": 4}),
            ], style={"height": "25%"}, className="g-0"),
            dbc.Row([
                html.Div([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='fig_guage',
                                      figure=control1(button1, my_slider),
                                      className=' mb-1',),
                                    ]),
                        dbc.CardFooter([dcc.Slider(min=1, max=5, step=None,
                                                   id='my_slider_num',
                                                   marks={
                                                       1: {"label": "Baseline", 'style': {'transform': 'scale(1.2)'}},
                                                       2: {"label": "25%", 'style': {'transform': 'scale(1.2)'}},
                                                       3: {"label": "50%", 'style': {'transform': 'scale(1.2)'}},
                                                       4: {"label": "75%", 'style': {'transform': 'scale(1.2)'}},
                                                       5: {"label": "100%", 'style': {'transform': 'scale(1.2)'}}},
                                                   value=1,
                                                   ),
                                        ]),
                    ], style={"width": "35rem",
                              # 'height':'50vh'
                              }),
                ])
            ]),
            dbc.Row([html.Div(['Decision variable'],
                              style={
                                  'font-size': 25,
                              }),
                     # html.Div(['selected risk condition of',
                     #           html.Br(),
                     #           ' Baseline: 0% of individuals in the dependent group improve ',
                     #           html.Br(),
                     #           ' 25%: 25% of individuals in the dependent group improve ',
                     #           html.Br(),
                     #           ' 50%: 50% of individuals in the dependent group improve ',
                     #           html.Br(),
                     #           ' 75%: 75% of individuals in the dependent group improve ',
                     #           html.Br(),
                     #           ' 100%: 100% of individuals in the dependent group improve ',
                     #           ],
                     #          style={
                     #              'font-size': 15,
                     #          }),
                     ])
        ]),
        dbc.Col([
            dbc.Row([html.Div('SHAP feature importance',
                              style={'font-weight': 'bold', 'font-size': 30}),
                     html.Div([
                         dcc.Graph(id='fig_shap'),
                     ]),
                     ]),
        ]),

    ])
])


@app.callback(
    Output('fig_guage', 'figure'),
    [Input('dp7', 'value'),
     Input('my_slider_num', 'value')]
)
def draw_plt(button1, my_slider_num):
    if my_slider_num == 1:
        my_slider = 'baseline'
    elif my_slider_num == 2:
        my_slider = 'Drop 25%'
    elif my_slider_num == 3:
        my_slider = 'Drop 50%'
    elif my_slider_num == 4:
        my_slider = 'Drop 75%'
    elif my_slider_num == 5:
        my_slider = 'Drop 100%'

    fig1 = control1(button1, my_slider)
    return fig1


@app.callback(
    Output('avg_risk', 'children'),
    [Input('dp7', 'value')]
)
def output(button1):
    cal_avg_risk = str(round(jwork[np.isin(jwork['button1'], button1) &
                                   (jwork['my_slider'] == 'baseline')]['value'].values[0] * 100, 1)) + '%'
    return cal_avg_risk

@app.callback(
    Output('fig_shap', 'figure'),
    [Input('dp7', 'value')]
)
def gen_shap_plot(button1):
    if button1 == 'Standing balance':
        df4plot = pd.read_csv('shap_value_for_plot_' + button1 + '.csv')
    elif button1 == 'Bowel':
        df4plot = pd.read_csv('shap_value_for_plot_' + button1 + '.csv')
    elif button1 == 'Housecleaning and home maintenance':
        df4plot = pd.read_csv('shap_value_for_plot_' + button1 + '.csv')
    elif button1 == 'Managing tasks associated with laundry':
        df4plot = pd.read_csv('shap_value_for_plot_' + button1 + '.csv')
    elif button1 == 'Uses public transportation as usual':
        df4plot = pd.read_csv('shap_value_for_plot_' + button1 + '.csv')
    elif button1 == 'Shopping for items required for daily life':
        df4plot = pd.read_csv('shap_value_for_plot_' + button1 + '.csv')
    elif button1 == 'Bladder':
        df4plot = pd.read_csv('shap_value_for_plot_' + button1 + '.csv')
    elif button1 == 'Meal Preparation':
        df4plot = pd.read_csv('shap_value_for_plot_' + button1 + '.csv')
    elif button1 == 'Managing Finance':
        df4plot = pd.read_csv('shap_value_for_plot_' + button1 + '.csv')
    elif button1 == 'Managing medications':
        df4plot = pd.read_csv('shap_value_for_plot_' + button1 + '.csv')

    df4plot1 = df4plot.sort_values('shap_value')
    fig = px.bar(df4plot1, x="shap_value", y="feature")

    fig.update_layout(
        xaxis_title="mean(|SHAP value|)(average impact on model output magnitude)",
        autosize=False,
        width=630,
        height=440,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            size=11,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=True,
            showline=True,
            gridcolor='lightgray',
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            showticklabels=True,
            linecolor='black',
            tickcolor='black',
            ticks='outside',
            ticklen=5
        ),
        margin={'t': 25, 'b': 50},
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)