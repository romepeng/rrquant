"""
see https://docs.python.org/zh-cn/3/library/sqlite3.html
"""

import sqlite3
con = sqlite3.connect('example.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE stocks
               (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()

# for row in cur.execute('SELECT * FROM stocks ORDER BY price'):
#        print(row)

# Never do this -- insecure!
#symbol = 'RHAT'
#cur.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

"""
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

con = sqlite3.connect(":memory:")
con.row_factory = dict_factory
cur = con.cursor()
cur.execute("select 1 as a")
print(cur.fetchone()["a"])
con.close()
将现有数据库复制到另一个数据库中：

import sqlite3

def progress(status, remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')

con = sqlite3.connect('existing_db.db')
bck = sqlite3.connect('backup.db')
with bck:
    con.backup(bck, pages=1, progress=progress)
bck.close()
con.close()
示例二，将现有数据库复制到临时副本中：

import sqlite3

source = sqlite3.connect('existing_db.db')
dest = sqlite3.connect(':memory:')
source.backup(dest)

# Convert file existing_db.db to SQL dump file dump.sql
import sqlite3

con = sqlite3.connect('existing_db.db')
with open('dump.sql', 'w') as f:
    for line in con.iterdump():
        f.write('%s\n' % line)
con.close()
"""

使用连接作为上下文管理器
连接对象可以用来作为上下文管理器，它可以自动提交或者回滚事务。如果出现异常，事务会被回滚；否则，事务会被提交。

import sqlite3

con = sqlite3.connect(":memory:")
con.execute("create table lang (id integer primary key, name varchar unique)")

# Successful, con.commit() is called automatically afterwards
with con:
    con.execute("insert into lang(name) values (?)", ("Python",))

# con.rollback() is called after the with block finishes with an exception, the
# exception is still raised and must be caught
try:
    with con:
        con.execute("insert into lang(name) values (?)", ("Python",))
except sqlite3.IntegrityError:
    print("couldn't add Python twice")

# Connection object used as context manager only commits or rollbacks transactions,
# so the connection object should be closed manually
con.close()
