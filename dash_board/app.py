import numpy as np
import pandas as pd
import datetime

import dash
import dash_table as dt
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px

# from apps import cases, counsel


# -------------------------------------Styles-------------------------------------
# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 15px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10px'
}

TEXT_STYLE = {
    'textAlign': 'center',
    # 'color': '#191970'
}

CELL_STYLE = {
    'padding': '5px',
    'whiteSpace': 'normal',
    'height': 'auto',
    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'font-family': 'Helvetica'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    # 'color': '#0074D9',
    'padding': '5px 0px'
}
'#f6511d', '#00a6ed', '#ffb400'
colors = {'red': '#f6511d', 'blue': '#00a6ed', 'yellow': '#ffb400'}

df = pd.read_csv(
    r"D:\aaProjectsStuff\Amicus\Dashboard\FinalData.csv")

cdf = pd.read_csv(
    r"D:\aaProjectsStuff\Amicus\Dashboard\dummy.csv"
)


# -------------------------------------Functions-------------------------------------
# def get_xy_from_count():
#     rc_count = df['RespondentCounsel'].value_counts()

#     rc_df = pd.DataFrame(rc_count)

#     rc_df_subset = rc_df[:10]

#     rc_counts_indices = rc_df_subset.index.tolist()
#     rc_counts_values = rc_df_subset.values.tolist()

#     return rc_counts_indices, rc_counts_values


def print_details(n_clicks='', dropdown_value='', range_slider_value='', check_list_value='', radio_items_value=''):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure


def date_time_extractor(df, date_col, date_format=None, year=1, quarter=0, month=1, weekofyear=0, dayofweek=0, dayofyear=0, daysinmonth=0, timestamp=0):

    df['TimeStamp'] = pd.to_datetime(df[date_col], format=date_format)
    # print(df.head())

    if year:
        df['Year'] = df['TimeStamp'].dt.year
    if quarter:
        df['Quarter'] = df['TimeStamp'].dt.quarter
    if month:
        df['Month'] = df['TimeStamp'].dt.month
    if weekofyear:
        df['WeekOfYear'] = df['TimeStamp'].dt.weekofyear
    if dayofweek:
        df['DayOfWeek'] = df['TimeStamp'].dt.dayofweek
    if dayofyear:
        df['DayOfYear'] = df['TimeStamp'].dt.dayofyear
    if daysinmonth:
        df['DaysInMonth'] = df['TimeStamp'].dt.daysinmonth

    # if (timestamp == 0):
    # df.drop(['TimeStamp'], inplace=True)

    return df


def customLegend(fig, nameSwap):
    for i, dat in enumerate(fig.data):
        for elem in dat:
            if elem == 'name':
                print(fig.data[i].name)
                fig.data[i].name = nameSwap[fig.data[i].name]
    return(fig)


print(datetime.datetime.now())

# -------------------------------------Graphs(Processing)-------------------------------------
# Donut Graph
jd_count = pd.DataFrame(df['FinalJudgement'].value_counts())
jd_unique = df['FinalJudgement'].unique()

# print(jd_unique)

jd_count.reset_index(inplace=True)
jd_count.columns = ['Judgement', 'No. of Cases']

# Tables Data Prep

plaintiff_df = pd.DataFrame(df.loc[:, ['Plaintiff']])
defendant_df = pd.DataFrame(df.loc[:, ['Defendant']])

pet_counsel_df = pd.DataFrame(
    df.loc[:, ['PetitionerCounsel']])
resp_counsel_df = pd.DataFrame(
    df.loc[:, ['RespondentCounsel']])


# Line Graph Prep

df['month_year'] = df.DateFiled.apply(
    lambda x: x.split('-')[1] + '/' + x.split('-')[0])

area_df = df.groupby(['month_year', 'FinalJudgement']).count()['Judge']
area_df = area_df.reset_index()
area_df.month_year = (pd.to_datetime(area_df.month_year))
area_df = area_df.sort_values(by='month_year')


