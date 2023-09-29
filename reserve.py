import dash
from dash import Input, Output, State, html, dcc, dash_table, callback
import pandas as pd
import sqlite3
import datetime
from choose_dropdown import define_dropdown_list
import re

choice_of_dropdown = pd.read_csv('create_eq/area_type_model.csv', encoding='cp1251', sep=";", header=None)
choice_of_dropdown.columns = ['area','type', 'detail']
detail_output = pd.read_csv('create_eq/details.csv', encoding='cp1251',sep=";", header=None)
detail_output.columns = ['detail', 'mech_part']



reserve_layout = html.Div([
    html.Div([
        html.Div("Выберите оборудование", className='title_reserve'),
        html.Div([
            html.Div([
                dcc.Dropdown(choice_of_dropdown.iloc[:, 0].unique(), id='dropdown_type_area_reserve',
                             placeholder="Выберите участок", clearable=True)],
                className='mill_reserve'),

            html.Div([
                dcc.Dropdown(choice_of_dropdown.iloc[:, 1].unique(), id='dropdown_type_eq_reserve',
                             placeholder="Выберите тип оборудования", clearable=True)],
                className='mill_reserve'),
            html.Div([
                dcc.Dropdown(choice_of_dropdown.iloc[:, 2], id='dropdown_eq_reserve',
                             placeholder="Выберите оборудование", clearable=True)],
                className='mill_reserve'),
        ]),
    ], className='main', id=f'div-0', style={'height':'115px'}),
    html.Div([
        html.Div("Заполните или обновите таблицу", id='eq_reserve_title', className='title_reserve'),
        dash_table.DataTable(
                    id="table_form_1",
                    data=[],
                    columns=[{"name": "Деталь или узел", "id": "detail"},
                             {"name": "Наличие\nна промплощадке", "id": "reserve_prom_area", 'type': 'numeric'},
                             {"name": "Дата запланированного ремонта", "id": "date_" },

                             ],
                    editable=True,


                    style_table={'margin-left': '1%', "width": "98%"},
                    style_header={"text-align": "center", "background": '#7571f9', 'color': 'white',
                                  'font-family': 'var(--bs-body-font-family)', 'whiteSpace': 'pre-wrap'},
                    style_data={"text-align": "center"},


        ),
        html.Div([
            html.Div([html.Button('Записать данные', id='write_reserve_area', className='button', n_clicks=0)], className='form_3')
        ], style={'height':'75px'}),
        html.Div(id="output-message"),

    ], className='table_info'),

    html.Div([
        html.Div("Заполните или обновите таблицу", id='eq_reserve_title2', className='title_reserve'),
        dash_table.DataTable(
                    id="table_form_2",
                    data=[],
                    columns=[{"name": "Деталь или узел", "id": "detail"},
                             {"name": "Бренд детали", "id": "brand", 'presentation': 'dropdown'},
                             {"name": "Стоимость, AMD", "id": "cost", 'type': 'numeric'},
                             {"name": "Дата, когда изменился бренд или стоимость детали", "id": "date_" },

                             ],
                    editable=True,

                    dropdown={
                        'brand': {
                            'options': [
                                {'label': i, 'value': i}
                                for i in ['Бренд 1', 'Бренд 2', '-']
                            ]
                        },
                    },

                    style_table={'margin-left': '1%', "width": "98%"},
                    style_header={"text-align": "center", "background": '#7571f9', 'color': 'white',
                                  'font-family': 'var(--bs-body-font-family)', 'whiteSpace': 'pre-wrap'},
                    style_data={"text-align": "center"},
        ),
        html.Div([
            html.Div([html.Button('Записать данные', id='write_reserve_brand', className='button', n_clicks=0)], className='form_3')
        ], style={'height':'75px'}),

    ], className='table_info'),


    html.Div([
        html.Div("Заполните или обновите таблицу", id='eq_reserve_title3', className='title_reserve'),
        dash_table.DataTable(
            id="table_form_3",
            data=[],
            columns=[{"name": "Деталь или узел", "id": "detail"},
                     {"name": "Номер заявки", "id": "num_app",},
                     {"name": "Дата заявки", "id": "date_"},

                     ],
            editable=True,
            style_table={'margin-left': '1%', "width": "98%"},
            style_header={"text-align": "center", "background": '#7571f9', 'color': 'white',
                          'font-family': 'var(--bs-body-font-family)', 'whiteSpace': 'pre-wrap'},
            style_data={"text-align": "center"},
        ),
        html.Div([
            html.Div([html.Button('Записать данные', id='write_reserve_app', className='button', n_clicks=0)],
                     className='form_3')
        ], style={'height': '75px'}),

    ], className='table_info'),

    html.Div(style={'height':'40px'}),
    # html.Div([
    #     html.Div("Если нужного бренда нет в таблице,\nто добавьте его", className='brand_title'),
    #     html.Div(dcc.Input(id="input_brand",
    #         type="text",
    #         placeholder="Введите название бренда",
    #         className='input_',
    #     ), className='brand_'),
    #     html.Div(html.Button('Добавить', id='button_brand', n_clicks=0, className='brand_button'), className='brand_'),
    # ],className='table_info',style={'height':'60px'}),
], className="mec")
click_button_write1 = 0
click_button_write2 = 0
click_button_write3 = 0
def read_from_db(name_db, eq):
    con = sqlite3.connect(f"Data_Bases/{name_db}.db")
    cursor = con.cursor()
    sql = f'SELECT * FROM {name_db} WHERE equipment == ?'
    cursor.execute(sql, (eq,))
    df_equipment = cursor.fetchall()
    cursor.close()
    con.close()
    return df_equipment

