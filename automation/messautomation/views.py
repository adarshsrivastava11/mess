from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate,login,logout

from django.shortcuts import redirect
from django.contrib.auth.decorators import *
import urllib2
import os
from random import randint
from bs4 import BeautifulSoup
from messautomation.models import *
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User


def email(to,subject,body):
    body = body + "\n\n -------------------------------------\n\n"+" This is an Auto Generated Email. For any queries contact Adarsh    "
    # print body
    send_mail(subject,body,'"Mess Automation" <noreply@hall3iitk.com>',[to],
                          fail_silently=False)

def main_page(request):
	project='Hello'
	now = datetime.now()
	now = now.strftime("%A")
	extras = Extras.objects.filter(day_of_week__contains=now,num=0)

	# return HttpResponse('Hello World!')
	return render(request,'index.html',{'project':project,'extra':extras})

def login_page(request):
	username = request.POST.get('username',False)
	password = request.POST.get('password',False)
	error = ""
	response = render(request,'login.html')
	if username != False:
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				current_user = request.user
				if current_user.has_perm('messautomation.add_student'):
					response = render(request,'login.html',{'error':error})
					response.set_cookie('ismess', 'yes941145287651819870377')
					#return redirect('/mess/')

				else:
					return redirect('/'+user.username+'/item_extra/')
		else:
			error = "Wrong Password!"
			response = render(request,'login.html',{'error':error})
	
	return response

def signup_view(request):
	name = request.POST.get('name',False)
	rollnumber = request.POST.get('rollnumber',False)
	random_num = str(randint(1,9))+str(randint(10,99))+str(randint(1,9))
	password = random_num
	error = ""
	if rollnumber != False:
		rollnumber = str(rollnumber)
		# print rollnumber
		if User.objects.filter(username=rollnumber).exists():
			error = "The roll number has already signed up :P"
		else:
			email_user = rollnumber+'@iitk.ac.in'
			# print email_user
			user = User.objects.create_user(username=rollnumber,password=password,email=email_user,first_name=name)
			user.save()
			student = Student(username=rollnumber,name=name,hall='HALL3',roll=rollnumber)
			student.save()
			to = email_user
			subject = "Mess Automation System:Your Password"
			body = "Your starting password is: "+password
			# print password
			email(to,subject,body)
			# print "Email Sent!"
			return redirect('/login/')

	return render(request,'signup.html',{'error':error})

def logout_view(request):
	logout(request)
	response = redirect('/')
	response.delete_cookie('ismess')
	return response
	# return redirect('/')

# @login_required
# def extra_login(request):
# 	response = render(request,'extra_login1.html')




# 	else:
# 		roll = request.POST.get('roll',False)
# 		if roll != False:
# 			return redirect('/'+roll+'/item_extra/')





