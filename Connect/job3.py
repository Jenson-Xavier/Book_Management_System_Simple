import psycopg2

conn = psycopg2.connect(database="db_tpcc", user="joe",password="Bigdata@123", host="121.36.37.200", port=26000)
cur = conn.cursor()

# 修改1
# 把1号课程的非空成绩提高10%
cur.execute("SELECT * FROM SC WHERE Cno = '81001';")
cmd1 = '''
    UPDATE SC
    SET Grade = Grade * 1.1
    WHERE Grade IS NOT NULL AND Cno = '81001';
    '''
# cur.execute(cmd1)
cur.execute("SELECT * FROM SC WHERE Cno = '81001';")
results = cur.fetchall()
# print(results)

# 修改2
# 在SC表中删除课程名为数据结构的成绩的元组
cmd2 = '''
    DELETE FROM SC
    WHERE Cno IN (SELECT Cno FROM C WHERE Cname = '数据结构');
'''
# cur.execute(cmd2)
cur.execute("SELECT * FROM SC;")
results = cur.fetchall()
# print(results)

# 修改3
# 在S和SC表中删除学号为202415122的所有数据
# 所建表无学号为202415122 用20180007代替
cmd3 = '''
    DELETE FROM SC WHERE Sno = '20180007';
    DELETE FROM S WHERE Sno = '20180007';
'''
cur.execute(cmd3)
cur.execute("SELECT * FROM S;")
results = cur.fetchall()
print(results)