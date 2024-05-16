import psycopg2
from dotenv import load_dotenv
import os
from os.path import join

load_dotenv('.env.dev')


class DataBase:
    def __init__(self):
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()

    @staticmethod
    def create_connection():
        try:
            conn = psycopg2.connect(
                host=os.getenv("HOST"),
                dbname=os.getenv("DBNAME"),
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD")
            )

            return conn
        except Exception as e:
            raise e

    def execute_query(self, query: str, values: list):
        try:
            self.cursor.execute(query=query, vars=values)
            data = self.cursor.fetchall()
            self.commit()

            return data

        except Exception as e:
            raise e

    def close_connection(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            raise e

    def commit(self):
        try:
            self.conn.commit()
        except Exception as e:
            raise e


if __name__ == "__main__":
    db = DataBase()
    db.close_connection()
