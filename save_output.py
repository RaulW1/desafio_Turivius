import pandas as pd
from dotenv import load_dotenv
import os
from os.path import join
from DataBase import DataBase
from psycopg2.errors import UniqueViolation

load_dotenv('.env.dev')


def save_on_dir(df_output: pd.DataFrame):
    """
    generates output file (.json) on directory
    :param df_output: pd.DataFrame containing the output data
    :return:
    """
    try:
        output_path = join(os.getenv("OUTPUT_PATH"), os.getenv("FILE_NAME"))
        df_output.to_csv(output_path)
    except Exception as e:
        raise e


def populate_table(db: DataBase, data: list, table: str, column: str):
    """
    insert new values into table if they don't already exist
    :param db: database connection instance
    :param data: data to be stored
    :param table: table name which data will be inserted into
    :param column: table's column
    :return:
    """
    try:
        for d in data:
            try:
                db.cursor.execute(query="""
                    insert into $TABLE ($COLUMN)
                    values (%s)
                """.replace("$TABLE", table).replace("$COLUMN", column),
                                  vars=(d,))
            except UniqueViolation:
                db.conn.rollback()
                continue

            db.commit()
    except Exception as e:
        db.conn.rollback()
        db.close_connection()
        raise e


def insert_registro(db: DataBase, df_output: pd.DataFrame):
    """
    insert records into table registro
    :param db: database connection instance
    :param df_output: pd.DataFrame containing the output data
    :return:
    """
    try:
        for index, row in df_output.iterrows():
            variables = (row["doc"], row["materia"], row["num_proc"], row["partes"], row["data_atuacao"], row["url"])
            try:
                db.cursor.execute(query="""
                    insert into registro (doc_id, materia_id, n_processo, partes, data_atuacao, url)
                    values ((select id from doc where doc=%s), 
                    (select id from materia where materia=%s), %s, %s, %s, %s)
                """, vars=variables)

            except UniqueViolation:
                db.conn.rollback()
                continue

            db.commit()
    except Exception as e:
        db.conn.rollback()
        db.close_connection()
        raise e


def save_on_database(df_output: pd.DataFrame):
    """
    saves output content on database
    :param df_output: pd.DataFrame containing the output data
    :return:
    """
    db = DataBase()

    # Inserindo dados da tabela doc. Novas instâncias de "doc" são inseridas a cada execução
    populate_table(db, df_output["doc"].unique().tolist(), "doc", "doc")

    # Inserindo dados da tabela materia. Novas instâncias de "materia" são inseridas a cada execução
    populate_table(db, df_output["materia"].unique().tolist(), "materia", "materia")

    # Inserindo dados na tabela registro
    insert_registro(db, df_output)

    db.close_connection()


def save_output(df_output: pd.DataFrame):
    """
    generates output file and saves its contents on the database
    :param df_output: pd.DataFrame containing the output data
    :return:
    """
    save_on_dir(df_output)
    save_on_database(df_output)
