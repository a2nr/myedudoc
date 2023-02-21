from gquiz import gquiz
import requests

q = gquiz()

q.generateService()

q.copy_file("16-rh3W-NwYzdKVBZJmi574sTWe_rMIdE-FQSw_33qXI", "Soal Masuk Penjara")
opt = [{"value" : "Salim sama hitler"},
       {"value" : "Memprovokasi suku jawa untuk membantu suku dayak ditragedi sampit"},
       {"value" : "Mengkorupsi beras subsidi bantuan sosial dari pemerintah"},
       {"value" : "Tidak menyapa Yuno dengan ~yuunoochiii~ ketika bertemu"},
       {"value" : "Membuatkan ayah kopi dengan mengganti gula dengan boncabe"},
       ]

qq = q.createQuestion(title = "Soal No 1", description = "Cobalah untuk menebak apa yang ada dipikiran dia ketika dia dapat mengulang waktu kembali?", indexAnswer = 4, options = opt, itemImage='/home/a2nr/Pictures/a/miyako_thinking.png')
q.submitQuestion(0,qq)
q.update()
