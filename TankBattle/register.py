import coonDB


def register(user_id):
    if check(user_id):
        sql = "INSERT INTO user_info VALUES(%s, 0, %s);"
        coonDB.insert(sql, (user_id, 1))
        coonDB.insert(sql, (user_id, 0))


def check(user_id):
    sql = "select * from  user_info WHERE user_id = %s"
    results = coonDB.query(sql, (user_id))
    if len(results) > 0:
        return False
    else:
        return True
