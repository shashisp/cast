from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
import csv
from urllib2 import urlopen
from simplejson import loads
import chardet
import StringIO
import requests
import json
from main.models import File
from django.core.mail import EmailMessage
import time
import datetime





class IndexView(TemplateView):
	template_name = "index.html"

pass



_file_id = 0

def submit(request):
	from main.models import File
	start_time = time.strftime('%x %X %z')
	a = datetime.datetime.now()
	file1 = request.FILES['file']
	data = csv.reader(file1)
	email = request.POST['email']
	global _file_id
	#_file_count+=1
	#print _file_id
	
	detail = File(csvfile=file1, email=email, pid=_file_id)
	
	detail.save()
	
	
	
	account_id = []
	for row in data:
		#print row
		account_id.append(row)
	#print account_id
	x = []
	for i in account_id:
		for k in i:
			print k
			x.append(k)
	
	
	current_acnt_id = []
	for i in x:
		current_acnt_id.append(i.split('_'))
	k = []	
	for j in current_acnt_id:
		k.append(j[1])
	
	print k

	           #list of current account ids as strings
	intlist = []
	for i in k:
		j = int(i)
		intlist.append(j)
		#print j
	#print intlist      # account ids typecasted in to integers

		
	
 
	id_list = []
	for i in x:
		data = requests.get('https://graph.facebook.com/'+i+'/customaudiences?fields=account_id&access_token=CAACcXbmWPQMBAHxPC0pKxsN5jZBzlR9UU1Vj8wMpZBkwwg1om63w4rlCh5oxMbkchL5KTwmWMOQtnSig1pKwoG6V7wuAbQ2mDoiarKglnN9a0CWdebQesJBVCrUO1WmyMmzMk6ZBixPLRzgNDhR4sd8JNrnoU5FsWfDKnls6anNJFjviDVj')
		jsondata = data.json()['data']
		print jsondata
		
		for j in jsondata:
			if j['account_id'] in intlist:
				id_list.append(j['id']) #getting list of ID's
	
	failed_request = 0
	Succeeded_request = 0
	mailresponse = []
	sucess_ids = []
	failed_ids = []
	for i in intlist:
		for j in id_list:
				payload = {'access_token': 'CAACcXbmWPQMBAHxPC0pKxsN5jZBzlR9UU1Vj8wMpZBkwwg1om63w4rlCh5oxMbkchL5KTwmWMOQtnSig1pKwoG6V7wuAbQ2mDoiarKglnN9a0CWdebQesJBVCrUO1WmyMmzMk6ZBixPLRzgNDhR4sd8JNrnoU5FsWfDKnls6anNJFjviDVj' ,'adaccounts': [i]} 
				r = requests.post('https://graph.facebook.com/'+j+'/adaccounts', data=payload)
				#counting the response
				if r.json()==1:
					sucess_ids.append(j)
					Succeeded_request+=1
				else:
					failed_request+=1
					failed_ids.append(j)
				

	x = str(Succeeded_request)
	y = str(failed_request)

	attachment = File.objects.get(pid=_file_id)
	_file_id+=1
	attachfile = attachment.csvfile
	last_time = time.strftime('%x %X %z')
	b = datetime.datetime.now()
	Duration = (b-a)
	email_body = """Submitted  at:"""+start_time+"""
Finished at: """+last_time+"""
Duration : """+str(Duration)+"""
Succeeded : """+x+"""
Failed : """+y
   	"""
   		creating log files of 	
	sucess_ids_str = ''.join(sucess_ids)
	failed_ids_str = ''.join(failed_ids)
	log =open("sucess_logs.txt", "a")
	log.write(sucess_ids_str)
	log.close()
	"""

	mail = EmailMessage('Audience Sharing | File: '+attachfile.name.split('/')[4]+'| '+x+' Succeeded, '+y+' Failed', email_body, to=[email])
	mail.attach(attachfile.name.split('/')[4], attachfile.read(), "text/csv")
	#mail.attach('sucess_ids.txt', 'sucess_ids.txt', 'text')
	mail.send()
	_file_id+=1
	

	return HttpResponseRedirect('/')



   
    
     
     
         
     

     
     
     





   