# 	# return render(request,'extra_login1.html',{'roll':roll})
# 	return response
@login_required(login_url = '/login/')
def item_extra(request,rollnumber):
	user = User.objects.get(username=rollnumber)
	first_name = user.first_name
	last_name = user.last_name
	name = first_name+last_name

	img_url = "https://oa.cc.iitk.ac.in/Oa/Jsp/Photo/"+rollnumber+"_0.jpg"
	bdmr = 0
	#wiki = "http://home.iitk.ac.in/~himnshu/studentsearch/index.php?query="+rollnumber+"&gender=all&batch=all&hall=all&degree=all&dept=all&blood=all"
	#page = urllib2.urlopen(wiki)
	#soup = BeautifulSoup(page,"html.parser")
	#all_links=soup.find_all("a")
	#a = " = "
	#for link in all_links:
		#a= link.get("href")

	#b = a.split('=')
	#username = b[1]
	item_cost=0
	item_name=''
	hall = "HALL3"
	item_total_cost=0
	item_length = 0
	now = datetime.now()
	now = now.strftime("%A")

	username = ""
	#info = "http://home.iitk.ac.in/~himnshu/studentsearch/profile.php?username="+b[1]+""
	#page = urllib2.urlopen(info)
	#soup = BeautifulSoup(page,"html.parser")
	#all_p = soup.find_all("p")
	#name = soup.find_all("h4")
	extras = Extras.objects.filter(day_of_week__contains=now,num=0)
	guest=Extras.objects.filter(day_of_week__contains=now,num=1)
	item = request.POST.get('item_detail',False)

	item1 = item
	quantity = request.POST.get('item_quantity',False)
	try:
		student_getname = Student.objects.get(roll=rollnumber)
		username = student_getname.roll
		name = name+''
	except Exception:
		name = "Please Define Your Name in the DataBase"
	else:


		#c =  all_p[4].text.split(',')
		#hall= c[0]
		# if hall != 'HALL3':
		# 	return redirect('/')



		if item != False and quantity != False:
			item = item.split(',')

			quantity = quantity.split(',')

			item_length = len(item)
			for i in range(0,item_length-1):
				all_items = item[i]

				all_items = all_items.split('-')
				item_name = all_items[0]

				item_cost = int(all_items[1])

				quantity1 = quantity[i]
				quantity1 = int(quantity1)
				print quantity1

				if quantity > 0:
					item_total_cost = item_total_cost+(item_cost*quantity1)

				else:
					return redirect("/")

		try:
	      			student = Student.objects.get(roll=rollnumber)
	      			student.total_cost = student.total_cost+item_total_cost
	      			student.recent_item=item1

	      			if item1 != False:
	      				student.name = name


	      				student.all_items_total_cost = student.all_items_total_cost+str(item_total_cost)+','
	      				now = datetime.now()
	      				now = str(now)
	      				student.all_items_date= student.all_items_date+now+','
		  			student.save()
		  			ran_id = str(randint(1,9))+str(randint(10,99))+str(randint(100,999))

		  			token = Token(roll = rollnumber,name=name,time_taken=now,item_taken=" ".join(item1),total_cost=item_total_cost,ran_id=ran_id)
		  			token.save()
		  			student.token_ids = student.token_ids+ran_id+','
		  			student.save()
		  			fo = open("tokens/"+ran_id+".txt","w")
		  			file_data = "Name - "+name+"<br>Roll Number - "+rollnumber+"<br>Item - "+" ".join(item1)+"</br>Total Cost - "+str(item_total_cost)+"</br>Token Number - <bold> "+ran_id+"</bold>"+"</br> Time Taken - "+now
		  			fo.write(file_data)
		  			fo.close()
		  			return redirect('/'+ran_id+'/token/')

		except Student.DoesNotExist:
				user = User.objects.get(username=rollnumber)
				if user.DoesNotExist != True:
					student = Student(name=name,roll=rollnumber,total_cost=bdmr+item_cost,hall=hall,username=username,recent_item_cost=item_cost,recent_item_name=item_name)
		  			student.save()
		  		else:
		  			return redirect("/signup/")



	# if Student.objects.get(roll=rollnumber).exists():

	# 	student.total_cost = student.total_cost+item_cost
	# 	student.save()

	# else:
	# 	student = Student(roll=rollnumber,total_cost=bdmr+item_cost,hall=hall,username=username,recent_item_cost=item_cost,recent_item_name=item_name)
	# 	student.save()

	return render(request,'item_extra.html',{'img_url':img_url,'item_cost':item_name,'extras':extras,'username':username,'hall':hall,'rollnumber':rollnumber,'name':name,'guest':guest})

@login_required(login_url='/login/')
def student_view(request):
	user_current = request.user
	roll = user_current.username
	username = roll
	#roll = request.POST.get('roll',False)
	img_url=''
	temp=""
	name=''
	total_bill =''
	last_date=''
	details = []
	b = ""
	a = " = "
	if roll != False:
		#img_url = "http://oa.cc.iitk.ac.in:8181/Oa/Jsp/Photo/"+roll+"_0.jpg"

		#wiki = "http://home.iitk.ac.in/~himnshu/studentsearch/index.php?query="+roll+"&gender=all&batch=all&hall=all&degree=all&dept=all&blood=all"
		#page = urllib2.urlopen(wiki)
		#soup = BeautifulSoup(page,"html.parser")
		#all_links=soup.find_all("a")
		#for link in all_links:
			#a= link.get("href")

		#b = a.split('=')
		#username = b[1]

		#info = "http://home.iitk.ac.in/~himnshu/studentsearch/profile.php?username="+b[1]+""
		#page = urllib2.urlopen(info)
		#soup = BeautifulSoup(page,"html.parser")
		#all_p = soup.find_all("p")
		#name = soup.find_all("h4")
		#name = name[0].text.split(' ')
		#name = name[0]
		#c =  all_p[4].text.split(',')
		student1 = Student.objects.get(roll=roll)
		name = student1.name
		hall= "HALL3"
		try:
			student = Student.objects.get(roll=roll)
			total_bill = student.total_cost
			names = student.all_items_name.split(',')
			costs = student.all_items_cost.split(',')
			quantities = student.all_items_quantity.split(',')
			total_costs = student.all_items_total_cost.split(',')
			dates = student.all_items_date.split(',')
			token_ids = student.token_ids.split(',')
			detail_tokens = zip(dates,token_ids)
			length = len(names)
			length_dates = len(dates)
			length_tokens = len(token_ids)
			print length_dates
			last_date = dates[length_dates-2]
			
			last_date = last_date.split('.')

			last_date = last_date[0]
			

		except Student.DoesNotExist:
			user = User.objects.get(username=roll)
			if user.DoesNotExist != True:
				student = Student(name=name,roll=roll,total_cost=0,hall=hall,username=username,recent_item_cost=0,recent_item_name='')
	  			student.save()
	  		else:
	  			return redirect("/signup/")






	return render(request,'student_view.html',{'img_url':img_url,'name':name,'total_bill':total_bill,'last_date':last_date,'rollnumber':roll,'detail_tokens':detail_tokens})

