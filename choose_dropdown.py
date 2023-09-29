def define_dropdown_list(values, choice_of_dropdown):
    if values[0] != None:
        dropdown_type_area_reserve = choice_of_dropdown.iloc[:, 0].unique()
        if values[1] != None:
            dropdown_type_eq_reserve = choice_of_dropdown.iloc[:, 1].unique()
            mask = (choice_of_dropdown['area'] == values[0]) & (choice_of_dropdown['type'] == values[1])
            dropdown_eq_reserve = choice_of_dropdown[mask]['detail']
        else:
            mask = choice_of_dropdown['area'] == values[0]
            dropdown_type_eq_reserve = choice_of_dropdown[mask].iloc[:, 1].unique()
            dropdown_eq_reserve = choice_of_dropdown[mask].iloc[:, 2]
    else:
        if values[1] != None:
            dropdown_type_eq_reserve = choice_of_dropdown.iloc[:, 1].unique()
            mask = choice_of_dropdown['type'] == values[1]
            dropdown_eq_reserve = choice_of_dropdown[mask]['detail']
            dropdown_type_area_reserve = choice_of_dropdown[mask]['area'].unique()
        else:
            dropdown_type_area_reserve = choice_of_dropdown.iloc[:, 0].unique()
            dropdown_type_eq_reserve = choice_of_dropdown.iloc[:, 1].unique()
            dropdown_eq_reserve = choice_of_dropdown.iloc[:, 2]
    return dropdown_type_area_reserve, dropdown_type_eq_reserve, dropdown_eq_reserve