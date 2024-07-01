import psycopg2

conn = psycopg2.connect(database="db_tpcc", user="joe",password="Bigdata@123", host="121.36.37.200", port=26000)
cur = conn.cursor()

# 视图1
# 建立男学生的视图 属性包括学号 姓名 选修课程名和成绩
cur.execute('''
            CREATE VIEW Boys_view AS
            SELECT S.Sno,S.Sname,C.Cname,SC.Grade
            FROM SC,S,C
            WHERE S.Ssex = '男' AND S.Sno = SC.Sno AND C.Cno = SC.Cno;
            ''')

# 视图2
# 在男学生视图中查询平均成绩大于80分的学生学号与姓名
cur.execute('''
            SELECT Sno,Sname FROM Boys_view
            GROUP BY Sno,Sname
            HAVING AVG(Grade) > 80;
            ''')
results = cur.fetchall()
print(results)