import dash
import pandas as pd
from dash import Input, Output, html, dcc, dash_table, callback, State
import sqlite3
import datetime
from choose_dropdown import define_dropdown_list

external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css']

write_db = False
time = ''
protect_from_fools = [0] * 13

choice_of_dropdown = pd.read_csv('create_eq/area_type_model.csv', encoding='cp1251', sep=";", header=None)
choice_of_dropdown.columns = ['area','type', 'detail']
detail_output = pd.read_csv('create_eq/details.csv', encoding='cp1251',sep=";", header=None)
detail_output.columns = ['detail', 'mech_part']

repair_layout = html.Div([
    html.Div([
        html.Div([], id='check_in_db', className='title_', style={'height':'25px'}),
        html.Div([
            html.Div([dcc.DatePickerSingle(id='date', placeholder='Дата', display_format='DD/MM/YYYY')], className='mill', style={'width':'10%', 'text-align':'justify '}),
            html.Div([
                dcc.Dropdown([f"Смена {i}" for i in range(1, 4)], placeholder="Смена",
                             id='dropdown_shift', clearable=False)], className='mill', style={'width':'10%'}),
            html.Div([
                dcc.Dropdown(choice_of_dropdown.iloc[:, 0].unique(), id='dropdown_area',
                             placeholder="Выберите участок", clearable=True)],
                className='mill'),
            html.Div([
                dcc.Dropdown(choice_of_dropdown.iloc[:, 1].unique(), id='dropdown_type_eq',
                             placeholder="Выберите тип оборудования", clearable=True)],
                className='mill'),
            html.Div([
                dcc.Dropdown(choice_of_dropdown.iloc[:, 2], id='dropdown_eq',
                             placeholder="Выберите оборудование", clearable=True)],
                className='mill'),
            # html.Div([
            #     dcc.Dropdown([f"{i} ч" for i in range(1, 12)], placeholder="Время ремонта", id='dropdown_time',
            #                  clearable=False)], className='mill'),
            # html.Div([
            #     dcc.Dropdown([f"{i} мин" for i in range(0, 61, 15)], placeholder="Время ремонта, мин", id='dropdown_time_min',
            #                  clearable=False)], className='mill'),
        ], className='form_1'),
        html.Div([
            html.Div([
                dcc.Dropdown(['Не выбрано оборудование'], placeholder="Выберите деталь",
                             id='dropdown_detail', clearable=False)], className='mill4', style={'width':'24.67%'}),
            html.Div([
                dcc.Input(id="input_brand", type='text', placeholder="Бренд")
            ], className='mill4', style={'width':'16.33%'}),
            html.Div([
                dcc.Input(id="input_amount", type='number', placeholder="Количество", min=0)
            ], className='mill4', style={'width':'10%'}),
            html.Div([
                dcc.Dropdown(['Штука', 'Комплект', 'Литр'], placeholder="Единица измерений",
                             id='dropdown_um', clearable=False)
            ], className='mill4', style={'width':'15%'}),
            html.Div([
                dcc.Dropdown(['Плановый', 'Внеплановый', 'Аварийный'], placeholder="Вид ремонта",
                             id='dropdown_type', clearable=False)], className='mill4', style={'width':'11%'}),
            html.Div([
                dcc.Input(id="input_time", type='number', placeholder="Время простоя (часы)", min = 0 )
            ], className='mill4', style={'width':'16%'}),
        ], className='form_1'),
        html.Div([
            html.Div([dcc.Textarea(placeholder='Примечание по простоям', id='comment_1')], className='comment'),
            html.Div([dcc.Textarea(placeholder='Прочее', id='comment_2')], className='another'),
        ], className='form_2'),
        # html.Div([
        #     html.Button('Записать данные', id='write', className='button', n_clicks=0),
        #
        # ], className='form_3'),
        html.Div([
            html.Div([html.Button('Записать данные', id='write', className='button_2', n_clicks=0)],
                     className='form_5'),
            html.Div([html.Button('Очистить все поля', id='refresh', className='button_3', n_clicks=0)],
                     className='form_6')
        ], className='form_1', style={'margin-top':'20px'}),
        # html.Div([
        #     html.Div([html.Button('Добавить', id='add_button', className='button_1', n_clicks=0),], className='div_button'),
        #     html.Div([html.Button('Удалить', id='delete_button', className='button_2', n_clicks=0),], className='div_button'),
        # ], className='form_4'),
    ], className='main', id=f'div-0', style={'height':'272px'}),
    # html.Div([
    #     #html.Div([], id='check_in_db', className='title_'),
    #     html.Div(dash_table.DataTable(
    #         id='table',
    #         style_table={
    #             'height': '70px', 'margin-left': '1%',
    #             "width": "98%"},
    #         style_header={"text-align": "center", "background": '#7571f9', 'color': 'white',
    #                       'font-family': 'var(--bs-body-font-family)'},
    #         style_data={"text-align": "center"},
    #     ), style={'margin-left': "0px", 'height':'80px'}),
    #     html.Div([
    #         html.Div([html.Button('Очистить все поля', id='refresh', className='button_2', n_clicks=0)],
    #                  className='form_5'),
    #         html.Div([html.Button('Удалить текущую запись', id='delete', className='button_3', n_clicks=0)],
    #                  className='form_6')
    #     ], className='form_1'),
    # ], className='aux_main', style={"height": "180px"}),

    html.Div([
        html.Div("ПОСЛЕДНИЕ 10 ЗАПИСЕЙ В БД (изменения можете вносить в столбцы: Смена, Количество, Вид ремонта, Время, Примечание, Прочее)", id='records_from_db', className='title_'),
        html.Div([
            #dcc.Interval(id='interval_pg', interval=20000000, n_intervals=0),
            dash_table.DataTable(
            id='records_from_db_table',
            # dropdown = {
            #         'shift': {
            #             'options': [
            #                 {'label': i, 'value': i}
            #                 for i in ['Смена 1', 'Смена 2', 'Смена 3']
            #             ]
            #         },
            #         'type_of_repair': {
            #             'options': [
            #                 {'label': i, 'value': i}
            #                 for i in ['Плановый', 'Внеплановый', 'Аварийный']
            #             ]
            #         }
            #     },
            row_deletable=True,
            style_table={
                'overflowX': 'auto', 'margin-left': '1%',
                "width": "98%"},
            style_header={"text-align": "center", "background": '#7571f9', 'color': 'white',
                          'font-family': 'var(--bs-body-font-family)'},
            style_data={"text-align": "center"},
        )], style={'margin-left': "0px"}),

        html.Div([html.Button('Применить изменения', id='refresh_db', className='button', style={'margin-top':'20px', 'width':'98%', 'margin-left':'1%'}, n_clicks=0)], className='form_3', style={'height':'77px'}),
    ], className='aux_main', ),
    html.Div(style={'height':'40px'})
    ])