# Date Processing
df = date_time_extractor(df, 'DateFiled')
cdf = date_time_extractor(cdf, 'DateFiled')


# -------------------------------------Layout-------------------------------------
controls = dbc.FormGroup(
    [
        html.Div([
            dcc.Tabs(id='tabs-id', value='tab-1', children=[
                dcc.Tab(label='Home',
                        value='tab-1',
                        className='custom-tab',
                        selected_className='custom-tab--selected'),
                dcc.Tab(label='Cases',
                        value='tab-2',
                        className='custom-tab',
                        selected_className='custom-tab--selected'),
            ]),
        ]),
        html.Br(),
        html.P('Range Slider', style={
            'textAlign': 'center'
        }),
        dcc.RangeSlider(
            id='date-range-slider',
            min=2015,
            max=2021,
            step=1,
            marks={2015: '2015', 2018: '2018',  2021: '2021'},
            value=[2015, 2021],
            pushable=1
        ),
        html.Br(),

        # MAIN TAB
        html.P('Plaintiff Search',
               style={
                   'textAlign': 'center'
               }),
        dbc.InputGroup([

            dbc.InputGroupAddon(
                dbc.Button("Search", id="plaintiff-search-button")
            ),
            dbc.Input(
                id='plaintiff-search',
                placeholder='Search...'),
        ]
        ),

        html.P('Defendant Search',
               style={
                   'textAlign': 'center'
               }),
        dbc.InputGroup([

            dbc.InputGroupAddon(
                dbc.Button("Search", id="defendant-search-button")
            ),
            dbc.Input(
                id='defendant-search',
                placeholder='Search...'),
        ]
        ),
        html.Br(),

        html.P('Type of Judgement', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='judgement-dropdown',
            options=[{'label': i, 'value': i}
                     for i in jd_unique],
            value=jd_unique.tolist(),
            multi=True
        ),
        html.Br(),

        # COUSNEL TAB
        html.P('Petitioner Counsel Search',
               style={
                   'textAlign': 'center'
               }),
        dbc.InputGroup([

            dbc.InputGroupAddon(
                dbc.Button("Search", id="pet-counsel-search-button")
            ),
            dbc.Input(
                id='pet-counsel-search',
                placeholder='Search...'),
        ]
        ),

        html.P('Respondent Counsel Search',
               style={
                   'textAlign': 'center'
               }),
        dbc.InputGroup([

            dbc.InputGroupAddon(
                dbc.Button("Search", id="resp-counsel-search-button")
            ),
            dbc.Input(
                id='resp-counsel-search',
                placeholder='Search...'),
        ]
        ),
        # html.Br(),


        # dbc.Button(
        #     id='submit_button',
        #     n_clicks=0,
        #     children='Submit',
        #     color='primary',
        #     block=True
        # ),

        # dbc.Button(
        #     id='switch-button',
        #     n_clicks=0,
        #     children='View Cases',
        #     color='primary',
        #     block=True,
        #     href='/apps/cases'
        # ),


    ]
)

sidebar = html.Div(
    [
        html.H2('Filters', style=TEXT_STYLE),
        html.Hr(),
        # TODO: Add dcc.Tabs
        controls
    ],
    style=SIDEBAR_STYLE,
)


content_search_row = dbc.Row([
    html.Div([
        html.H4('Keyword Search',
                style={
                    'textAlign': 'center'
                },
                className='search-header'),
    ],
        className='search-header-div'),
    dbc.InputGroup([
        dbc.InputGroupAddon(
            dbc.Button("Search", id="keyword-search-button")
        ),
        dbc.Input(
            id='keyword-search',
            placeholder='Search for Keywords...'),
    ],
        style={'padding': '5px 25px 25px 25px'}
    ),
])

content_donut_row = dbc.Row([

    dbc.Col(
        dcc.Graph(
            id='donut-graph',
            # figure=fig_donut,
        ),
        md=12
    ),

])

