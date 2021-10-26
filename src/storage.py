import atexit
from datetime import datetime
import os
import sqlite3

def remove_db():
    # os.remove('test.db')
    pass

atexit.register(remove_db);


class Storage():
    def __init__(self,path = 'test.db') -> None:
        self.path = path
        with self as q:
            cursor = q.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS counters (counter_name, created_date_time, desc, _type)")


    def create_counter(self, counter_name, desc='', _type=1):
        created_date_time = datetime.now()
        print(f"{counter_name}, {_type}, {desc}")
        with self as q:
            # create table for counter
            q.cursor().execute(f"CREATE TABLE IF NOT EXISTS {counter_name} ('value', 'comment', 'date_and_time')")
            
            # update main table
            sql = f"""
            INSERT INTO counters (counter_name, desc , _type, created_date_time)
                VALUES('{counter_name}', '{desc}', '{_type}', '{created_date_time}');
            """
            q.cursor().execute(sql)

            # Save (commit) the changes
            q.commit()

    def update_counter(self, counter_name, value, comment, date_and_time=datetime.now()):
        with self as q:
            # update counter with value, comment and date_time
            sql = f"""
            INSERT INTO {counter_name} (value , comment, date_and_time)
                VALUES('{value}', '{comment}', '{date_and_time}');
            """

            q.cursor().execute(sql)
            # Save (commit) the changes
            q.commit()

    def remove_counter(self, counter_name):
        with self as q:
            # remove counter
            sql = f"""
            DROP TABLE {counter_name}
            """
            q.cursor().execute(sql)

            # update main table
            sql = f"""
            DELETE FROM counters WHERE counter_name={counter_name};
            """
            q.cursor().execute(sql)

            # Save (commit) the changes
            q.commit()

    def get_counters(self):
        with self as q:
            # get list of counters
            sql = f"""
            SELECT counter_name
            FROM counters
            """

            counters = q.cursor().execute(sql).fetchall()

            for index, counter in enumerate(counters):
                sql = f"""
                SELECT SUM(value) from {counter[0]};
                """
                sum_value = q.cursor().execute(sql).fetchone()
                counters[index] = (counter[0], sum_value[0])

            # Save (commit) the changes
            q.commit()

        return counters

    def __enter__(self):
        return sqlite3.connect(self.path)


    def __exit__(self, exc_my_type, exc_value, tb):
        pass
        


if __name__ == '__main__':
    Storage()
