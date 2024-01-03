# coding: utf-8
from __future__ import unicode_literals
import sys, os
import requests
import importlib

# to run separatly from soffice
# $ soffice --calc --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"

# uncomemnt for run separatly from soffice
# sys.path.append("/lib64/libreoffice/program/")

from scriptforge import ScriptForge, CreateScriptService
from unohelper import fileUrlToSystemPath

#[start] comment for run separatly from soffice
if (not 'gquiz' in sys.modules) or (not 'moodleQuiz' in sys.modules):
    doc = XSCRIPTCONTEXT.getDocument()
    url = fileUrlToSystemPath('{}/{}'.format(doc.URL,'Scripts/python/Library'))
    sys.path.insert(0, url)
else:
    importlib.reload(gquiz)
    importlib.reload(moodleQuiz)

#[end]
#[start] uncomemnt for run separatly from soffice
#sys.path.insert(0, '{}/{}'.format(os.getcwd(),'Library'))
#ScriptForge(hostname='localhost', port=2002)
#[end]

from gquiz import gquiz
from moodleQuiz import moodleQuiz

ui = CreateScriptService("UI")
doc = CreateScriptService("Calc")
bas = CreateScriptService("Basic")

def MakeTemplate():
    doc.SetArray(doc.CurrentSelection, \
            (("<Text question>","<IMG question image>", \
            "<isAnswerA>", "<IMG option1>", "<Text Option1>",  \
            "<isAnswerB>", "<IMG option2>", "<Text Option2>",  \
            "<isAnswerC>", "<IMG option3>", "<Text Option3>",  \
            "<isAnswerD>", "<IMG option4>", "<Text Option4>",  \
            "<isAnswerE>", "<IMG option5>", "<Text Option5>", ),))

def _statusBarInfoUpdate(text : str, progress : int):
    ui.SetStatusbar("{}% {}".format(progress,text), progress)

def _updateQuestion(q):
    selctedCell = doc.CurrentSelection
    cwd = os.getcwd()
    maxRow = doc.LastRow(selctedCell)+1-doc.FirstRow(selctedCell)
    for nrow in range(0, maxRow):
        q.setProgress(int(((nrow+1)/maxRow)*100))
        item = doc.getValue(doc.Offset(doc.FirstCell(selctedCell),nrow,0,1,17))
        opt = []
        theAnswer = -1
        c = 1
        for o in range(2,17,3):
            if (item[o] == 1):
                theAnswer = c
            if (item[o+1] != ""): 
                opt.append(q.createOption("{}. {}".format(chr(64+c),item[o+2]),cwd+item[o+1]))
            else:
                opt.append(q.createOption("{}. {}".format(chr(64+c),item[o+2])))
            c = c+1
    
        if (theAnswer == -1):
            raise Exception("Chose the correct answer")	
    
        if( item[1] != ""):
            img = cwd+item[1]
        else:
            img = None
    
        qq = q.createQuestion(title = "Soal No {}".format(nrow+1),\
                description = item[0],\
                indexAnswer = theAnswer, \
                options = opt, itemImage=img)
        q.submitQuestion(nrow,qq)
    q.update()	

def GoogleQuiz():
    q = gquiz()
    q.AttachProcessInfo(_statusBarInfoUpdate)
    q.setProgress(0)
    q.generateService()
    q.createForm("Demo Soal")
    _updateQuestion(q)
    ui.SetStatusbar("creating google form quiz done!")
    bas.InputBox("Open link to edit your form:","Your Google Form Quiz, done!", "{}".format(q.resultUri))

def MoodleQuiz():
    q = moodleQuiz()
    q.AttachProcessInfo(_statusBarInfoUpdate)
    q.setProgress(0)
    _updateQuestion(q)
    ui.SetStatusbar("Done!")
    bas.MsgBox("Check *.xml file in curent folder!")

g_exportedScripts = (MakeTemplate, GoogleQuiz, MoodleQuiz)
