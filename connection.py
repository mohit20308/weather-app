from pymongo import MongoClient

import utils


def get_db_handle():
    db_password = utils.db_password
    connection_string = 'mongodb+srv://mydb:' + db_password + '@data.drmq9.mongodb.net/?retryWrites=true&w=majority&appName=data'
    cluster = MongoClient(connection_string)

    db_handle = cluster["data"]

    return db_handle