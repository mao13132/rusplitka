import datetime
import re
import sqlite3
from datetime import datetime


class BotDB:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:


            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, db_file):
        try:

            self.conn = sqlite3.connect(db_file, timeout=30)
            print('Подключился к SQL DB:', db_file)
            self.cursor = self.conn.cursor()
            self.check_table()
        except Exception as es:
            print(f'Ошибка при работе с SQL {es}')

    def check_table(self):

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"plu (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"link TEXT,"
                                f"name TEXT,"
                                f"country TEXT,"
                                f"artikl TEXT,"
                                f"collection TEXT,"
                                f"proiz TEXT,"
                                f"other TEXT)")
        except Exception as es:
            print(f'SQL исключение check_table имя таблицы{es}')

    def exist_plu(self, artikl, proiz):
        try:
            result = self.cursor.execute(f"SELECT * FROM plu WHERE artikl = '{artikl}' AND proiz = '{proiz}'")
            response = result.fetchall()
        except Exception as es:
            print(f'SQL ошибка! При exist_plu в DB "{es}"')
            return []

        return response

    def add_plu(self, link, name, artikl, collection, proiz):
        try:
            self.cursor.execute("INSERT OR IGNORE INTO plu ('link', 'name', "
                                "'artikl', 'collection', 'proiz') VALUES (?,?,?,?,?)", (link, name, artikl,
                                                                                        collection, proiz))
            self.conn.commit()
        except Exception as es:
            print(f'SQL ошибка! Не смог добавить plu в DB "{es}"')

            return False

        return True

    def update_double(self, artikl, collection, proiz):
        try:
            result = self.cursor.execute(f"SELECT id_pk, collection FROM plu WHERE artikl = '{artikl}' AND "
                                         f"proiz = '{proiz}'")
            response = result.fetchall()
        except Exception as es:
            print(f'SQL ошибка! При update_double 1 в DB "{es}"')
            return []

        if response != []:
            id_pk = response[0][0]
            coll_sql = response[0][1]

            if collection in coll_sql:
                print(f'Уже есть коллекция {collection} в sql пропускаю')
                return True

            update_coll = coll_sql + ';' + collection

            try:

                result = self.cursor.execute(
                    f"UPDATE plu SET collection = '{update_coll}' WHERE id_pk = '{id_pk}'")
                self.conn.commit()
                # x = result.fetchall()
            except Exception as es:
                print(f'Ошибка SQL update_double 2: {es}')


        return True




    def get_all_count(self):
        try:
            result = self.cursor.execute("SELECT count(*) FROM plu")
            response = result.fetchall()
        except Exception as es:
            print(f'SQL ошибка! Не смог добавить get_all_count в DB "{es}"')

            return 0

        try:
            res = int(response[0][0])
        except:
            res = 0

        return res


    def get_tovar(self, id_pk):
        try:
            result = self.cursor.execute(f"SELECT * FROM plu WHERE id_pk = '{id_pk}'")
            response = result.fetchall()
        except Exception as es:
            print(f'SQL ошибка! Не смог добавить get_tovar в DB "{es}"')

            return False

        try:
            res = response[0]
        except:
            return []

        return res




    def close(self):
        # Закрытие соединения
        self.conn.close()
        print('Отключился от SQL BD')
