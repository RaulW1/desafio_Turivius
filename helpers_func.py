from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


def format_table(df: pd.DataFrame):
    """
    format table and its contents for saving
    :param df: pandas DataFrame with table content
    :return: formatted DataFrame
    """
    df.dropna(axis=0, inplace=True, ignore_index=True)
    df.drop(labels=[6, 7], axis=1, inplace=True)
    # df.reset_index(inplace=True)
    df[0] = [doc.split("\n")[2].replace("  ", "") for doc in df[0]]
    df[1] = [num_proc.split("\n")[0].replace("/", "") for num_proc in df[1]]
    df["partes"] = df[[3, 4]].values.tolist()
    df.drop(labels=[3, 4], axis=1, inplace=True)

    return df


def extract_table_content(target_url: str):
    """
    extract data from all tables inside the page
    :param target_url: url of the page containing the table
    :return: Pandas DataFrame containing the table`s contents
    """
    page = requests.get(target_url)

    soup = bs(page.content, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")
    table_data = []
    for row in rows:
        row_data = row.find_all("td")
        data = [d.text for d in row_data]
        table_data.append(data)

    df_table = pd.DataFrame(table_data)

    return df_table


def extract_table_urls(target_url: str):
    """
    extract urls from all tables inside the page
    :param target_url: url of the page containing the table
    :return: Pandas DataFrame containing the table`s urls
    """
    page = requests.get(target_url)

    soup = bs(page.content, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")
    table_urls = []
    for row in rows:
        row_data = row.find_all("a")
        if len(row_data) == 0:
            continue

        urls = [url.attrs["href"] for url in row_data]
        doc = row_data[0].text.replace("\n", "").replace("  ", "")
        num_proc = row_data[1].text
        urls.append(num_proc)
        urls.append(doc)
        table_urls.append(urls)

    df_table_urls = pd.DataFrame(table_urls)
    df_table_urls.drop([0], axis=0, inplace=True)
    df_table_urls.dropna(inplace=True, ignore_index=True, axis=1)
    df_table_urls.rename(columns={0: "url", 1: "processo", 2: "num_proc", 3: "doc"}, inplace=True)

    return df_table_urls


def format_table_contents(table_contents: list):
    print(table_contents)
    contents = []
    for df_contents in table_contents:
        num_proc = df_contents[1][0]
        proc_partes = [df_contents[1][1], df_contents[3][1]]
        materia = df_contents[1][2]
        data_atuacao = df_contents[3][0]
        content = [num_proc, proc_partes, materia, data_atuacao]

        contents.append(content)

    df_table_contents = pd.DataFrame(contents, columns=["num_proc", "partes", "materia", "data_atuacao"])

    return df_table_contents


def format_output(df_table_contents: pd.DataFrame, df_table_urls: pd.DataFrame):
    df_output = df_table_contents.merge(df_table_urls, left_on="num_proc", right_on="num_proc")
    df_output.drop(["processo"], axis=1, inplace=True)

    return df_output
