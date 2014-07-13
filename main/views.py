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





class IndexView(TemplateView):
	template_name = "index.html"

pass





def submit(request):
	from main.models import File
	file1 = request.FILES['file']
	data = csv.reader(file1)
	email = request.POST['email']
	detail = File(csvfile=file1, email=email)
	detail.save()
	
	account_id = []
	for row in data:
		print row
		account_id.append(row)
	x =  account_id[0]
	current_acnt_id = []
	for i in x:
		current_acnt_id.append(i.split('_'))
	k = []	
	for j in current_acnt_id:
		k.append(j[1])
	
	#print k           #list of current account ids as strings
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
	for i in intlist:
		for j in id_list:
				payload = {'access_token': 'CAACcXbmWPQMBAHxPC0pKxsN5jZBzlR9UU1Vj8wMpZBkwwg1om63w4rlCh5oxMbkchL5KTwmWMOQtnSig1pKwoG6V7wuAbQ2mDoiarKglnN9a0CWdebQesJBVCrUO1WmyMmzMk6ZBixPLRzgNDhR4sd8JNrnoU5FsWfDKnls6anNJFjviDVj' ,'adaccounts': [i]} 
				r = requests.post('https://graph.facebook.com/'+j+'/adaccounts', data=payload)
				#counting the response
				if r.json()==1:
					Succeeded_request+=1
				else:
					failed_request+=1
				

	x = str(Succeeded_request)
	y = str(failed_request)
	attachment = File.objects.get(email=email)
	attachfile = attachment.csvfile

	mail = EmailMessage('Audience Sharing | File: <attachment.csv> | ['+x+'] Succeeded, ['+y+'] Failed', 'Custom Audience Sharing tool', to=[email])
	mail.attach('attachment.csv', attachfile.read(), 'text/csv')
	mail.send()

	return HttpResponseRedirect('/')



   
    
     
     
         
     

     
     
     





   


