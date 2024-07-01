function initUserScan(userName,Page)
{
	$('#startpage').val(Page);
	var userHtml = '',pageHtml = '';
	var username = userName;
	var offset = $('#offset').val(),startPage = Page;
	$.get('/staff_view_user',{'username':username,'offset':offset,'startpage':startPage},function(data)
	{
		for(var i=0;i<data.userList.length;i++)
		{
			userItem = data.userList[i];
			// 构建用于显示的HTML
			userHtml += '<a href="/staff_view_user_info/?userid='+userItem.userid+'" class="userItem">'+
						'<div><span>用户ID：'+userItem.userid+'</span>&nbsp;&nbsp;&nbsp;<span>用户名：'+userItem.username+'</span></div>'+
						'<div><span>用户年龄：'+userItem.userage+'</span></div>'+
						'<div><span>用户联系方式：'+userItem.userphone+'</span></div>'+
						'</a>';
		}
		$('.templateUserContainer').html(userHtml);

		if(startPage!=1){pageHtml = '<button class="prev pageBtn"><<</button>';}
		for(var i=0;i<data.pageList.length;i++)
		{
			pageItem = data.pageList[i];
			if(pageItem == data.currentPage)pageHtml += '<button class="active pageBtn">'+pageItem+'</button>';
			else pageHtml += '<button class="pageBtn">'+pageItem+'</button>';
		}
		if(startPage != data.pageList[data.pageList.length-1])pageHtml += '<button class="next pageBtn">>></button>';
		$('.pageList').html(pageHtml);
		$('.pageBtn').click(function(event)
		{
			if($(this).hasClass('next'))targetPage = parseInt($('#startPage').val())+1;
			else if($(this).hasClass('prev'))targetPage = parseInt($('#startPage').val())-1;
			else targetPage = $(this).text();
			initUserScan($('#changeUserName').val(),targetPage);
		});
	});
}

initUserScan('',1);