def init_data_table(type_table):
    if type_table == "industrial_area":
        data = {'detail': ['-'],
                'reserve_prom_area': ['-'],
                'date_': ['ДД.ММ.ГГГГ'],
                }
    elif type_table == "brand":
        data = {'detail': ['-'],
                'brand': ['-'],
                'cost': ['-'],
                'date_': ['ДД.ММ.ГГГГ'],
                }
    else:
        data = {'detail': ['-'],
                'num_app': ['-'],
                'date_': ['ДД.ММ.ГГГГ'],
                }
    df_table = pd.DataFrame(data)
    return df_table

def clean_df(df, columns):
    df_table_dirty = pd.DataFrame(df, columns=columns)
    df_table_dirty['time'] = pd.to_datetime(df_table_dirty['time'],  dayfirst=True)
    df_table = df_table_dirty[df_table_dirty['time'] == df_table_dirty['time'].max()].drop(['id', 'time', 'equipment'],
                                                                                           axis=1)
    return df_table

def empty_df(type_table, eq):
    mask = detail_output['detail'].apply(lambda x: True if eq in x else False)
    detail_output_mech_part = detail_output[mask]['mech_part']
    if type_table == "industrial_area":
        data = {'detail': detail_output_mech_part,
                'reserve_prom_area': [0] * len(detail_output_mech_part),
                'date_': ['ДД.ММ.ГГГГ'] * len(detail_output_mech_part),
                }
    elif type_table == "brand":
        data = {'detail': detail_output_mech_part,
                'brand': ['Бренд 1'] * len(detail_output_mech_part),
                'cost': [0] * len(detail_output_mech_part),
                'date_': ['ДД.ММ.ГГГГ'] * len(detail_output_mech_part),
                }
    else:
        data = {'detail': detail_output_mech_part,
                'num_app': [0] * len(detail_output_mech_part),
                'date_': ['ДД.ММ.ГГГГ'] * len(detail_output_mech_part),
                }
    return pd.DataFrame(data)

def output_title(eq, table, name_button):

    global click_button_write1
    global click_button_write2
    global click_button_write3

    if eq != None:
        date_pattern = r'^(0[1-9]|[1-2]\d|3[01])\.(0[1-9]|1[0-2])\.\d{4}$'
        df_table = pd.DataFrame(table)
        if df_table[df_table['date_'] != 'ДД.ММ.ГГГГ']['date_'].str.match(date_pattern).eq(False).sum() > 0:
            title = 'Ошибка в формате данных'

        else:
            if (df_table.eq(0).sum().sum() > 0 and click_button_write1 == 0) or (df_table.eq(0).sum().sum() > 0 and click_button_write2 == 0) or (df_table.eq(0).sum().sum() > 0 and click_button_write3 == 0):
                click_button_write1 = 1
                click_button_write2 = 1
                click_button_write3 = 1
                title = 'В таблице содержатся нулевые значения. Если вы хотите все равно записать информацию в БД' \
                        ' нажмите еще раз на кнопку "Записать данные"'
            else:
                click_button_write1 = 0
                click_button_write2 = 0
                click_button_write3 = 0
                current_datetime = datetime.datetime.now()
                time = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                if name_button == 'warehouse':
                    connection = sqlite3.connect(f'Data_Bases/warehouse.db')  # need change directory
                    cursor = connection.cursor()
                    for item in df_table.index:
                        sql = """
                              INSERT INTO warehouse (equipment, detail, industrial_place, date, time)
                              VALUES (?, ?, ?, ?, ?)
                              """
                        cursor.execute(sql,
                                       (eq, df_table['detail'].iloc[item], int(df_table['reserve_prom_area'].iloc[item]),
                                        df_table['date_'].iloc[item], time))
                    connection.commit()
                    connection.close()
                elif name_button == 'brand_cost':
                    connection = sqlite3.connect(f'Data_Bases/brand_cost.db')  # need change directory
                    cursor = connection.cursor()
                    for item in df_table.index:
                        sql = """
                              INSERT INTO brand_cost (equipment, detail, brand, cost, date, time)
                              VALUES (?, ?, ?, ?, ?, ?)
                              """
                        cursor.execute(sql,
                                       (eq, df_table['detail'].iloc[item], df_table['brand'].iloc[item], float(df_table['cost'].iloc[item]),
                                        df_table['date_'].iloc[item], time))
                    connection.commit()
                    connection.close()
                else:
                    connection = sqlite3.connect(f'Data_Bases/applications.db')  # need change directory
                    cursor = connection.cursor()
                    for item in df_table.index:
                        sql = """
                              INSERT INTO applications (equipment, detail, num_app, date, time)
                              VALUES (?, ?, ?, ?, ?)
                              """
                        cursor.execute(sql,
                                       (eq, df_table['detail'].iloc[item], df_table['num_app'].iloc[item],
                                        df_table['date_'].iloc[item], time))
                    connection.commit()
                    connection.close()
                title = 'Данные успешно записы в БД'

    else:
        title = 'Выберете оборудование'

    return title, pd.DataFrame(table)


