import psycopg2
from dotenv import load_dotenv
import os

PROD = True
if not PROD:
    load_dotenv('.env.dev')
else:
    load_dotenv('.env.prod')


class DataBase:
    def __init__(self):
        """
        Class responsible for connecting to the database
        """
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()

    @staticmethod
    def create_connection():
        """
        Creates connection with the database server
        :return: database Connection instance
        """
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

    def close_connection(self):
        """
        close connection with the database server
        :return:
        """
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            raise e

    def commit(self):
        """
        commits transactions to the database
        :return:
        """
        try:
            self.conn.commit()
        except Exception as e:
            raise e