$(document).ready(function()
{
	var typeOptions_Id = [];
	var typeOptions_Info = [];
	$.get('/get_book_types', function(data)
	{
	    typeOptions_Id = data.typeId;
	    typeOptions_Info = data.typeInfo;
    });

    // 浏览用户信息
	$('.changeUserBtnCheck').click(function(event) {initUserScan($('#changeUserName').val(),1);});

    // 还书反馈
	$('.returnBtnCheck').click(function(event)
	{
		var bookid=$('#returnBookid').val();
		var userid=$('#returnUserid').val();
		$.get('/staff_return_book',{"bookid":bookid,"userid":userid},function(data)
		{
			$('.returnBookMsg').removeClass('success').removeClass('fail').text("");
			if(data.msg=='请输入数据再进行操作！')$('.returnBookMsg').addClass('success').text(data.msg);
			else
			{
			    bookid=$('#returnBookid').val("");
                userid=$('#returnUserid').val("");
			    if(data.end)$('.returnBookMsg').addClass('success').text(data.msg);
			    else $('.returnBookMsg').addClass('fail').text(data.msg);
			}
		});
	});

    // 借书反馈
	$('.borrowBtnCheck').click(function(event)
	{
		var bookid=$('#borrowBookid').val();
		var userid=$('#borrowUserid').val();
		$.get('/staff_borrow_book',{"bookid":bookid,"userid":userid},function(data)
		{
		    console.log(data)
			$('.borrowBookMsg').removeClass('success').removeClass('fail').text("");
			if(data.msg=='请输入数据再进行操作！')$('.borrowBookMsg').addClass('success').text(data.msg);
			else
			{
                $('#borrowBookid').val("");
                $('#borrowUserid').val("");
                if(data.end)$('.borrowBookMsg').addClass('success').text(data.msg);
                else $('.borrowBookMsg').addClass('fail').text(data.msg);
			}
		});
	});

	// 添加图书信息的反馈
	$('.createBtnCheck').click(function(event)
	{
		var bookid = $('#createBookId').val();
		var bookname = $('#createBookName').val();
		var booktype = $('#createBookType').val();
		var bookpub = $('#createBookPub').val();
		var bookauthor = $('#createBookAuthor').val();
		var bookintro = $('#createBookIntro').val();
		var bookprice = $('#createBookPrice').val();
		var booknum = $('#createBookNum').val();
		$.get('/staff_add_book',
			{"bookid":bookid,
			"bookname":bookname,
			"booktype":booktype,
			"bookpublisher":bookpub,
			"bookauthor":bookauthor,
			"bookintroduction":bookintro,
			"bookprice":bookprice,
			"booknum":booknum},function(data)
			{
			    console.log(data);
			    $('.addBookMsg').removeClass('success').removeClass('fail').text("")
			    if(data.msg=='请输入数据再进行操作！')$('.addBookMsg').addClass('success').text(data.msg)
			    else
			    {
                    $('#createBookId').val("");
                    $('#createBookName').val("");
                    $('#createBookType').val("");
                    $('#createBookPub').val("");
                    $('#createBookAuthor').val("");
                    $('#createBookIntro').val("");
                    $('#createBookPrice').val("");
                    $('#createBookNum').val("");
                    if(data.end)$('.addBookMsg').addClass('success').text(data.msg)
                    else $('.addBookMsg').addClass('fail').text(data.msg)
			    }
		    });
	});

	// 添加图书数量的反馈
	$('.addBtnCheck').click(function(event)
	{
		var bookid = $('#addBookId').val();
		var addnum = $('#addBookNum').val();
		$.get('/staff_alter_book',{"bookid":bookid,"addbooknum":addnum},function(data)
		{
			console.log(data);
			$('.addNumMsg').removeClass('success').removeClass('fail').text("");
			if(data.msg=='请输入数据再进行操作！')$('.addNumMsg').addClass('success').text(data.msg);
			else
			{
			    $('#addBookId').val("");
			    $('#addBookNum').val("");
			    if(data.end)$('.addNumMsg').addClass('success').text(data.msg);
			    else $('.addNumMsg').addClass('fail').text(data.msg)
			}
		});
	});

	// 更改图书信息的反馈
	$('.changeBookBtnCheck').click(function(event)
	{
		var template ='';
		var bookid = $('#changeBookId').val();
		$.get('/viewbook',{"mode":"Detail","startpage":0,"offset":10,"booklikename":bookid},function(data)
		{
		    optionTemplate = '';
		    for(var i=0;i<typeOptions_Id.length;i++)
		    {
		        option = typeOptions_Id[i];
		        optionName = typeOptions_Info[i];
		        if(optionName == data.msg.booktype)
		            optionTemplate+='<option value="'+option+'" selected="true">'+optionName+'</option>'
		        else optionTemplate+='<option value="'+option+'">'+optionName+'</option>'
		    }
			console.log(data);
            $('.changeBookCheckMsg').removeClass('success').removeClass('fail').text("");
            if(bookid == '')$('.changeBookCheckMsg').addClass('success').text('请输入数据再进行操作！');
            else
            {
                if(data.end)
                {
                    $('.changeBookCheckMsg').addClass('success').text('检索成功！');
                    template += '<input class="changeBookId" value="'+data.msg.bookId+'" type="hidden"/>'+
                                '<div class="line">'+
                                    '<span>图书名称：</span><input type="text" class="changeBookName" value="'+data.msg.bookName+'"/>'+
                                '</div>'+
                                '<div class="line">'+
							        '<span>图书类型：</span>'+'<select class="changeBookType">'+optionTemplate+'</select>'+
						        '</div>'+
                                '<div class="line">'+
                                    '<span>作者：</span><input type="text" class="changeBookAuthor" value="'+data.msg.bookAuthor+'"/>'+
                                '</div>'+
                                '<div class="line">'+
                                    '<span>出版社：</span><input type="text" class="changeBookPublisher" value="'+data.msg.bookPublisher+'"/>'+
                                '</div>'+
                                '<div class="line">'+
                                    '<span>简介：</span><input type="text" class="changeBookIntro" value="'+data.msg.bookIntroduction+'"/>'+
                                '</div>'+
                                '<div class="line">'+
                                    '<span>价格：</span><input type="text" class="changeBookPrice" value="'+data.msg.bookPrice+'"/>'+
                                '</div>'+
                                '<div class="line">'+
                                    '<span>库存：</span><input type="text" class="changeBookNum" value="'+data.msg.bookNum+'"/>'+
                                '</div>';
                    $('.templateBookContainer').html(template);
                    $('.changeBookBtnSubmit').removeClass('hid');
                }
                else $('.changeBookCheckMsg').addClass('fail').text(data.msg);
            }
		});
	});

	// 更改提交按钮的反馈
	$('.changeBookBtnSubmit').click(function(event)
	{
		var bookid = $('.changeBookId').val();
		var bookname = $('.changeBookName').val();
		var booktype = $('.changeBookType').val();
		var bookauthor = $('.changeBookAuthor').val();
		var bookpublisher = $('.changeBookPublisher').val();
		var bookintro = $('.changeBookIntro').val();
		var bookprice = $('.changeBookPrice').val();
		var booknum = $('.changeBookNum').val();
		$.get('/staff_change_book_info',
			{"bookid":bookid,
			"bookname":bookname,
			"booktype":booktype,
			"bookauthor":bookauthor,
			"bookpublisher":bookpublisher,
			"bookintroduction":bookintro,
			"bookprice":bookprice,
			"booknum":booknum},function(data)
            {
                console.log(data);
                $('.changeBookSubmitMsg').removeClass('success').removeClass('fail').text("");
                if(data.msg=='请输入数据再进行操作！')$('.changeBookSubmitMsg').addClass('success').text(data.msg);
                else
                {
                    if(data.end)$('.changeBookSubmitMsg').addClass('success').text(data.msg)
                    else $('.changeBookSubmitMsg').addClass('fail').text(data.msg)
                }
            });
	});
});
