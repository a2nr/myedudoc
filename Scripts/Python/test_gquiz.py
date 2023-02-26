# coding: utf-8
from __future__ import unicode_literals

import sys, requests
from unohelper import fileUrlToSystemPath

def gquiz_test():
	if not 'gquiz' in sys.modules:
		doc = XSCRIPTCONTEXT.getDocument()
		url = fileUrlToSystemPath('{}/{}'.format(doc.URL,'Scripts/python/Library'))
		sys.path.insert(0, url)
	from gquiz import gquiz
	
	q = gquiz()

	q.generateService()

	q.copyFile("16-rh3W-NwYzdKVBZJmi574sTWe_rMIdE-FQSw_33qXI", "Soal Masuk Penjara")
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
