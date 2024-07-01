import psycopg2

conn = psycopg2.connect(database="db_tpcc", user="joe", password="Bigdata@123", host="121.36.37.200", port=26000)
cur = conn.cursor()

# 获取结果模板
# cur.execute('SELECT * FROM student')
# results = cur.fetchall()
# print(results)


# 查询1
# 查询选修1号课程的学生学号与姓名
cur.execute("SELECT S.Sno,S.Sname FROM S,SC WHERE S.Sno = SC.Sno AND SC.Cno = '81001';")
results = cur.fetchall()
# print(results)

# 查询2
# 查询选修课程名为数据结构的学生学号与姓名
cur.execute("SELECT S.Sno,S.Sname FROM S,C,SC WHERE S.Sno = SC.Sno AND C.Cno = SC.Cno AND C.Cname = '数据结构';")
results = cur.fetchall()
# print(results)

# 查询3
# 查询不选1号课程的学生学号与姓名
cur.execute("SELECT S.Sno,S.Sname FROM S,SC WHERE S.Sno = SC.Sno AND SC.Cno NOT LIKE '81001';")
results = cur.fetchall()
# print(results)

# 查询4
# 查询学习全部课程学生姓名
cur.execute('''
            SELECT Sname FROM S WHERE NOT EXISTS
            (SELECT * FROM C WHERE NOT EXISTS
            (SELECT * FROM SC WHERE Sno = S.Sno AND Cno = C.Cno));
            ''')
results = cur.fetchall()
# print(results)

# 查询5
# 查询所有学生除了选修1号课程外所有成绩均及格的学生的学号和平均成绩 其结果按平均成绩的降序排列
cur.execute('''
            SELECT SCX.Sno,AVG(SCX.Grade) FROM SC SCX
            WHERE 59 < all(SELECT SCY.Grade FROM SC SCY
            WHERE SCY.Sno = SCX.Sno AND SCY.Cno != '81001')
            AND SCX.Cno != '1'
            GROUP BY SCX.Sno
            ORDER BY AVG(SCX.Grade) DESC;
            ''')
results = cur.fetchall()
# print(results)

# 查询6
# 查询选修数据库原理成绩第2名的学生姓名
# 所建表中无数据库原理这一课程 用数据库系统概论课程代替
cur.execute('''
            SELECT Sname FROM S
            WHERE Sno IN (
            SELECT Sno FROM SC,C
            WHERE C.Cname = '数据库系统概论' AND SC.Cno = C.Cno
            ORDER BY Grade DESC
            LIMIT 1 OFFSET 1);
            ''')
results = cur.fetchall()
# print(results)

# 查询7
# 查询所有3个学分课程中有3门以上(含3门)课程获80分以上(含80分)的学生的姓名
cur.execute('''
            SELECT Sname FROM S
            WHERE Sno IN (
            SELECT Sno FROM SC,C
            WHERE C.Cno = SC.Cno AND C.Ccredit = 3 AND SC.Grade >= 80
            GROUP BY Sno
            HAVING COUNT(Grade) >=3);
            ''')
results = cur.fetchall()
# print(results)

# 查询8
# 查询选课门数唯一的学生的学号
cur.execute('''
            SELECT SCX.Sno FROM SC SCX
            GROUP BY SCX.Sno
            HAVING COUNT(*) NOT IN(
            SELECT COUNT(*) FROM SC SCY
            WHERE SCY.Sno != SCX.Sno
            GROUP BY SCY.Sno);
            ''')
results = cur.fetchall()
# print(results)

# 查询9
# 自行SELECT test