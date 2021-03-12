import numpy as np
import pandas as pd
import datetime as dt
import time
from dateutil.relativedelta import relativedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv(
    r"D:\aaProjectsStuff\Amicus\Dashboard\dash_board\mega_case.csv")
# print(df.head())


def get_xy_from_count():
    rc_count = df['respondent_counsel'].value_counts()

    rc_df = pd.DataFrame(rc_count)

    rc_df_subset = rc_df[:10]

    rc_counts_indices = rc_df_subset.index.tolist()
    rc_counts_values = rc_df_subset.values.tolist()

    return rc_counts_indices, rc_counts_values


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


def generate_input_box(type):

    return dcc.Input(
        id="{}_input".format(type),
        type="search",
        placeholder="Search for {}".format(type),
    ),


# Returning years in datetime format from df['date']


def date_conversion_first(df):
    years = df['date'].unique()
    years = np.delete(years, 0)

    years_list = []
    valueErrorCounter = 0
    typeErrorCounter = 0

    for year in years:
        try:
            # print(type(year))
            years_list.append(dt.datetime.strptime(year, '%B %d, %Y').date())

        except ValueError as e:
            valueErrorCounter += 1
            continue
        except TypeError as t:
            typeErrorCounter += 1
            continue

    return years_list


# TIME STUFF
epoch = dt.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):

    return (dt - epoch).total_seconds()  # * 1000.0


daterange = pd.date_range(start='1930', end='2021', freq='AS')

# def unixTimeMillis(dt):
#     ''' Convert datetime to unix timestamp '''
#     return int(time.mktime(dt.timetuple()))


# def unixToDatetime(unix):
#     ''' Convert unix timestamp to datetime. '''
#     return pd.to_datetime(unix, unit='s')


# def getMarks(daterange, start, end, Nth=100):
#     ''' Returns the marks for labeling.
#         Every Nth value will be used.
#     '''

#     result = {}
#     for i, date in enumerate(daterange):
#         if(i % Nth == 1):
#             # Append value to dict
#             result[unixTimeMillis(date)] = str(date.strftime('%Y-%m-%d'))

#     return result


def get_year_marks(start, end, inter=1):
    ''' Returns the marks for labeling.
        Interval for years to leave in between
    '''

    result = {}
    for i, date in enumerate(range(start, end, inter)):
        result[i] = str(date)

    return result


mark_test = get_year_marks(1930, 2021, inter=20)
print(mark_test)


# -------------------------------------DASH APP STARTS-------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

rc_counts_indices, rc_counts_values = get_xy_from_count()
print(len(rc_counts_indices), len(rc_counts_values))

# fig = px.bar(x=rc_counts_values, y=rc_counts_indices,
#              color="judgement")


# -------------------------------------Date Cleaning-------------------------------------
years_list = date_conversion_first(df)

# -------------------------------------Graphs-------------------------------------
# Donut Graph
jd_count = pd.DataFrame(df['judgement'].value_counts())
jd_unique = df['judgement'].unique()
jd_unique[-1] = 'NA'

jd_count.reset_index(inplace=True)
jd_count.columns = ['Judgement', 'No. of Cases']


# Input Boxes
input_types = ['appellant', 'respondent',
               'appellant_counsel', 'respondent_counsel']
input_boxes = []

for type in input_types:
    input_boxes.append(generate_input_box(type))


# Table_1 Data Prep
t1_df = pd.DataFrame(df.loc[5000:5020, ['respondent', 'appellant']])


# ----------------------------LAYOUT------------------------------
app.layout = html.Div([
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i}
                         for i in jd_unique],
                value=jd_unique.tolist()[:-1],
                multi=True
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i}
                         for i in jd_unique],
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    ]),

    html.Div([

        html.Div([
            dcc.Graph(
                id='donut-graph',
                # figure=fig_donut,
            ),

        ],
            style={'width': '48%', 'display': 'inline-block', 'float': 'left'}),

        html.Div([
            html.H3(
                children="Table 1"
            ),
            generate_table(t1_df)
        ],
            style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
    ]),

    # dcc.Slider(
    #     id='year--slider',
    #     min=np.min(years_list),
    #     max=np.max(years_list),
    #     value=years_list[0],
    #     marks={str(year): str(year) for year in years_list},
    #     step=None
    # )

    # dcc.RangeSlider(
    #     id='datetime_RangeSlider',
    #     updatemode='mouseup',  # don't let it update till mouse released
    #     min=unix_time_millis(dt.datetime.min()),
    #     max=unix_time_millis(dt.datetime.max()),
    #     value=[unix_time_millis(dt.datetime.min()),
    #            unix_time_millis(dt.datetime.max())],
    #     # TODO add markers for key dates
    #     marks=get_marks_from_start_end(dt.datetime.min(),
    #                                    dt.datetime.max()),
    # ),

    # dcc.RangeSlider(
    #     id='year_slider',
    #     min=unixTimeMillis(daterange.min()),
    #     max=unixTimeMillis(daterange.max()),
    #     value=[unixTimeMillis(daterange.min()),
    #            unixTimeMillis(daterange.max())],
    #     marks=getMarks(daterange.min(),
    #                    daterange.max())
    # )

    dcc.RangeSlider(
        id='year-slider',
        min=1930,  # Try changing to dd-mm-yyyy format, use
        max=2021,
        step=20,
        value=[1930, 2021],
        marks=mark_test
    ),

    html.Div(
        id='date_check_div'
    )

])

# Donut Graph


@app.callback(
    Output(component_id='donut-graph', component_property='figure'),
    Input(component_id='xaxis-column', component_property='value')
)
def update_output_donut(input_values):

    fig_donut = px.pie(data_frame=jd_count.loc[jd_count['Judgement'].isin(input_values)], values='No. of Cases',
                       hover_name='Judgement', hole=0.6)
    return fig_donut


# DateRange Slider Date Display
@app.callback(
    Output(component_id='date_check_div', component_property='children'),
    Input('year-slider', 'value')
)
def display_date_from_slider(input_value):
    return f"Current selected date is {input_value}"


if __name__ == '__main__':
    app.run_server(debug=True)
