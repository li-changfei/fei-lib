import MySQLdb
import importlib

from dbutils.pooled_db import PooledDB


def get_conn():
    conn = MySQLdb.connect(host="database-tank1.c9103kdqidvw.ap-northeast-1.rds.amazonaws.com", port=3306, user="admin",
                           password="123456a?", db="tank_battle")
    # pool = PooledDB(MySQLdb, 3, host="database-tank1.c9103kdqidvw.ap-northeast-1.rds.amazonaws.com", user="admin", passwd="123456a?", db="tank_battle",
    #                 port=3306, charset="utf8", use_unicode=True)
    return conn


def insert(sql, args):
    conn = get_conn()
    cur = conn.cursor()
    result = cur.execute(sql, args)
    print(result)
    conn.commit()
    cur.close()
    conn.close()


def query(sql, args):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, args)
    results = cur.fetchall()
    print(type(results))  # 返回<class 'tuple'> tuple元组类型

    # for row in results:
    #     print(row)
    #     user_id = row[0]
    #     score = row[1]
    #     double_flg = row[2]
    #     print('Sno: ' + str(id) + '  Sname: ' + name + '  Ssex: ')
    #     pass

    conn.commit()
    cur.close()
    conn.close()

    return results


def query_no_args(sql):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    print(type(results))  # 返回<class 'tuple'> tuple元组类型

    # for row in results:
    #     print(row)
    #     user_id = row[0]
    #     score = row[1]
    #     double_flg = row[2]
    #     print('Sno: ' + str(id) + '  Sname: ' + name + '  Ssex: ')
    #     pass

    conn.commit()
    cur.close()
    conn.close()

    return results

def update(sql, args):
    conn = get_conn()
    cur = conn.cursor()
    result = cur.execute(sql, args)

    print(result)

    conn.commit()
    cur.close()
    conn.close()