def define_area_type_eq(area_, type_, eq):
    if area_ == None:
        area = choice_of_dropdown.query("detail == @eq")['area'].iloc[0]
    else:
        area = area_
    if type_ == None:
        type_eq = choice_of_dropdown.query("detail == @eq")['type'].iloc[0]
    else:
        type_eq = type_
    return area, type_eq

saved_id = []
def open_db_for_show():
    connection = sqlite3.connect(f'Data_Bases/info_mechanic.db')
    query = f'SELECT * FROM info_mechanic ORDER BY id DESC LIMIT 10'
    df = pd.read_sql(query, con=connection)
    connection.close()
    #df.drop('id', axis = 1, inplace=True)
    russian_columns_name =['id', 'Дата', 'Смена', 'Оборудование', 'Деталь', 'Количество', 'Вид ремонта', 'Время', 'Примечание', 'Прочее']
    df.drop(['time','area','type_eq', 'brand', 'unit_meas'], axis=1, inplace=True)
    columns = [
        {
        'name': str(y),
        'id': str(x),
        'editable': True,
        'presentation': 'dropdown',
        } if y == 'Количество' or y == 'Время' or y == 'Примечание' or y == 'Прочее' or y == 'Смена' or 'Вид ремонта'
        else
        {
            'name': str(y),
            'id': str(x),
        }
        for x,y in zip(df.columns, russian_columns_name)]
    #add editable columns (5-Количество, 7 - Время, 8 - Примечание, 9 - Прочее)
    # edit_col_num = [5,7,8,9]
    # for item in edit_col_num:
    #     columns[item]['editable'] = True
    return columns, df

