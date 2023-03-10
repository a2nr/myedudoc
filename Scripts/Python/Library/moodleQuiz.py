# coding: utf-8
from __future__ import unicode_literals
import base64
import xml.etree.ElementTree as ET

class moodleQuiz:
    def __init__(self):
        self.infoPrint = self._defaultPrint
        self.progress = -1
        self.resultUri = ""
        self.data = ET.Element('quiz')

    def setProgress(self, i : int):
        self.progress = i
        self.infoPrint("generating...", self.progress)
        
    def AttachProcessInfo(self, callback):
        self.infoPrint = callback

    def _defaultPrint(self, text : str, progress: int):
        print("{}% {}".format(progress, text))

    def _subElementFile(self, parent, file):
        Efile = ET.SubElement(parent, "file")
        Efile.set('name',file.name.split("/").pop())
        Efile.set('path','/')
        Efile.set('encoding','base64')
        Efile.text = base64.b64encode(file.read()).decode('utf-8')

    def createOption(self, value, image=None):
        ans = ET.Element('answer')
        ans.set('fraction', '0')
        ans.set('format', 'html')
        if(image == None):
            ET.SubElement(ans, 'text').text = "<p dir=\"ltr\" style=\"text-align: left;\">{}</p>".format(value)
        else :
            f = open(image,"rb")
            ET.SubElement(ans, 'text').text = "<p dir=\"ltr\" style=\"text-align: left;\">" + \
                    "<img src=\"@@PLUGINFILE@@/{}\" alt=\"{}\" class=\"img-fluid atto_image_button_text-bottom\"></p>"\
                    .format(f.name.split("/").pop(), f.name.split("/").pop().split(".")[0])
            self._subElementFile(ans, f)
        ET.SubElement(ET.SubElement(ans,'feedback'), 'text').text = "Ooopss!"
        return ans


    def createQuestion(self, title, description, options, indexAnswer, itemImage=None):
        question = ET.Element('question')
        question.set('type','multichoice')

        ET.SubElement(ET.SubElement(question, 'name'), 'text')\
                .text = title

        descQuestion = ET.SubElement(question, 'questiontext')
        descQuestion.set('format', 'html')
        descText = ET.SubElement(descQuestion, 'text')
        descText.text = "<p dir=\"ltr\" style=\"text-align: left;\">{}</p>".format(description)

        if (itemImage != None):
            f = open(itemImage,"rb")
            descText.text = descText.text + "<p dir=\"ltr\" style=\"text-align: left;\">" + \
                    "<img src=\"@@PLUGINFILE@@/{}\" alt=\"{}\" class=\"img-fluid atto_image_button_text-bottom\"></p>"\
                    .format(f.name.split("/").pop(), f.name.split("/").pop().split(".")[0])
            self._subElementFile(descQuestion, f)

        for i in range(0, len(options)):
            ans = options[i]
            if i == (indexAnswer-1) : 
                ans.set('fraction', '100')
                ans.find('feedback').find('text').text = "YES!"
            question.append(ET.fromstring(ET.tostring(ans)))

        ET.SubElement(question, 'shuffleanswers').text = '0'
        ET.SubElement(question, 'answernumbering').text = 'abc'
        return question

    def submitQuestion(self, index, item):
        self.data.append(ET.fromstring(ET.tostring(item)))

    def copyFile(self,origin_file_id, copy_title):
        print("noting to copy, it for moodle")

    def update(self):
        ET.indent(self.data)
        print(ET.tostring(self.data))
        ET.ElementTree(self.data).write("./moodleXMLMultichoiceQuestion.xml")


