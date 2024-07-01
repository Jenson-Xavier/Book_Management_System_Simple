import psycopg2

conn = psycopg2.connect(database="db_tpcc", user="joe",password="Bigdata@123", host="121.36.37.200", port=26000)
cur = conn.cursor()

# 计算每个学生有成绩的课程门数 平均成绩
cur.execute('''
            SELECT Sno,COUNT(Cno),AVG(Grade)
            FROM SC
            WHERE Grade IS NOT NULL
            GROUP BY Sno;
            ''')
results = cur.fetchall()
print(results)

# 使用GRANT语句 把对基本表 S SC C 的使用权限授给其它用户
cur.execute('''
            GRANT ALL PRIVILEGES
            ON TABLE S
            TO PUBLIC;
            ''')

cur.execute('''
            GRANT ALL PRIVILEGES
            ON TABLE C
            TO PUBLIC;
            ''')

cur.execute('''
            GRANT ALL PRIVILEGES
            ON TABLE SC
            TO PUBLIC;
            ''')

# 实验完成后 撤消建立的基本表和视图
cur.execute('''
            DROP VIEW Boys_view;
            DROP TABLE S,C,SC;
            ''')