content_line_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='line-graph'), md=12
        ),

    ]
)

content_counsel_row = dbc.Row([
    dbc.Col(
        dt.DataTable(
            id='petitioner-counsel-table',
            # columns=[{"name": i, "id": i} for i in pet_counsel_df.columns],
            columns=[{"name": "Top Petitioner Counsel",
                      "id": "PetitionerCounsel"}],
            data=df[["PetitionerCounsel"]][:50].dropna().to_dict('records'),
            page_action='none',
            fixed_rows={'headers': True},

            css=[{
                 'selector': '.dash-spreadsheet td div',
                 'rule': '''
                    line-height: 15px;
                    max-height: 30px; min-height: 30px; height: 30px;
                   
                    display: block;
                    overflow-y: hidden;
                '''
                 }],

            # tooltip_data=[
            #     {
            #         column: {'value': str(value), 'type': 'markdown'}
            #         for column, value in row.items()
            #     } for row in df[['PetitionerCounsel']][:50].to_dict('records')
            # ],
            # tooltip_duration=None,

            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_as_list_view=True,
            style_cell=CELL_STYLE,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[{'textAlign': 'left'}],
            style_table={'height': '300px', 'overflow': 'hidden'}
        ),
        md=6
    ),
    dbc.Col(
        dt.DataTable(
            id='defendant-counsel-table',
            # columns=[{"name": i, "id": i} for i in resp_counsel_df.columns],
            columns=[{"name": "Top Respondent Counsel",
                      "id": "RespondentCounsel"}],
            data=df[['RespondentCounsel']][:50].dropna().to_dict('records'),
            page_action='none',
            fixed_rows={'headers': True},

            css=[{
                 'selector': '.dash-spreadsheet td div',
                 'rule': '''
                    line-height: 15px;
                    max-height: 30px; min-height: 30px; height: 30px;
                   
                    display: block;
                    overflow-y: hidden;
                '''
                 }],

            # tooltip_data=[
            #     {
            #         column: {'value': str(value), 'type': 'markdown'}
            #         for column, value in row.items()
            #     } for row in df[['RespondentCounsel']][:50].to_dict('records')
            # ],
            # tooltip_duration=None,

            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_as_list_view=True,
            style_cell=CELL_STYLE,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[{'textAlign': 'left'}],
            style_table={'height': '300px', 'overflow': 'hidden'}
        ),
        md=6
    ),
])

# bar_content_fourth_row = dbc.Row(
#     [
#         dbc.Col(
#             dcc.Graph(id='ac-bar-graph'), md=6
#         ),
#         dbc.Col(
#             dcc.Graph(id='rc-bar-graph'), md=6
#         )
#     ]
# )

content_heatmap_row = html.Div([
    dbc.Row(
        dcc.Graph(id='ac-heatmap'),  # md=12
    ),
    dbc.Row(
        dcc.Graph(id='rc-heatmap'),  # md=12
    )
])


content_table_row = dbc.Row([
    dbc.Col(
        # dbc.Table.from_dataframe(
        #     plaintiff_df, striped=True, bordered=True, hover=True, responsive='sm'),

        dt.DataTable(
            id='plaintiff-table',
            columns=[{"name": "Top Plaintiff", "id": "Plaintiff"}],
            data=df[['Plaintiff']][:50].to_dict('records'),
            page_action='none',
            fixed_rows={'headers': True},

            style_as_list_view=True,
            style_cell=CELL_STYLE,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[{'textAlign': 'left'}],
            style_table={'height': '426px', 'overflow': 'hidden'}
        ),
        md=6
    ),
    dbc.Col(

        dt.DataTable(
            id='defendant-table',
            # columns=[{"name": i, "id": i} for i in defendant_df.columns],
            columns=[{"name": "Top Defendant", "id": "Defendant"}],
            data=df[['Defendant']][:50].to_dict('records'),
            page_action='none',
            fixed_rows={'headers': True},

            style_as_list_view=True,
            style_cell=CELL_STYLE,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[{'textAlign': 'left'}],
            style_table={'height': '426px', 'overflow': 'hidden'}
        ),
        md=6
    ),
])