@callback(
    Output("table_form_1", "data"),
    Output("dropdown_type_eq_reserve", "options"),
    Output("dropdown_eq_reserve", "options"),
    Output("dropdown_type_area_reserve", "options"),
    Output('eq_reserve_title','children'),
    Output("table_form_2", "data"),
    Output('eq_reserve_title2','children'),
    Output("table_form_3", "data"),
    Output('eq_reserve_title3', 'children'),


    Input("write_reserve_area", "n_clicks"),
    Input('dropdown_type_area_reserve', 'value'),
    Input('dropdown_type_eq_reserve', 'value'),
    Input('dropdown_eq_reserve', 'value'),
    Input("write_reserve_brand", "n_clicks"),
    State("table_form_1", "data"),
    State("table_form_2", "data"),
    State("table_form_3", "data"),
    Input("write_reserve_app", "n_clicks"),

)
def save_data(*values):
    dropdown_type_area_reserve, dropdown_type_eq_reserve, dropdown_eq_reserve = define_dropdown_list(values[1:3], choice_of_dropdown)
    if values[3] != None:
        df_warehouse = read_from_db('warehouse', values[3])
        df_brand_cost = read_from_db('brand_cost', values[3])
        df_applications = read_from_db('applications', values[3])

        if len(df_warehouse) > 0:
            columns = ['id', 'equipment', 'detail', 'reserve_prom_area', 'date_', 'time']
            df_table = clean_df(df_warehouse, columns)
        else:
            df_table = empty_df('industrial_area', values[3])

        if len(df_brand_cost) > 0:
            columns2 = ['id', 'equipment', 'detail', 'brand', 'cost', 'date_', 'time']
            df_table2 = clean_df(df_brand_cost, columns2)
        else:
            df_table2 = empty_df('brand', values[3])

        if len(df_applications) > 0:
            columns = ['id', 'equipment', 'detail', 'num_app', 'date_', 'time']
            df_table3 = clean_df(df_applications, columns)
        else:
            df_table3 = empty_df('app', values[3])

    else:
        #table_form = [{'detail': '-', 'reserve_prom_area': '-', 'detail_of_': 'A', 'cost_':'-', 'date_':'ДД.ММ.ГГГГ' }]
        df_table = init_data_table('industrial_area')
        df_table2 = init_data_table('brand')
        df_table3 = init_data_table('app')



    triggered_button = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_button == 'write_reserve_area':
        title, df_table = output_title(values[3], values[5], 'warehouse')
        df_table2 = pd.DataFrame(values[6])
        df_table3 = pd.DataFrame(values[7])
    else:
        title = 'Заполните или обновите таблицу'

    if triggered_button == 'write_reserve_brand':
        title2, df_table2 = output_title(values[3], values[6], 'brand_cost')
        df_table = pd.DataFrame(values[5])
        df_table3 = pd.DataFrame(values[7])
    else:
        title2 = 'Заполните или обновите таблицу'

    if triggered_button == 'write_reserve_app':
        title3, df_table3 = output_title(values[3], values[7], 'applications')
        df_table = pd.DataFrame(values[5])
        df_table2 = pd.DataFrame(values[6])
    else:
        title3 = 'Заполните или обновите таблицу'

    return df_table.to_dict('records'), dropdown_type_eq_reserve, dropdown_eq_reserve, dropdown_type_area_reserve, title, df_table2.to_dict('records'), title2, df_table3.to_dict('records'), title3
