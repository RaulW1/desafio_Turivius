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
