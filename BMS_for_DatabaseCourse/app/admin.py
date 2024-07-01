from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Book)
admin.site.register(BookType)
admin.site.register(BookNum)
admin.site.register(AddBook)
admin.site.register(BorrowBook)
admin.site.register(UserInfo)
admin.site.register(StaffInfo)