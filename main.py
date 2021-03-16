import re

import pandas as pd


def get_key(data: object) -> list:
    title_list = data["Title"].to_list()
    result_list = []
    for i in title_list:
        if isinstance(i, float):
            result_list.append("NAN")
        else:
            result_list.append((re.sub("[^А-Яа-яA-Za-z0-9]", "", i)).upper())
    return result_list


def get_even(list_data: list) -> list:
    result_list = []
    for i in range(len(list_data)):
        if i % 2 != 0:
            result_list.append(list_data[i])
    return result_list


def filter_and_key_scopus(data: object) -> object:
    data = data.filter(["Authors", "Title", "Source title",  "Year"])
    data.rename(columns={"Source title": "Source Title"}, inplace=True)
    data["KEY"] = get_key(data)
    return data


def filter_and_key_wos(data: object) -> object:
    data = data.filter(["Authors", "Article Title", "Source Title", "Publication Date", "Publication Year"])
    data.rename(columns={"Article Title": "Title", "Publication Year": "Year"}, inplace=True)
    data["KEY"] = get_key(data)
    return data


def main():
    data_df = pd.read_excel("data.xlsx")
    wos_data_df = filter_and_key_wos(pd.read_excel("WoS2020.xlsx"))
    scopus_data_df = filter_and_key_scopus(pd.read_csv("scopus2020.csv"))
    date_list = data_df["Дата создания"]
    name_list = data_df["Наименование"]
    name_book_list = data_df["Название журнала"]
    prepared_list = data_df["Подготовил"]
    signed_list = data_df["Подписан ЭП"]

    date_list = get_even(date_list)
    name_list = get_even(name_list)
    name_book_list = get_even(name_book_list)
    prepared_list = get_even(prepared_list)
    signed_list = get_even(signed_list)

    scopus_and_wos_data = pd.concat([scopus_data_df, wos_data_df])
    scopus_and_wos_data.drop_duplicates(subset=["KEY"], inplace=True)

    result_df = pd.DataFrame(
        {"Date": date_list, "Title": name_list, "Source Title": name_book_list, "Подготовил": prepared_list,
         "Подписан": signed_list})
    result_df["KEY"] = get_key(result_df)
    result_df = pd.merge(left=result_df, right=scopus_and_wos_data, left_on="KEY", right_on="KEY")
    result_df.rename(columns={"Title_x": "Title", "Source Title_x": "Source Title"}, inplace=True)
    result_df.drop(["Title_y", "Source Title_y"], axis=1, inplace=True)
    result_df.to_excel("result.xlsx", index=False)



