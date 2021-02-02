import MySQLdb


def get_coon():
    db = MySQLdb.connect(host="database-tank1.c9103kdqidvw.ap-northeast-1.rds.amazonaws.com", port=3306, user="admin",
                         password="123456a?", db="tank_battle")
    return db


def close_coon(db):

    db.close()
