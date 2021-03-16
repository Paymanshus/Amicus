import numpy as np
import pandas as pd
import datetime as dt

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
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9',
    'padding': '5px 0px'
}

df = pd.read_csv(
    r"D:\aaProjectsStuff\Amicus\Dashboard\dash_board\mega_case.csv")
# print(df.head())


# -------------------------------------Functions-------------------------------------
def get_xy_from_count():
    rc_count = df['respondent_counsel'].value_counts()

    rc_df = pd.DataFrame(rc_count)

    rc_df_subset = rc_df[:10]

    rc_counts_indices = rc_df_subset.index.tolist()
    rc_counts_values = rc_df_subset.values.tolist()

    return rc_counts_indices, rc_counts_values


def print_details(n_clicks='', dropdown_value='', range_slider_value='', check_list_value='', radio_items_value=''):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure


# -------------------------------------Graphs(Processing)-------------------------------------
# Donut Graph
jd_count = pd.DataFrame(df['judgement'].value_counts())
jd_unique = df['judgement'].unique()
jd_unique[-1] = 'NA'

jd_count.reset_index(inplace=True)
jd_count.columns = ['Judgement', 'No. of Cases']


# Tables Data Prep

appellant_df = pd.DataFrame(df.loc[5000:5050, ['appellant']])
respondent_df = pd.DataFrame(df.loc[5000:5050, ['respondent']])

app_counsel_df = pd.DataFrame(df.loc[5000:5050, ['appellant_counsel']])
resp_counsel_df = pd.DataFrame(df.loc[5000:5050, ['respondent_counsel']])

# TODO: Change to data indicing rather than df duplication, delete appellant_df, respondent_df, etc. and replace with df['appellant']
# directly once scrolling issues are sorted out

# -------------------------------------Layout-------------------------------------
controls = dbc.FormGroup(
    [
        html.P('Range Slider', style={
            'textAlign': 'center'
        }),
        dcc.RangeSlider(
            id='date-range-slider',
            min=2016,
            max=2021,
            step=1,
            marks={2015: '2015', 2017: '2017',  2020: '2020'},
            value=[2015, 2020]
        ),
        # html.Br(),

        html.P('Appellant Search',
               style={
                   'textAlign': 'center'
               }),
        dbc.InputGroup([

            dbc.InputGroupAddon(
                dbc.Button("Search", id="appellant-search-button")
            ),
            dbc.Input(
                id='appellant-search',
                placeholder='Search for Appellant...'),
        ]
        ),

        html.P('Respondent Search',
               style={
                   'textAlign': 'center'
               }),
        dbc.InputGroup([

            dbc.InputGroupAddon(
                dbc.Button("Search", id="respondent-search-button")
            ),
            dbc.Input(
                id='respondent-search',
                placeholder='Search for respondent...'),
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
            value=jd_unique.tolist()[:-1],
            multi=True
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
        #     appellant_df, striped=True, bordered=True, hover=True, responsive='sm'),

        dt.DataTable(
            id='appellant-table',
            columns=[{"name": i, "id": i} for i in appellant_df.columns],
            data=appellant_df.to_dict('records'),
            page_action='none',
            fixed_rows={'headers': True},

            style_as_list_view=True,
            style_table={'height': '20em', 'overflow': 'hidden'}
        ),
        md=4
    ),
    dbc.Col(
        # dbc.Table.from_dataframe(
        #     appellant_df, striped=True, bordered=True, hover=True, responsive='sm'),

        dt.DataTable(
            id='respondent-table',
            columns=[{"name": i, "id": i} for i in respondent_df.columns],
            data=respondent_df.to_dict('records'),
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
            dcc.Graph(id='graph_1'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_2'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_3'), md=4
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_4'), md=12,
        )
    ]
)

content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_5'), md=6
        ),
        dbc.Col(
            dcc.Graph(id='graph_6'), md=6
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


app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY, 'dash_board\app.css'])
app.layout = html.Div([sidebar, content])

# -------------------------------------Callbacks-------------------------------------


@app.callback(
    Output('graph_1', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('date-range-slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_bottom(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print_details(n_clicks, dropdown_value, range_slider_value,
                  check_list_value, radio_items_value)
    fig = {
        'data': [{
            'x': [1, 2, 3],
            'y': [3, 4, 5]
        }]
    }
    return fig


@app.callback(
    Output('donut-graph', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('judgement-dropdown', 'value'), State('date-range-slider', 'value')])
def update_graph_donut(n_clicks, dropdown_value, range_slider_value):
    fig_donut = px.pie(data_frame=jd_count.loc[jd_count['Judgement'].isin(dropdown_value)], values='No. of Cases',
                       hover_name='Judgement', hole=0.6)

    # fig_donut.update_layout(transition_duration=250)

    return fig_donut


@app.callback(
    Output('graph_3', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('date-range-slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_3(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print_details(n_clicks, dropdown_value, range_slider_value,
                  check_list_value, radio_items_value)

    df = px.data.iris()
    fig = px.density_contour(df, x='sepal_width', y='sepal_length')
    return fig


@app.callback(
    Output('graph_4', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('date-range-slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print_details(n_clicks, dropdown_value, range_slider_value,
                  check_list_value, radio_items_value)

    df = px.data.gapminder().query('year==2007')
    fig = px.scatter_geo(df, locations='iso_alpha', color='continent',
                         hover_name='country', size='pop', projection='natural earth')
    fig.update_layout({
        'height': 600
    })
    return fig


@app.callback(
    Output('graph_5', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_5(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print_details(n_clicks, dropdown_value, range_slider_value,
                  check_list_value, radio_items_value)

    fig = px.scatter(df, x='sepal_width', y='sepal_length')
    return fig


@app.callback(
    Output('graph_6', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('date-range-slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_6(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print_details(n_clicks, dropdown_value, range_slider_value,
                  check_list_value, radio_items_value)

    df = px.data.tips()
    fig = px.bar(df, x='total_bill', y='day', orientation='h')
    return fig


@app.callback(
    Output('card_title_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('date-range-slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print_details(n_clicks, dropdown_value, range_slider_value,
                  check_list_value, radio_items_value)
    return 'Card Tile 1 change by call back = {}'.format(dropdown_value)


@app.callback(
    Output('card_text_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('date-range-slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    return 'Card text change by call back'


@app.callback(
    Output("appellant-table", "data"),
    [Input("appellant-search-button", "n_clicks")],
    [State("appellant-search", 'value')],
)
def on_search_click_app(n_clicks, search_value):

    search_values = []
    search_values.extend([
        search_value, search_value.lower(), search_value.upper()])

    if n_clicks:
        if (search_value != None or search_value != '' or search_value != ' '):
            return appellant_df[appellant_df['appellant'].str.contains(
                '|'.join(search_values))].to_dict('records')
            # return appellant_df[appellant_df['appellant'].str.contains(
            #     (search_value))].to_dict('records')

    else:
        return appellant_df.to_dict('records')


@app.callback(
    Output("respondent-table", "data"),
    [Input("respondent-search-button", "n_clicks")],
    [State("respondent-search", 'value')],
)
def on_search_click_resp(n_clicks, search_value):

    search_values = []
    search_values.extend([
        search_value, search_value.lower(), search_value.upper()])
    if n_clicks:
        if (search_value != None or search_value != '' or search_value != ' '):
            return respondent_df[respondent_df['respondent'].str.contains(
                '|'.join(search_values))].to_dict('records')

    else:
        return respondent_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(port='8085', debug=True)