content_case_row = dbc.Row(
    [
        dbc.Col(
            dt.DataTable(
                id='cases-table',
                columns=[{"name": "Case Files", "id": "CaseFile"}],
                data=df[['CaseFile']][:50].to_dict('records'),
                page_action='none',
                fixed_rows={'headers': True},


                # css=[{
                #     'selector': '.dash-spreadsheet td div',
                #     'rule': '''
                #     line-height: 30px;
                #     max-height: 160px; min-height: 60px; height: 60px;

                #     display: block;
                #     overflow-y: auto;
                # '''
                # }],

                # tooltip_data=[
                #     {
                #         column: {'value': str(value), 'type': 'markdown'}
                #         for column, value in row.items()
                #     } for row in df[['CaseFile']][:50].to_dict('records')
                # ],
                # tooltip_duration=None,

                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_as_list_view=True,
                style_cell={
                    'padding': '5px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '180px', 'width': '180px', 'maxWidth': '360px',
                    'font-family': 'Helvetica'
                },
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                style_cell_conditional=[{'textAlign': 'left'}],
                style_table={'overflow': 'hidden'}
            ), md=12
        )
    ], style={'height': '500px', 'padding': '20px 0px'}
)

main_content = html.Div(
    [
        html.H2('Amicus.ai', style=TEXT_STYLE),
        html.Hr(),
        # content_search_row,
        html.H3('Visualisations'),
        html.H5('Case Count per Judgement Type', style=TEXT_STYLE),
        content_donut_row,
        html.Br(),
        html.H5('Judgement of Cases over Time', style=TEXT_STYLE),
        content_line_row,
        html.Br(),
        html.H5('Strike Rate Heatmaps', style=TEXT_STYLE),
        content_heatmap_row,
        html.Br(),
        html.H5('Data Tables', style=TEXT_STYLE),
        content_counsel_row,  # Contatins Bar Graphs, hidden, replace with heatmap
        html.Br(),
        content_table_row
    ],
    style=CONTENT_STYLE
)


case_content = html.Div(
    [
        html.H2('Amicus.ai', style=TEXT_STYLE),
        html.Hr(),
        content_search_row,
        # html.H5('Data Tables', style=TEXT_STYLE),
        content_case_row,  # Contatins Bar Graphs, hidden, replace with heatmap
        html.Br(),
    ],
    style=CONTENT_STYLE
)

# TODO: Add dcc.loading when loading

app = dash.Dash(external_stylesheets=[dbc.themes.LUX, 'dash_board\assets\app.css'],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                suppress_callback_exceptions=True
                )
app.layout = html.Div([sidebar,
                       html.Div(id='tabs-content')
                       ])


# -------------------------------------Callbacks-------------------------------------

