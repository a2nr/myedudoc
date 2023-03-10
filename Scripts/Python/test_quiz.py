# coding: utf-8
from __future__ import unicode_literals

import sys, requests, os
from unohelper import fileUrlToSystemPath

sys.path.insert(0, "{}/{}".format(os.getcwd(),"Library"))
from gquiz import gquiz
from moodleQuiz import moodleQuiz
	
def test(q):
    opt = [	q.createOption("A.","./asset/option1.png"),
            q.createOption("B.","./asset/option2.png"),
            q.createOption("C.","./asset/option3.png"),
            q.createOption("D.","./asset/option4.png"),
            q.createOption("E.","./asset/option5.png") ]
    qq = q.createQuestion(title = "Soal No 1",\
            description = "Dari gambar dibawah ini, ada bagian gambar yang hilang. Dari pilihan dibawah, manakah gambar yang benar?",\
            indexAnswer = 4, options = opt, itemImage='./asset/test_image.png')
    q.submitQuestion(0,qq)
    q.update()

os.system("mkdir asset && mkdir secret")
os.system("cp ../../asset/* ./asset")
os.system("cp ../../secret/client_secrets.json ./secret")

q = moodleQuiz()
test(q)

q = gquiz()
q.generateService()
q.createForm("test")
test(q)
