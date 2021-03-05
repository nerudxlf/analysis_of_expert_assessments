import pandas as pd


def get_even(list_data: list) -> list:
    result_list = []
    for i in range(len(list_data)):
        if i % 2 != 0:
            result_list.append(list_data[i])
    return result_list


def main():
    data_df = pd.read_excel("data.xlsx")
    wos_data_df = pd.read_excel("WoS2020.xlsx")

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

    result_df = pd.DataFrame(
        {"Дата": date_list, "Название": name_list, "Название журнала": name_book_list, "Подготовил": prepared_list,
         "Подписан": signed_list})
    result_df = pd.merge(left=result_df, right=wos_data_df, left_on="Название", right_on="Article Title", how="left")

    result_df.to_excel("result.xlsx", index=False)