# GRAPHS
# Donut Graph
@app.callback(
    Output('donut-graph', 'figure'),
    [Input(
        'judgement-dropdown', 'value'), Input('date-range-slider', 'value')]
)
def update_graph_donut(dropdown_value, range_slider_value):

    judgement_df = df.dropna(axis=0, subset=['FinalJudgement', 'DateFiled'])

    judgement_df = judgement_df[(judgement_df['Year'] >= range_slider_value[0])
                                & (judgement_df['Year'] <= range_slider_value[1])]

    judgement_df = judgement_df.loc[judgement_df['FinalJudgement'].isin(
        dropdown_value)]
    jd_count = pd.DataFrame(judgement_df['FinalJudgement'].value_counts())

    jd_count.reset_index(inplace=True)
    jd_count.columns = ['Judgement', 'No. of Cases']

    jd_unique = judgement_df.FinalJudgement.unique()

    # TODO: Add Legend
    fig_donut = px.pie(data_frame=jd_count.loc[jd_count['Judgement'].isin(dropdown_value)], values='No. of Cases',
                       hover_name='Judgement', hole=0.6, color='Judgement',
                       #                color_discrete_sequence=[
                       # colors['blue'], colors['blue'], colors['yellow']],
                       color_discrete_map={
        'dismissed': colors['red'], 'allowed': colors['blue'], 'tied / unclear': colors['yellow']},

    )

    # fig_donut = customLegend(fig_donut, jd_unique)
    # Dismissed  Allowed  Tied / Unclear
    # for i in range(len(jd_unique)):
    #     fig_donut.data[i].name = jd_unique[i]

    fig_donut.update_layout(transition_duration=1000)
    fig_donut.update_layout(margin=dict(t=30, b=30, l=10, r=10))

    fig_donut.update_traces(showlegend=True, selector=dict(type='pie'), )

    fig_donut.update_traces(textposition='outside',
                            textinfo='percent+label',
                            marker=dict(line=dict(color='#000000',
                                                        width=2)),
                            pull=[0.05, 0, 0.03],
                            opacity=0.9,
                            # rotation=180
                            )

    return fig_donut

# Line/Area Graph


@app.callback(
    Output('line-graph', 'figure'),
    [Input(
        'judgement-dropdown', 'value'), Input('date-range-slider', 'value')],
)
def update_graph_line(dropdown_value, range_slider_value):

    area_df = df.dropna(axis=0, subset=['FinalJudgement', 'DateFiled'])

    # Judgement filtering on the basis of selected dropdown values
    area_df = area_df.loc[area_df['FinalJudgement'].isin(dropdown_value)]

    area_df = area_df[(area_df['Year'] >= range_slider_value[0]) & (
        area_df['Year'] <= range_slider_value[1])]

    # DateTime conversions for area graph
    area_df = area_df.groupby(
        ['month_year', 'FinalJudgement']).count()['DateFiled']
    area_df = area_df.reset_index()
    area_df.month_year = (pd.to_datetime(area_df.month_year))
    area_df = area_df.sort_values(by='month_year')

    jd_unique = area_df.FinalJudgement.unique()

    fig = px.area(area_df, x='month_year', y='DateFiled',
                  color='FinalJudgement', labels={'FinalJudgement': 'Judgement', "DateFiled": "No. of Cases"},
                  color_discrete_sequence=[
                      colors['blue'], colors['red'], colors['yellow']],
                  color_discrete_map={
                      'dismissed': colors['red'], 'allowed': colors['blue'], 'tied / unclear': colors['yellow']},
                  width=1050,
                  )

    fig.update_layout(margin=dict(t=20, b=20, l=0, r=0))

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=1.02,
        xanchor="right",
        x=1
    ))

    fig.update_layout(transition_duration=500)

    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='No. of Cases')

    return fig

# Stacked Bar Graph
# Petitioner Counsel


# @app.callback(
#     Output('ac-bar-graph', 'figure'),
#     [Input('submit_button', 'n_clicks')],
#     [State('judgement-dropdown', 'value'), State('date-range-slider', 'value')
#      ])
# def update_graph_bar_ac(n_clicks, dropdown_value, range_slider_value):

#     # Judgement filtering on the basis of selected dropdown values
#     bar_df = df[(df['Year'] >= range_slider_value[0]) &
#                 (df['Year'] <= range_slider_value[1])]
#     bar_df = bar_df.loc[bar_df['FinalJudgement'].isin(dropdown_value)]

#     # DateTime conversions for area graph
#     bar_df1 = bar_df.groupby(['PetitionerCounsel', 'FinalJudgement']).count()[
#         'Judge'].reset_index()
#     bar_df2 = bar_df1.groupby(['PetitionerCounsel']).sum().reset_index()
#     final = pd.merge(bar_df1, bar_df2, on=['PetitionerCounsel'])
#     final['Percent'] = (final['Judge_x'] / final['Judge_y']) * 100

