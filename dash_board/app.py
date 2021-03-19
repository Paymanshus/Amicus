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
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    # 'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    # 'color': '#0074D9',
    'padding': '5px 0px'
}

df = pd.read_csv(
    r"D:\aaProjectsStuff\Amicus\Dashboard\newNewData.csv")


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


# -------------------------------------Graphs(Processing)-------------------------------------
# Donut Graph
jd_count = pd.DataFrame(df['FinalJudgement'].value_counts())
jd_unique = df['FinalJudgement'].unique()

# print(jd_unique)

jd_count.reset_index(inplace=True)
jd_count.columns = ['Judgement', 'No. of Cases']

# Tables Data Prep

plaintiff_df = pd.DataFrame(df.loc[5000:5050, ['Plaintiff']])
defendant_df = pd.DataFrame(df.loc[5000:5050, ['Defendant']])

pet_counsel_df = pd.DataFrame(df.loc[15000:15050, ['PetitionerCounsel']])
resp_counsel_df = pd.DataFrame(df.loc[15000:15050, ['RespondentCounsel']])

# TODO: Change to data indicing rather than df duplication, delete plaintiff_df, defendant_df, etc. and replace with df['Plaintiff']
# directly once scrolling issues are sorted out

# Date Processing

# def date_time_extractor(df, date_col, date_format, year=1, quarter=0, month=1, weekofyear=0, dayofweek=0, dayofyear=0, daysinmonth=0, timestamp=0):

#     df['TimeStamp'] = pd.to_datetime(df[date_col], format=date_format)

#     if year:
#         df['Year'] = df['TimeStamp'].dt.year
#     if quarter:
#         df['Quarter'] = df['TimeStamp'].dt.quarter
#     if month:
#         df['Month'] = df['TimeStamp'].dt.month
#     if weekofyear:
#         df['WeekOfYear'] = df['TimeStamp'].dt.weekofyear
#     if dayofweek:
#         df['DayOfWeek'] = df['TimeStamp'].dt.dayofweek
#     if dayofyear:
#         df['DayOfYear'] = df['TimeStamp'].dt.dayofyear
#     if daysinmonth:
#         df['DaysInMonth'] = df['TimeStamp'].dt.daysinmonth

#     if ~timestamp:
#         df.drop(['TimeStamp'], inplace=True)

#     return df

# -------------------------------------Layout-------------------------------------
controls = dbc.FormGroup(
    [
        html.P('Range Slider', style={
            'textAlign': 'center'
        }),
        dcc.RangeSlider(
            id='date-range-slider',
            min=2015,
            max=2021,
            step=1,
            marks={2015: '2015', 2018: '2018',  2021: '2021'},
            value=[2015, 2021]
        ),
        # html.Br(),

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
                placeholder='Search for Plaintiff...'),
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
                placeholder='Search for defendant...'),
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
        html.Br(),

        # html.P('Check Box', style={
        #     'textAlign': 'center'
        # }),
        # dbc.Card([dbc.Checklist(
        #     id='check_list',
        #     options=[{
        #         'label': 'Value One',
        #         'value': 'value1'
        #     },
        #         {
        #             'label': 'Value Two',
        #             'value': 'value2'
        #     },
        #         {
        #             'label': 'Value Three',
        #             'value': 'value3'
        #     }
        #     ],
        #     value=['value1', 'value2'],
        #     inline=True
        # )]),
        # html.Br(),
        # html.P('Radio Items', style={
        #     'textAlign': 'center'
        # }),
        # dbc.Card([dbc.RadioItems(
        #     id='radio_items',
        #     options=[{
        #         'label': 'Value One',
        #         'value': 'value1'
        #     },
        #         {
        #             'label': 'Value Two',
        #             'value': 'value2'
        #     },
        #         {
        #             'label': 'Value Three',
        #             'value': 'value3'
        #     }
        #     ],
        #     value='value1',
        #     style={
        #         'margin': 'auto'
        #     }
        # )]),
        # html.Br(),

        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        ),
    ]
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row([
    dbc.Col(
        # dbc.Table.from_dataframe(
        #     plaintiff_df, striped=True, bordered=True, hover=True, responsive='sm'),

        dt.DataTable(
            id='plaintiff-table',
            columns=[{"name": i, "id": i} for i in plaintiff_df.columns],
            data=plaintiff_df.to_dict('records'),
            page_action='none',
            fixed_rows={'headers': True},

            style_as_list_view=True,
            style_table={'height': '20em', 'overflow': 'hidden'}
        ),
        md=4
    ),
    dbc.Col(
        # dbc.Table.from_dataframe(
        #     plaintiff_df, striped=True, bordered=True, hover=True, responsive='sm'),

        dt.DataTable(
            id='defendant-table',
            columns=[{"name": i, "id": i} for i in defendant_df.columns],
            data=defendant_df.to_dict('records'),
            page_action='none',
            fixed_rows={'headers': True},

            style_as_list_view=True,
            style_table={'height': '20em', 'overflow': 'hidden'}
        ),
        md=4
    ),
    dbc.Col(
        dcc.Graph(
            id='donut-graph',
            # figure=fig_donut,
        ),
        md=4
    ),
    # dbc.Col(
    #     dbc.Card(
    #         [
    #             dbc.CardBody(
    #                 [
    #                     html.H4('Card Title 4', className='card-title',
    #                             style=CARD_TEXT_STYLE),
    #                     html.P('Sample text.', style=CARD_TEXT_STYLE),
    #                 ]
    #             ),
    #         ]
    #     ),
    #     md=3
    # )
])

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='line-graph'), md=12
        ),

    ]
)

