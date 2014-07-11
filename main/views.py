from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
import csv
from urllib2 import urlopen
from simplejson import loads
import chardet
import StringIO



class IndexView(TemplateView):
	template_name = "index.html"

pass





def submit(request):
	data = csv.reader(request.FILES['file'])
	email = request.POST['email']
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
	print k

		
	"""
	account_id = ['act_1377346239145180', 'act_1382514281960557']
	current_acnt_id = []
	for i in account_id:
		y = i.split('_')
		current_acnt_id.append(y[1])
		"""

	for i in x:
		data = loads(urlopen('https://graph.facebook.com/'+i+'/customaudiences?fields=account_id&access_token=CAACcXbmWPQMBAHxPC0pKxsN5jZBzlR9UU1Vj8wMpZBkwwg1om63w4rlCh5oxMbkchL5KTwmWMOQtnSig1pKwoG6V7wuAbQ2mDoiarKglnN9a0CWdebQesJBVCrUO1WmyMmzMk6ZBixPLRzgNDhR4sd8JNrnoU5FsWfDKnls6anNJFjviDVj').read())
		print data

	

	return HttpResponseRedirect('/')


def upload(request):
	email = request.POST['email']
	#paramFile = request.FILES['file'].read()
	data = csv.DictReader(request.FILES['file'])


	#data = csv.DictReader(paramFile)
	list1 = []
	for row in data:
		list1.append(row)
	
	print list1
	"""
	content = f.read()
	encoding = chardet.detect(content)['encoding']
	if encoding != 'utf-8':
         content = content.decode(encoding, 'replace').encode('utf-8')

   	filestream = StringIO.StringIO(content)
   	dialect = csv.Sniffer().sniff(content)
   	reader = csv.DictReader(filestream.read().splitlines(), dialect=dialect)
   	print email
   	for row in reader:
   		print row
   		"""
   
   	return HttpResponseRedirect('/')

   
    
     
     
         
     

     
     
     





   