#     fig = px.bar(final[:50], y='Percent',
#                  x='PetitionerCounsel', color='FinalJudgement')
#     fig.update_layout(transition_duration=500)
#     fig.update_xaxes(showticklabels=False)
#     # fig.update_yaxes()

#     return fig


# # Respondent Counsel
# @app.callback(
#     Output('rc-bar-graph', 'figure'),
#     [Input('submit_button', 'n_clicks')],
#     [State('judgement-dropdown', 'value'), State('date-range-slider', 'value')
#      ])
# def update_graph_bar_rc(n_clicks, dropdown_value, range_slider_value):

#     bar_df = df[(df['Year'] >= range_slider_value[0]) &
#                 (df['Year'] <= range_slider_value[1])]

#     # Judgement filtering on the basis of selected dropdown values
#     bar_df = bar_df.loc[bar_df['FinalJudgement'].isin(dropdown_value)]

#     # DateTime conversions for area graph
#     bar_df1 = bar_df.groupby(['RespondentCounsel', 'FinalJudgement']).count()[
#         'Judge'].reset_index()
#     bar_df2 = bar_df1.groupby(['RespondentCounsel']).sum().reset_index()
#     final = pd.merge(bar_df1, bar_df2, on=['RespondentCounsel'])
#     final['Percent'] = (final['Judge_x'] / final['Judge_y']) * 100

#     fig = px.bar(final[:50], y='Percent',
#                  x='RespondentCounsel', color='FinalJudgement')
#     fig.update_layout(transition_duration=500)
#     fig.update_xaxes(showticklabels=False)
#     # fig.update_yaxes()

#     return fig


# Heatmaps
# Petitioner Counsel
@app.callback(
    Output('ac-heatmap', 'figure'),
    [Input(
        'judgement-dropdown', 'value'), Input('date-range-slider', 'value')]
)
def update_ac_heatmap(dropdown_value, range_slider_value):

    # heat_df = df.dropna(
    #     axis=0, subset=['PetitionerCounsel', 'Judge', 'FinalJudgement'])

    # Judgement filtering on the basis of selected dropdown values
    heat_df = cdf[(cdf['Year'] >= range_slider_value[0]) &
                  (cdf['Year'] <= range_slider_value[1])]
    heat_df = heat_df.loc[heat_df['FinalJudgement'].isin(dropdown_value)]

    # Data Processing and creation of heatmap
    dat = heat_df.groupby(['PetitionerCounsel', 'Judge']).count()[
        'FinalJudgement'].reset_index()
    data1 = dat.pivot(index='PetitionerCounsel', columns='Judge')
    data1.columns = data1.columns.droplevel(0)

    fig = px.imshow(data1, labels=dict(x="Petitioner Counsel", y="Judge", color="Efficacy")                    # ,x = data1.index.tolist(), y = data1.columns.tolist()
                    , width=1000,  # , height=1000,
                    # autosize=True
                    )

    fig.update_layout(margin=dict(t=20, b=20, l=0, r=0),
                      autosize=True)

    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=True)

    fig.update_layout(transition_duration=500)

    return fig


# Respondent Counsel
@app.callback(
    Output('rc-heatmap', 'figure'),
    [Input(
        'judgement-dropdown', 'value'), Input('date-range-slider', 'value')]
)
def update_rc_heatmap(dropdown_value, range_slider_value):

    # heat_df = df.dropna(
    #     axis=0, subset=['RespondentCounsel', 'Judge', 'FinalJudgement'])

    # Judgement filtering on the basis of selected dropdown values
    heat_df = cdf[(cdf['Year'] >= range_slider_value[0]) &
                  (cdf['Year'] <= range_slider_value[1])]
    heat_df = heat_df.loc[heat_df['FinalJudgement'].isin(dropdown_value)]

    # Data Processing and creation of heatmap
    dat = heat_df.groupby(['RespondentCounsel', 'Judge']).count()[
        'FinalJudgement'].reset_index()
    data1 = dat.pivot(index='RespondentCounsel', columns='Judge')
    data1.columns = data1.columns.droplevel(0)

    fig = px.imshow(data1, labels=dict(x="Respondent Counsel", y="Judge", color="Efficacy")                    # ,x = data1.index.tolist(), y = data1.columns.tolist()
                    , width=1000,  # height=1000
                    )

    fig.update_layout(margin=dict(t=20, b=20, l=5, r=5))

    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=True)

    fig.update_layout(transition_duration=500)

    return fig