content_third_row = dbc.Row([
    dbc.Col(
        dt.DataTable(
            id='petitioner-counsel-table',
            columns=[{"name": i, "id": i} for i in pet_counsel_df.columns],
            data=pet_counsel_df.to_dict('records'),
            page_action='none',
            fixed_rows={'headers': True},

            style_as_list_view=True,
            style_table={'height': '20em', 'overflow': 'hidden'}
        ),
        md=4
    ),
    dbc.Col(
        dt.DataTable(
            id='defendant-counsel-table',
            columns=[{"name": i, "id": i} for i in resp_counsel_df.columns],
            data=resp_counsel_df.to_dict('records'),
            page_action='none',
            fixed_rows={'headers': True},

            style_as_list_view=True,
            style_table={'height': '20em', 'overflow': 'hidden'}
        ),
        md=4
    ),
    # dbc.Col(
    #     dcc.Graph(
    #         id='donut-graph',
    #     ),
    #     md=4
    # ),
])

content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='ac_bar_graph'), md=6
        ),
        dbc.Col(
            dcc.Graph(id='rc_bar_graph'), md=6
        )
    ]
)

content = html.Div(
    [
        html.H2('Amicus.ai', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        content_second_row,
        content_third_row,
        content_fourth_row
    ],
    style=CONTENT_STYLE
)


app = dash.Dash(external_stylesheets=[
                dbc.themes.LUX, 'dash_board\styles\app.css'])
app.layout = html.Div([sidebar, content])

# -------------------------------------Callbacks-------------------------------------


@app.callback(
    Output('donut-graph', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('judgement-dropdown', 'value'), State('date-range-slider', 'value')])
def update_graph_donut(n_clicks, dropdown_value, range_slider_value):

    # TODO: df filtering on the basis of date before passing through and creating jd_count
    # judgement_df = df[df[]]
    judgement_df = df

    jd_count = pd.DataFrame(judgement_df['FinalJudgement'].value_counts())
    jd_unique = judgement_df['FinalJudgement'].unique()

    # print(jd_unique)

    jd_count.reset_index(inplace=True)
    jd_count.columns = ['Judgement', 'No. of Cases']

    fig_donut = px.pie(data_frame=jd_count.loc[jd_count['Judgement'].isin(dropdown_value)], values='No. of Cases',
                       hover_name='Judgement', hole=0.6)

    # fig_donut.update_layout(transition_duration=250)

    return fig_donut


@app.callback(
    Output('line-graph', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('judgement-dropdown', 'value'), State('date-range-slider', 'value')
     ])
def update_graph_line(n_clicks, dropdown_value, range_slider_value):
    print_details(n_clicks, dropdown_value, range_slider_value)

    area_df = df.loc[df['FinalJudgement'].isin(dropdown_value)]

    fig = px.area(area_df, x='DateFiled', color="FinalJudgement")

    return fig


# @app.callback(
#     Output('card_title_1', 'children'),
#     [Input('submit_button', 'n_clicks')],
#     [State('judgement-dropdown', 'value'), State('date-range-slider', 'value')
#      ])
# def update_card_title_1(n_clicks, dropdown_value, range_slider_value):
#     print_details(n_clicks, dropdown_value, range_slider_value,
#                   )
#     return 'Card Tile 1 change by call back = {}'.format(dropdown_value)


@app.callback(
    Output("plaintiff-table", "data"),
    [Input("plaintiff-search-button", "n_clicks")],
    [State("plaintiff-search", 'value')],
)
def on_search_click_app(n_clicks, search_value):

    search_values = []

    if n_clicks:
        if (search_value != None or search_value != '' or search_value != ' '):
            search_values.extend([
                search_value, search_value.lower(), search_value.upper()])
            return plaintiff_df[plaintiff_df['Plaintiff'].str.contains(
                '|'.join(search_values))].to_dict('records')
            # return plaintiff_df[plaintiff_df['Plaintiff'].str.contains(
            #     (search_value))].to_dict('records')

    else:
        return plaintiff_df.to_dict('records')


@app.callback(
    Output("defendant-table", "data"),
    [Input("defendant-search-button", "n_clicks")],
    [State("defendant-search", 'value')],
)
def on_search_click_resp(n_clicks, search_value):

    search_values = []

    if n_clicks:
        if (search_value != None or search_value != '' or search_value != ' '):
            search_values.extend([
                search_value, search_value.lower(), search_value.upper()])
            return defendant_df[defendant_df['Defendant'].str.contains(
                '|'.join(search_values))].to_dict('records')

    else:
        return defendant_df.to_dict('records')


@app.callback(
    Output("petitioner-counsel-table", "data"),
    [Input("pet-counsel-search-button", "n_clicks")],
    [State("pet-counsel-search", 'value')],
)
def on_search_click_ac(n_clicks, search_value):

    search_values = []

    if n_clicks:
        if (search_value != None or search_value != '' or search_value != ' '):
            search_values.extend([
                search_value, search_value.lower(), search_value.upper()])
            return pet_counsel_df[pet_counsel_df['PetitionerCounsel'].str.contains(
                '|'.join(search_values))].to_dict('records')
            # return plaintiff_df[plaintiff_df['Plaintiff'].str.contains(
            #     (search_value))].to_dict('records')

    else:
        return pet_counsel_df.to_dict('records')


@app.callback(
    Output("defendant-counsel-table", "data"),
    [Input("resp-counsel-search-button", "n_clicks")],
    [State("resp-counsel-search", 'value')],
)
def on_search_click_rc(n_clicks, search_value):

    search_values = []
    if n_clicks:
        if (search_value != None or search_value != '' or search_value != ' '):
            search_values.extend([
                search_value, search_value.lower(), search_value.upper()])
            return resp_counsel_df[resp_counsel_df['Defendant'].str.contains(
                '|'.join(search_values))].to_dict('records')

    else:
        return resp_counsel_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(port='8085', debug=True)