@login_required
def mess_view(request):
	if request.COOKIES.get('ismess') != 'yes941145287651819870377':
		return redirect('/student_view/')
	student = Student.objects.all()
	tokens = Token.objects.all()
	rollnumber = request.POST.get('rollnumber',False)
	cost = request.POST.get('cost',False)

	if rollnumber != False and cost != False:
		student1 = Student.objects.get(roll=rollnumber)
		total_bill = student1.total_cost
		cost = int(cost)
		student1.total_cost = total_bill-cost
		student1.save()
	return render(request,'mess.html',{'students':student,'tokens':tokens})

@login_required
def token_view(request):
	if request.COOKIES.get('ismess') != 'yes941145287651819870377':
		return redirect('/student_view/')
	tokens = Token.objects.all()
	return render(request,'token_detail.html',{'tokens':tokens})

@login_required
def delete_all(request):
	if request.COOKIES.get('ismess') != 'yes941145287651819870377':
		return redirect('/student_view/')
	to = 'surajydv@iitk.ac.in'
	today = datetime.now()
	month = today.strftime('%B')
	subject = "Mess Bill for Month - "+month
	student = Student.objects.all()
	total = 0
	for students in student:
		total = students.total_cost + total
	body = "The Total is - "+str(total)

	email(to,subject,body)

	Student.objects.all().delete()

	return redirect('/mess/')


@login_required
def changepassword(request,rollnumber):
	current_user = request.user
	error = ''
	if current_user.username != rollnumber:
		return redirect('/login/')


	else:
		user = User.objects.get(username=rollnumber)
		oldpass = request.POST.get('oldpass',False)
		newpass = request.POST.get('newpass',False)
		if oldpass != False and newpass!= False:
			if user.check_password(oldpass):
				user.set_password(newpass)
				user.save()
				return redirect('/login/')
			else:
				error = 'Wrong!! Old Password,try again'

	return render(request,'changepassword.html',{'error':error,'rollnumber':rollnumber})

def backup_data(request):
	student = Student.objects.all()
	return render(request,'backup.html',{'students':student})

def forgot_password(request):
	logout(request)
	rollnumber = request.POST.get('rollnumber',False)
	error = ""
	if rollnumber != False:
		if User.objects.filter(username=rollnumber).exists():

			email_user = rollnumber+'@iitk.ac.in'
			user = User.objects.get(username=rollnumber)
			random_num = str(randint(1,9))+str(randint(10,99))+str(randint(1,9))
			newpassword = random_num
			user.set_password(newpassword)
			user.save()
			to = email_user
			subject = "Your New Password"
			body = "Your changed password is: "+newpassword
			email(to,subject,body)
			return redirect('/login/')
		else:
			error = "not_signed_up" #do not edit this text
 	return render(request,'forgotpass.html',{'error':error})

def token_generator(request,tokennum):
	user_current = request.user
	rollnumber = user_current.username
	img_url = "https://oa.cc.iitk.ac.in/Oa/Jsp/Photo/"+rollnumber+"_0.jpg"
	fo = open("tokens/"+tokennum+".txt","r+")
	data = fo.read()
	fo.close()
	return render(request,'token.html',{'data':data,'image_url':img_url,'token_id':tokennum})
