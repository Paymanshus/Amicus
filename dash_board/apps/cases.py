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


content_case_row = dbc.Row(
    [
        dbc.Col(
            dt.DataTable(
                id='cases-table',
                columns=[{"name": "Case Files", "id": "CaseFile"}],
                data=df[['CaseFile']][:50].to_dict('records'),
                page_action='none',
                fixed_rows={'headers': True},


                css=[{
                    'selector': '.dash-spreadsheet td div',
                    'rule': '''
                    line-height: 15px;
                    max-height: 60px; min-height: 60px; height: 60px;
                   
                    display: block;
                    overflow-y: auto;
                '''
                }],

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
                },
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                style_cell_conditional=[{'textAlign': 'left'}],
                style_table={'height': '300px', 'overflow': 'hidden'}
            ), md=12
        )
    ], style={'padding': '20px 0px'}
)


# CaseFiles Table
@app.callback(
    Output("cases-table", "data"),
    [Input("keyword-search-button", "n_clicks"),
     #  Input('submit_button', 'n_clicks')
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