# TABLES
# Plaintiff Table
@app.callback(
    Output("plaintiff-table", "data"),
    [Input("plaintiff-search-button", "n_clicks"),
     ],
    [State("plaintiff-search", 'value'), State('judgement-dropdown',
                                               'value'), State('date-range-slider', 'value')],
)
def on_search_click_app(n_clicks, search_value, dropdown_value, range_slider_value):

    # Filtering by selected dates
    plaintiff_df = df[(df['Year'] >= range_slider_value[0])
                      & (df['Year'] <= range_slider_value[1])]

    # Filtering by selected Judgements from dropdown menu
    plaintiff_df = plaintiff_df.loc[plaintiff_df['FinalJudgement'].isin(
        dropdown_value)]

    # Creating separate plaintiff_df with just plaintiff column
    plaintiff_df = pd.DataFrame(plaintiff_df.loc[:, ['Plaintiff']])

    search_values = []

    if n_clicks:
        # if (n_clicks != None) | (sub_clicks != None):
        if (search_value != None or search_value != '' or search_value != ' '):
            search_values.extend([
                search_value, search_value.lower(), search_value.upper()])
            return plaintiff_df[plaintiff_df['Plaintiff'].str.contains(
                '|'.join(search_values), na=False)].to_dict('records')
            # return plaintiff_df[plaintiff_df['Plaintiff'].str.contains(
            #     (search_value))].to_dict('records')

    else:
        return plaintiff_df.iloc[:30].to_dict('records')


@app.callback(
    Output("defendant-table", "data"),
    [Input("defendant-search-button", "n_clicks"),
     ],
    [State("defendant-search", 'value'), State('judgement-dropdown',
                                               'value'), State('date-range-slider', 'value')],
)
def on_search_click_resp(n_clicks, search_value, dropdown_value, range_slider_value):

    # Filtering by selected dates
    defendant_df = df[(df['Year'] >= range_slider_value[0])
                      & (df['Year'] <= range_slider_value[1])]

    # Filtering by selected Judgements from dropdown menu
    defendant_df = defendant_df.loc[defendant_df['FinalJudgement'].isin(
        dropdown_value)]

    # Creating separate defendant_df with just plaintiff column
    defendant_df = pd.DataFrame(defendant_df.loc[:, ['Defendant']])

    search_values = []

    if n_clicks:
        # if (n_clicks != None) | (sub_clicks != None):
        if (search_value != None or search_value != '' or search_value != ' '):
            search_values.extend([
                search_value, search_value.lower(), search_value.upper()])
            return defendant_df[defendant_df['Defendant'].str.contains(
                '|'.join(search_values), na=False)].to_dict('records')

    else:
        return defendant_df[:30].to_dict('records')

# TODO: Fix Petitioner Counsel and Respondent Counsel table searchings(case sensitive)


