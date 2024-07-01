from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# 用户信息模型 数据库中的一个表
# 作为Django中用户认证的外键用于登录
class UserInfo(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    userName = models.CharField(max_length=30)
    userSex = models.BooleanField(default=True)
    userAge = models.IntegerField()
    userPhone = models.CharField(max_length=12, null=True, blank=True)
    userRegisterTime = models.DateField(auto_now_add=True)


# 书本类型数据模型
class BookType(models.Model):
    TypeId = models.IntegerField(primary_key=True)
    TypeName = models.CharField(max_length=20)


# 书本数据模型
class Book(models.Model):
    bookId = models.CharField(max_length=40, primary_key=True)
    bookName = models.CharField(max_length=40)
    bookType = models.ForeignKey(BookType, on_delete=models.CASCADE)
    bookPublisher = models.CharField(max_length=40)
    bookAuthor = models.CharField(max_length=40)
    bookIntroduction = models.TextField()
    bookPrice = models.IntegerField()


# 书本数量模型
class BookNum(models.Model):
    bookId = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookNum = models.IntegerField()


# 图书管理员模型
class StaffInfo(models.Model):
    staffId = models.ForeignKey(User, on_delete=models.CASCADE)
    staffName = models.CharField(max_length=40)


# 添加书籍数据模型
class AddBook(models.Model):
    bookId = models.ForeignKey(Book, on_delete=models.CASCADE)
    staffId = models.ForeignKey(StaffInfo, on_delete=models.CASCADE)
    addNum = models.IntegerField()


# 借书模型
class BorrowBook(models.Model):
    borrowId = models.IntegerField(primary_key=True)
    bookId = models.ForeignKey(Book, on_delete=models.CASCADE)
    staffId = models.ForeignKey(StaffInfo, on_delete=models.CASCADE)
    userId = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    hasReturned = models.BooleanField(default=False)
