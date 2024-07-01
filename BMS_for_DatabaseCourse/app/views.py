from django.contrib.auth.models import *
from django.core.paginator import *
from django.http import *
from django.shortcuts import render

from app.models import *


# Create your views here.


# 用户登录界面
def login_view(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return render(request, "login.html")
    else:
        return render(request, "login.html")


# 用户登出界面
def logout_view(request):
    auth.logout(request)
    return render(request, "logout.html")


# 用户注册界面
def register_view(request):
    return render(request, "register.html")


# 用户注册逻辑
def register(request):
    try:
        userid = request.POST['id']
        userpw = request.POST['pw']
        username = request.POST['name']
        usersex = request.POST['sex']
        if usersex == 'True':
            usersex = True
        else:
            usersex = False
        userage = request.POST['age']
        useremail = request.POST['email']
        userphone = request.POST['phone']
    except:
        return render(request, "register.html", {'msgFail': 'GET Error，注册失败，请重新操作！'})

    try:
        user = User.objects.create_user(username=userid, password=userpw, email=useremail)
        user.is_staff = False
        user.save()
        try:
            UserInfo.objects.create(userId=user, userName=username, userSex=usersex, userAge=userage,
                                    userPhone=userphone)
        except Exception as e:
            return render(request, "register.html", {'msgFail': f'注册失败，请重新操作！可能原因是：{e}'})
        return render(request, "login.html", {'msgTrue': '注册成功，请登录系统！'})
    except Exception as e:
        return render(request, "register.html", {'msgFail': f'注册失败，请重新操作！可能原因是：{e}'})


# 用户登录逻辑
def login(request):
    try:
        userId = request.POST['id']
        userPw = request.POST['pw']
    except:
        return render(request, "login.html", {'msgFail': 'POST Error，现在登出并请重新登录！'})
    user = auth.authenticate(request, username=userId, password=userPw)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index')
    else:
        return render(request, "login.html", {'msgFail': '身份验证失败，现在登出并请重新登录！'})


# 查看书籍信息的视图逻辑
def view_bookinfo(request):
    if request.user.is_authenticated:  # django验证身份
        cur_user = request.user
        try:
            if cur_user.is_staff:  # 验证管理员
                staff_flag = True
                username = StaffInfo.objects.get(staffId=cur_user).staffName
            else:
                staff_flag = False
                username = UserInfo.objects.get(userId=cur_user).userName
            cur_user_info = {"userId": cur_user.username, "userName": username}  # cur_user是request中的user类型
        except:
            return JsonResponse({'end': False, 'msg': '数据库中不存在所查找的数据!'})

        try:
            mode = request.GET['mode']
            startpage = request.GET['startpage']
            offset = request.GET['offset']
            booklikename = request.GET['booklikename']
            # 由于Simple和Detail在同一个视图处理 故这里的空输入判断移交到js脚本文件中进行判断
        except:
            return JsonResponse({'end': False, 'msg': 'GET Error!'})

        results = []
        if mode == 'Detail':  # 详细显示某个书籍的具体信息
            try:
                get_book = Book.objects.get(bookId=booklikename)
                get_book_num_fk = BookNum.objects.get(bookId=get_book)
                book_detail = {"bookId": get_book.bookId,
                               "bookName": get_book.bookName,
                               "bookType": get_book.bookType.TypeName,
                               "bookPublisher": get_book.bookPublisher,
                               "bookAuthor": get_book.bookAuthor,
                               "bookIntroduction": get_book.bookIntroduction,
                               "bookPrice": get_book.bookPrice,
                               "bookNum": get_book_num_fk.bookNum}
                return JsonResponse({'end': True, 'msg': book_detail})
            except:
                return JsonResponse({'end': False, 'msg': '数据库中不存在所查找的数据!'})
        elif mode == 'Simple':  # 用于图书馆library界面所有书籍信息的展示
            cur_page = int(startpage)
            try:
                if booklikename == '':
                    book_all = Book.objects.all().order_by('bookName')
                    all_Items = Book.objects.all().count()
                else:
                    if '书' in booklikename:
                        book_all = Book.objects.filter(bookName__contains=booklikename).order_by('bookName')
                        all_Items = book_all.count()
                    elif '作者' in booklikename:
                        book_all = Book.objects.filter(bookAuthor__contains=booklikename).order_by('bookName')
                        all_Items = book_all.count()
                    elif '出版社' in booklikename:
                        book_all = Book.objects.filter(bookPublisher__contains=booklikename).order_by('bookName')
                        all_Items = book_all.count()
                    else:
                        book_all1 = Book.objects.filter(bookName__contains=booklikename).order_by('bookName')
                        book_all2 = Book.objects.filter(bookAuthor__contains=booklikename).order_by('bookName')
                        book_all3 = Book.objects.filter(bookPublisher__contains=booklikename).order_by('bookName')
                        book_all = []
                        book_all.extend(book_all1)
                        book_all.extend(book_all2)
                        book_all.extend(book_all3)
                        all_Items = book_all1.count() + book_all2.count() + book_all3.count()
            except:
                return HttpResponse('数据库中不存在所查找的数据!')
            try:
                book_pages = Paginator(book_all, int(offset))  # 创建分页器 用于页面显示时分页
                pagen = book_pages.page(cur_page)
                pagenum = book_pages.page_range[-1]
                after_range_num = 5
                before_range_num = 4
                book_results = pagen.object_list
                if cur_page - 1 > after_range_num:
                    pagelist = book_pages.page_range[cur_page - 1 - after_range_num:cur_page - 1 + before_range_num]
                else:
                    pagelist = book_pages.page_range[0:cur_page - 1 + before_range_num]
                for book_result in book_results:
                    book_num_fk = BookNum.objects.get(bookId=book_result)
                    book_detail = {"bookName": book_result.bookName,
                                   "bookId": book_result.bookId,
                                   "bookType": book_result.bookType.TypeName,
                                   "bookPublisher": book_result.bookPublisher,
                                   "bookAuthor": book_result.bookAuthor,
                                   "bookPrice": book_result.bookPrice,
                                   "bookNum": book_num_fk.bookNum,
                                   "bookIntroduction": book_result.bookIntroduction[:60]}
                    results.append(book_detail)
                return render(request, 'library.html', {"currentUser": cur_user_info,
                                                        "is_staff": staff_flag,
                                                        "bookList": results,
                                                        "bookLikeName": booklikename,
                                                        "pageList": pagelist,
                                                        "currentPage": cur_page,
                                                        "nextPage": cur_page + 1,
                                                        "prevPage": cur_page - 1,
                                                        "endPage": pagenum,
                                                        "curpageItems": len(results),
                                                        "allpageItems": all_Items})
            except:
                return HttpResponse('图书数据信息查找失败！')
    else:
        return HttpResponseRedirect('/login_page')  # 重定向


# 管理员添加书籍的视图逻辑
def staff_add_book(request):
    if request.user.is_authenticated:  # django验证身份
        cur_user = request.user
        if cur_user.is_staff:  # 验证管理员
            try:
                bookid = request.GET['bookid']
                bookname = request.GET['bookname']
                booktype = request.GET['booktype']
                bookpublisher = request.GET['bookpublisher']
                bookauthor = request.GET['bookauthor']
                bookintroduction = request.GET['bookintroduction']
                bookprice = request.GET['bookprice']
                booknum = request.GET['booknum']
                if bookid == '' or bookname == '' or booktype == '' or bookpublisher == '' \
                        or bookauthor == '' or bookintroduction == '' or bookprice == '' or booknum == '':
                    return JsonResponse({'end': True, 'msg': '请输入数据再进行操作！'})
            except:
                return JsonResponse({'end': False, 'msg': 'GET Error!'})
            try:
                booktype_fk = BookType.objects.get(TypeId=booktype)
                book_added = Book.objects.create(bookId=bookid,
                                                 bookName=bookname,
                                                 bookType=booktype_fk,
                                                 bookPublisher=bookpublisher,
                                                 bookAuthor=bookauthor,
                                                 bookIntroduction=bookintroduction,
                                                 bookPrice=bookprice)
                BookNum.objects.create(bookId=book_added, bookNum=booknum)
                AddBook.objects.create(bookId=book_added,
                                       staffId=StaffInfo.objects.get(staffId=cur_user),
                                       addNum=booknum)
                return JsonResponse({'end': True, 'msg': '添加书籍成功！'})
            except:
                return JsonResponse({'end': False, 'msg': '添加书籍失败，请注意输入格式并不要输入重复书籍ID，请重试！'})
        else:
            return JsonResponse({'end': False, 'msg': 'Permission Denied!'})
    else:
        return JsonResponse({'end': False, 'msg': 'Permission Denied!'})


# 管理员修改书籍相关的属性的视图逻辑
# 主要是增加图书数量这一操作
def staff_alter_book(request):
    if request.user.is_authenticated:
        cur_user = request.user
        if cur_user.is_staff:  # 验证为管理员则可以修改
            try:
                bookid = request.GET['bookid']
                addbooknum = request.GET['addbooknum']
                if bookid == '' or addbooknum == '':
                    return JsonResponse({'end': True, 'msg': '请输入数据再进行操作！'})
            except:
                return JsonResponse({'end': False, 'msg': 'GET Error!'})
            try:  # try查找数据
                book_fk = Book.objects.get(bookId=bookid)
                staffinfo_fk = StaffInfo.objects.get(staffId=cur_user)
                AddBook.objects.create(bookId=book_fk,
                                       staffId=staffinfo_fk,
                                       addNum=addbooknum)
            except:
                return JsonResponse({'end': False, 'msg': '数据库中不存在所查找的数据!'})
            try:
                try:  # try修改数据
                    changebooknum = BookNum.objects.get(bookId__bookId=bookid)
                    changebooknum.bookNum += int(addbooknum)
                    changebooknum.save()
                except:  # 否则新增对应的数据
                    BookNum.objects.create(bookId=book_fk, bookNum=addbooknum)
                return JsonResponse({'end': True, 'msg': '添加图书数量成功!'})
            except:
                return JsonResponse({'end': False, 'msg': '添加图书失败，请重新操作！'})
        else:
            auth.logout(request)  # 非管理员退出
            return JsonResponse({'end': False, 'msg': 'Permission Denied!'})
    else:
        return JsonResponse({'end': False, 'msg': 'Permission Denied!'})


# 管理员负责用户借书
def staff_borrow_book(request):
    if request.user.is_authenticated:
        cur_user = request.user
        if cur_user.is_staff:
            try:
                bookid = request.GET['bookid']  # 用户所借书的信息
                userid = request.GET['userid']  # 需要进行借书的用户
                if bookid == '' or userid == '':  # 用户没有输入数据时
                    return JsonResponse({'end': True, 'msg': '请输入数据再进行操作！'})
            except:
                return JsonResponse({'end': False, 'msg': 'GET Error!'})
            try:
                booknum = BookNum.objects.get(bookId__bookId=bookid)
            except:
                return JsonResponse({'end': False, 'msg': '数据库中不存在所查找的数据!'})
            if booknum.bookNum == 0:
                return JsonResponse({'end': False, 'msg': '所借书数据库中无法提供更多的数量!'})
            try:
                borrowbook_len = len(BorrowBook.objects.all())
                borrowbook = BorrowBook.objects.create(borrowId=borrowbook_len + 1,
                                                       bookId=Book.objects.get(bookId=bookid),
                                                       staffId=StaffInfo.objects.get(staffId=cur_user),
                                                       userId=UserInfo.objects.get(userId__username=userid),
                                                       hasReturned=False)
                booknum.bookNum -= 1
                booknum.save()
                return JsonResponse({'end': True, 'msg': '借书成功！'})
            except:
                return JsonResponse({'end': False, 'msg': '借书失败，请重新操作！'})
        else:
            return JsonResponse({'end': False, 'msg': 'Permission Denied!'})
    else:
        return JsonResponse({'end': False, 'msg': 'Permission Denied!'})


# 管理员负责用户还书
def staff_return_book(request):
    if request.user.is_authenticated:
        cur_user = request.user
        if cur_user.is_staff:
            try:
                bookid = request.GET['bookid']  # 用户所还书的信息
                userid = request.GET['userid']  # 需要进行还书的用户
                if bookid == '' or userid == '':
                    return JsonResponse({'end': True, 'msg': '请输入数据再进行操作！'})
            except:
                return JsonResponse({'end': False, 'msg': 'GET Error!'})
            try:
                booknum = BookNum.objects.get(bookId__bookId=bookid)
                borrowbooks = BorrowBook.objects.filter(bookId__bookId=bookid,
                                                        userId__userId__username=userid).exclude(hasReturned=True)
            except:
                return JsonResponse({'end': False, 'msg': '数据库中不存在所查找的数据!'})
            if len(borrowbooks) == 0:
                return JsonResponse({'end': False, 'msg': '不存在可以还的书！'})  # 无可以还的书
            try:
                for borrowbook in borrowbooks:
                    if borrowbook.hasReturned:
                        continue
                    borrowbook.hasReturned = True
                    borrowbook.save()
                    booknum.bookNum += 1
                booknum.save()
                return JsonResponse({'end': True, 'msg': '还书成功！'})
            except:
                return JsonResponse({'end': False, 'msg': '还书失败，请重新操作！'})
        else:
            return JsonResponse({'end': False, 'msg': 'Permission Denied!'})
    else:
        return JsonResponse({'end': False, 'msg': 'Permission Denied!'})


# 获取书籍类型
def get_book_types(request):
    if request.user.is_authenticated:
        book_type_id = []
        book_type_info = []
        types = BookType.objects.all()
        for type in types:
            book_type_id.append(type.TypeId)
            book_type_info.append(type.TypeName)
        return JsonResponse({'typeId': book_type_id, 'typeInfo': book_type_info})
    else:
        return HttpResponse('Permission Denied!')


# 查看用户信息
# 当以非管理员用户身份登录时会以此视图进行跳转
def staff_view_user_info(request):
    if request.user.is_authenticated:
        cur_user = request.user
        if cur_user.is_staff:  # 管理员
            try:
                userid = request.GET['userid']
            except:
                return HttpResponseRedirect('/login_page')
            cur_login_user = {'userId': cur_user.username,
                              'userName': StaffInfo.objects.get(staffId=cur_user).staffName}
            auth_user = User.objects.get(username=userid)
            user_info_fk = UserInfo.objects.get(userId=auth_user)
            borrow_books = BorrowBook.objects.filter(userId=user_info_fk).order_by('borrowId')
            user_info = {'userid': auth_user.username,
                         'username': user_info_fk.userName,
                         'email': auth_user.email,
                         'sex': user_info_fk.userSex,
                         'age': user_info_fk.userAge,
                         'pn': user_info_fk.userPhone,
                         'time': user_info_fk.userRegisterTime.strftime('%Y-%m-%d')}
            borrow_info_list = []
            for i, borrow_book in enumerate(borrow_books):
                borrow_info_list.append({'bookName': borrow_book.bookId.bookName,
                                         'itemNum': i + 1,
                                         'staffId': borrow_book.staffId.staffId.username,
                                         'hasReturn': borrow_book.hasReturned})
            borrow_info_list.reverse()
            return render(request, 'userdetail.html', {'userInfo': user_info,
                                                       'borrowList': borrow_info_list,
                                                       'currentUser': cur_login_user,
                                                       'is_staff': True})
        else:  # 非管理员
            userid = cur_user.username
            cur_login_user = {'userId': cur_user.username,
                              'userName': UserInfo.objects.get(userId=cur_user).userName}
            auth_user = User.objects.get(username=userid)
            user_info_fk = UserInfo.objects.get(userId=auth_user)
            borrow_books = BorrowBook.objects.filter(userId=user_info_fk).order_by('borrowId')
            user_info = {'userid': auth_user.username,
                         'username': user_info_fk.userName,
                         'email': auth_user.email,
                         'sex': user_info_fk.userSex,
                         'age': user_info_fk.userAge,
                         'pn': user_info_fk.userPhone,
                         'time': user_info_fk.userRegisterTime.strftime('%Y-%m-%d')}
            borrow_info_list = []
            for i, borrow_book in enumerate(borrow_books):
                borrow_info_list.append({'bookName': borrow_book.bookId.bookName,
                                         'itemNum': i + 1,
                                         'staffId': borrow_book.staffId.staffId.username,
                                         'hasReturn': borrow_book.hasReturned})
            borrow_info_list.reverse()
            return render(request, 'userdetail.html', {'userInfo': user_info,
                                                       'borrowList': borrow_info_list,
                                                       'currentUser': cur_login_user,
                                                       'is_staff': False})
    else:
        return HttpResponseRedirect('/login_page')


# 管理员查看用户
# 此视图逻辑用于在管理员界面浏览所有注册的用户信息
def staff_view_user(request):
    if request.user.is_authenticated:
        cur_user = request.user
        if cur_user.is_staff:
            try:
                username = request.GET['username']
                offset = request.GET['offset']
                startpage = request.GET['startpage']
            except:
                return HttpResponse('GET Error!')
            cur_page = int(startpage)
            if username == '':
                scan_user = UserInfo.objects.all().order_by('userName')
            else:
                scan_user = UserInfo.objects.filter(userName__contains=username)
            user_pagi = Paginator(scan_user, int(offset))
            pageN = user_pagi.page(cur_page)
            after_page_num = 5
            before_page_num = 4
            scan_user_list = pageN.object_list
            results = []
            for useri in scan_user_list:
                results.append({'userid': useri.userId.username,
                                'username': useri.userName,
                                'usersex': useri.userSex,
                                'userage': useri.userAge,
                                'userphone': useri.userPhone})
            if cur_page - 1 > after_page_num:
                page_list = user_pagi.page_range[cur_page - 1 - after_page_num:cur_page - 1 + before_page_num]
            else:
                page_list = user_pagi.page_range[0:cur_page - 1 + before_page_num]
            ret = {'userList': results, 'pageList': list(page_list), 'currentPage': cur_page}
            return JsonResponse(ret)
        else:
            return HttpResponse('Permission Denied!')
    else:
        return HttpResponse('Permission Denied!')


# 管理员修改书籍的任意属性
def staff_change_book_info(request):
    if request.user.is_authenticated:
        cur_user = request.user
        if cur_user.is_staff:
            try:
                bookid = request.GET['bookid']
                bookname = request.GET['bookname']
                booktype = request.GET['booktype']
                bookpub = request.GET['bookpublisher']
                bookauthor = request.GET['bookauthor']
                bookintro = request.GET['bookintroduction']
                bookprice = request.GET['bookprice']
                booknum = request.GET['booknum']
                if bookid == '' or bookname == '' or booktype == '' or bookpub == '' \
                        or bookauthor == '' or bookintro == '' or bookprice == '' or booknum == '':
                    return JsonResponse({'end': True, 'msg': '请输入数据再进行操作！'})
            except:
                return JsonResponse({'end': False, 'msg': 'GET Error!'})
            try:
                book_fk = Book.objects.get(bookId=bookid)
                booknum_fk = BookNum.objects.get(bookId__bookId=bookid)
                book_fk.bookName = bookname
                book_fk.bookType = BookType.objects.get(TypeId=booktype)
                book_fk.bookPublisher = bookpub
                book_fk.bookAuthor = bookauthor
                book_fk.bookIntroduction = bookintro
                book_fk.bookPrice = bookprice
                book_fk.save()
                booknum_fk.bookNum = booknum
                booknum_fk.save()
                return JsonResponse({'end': True, 'msg': '更新书籍信息成功！'})
            except:
                return JsonResponse({'end': False, 'msg': '输入格式有误，更新操作失败，请重试！'})
        else:
            return JsonResponse({'end': False, 'msg': 'Permission Denied!'})
    else:
        return JsonResponse({'end': False, 'msg': 'Permission Denied!'})


# 主界面 用于管理员
def index_staff(request):
    if request.user.is_authenticated:
        cur_user = request.user
        if cur_user.is_staff:
            staff_info = StaffInfo.objects.get(staffId=cur_user)
            types = []
            for type in BookType.objects.all():
                types.append({'typeNum': type.TypeId, 'typeInfo': type.TypeName})
            cur_user_info = {'userId': cur_user.username, 'username': staff_info.staffName}
            return render(request, 'indexstaff.html', {'currentUser': cur_user_info,
                                                       'is_staff': True,
                                                       'typeList': types})
        else:
            return HttpResponseRedirect('/staff_view_user_info')  # 网站主页面为index 当用户非管理员时会跳转到user_info视图导向的界面
    else:
        return HttpResponseRedirect('/login_page')


from faker import Faker
import random
import pandas as pd


# 百万条数据的压力测试
def pressure_test(request):
    isTest = False  # 是否进行测试 设置为真时执行会添加数据
    if isTest:
        numTestEpoll = 600  # 每轮测试添加的数据数量 书籍表中的前100条书籍编号保留用于人工测试 后100w条用于随机生成添加

        bookTypes = BookType.objects.all()
        BOOKID = 980000  # 自定义开始添加数据的编号
        fake = Faker('zh_CN')  # 设置随机数据生成器
        cur_user = request.user

        try:
            for bookType in bookTypes:  # 对每个书籍类型依次进行添加
                for i in range(numTestEpoll):
                    testID = str(BOOKID)
                    bookid = BOOKID
                    BOOKID += 1
                    bookname = fake.company_prefix()
                    # bookname = '测试书' + testID
                    booktype = bookType
                    bookpublisher = fake.company()
                    # bookpublisher = '测试出版社' + testID
                    bookauthor = fake.name()
                    # bookauthor = '测试作者' + testID
                    bookintroduction = fake.sentence()
                    # bookintroduction = '测试简介' + testID
                    # bookprice = fake.random_int(min=20, max=200)
                    bookprice = random.randint(20, 200)
                    # booknum = fake.random_int(min=50, max=1000)
                    booknum = random.randint(50, 1000)
                    book_added = Book.objects.create(bookId=bookid,
                                                     bookName=bookname,
                                                     bookType=booktype,
                                                     bookPublisher=bookpublisher,
                                                     bookAuthor=bookauthor,
                                                     bookIntroduction=bookintroduction,
                                                     bookPrice=bookprice)
                    BookNum.objects.create(bookId=book_added, bookNum=booknum)
                    AddBook.objects.create(bookId=book_added,
                                           staffId=StaffInfo.objects.get(staffId=cur_user),
                                           addNum=booknum)
            return HttpResponse('Pressure Test Success')
        except:
            return HttpResponse('Pressure Test Fail!')
    else:
        return HttpResponse('Pressure Test Has Done!')