@app.callback(
    Output("petitioner-counsel-table", "data"),
    [Input("pet-counsel-search-button", "n_clicks")
     ],
    [State("pet-counsel-search", 'value'), State('judgement-dropdown',
                                                 'value'), State('date-range-slider', 'value')],
)
def on_search_click_ac(n_clicks, search_value, dropdown_value, range_slider_value):

    # Filtering by selected dates
    pet_counsel_df = cdf[(cdf['Year'] >= range_slider_value[0])
                         & (cdf['Year'] <= range_slider_value[1])]

    # Filtering by selected Judgements from dropdown menu
    pet_counsel_df = pet_counsel_df.loc[pet_counsel_df['FinalJudgement'].isin(
        dropdown_value)]

    # Creating separate pet_counsel_df with just plaintiff column
    pet_counsel_df = pd.DataFrame(pet_counsel_df.loc[:, ['PetitionerCounsel']])

    search_values = []

    if n_clicks:
        # if (n_clicks != None) | (sub_clicks != None):
        if (search_value != None or search_value != '' or search_value != ' '):
            search_values.extend([
                search_value, search_value.lower(), search_value.upper()])

            return pet_counsel_df[pet_counsel_df['PetitionerCounsel'].str.contains(
                '|'.join(search_values), na=False)].dropna().to_dict('records')
            # return plaintiff_df[plaintiff_df['Plaintiff'].str.contains(
            #     (search_value))].to_dict('records')

    else:
        return pet_counsel_df[:30].dropna().to_dict('records')


@app.callback(
    Output("defendant-counsel-table", "data"),
    [Input("resp-counsel-search-button", "n_clicks"),
     ],
    [State("resp-counsel-search", 'value'), State('judgement-dropdown',
                                                  'value'), State('date-range-slider', 'value')],
)
def on_search_click_rc(n_clicks, search_value, dropdown_value, range_slider_value):

    # Filtering by selected dates
    resp_counsel_df = cdf[(cdf['Year'] >= range_slider_value[0]) & (
        cdf['Year'] <= range_slider_value[1])]

    # Filtering by selected Judgements from dropdown menu
    resp_counsel_df = resp_counsel_df.loc[resp_counsel_df['FinalJudgement'].isin(
        dropdown_value)]

    # Creating separate resp_counsel_df with just plaintiff column
    resp_counsel_df = pd.DataFrame(
        resp_counsel_df.loc[:, ['RespondentCounsel']])

    search_values = []

    if n_clicks:
        # if (n_clicks != None) | (sub_clicks != None):
        if (search_value != None or search_value != '' or search_value != ' '):
            search_values.extend([
                search_value, search_value.lower(), search_value.upper()])
            return resp_counsel_df[resp_counsel_df['RespondentCounsel'].str.contains(
                '|'.join(search_values), na=False)].to_dict('records')

    else:
        return resp_counsel_df[:30].to_dict('records')


# CaseFiles Table
@app.callback(
    Output("cases-table", "data"),
    [Input("keyword-search-button", "n_clicks"),
     #  Input(' on', 'n_clicks')
     ],
    [State("keyword-search", 'value'), State('judgement-dropdown',
                                             'value'), State('date-range-slider', 'value')],
)
def on_search_click_case(n_clicks, search_value, dropdown_value, range_slider_value):

    # Filtering by selected dates
    case_df = df[(df['Year'] >= range_slider_value[0])
                 & (df['Year'] <= range_slider_value[1])]

    # Filtering by selected Judgements from dropdown menu
    case_df = case_df.loc[case_df['FinalJudgement'].isin(
        dropdown_value)]

    # Creating separate plaintiff_df with just plaintiff column
    case_df = pd.DataFrame(case_df.loc[:, ['CaseFile']])

    search_values = []

    if n_clicks:
        # if (n_clicks != None) | (sub_clicks != None):
        if (search_value != None or search_value != '' or search_value != ' '):
            search_values.extend([
                search_value, search_value.lower(), search_value.upper()])
            return case_df[case_df['CaseFile'].str.contains(
                '|'.join(search_values), na=False)].to_dict('records')
            # return plaintiff_df[plaintiff_df['Plaintiff'].str.contains(
            #     (search_value))].to_dict('records')

    else:
        return case_df.iloc[:30].to_dict('records')


@app.callback(Output('tabs-content', 'children'),
              Input('tabs-id', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            main_content
        ])
    elif tab == 'tab-2':
        return html.Div([
            case_content
        ])


if __name__ == '__main__':
    app.run_server(port='8085', debug=True)
