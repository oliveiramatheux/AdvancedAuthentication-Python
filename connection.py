import MySQLdb

host = "localhost"
user = "root"
password = ""
db = "authentication"
port = 3306


conn = MySQLdb.connect(host, user, password, db, port)

c = conn.cursor(MySQLdb.cursors.DictCursor)


def select(fields, tables, where=None):
    global c
    query = "SELECT " + fields + " FROM " + tables
    if where:
        query = query + " WHERE " + where

    c.execute(query)
    return c.fetchall()

# select("fields", "table", "where - optional")
# print(select("*", "usuario"))


def insert(values, table, fields=None):
    global c, conn
    query = "INSERT INTO " + table
    if fields:
        query = query + " (" + fields + ") "
    query = query + " VALUES " + ",".join(["(" + v + ")" for v in values])

    c.execute(query)
    conn.commit()

# insert(values, table)
# values = ["DEFAULT, 'Joao', '1234'"]
# insert(values, "usuario")


def update(sets, table, where=None):
    global c, conn

    query = "UPDATE " + table
    query = query + " SET " + ",".join([field + " = '" + value + "'" for field, value in sets.items()])
    if where:
        query = query + " WHERE " + where

    c.execute(query)
    conn.commit()

# update({"name of camp":"value of camp"}, "table", "optional where")
# update({"usuario_nome":"Matheus", "usuario_senha": "1234567"}, "usuario", "usuario_id = 1")


def delete(table, where):
    global c, conn

    query = "DELETE FROM " + table + " WHERE " + where

    c.execute(query)
    conn.commit()

# delete("table", "condition")
# delete("usuario", "usuario_id = 2")
