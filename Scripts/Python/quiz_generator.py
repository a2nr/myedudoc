# coding: utf-8
from __future__ import unicode_literals
from scriptforge import CreateScriptService


def generateTemplate():
	doc = CreateScriptService("Calc")
	basic = CreateScriptService("Basic")
	doc.SetArray(doc.CurrentSelection, \
	  (("<Text question>","<IMG question image>", \
	    "<isAnswerA>", "<IMG option1>", "<Text Option1>",  \
	    "<isAnswerB>", "<IMG option2>", "<Text Option2>",  \
	    "<isAnswerC>", "<IMG option3>", "<Text Option3>",  \
	    "<isAnswerD>", "<IMG option4>", "<Text Option4>",  \
	    "<isAnswerE>", "<IMG option5>", "<Text Option5>", ),))
			
def updateQuestion():
  import sys, os
  from unohelper import fileUrlToSystemPath
  if not 'gquiz' in sys.modules:
    doc = XSCRIPTCONTEXT.getDocument()
    url = fileUrlToSystemPath('{}/{}'.format(doc.URL,'Scripts/python/Library'))
    sys.path.insert(0, url)
    
  from gquiz import gquiz
  import requests
	
  doc = CreateScriptService("Calc")
  selctedCell = doc.CurrentSelection
  
  q = gquiz()
  q.generateService()
  q.createForm("Demo Soal")
	cwd = os.getcwd()
  for nrow in range(0, doc.LastRow(selctedCell)+1-doc.FirstRow(selctedCell)):
    item = doc.getValue(doc.Offset(doc.FirstCell(selctedCell),nrow,0,1,17))
    opt = []
    theAnswer = -1
    c = 1
    
    for o in range(2,17,3):
      if (item[o] == 1):
        theAnswer = c
      c = c+1
      if (item[o+1] != ""): 
        opt.append(q.createOption(item[o+2],cwd+item[o+1]))
      else:
        opt.append(q.createOption(item[o+2]))
    
    if (theAnswer == -1):
      raise Exception("Chose the correct answer")	

    if( item[1] != ""):
      img = cwd+item[1]
    else:
      img = None
      
    qq = q.createQuestion(title = "Soal No 1",\
      description = item[0],\
      indexAnswer = theAnswer, \
      options = opt, itemImage=img)
    q.submitQuestion(nrow,qq)
  q.update()	
	
g_exportedScripts = (generateTemplate, updateQuestion, )
