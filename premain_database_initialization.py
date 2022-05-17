import os
import time

import mariadb

import secret


FLAGS = _ = None
DEBUG = False
STIME = time.time()


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    conn, cur = utils.connectdb(user=secret.db_username,
                                password=secret.db_password,
                                host=secret.db_host,
                                port=secret.db_port,
                                database=secret.db_databasename)
    if DEBUG:
        print(f'[{int(time.time()-STIME)}] Connect to database')

    if FLAGS.reset:
        cur.execute('''DROP TABLE IF EXISTS blk;''')
        if DEBUG:
            print(f'[{int(time.time()-STIME)}] DROP all tables of {secret.db_database}')

    cur.execute('''CREATE TABLE blk (
                     id INT NOT NULL,
                     blkhash CHAR(64) NOT NULL,
                     miningtime TIMESTAMP NOT NULL,
                     PRIMARY KEY (id),
                     UNIQUE (blkhash)
                   );''')
    cur.execute('''CREATE INDEX idx_miningtime ON blk (miningtime);''')
    conn.commit()

    cur.execute('''SHOW TABLES;''')
    res = cur.fetchall()
    if DEBUG:
        print(f'[{int(time.time()-STIME)}] CREATE TABLES: {res}')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    import argparse

    root_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(root_path)
    os.chdir(root_dir)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--reset', action='store_true',
                        help='Clear exists tables before creation')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()

