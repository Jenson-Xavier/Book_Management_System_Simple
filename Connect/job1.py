import psycopg2

# 创建连接对象
conn = psycopg2.connect(database="db_tpcc", user="joe", password="Bigdata@123", host="121.36.37.200", port=26000)
cur = conn.cursor()  # 创建指针对象

# 创建表
cur.execute("CREATE TABLE S"
            "(Sno VARCHAR(8) PRIMARY KEY,"
            "Sname VARCHAR(20),"
            "Ssex VARCHAR(6),"
            "Sbirthdate Date,"
            "Sdept VARCHAR(40)"
            ");")

cur.execute("CREATE TABLE C"
            "(Cno VARCHAR(8) PRIMARY KEY,"
            "Cname VARCHAR(40) NOT NULL,"
            "Cpno VARCHAR(8),"
            "Ccredit SMALLINT,"
            "FOREIGN KEY(Cpno) REFERENCES C(Cno)"
            ");")

cur.execute("CREATE TABLE SC"
            "(Sno VARCHAR(8),"
            "Cno VARCHAR(5),"
            "Grade SMALLINT,"
            "Semester VARCHAR(10),"
            "Teachingclass VARCHAR(10),"
            "PRIMARY KEY(Sno,Cno),"
            "FOREIGN KEY(Sno) REFERENCES S(Sno),"
            "FOREIGN KEY(Cno) REFERENCES C(Cno)"
            ");")

# 建立索引
cur.execute("CREATE UNIQUE INDEX Idx_StuSname ON S(Sname);")
cur.execute("CREATE UNIQUE INDEX Idx_CouCname ON C(Cname);")
cur.execute("CREATE UNIQUE INDEX IdxSCCno ON SC(Sno ASC,Cno DESC);")

# 删除索引
cur.execute("DROP INDEX Idx_StuSname;")
cur.execute("DROP INDEX Idx_CouCname;")
cur.execute("DROP INDEX IdxSCCno;")

# 插入数据 为实验一到实验五服务
# 插入S表
cur.execute("INSERT INTO S VALUES('20180001','李勇','男','2000-3-8','信息安全');")
cur.execute("INSERT INTO S VALUES('20180002','刘晨','女','1999-9-1','计算机科学与技术');")
cur.execute("INSERT INTO S VALUES('20180003','王敏','女','2001-8-1','计算机科学与技术');")
cur.execute("INSERT INTO S VALUES('20180004','张立','男','2000-1-8','计算机科学与技术');")
cur.execute("INSERT INTO S VALUES('20180005','陈新奇','男','2001-11-1','信息管理与信息系统');")
cur.execute("INSERT INTO S VALUES('20180006','赵明','男','2000-6-12','数据科学与大数据技术');")
cur.execute("INSERT INTO S VALUES('20180007','王佳佳','女','2001-12-7','数据科学与大数据技术');")

# 插入C表
cur.execute("INSERT INTO C VALUES('81001','程序设计基础与C语言',NULL,4);")
cur.execute("INSERT INTO C VALUES('81002','数据结构','81001',4);")
cur.execute("INSERT INTO C VALUES('81003','数据库系统概论','81002',4);")
cur.execute("INSERT INTO C VALUES('81004','信息系统概论','81003',4);")
cur.execute("INSERT INTO C VALUES('81005','操作系统','81001',4);")
cur.execute("INSERT INTO C VALUES('81006','Python语言','81002',3);")
cur.execute("INSERT INTO C VALUES('81007','离散数学',NULL,4);")
cur.execute("INSERT INTO C VALUES('81008','大数据技术概论','81003',4);")

# 插入SC表
cur.execute("INSERT INTO SC VALUES('20180001','81001',85,'20192','81001-01');")
cur.execute("INSERT INTO SC VALUES('20180001','81002',96,'20201','81002-01');")
cur.execute("INSERT INTO SC VALUES('20180001','81003',87,'20202','81003-01');")
cur.execute("INSERT INTO SC VALUES('20180002','81001',80,'20192','81001-02');")
cur.execute("INSERT INTO SC VALUES('20180002','81002',98,'20201','81002-01');")
cur.execute("INSERT INTO SC VALUES('20180002','81003',71,'20202','81003-02');")
cur.execute("INSERT INTO SC VALUES('20180003','81001',81,'20192','81001-01');")
cur.execute("INSERT INTO SC VALUES('20180003','81002',76,'20201','81002-02');")
cur.execute("INSERT INTO SC VALUES('20180004','81001',56,'20192','81001-02');")
cur.execute("INSERT INTO SC VALUES('20180004','81002',97,'20201','81002-02');")
cur.execute("INSERT INTO SC VALUES('20180005','81003',68,'20202','81003-01');")

conn.commit()

# 获取结果
# cur.execute('SELECT * FROM student')
# results = cur.fetchall()
# print(results)