# @callback(
#           Output('records_from_db_table', 'columns'),
#           Output('records_from_db_table', 'data'),
#
#           #Input('interval_pg', 'n_intervals'),
#           Input('refresh_db', 'n_clicks'),
#           State("records_from_db_table", "data"),
#          )
# def show_db(n_intervals, n_clicks, data):
#     global saved_id
#     columns, df = open_db_for_show()
#     triggered_button = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
#     saved_id = list(df['id'])
#     #df.drop('id', axis=1, inplace=True)
#     if triggered_button == "refresh_db":
#         deleted_rows = list(set(saved_id)-set([(id['id']) for id in data]))
#         connection = sqlite3.connect(f'Data_Bases/info_mechanic.db')
#         cursor = connection.cursor()
#         sql = f"DELETE FROM info_mechanic WHERE id IN ({','.join(map(str, deleted_rows))});"
#         cursor.execute(sql)
#         connection.commit()
#         cursor.close()
#         connection.close()
#         columns, df = open_db_for_show()
#
#     return columns, df.to_dict('records')
_, init_df_date = open_db_for_show()


@callback(
    #Output('table', 'columns'),
    #Output('table', 'data'),
    Output('check_in_db', 'children'),
    Output('write', 'className'),
    Output('refresh', 'className'),
    #Output('delete', 'className'),
    Output('date', 'date'),
    Output('dropdown_shift', 'value'),
    Output('dropdown_area', 'value'),
    Output('dropdown_type_eq', 'value'),
    Output('dropdown_eq', 'value'),
    Output('dropdown_detail', 'value'),
    Output('input_brand', 'value'),
    Output('input_amount', 'value'),
    Output('dropdown_um', 'value'),
    Output('dropdown_type', 'value'),
    Output('input_time', 'value'),
    Output('comment_1', 'value'),
    Output('comment_2', 'value'),
    Output('dropdown_detail', 'options'),
    Output('dropdown_area', 'options'),
    Output('dropdown_type_eq', 'options'),
    Output('dropdown_eq', 'options'),
    Output('records_from_db_table', 'columns'),
    Output('records_from_db_table', 'data'),
    Output('records_from_db_table', 'dropdown'),

    Input('date', 'date'),
    Input('dropdown_shift', 'value'),
    Input('dropdown_area', 'value'),
    Input('dropdown_type_eq', 'value'),
    Input('dropdown_eq', 'value'),
    Input('dropdown_detail', 'value'),
    Input('input_brand', 'value'),
    Input('input_amount', 'value'),
    Input('dropdown_um', 'value'),
    Input('dropdown_type', 'value'),
    Input('input_time', 'value'),
    Input('comment_1', 'value'),
    Input('comment_2', 'value'),
    Input('write', 'n_clicks'),
    #Input('delete', 'n_clicks'),
    Input('refresh', 'n_clicks'),
    Input('refresh_db', 'n_clicks'),
    State("records_from_db_table", "data"),
)
def display_output(*values):
    global write_db
    global time
    global protect_from_fools

    variable_ = -6

    #values_tables = values[:11]
    triggered_button = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    #Display a working buttons
    if not None in values[:2] + values[4:variable_]:
        message = 'ЗАПОЛНИЛИ ВСЮ ИНФОМРАЦИЮ МОЖЕТЕ НАЖАТЬ НА КНОПКУ "Записать данные"'
        hidden_1 = 'button'
        #hidden_3 = 'button_hidden_3'
    else:
        message = 'ЗАПОЛНИЛИ НЕ ВСЕ ПОЛЯ С ИНФОРМАЦИЕЙ'
        hidden_1 = 'button_hidden'
        #hidden_3 = 'button_hidden_3'

    if all(element == values[0] for element in values[:-4]):
        hidden_2 = 'button_hidden_2'
    else:
        hidden_2 = 'button_2'


    if triggered_button == 'write':
        if not None in values[:2] + values[4:variable_]:
            area, type_eq = define_area_type_eq(values[2], values[3], values[4])
            if protect_from_fools[:1] + protect_from_fools[4:13] != list(values[:1] + values[4:13]) or area != protect_from_fools[2] or type_eq != protect_from_fools[3]:
            #if protect_from_fools != list(values[:13]):
                current_datetime = datetime.datetime.now()
                time = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                connection = sqlite3.connect(f'Data_Bases/info_mechanic.db')  # need change directory
                cursor = connection.cursor()
                #area, type_eq = define_area_type_eq(values[2], values[3], values[4])
                sql = """
                      INSERT INTO info_mechanic (time, date, shift, area, type_eq, equipment, detail, 
                      brand, amount, unit_meas, type_of_repair, repair_time, comment_1, comment_2)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                      """
                cursor.execute(sql,
                               (time, values[0], values[1], area,
                                type_eq, values[4], values[5],
                                values[6], values[7], values[8],
                                values[9], values[10],values[11], values[12]))
                connection.commit()
                connection.close()
                message = 'ИНФОРМАЦИЯ ЗАПИСАНА В БАЗУ ДАННЫХ'
                #hidden_3 = 'button_3'
                protect_from_fools = [values[0], values[1], area,
                                      type_eq, values[4], values[5],
                                      values[6], values[7], values[8],
                                      values[9], values[10], values[11], values[12]
                                      ]
                write_db = True


            else:
                message = 'ПОВТОР'
                #hidden_3 = 'button_3'
        else:
            message = 'ВЫБРАНЫ НЕ ВСЕ ПОЛЯ'
            hidden_2 = 'button_hidden_2'
            #hidden_3 = 'button_hidden_3'



    if triggered_button == 'refresh':
        message = 'ВСЕ ПОЛЯ ОЧИЩЕНЫ'
        #values_tables = [None] * 11
        values= [None] * 13
        values[6], values[11], values[12] = '', '', ''
        hidden_1 = 'button_hidden'
        hidden_2 = 'button_hidden_2'
        #hidden_3 = 'button_hidden_3'
        write_db = False

    #work of button which refresh a table from data base
    global saved_id
    columns, df = open_db_for_show()
    saved_id = list(df['id'])
    data = values[-1]
    if triggered_button == "refresh_db":
        deleted_rows = list(set(saved_id)-set([(id['id']) for id in data]))
        connection = sqlite3.connect(f'Data_Bases/info_mechanic.db')
        cursor = connection.cursor()
        sql = f"DELETE FROM info_mechanic WHERE id IN ({','.join(map(str, deleted_rows))});"
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()

        #update a database
        df1 = pd.DataFrame(df)
        df2 = pd.DataFrame(data)
        diff_df = pd.concat([df1, df2]).drop_duplicates(keep=False)
        df_update = diff_df[int(len(diff_df)/2):][['id', 'amount', 'repair_time', 'shift', 'type_of_repair', 'comment_1', 'comment_2']]
        connection = sqlite3.connect(f'Data_Bases/info_mechanic.db')
        cursor = connection.cursor()
        for index, row in df_update.iterrows():
            update_query = '''
                UPDATE info_mechanic
                SET shift = ?, type_of_repair = ?, amount = ?,  repair_time = ?, comment_1 = ?, comment_2 = ?  
                WHERE id = ?; 
                '''
            values_ = (row['shift'], row['type_of_repair'], row['amount'], row['repair_time'], row['comment_1'], row['comment_2'], row['id'])
            cursor.execute(update_query, values_)
        connection.commit()
        cursor.close()
        connection.close()

        columns, df = open_db_for_show()




    dropdown_type_area, dropdown_type_eq, dropdown_eq = define_dropdown_list(values[2:4], choice_of_dropdown)

    if values[4] != None:
        mask = detail_output['detail'].apply(lambda x: True if values[4] in x else False)
        detail_output_mech_part = detail_output[mask]['mech_part']
    else:
        detail_output_mech_part = ['Не выбрано оборудование']

    dropdown = {
        'shift': {
            'options': [
                {'label': i, 'value': i}
                for i in ['Смена 1', 'Смена 2', 'Смена 3']
            ]
        },
        'type_of_repair': {
            'options': [
                {'label': i, 'value': i}
                for i in ['Плановый', 'Внеплановый', 'Аварийный']
            ]
        }
    }

    return message, hidden_1, hidden_2, *values[:13], detail_output_mech_part, dropdown_type_area, dropdown_type_eq, dropdown_eq, columns, df.to_dict('records'), dropdown
