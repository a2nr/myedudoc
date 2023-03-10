# coding: utf-8
from __future__ import unicode_literals

import os.path, time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pprint import pprint
import requests
from urllib.parse import urlparse

class gquiz:
    def __init__(self):
        '''
        Args : 
            templateId : get the id from link GoogleForm
        '''
        self.image_temp_service_url = "https://tmpfiles.org/api/v1/upload"
        # self.image_temp_service_url = "https://uguu.se/upload.php"
        self.submition = {"requests":[]}
        self.form_service = None
        self.drive_service = None 
        self.main_form = None
        self.infoPrint = self._defaultPrint
        self.progress = -1
        self.resultUri = ""

        self.submition["requests"].append({
            "updateSettings": {
                "updateMask": "*" ,
                "settings": {
                    "quizSettings": {
                        "isQuiz": True 
                        }
                    }
                }
            })

    def setProgress(self, i : int):
        self.progress = i
    def AttachProcessInfo(self, callback):
        self.infoPrint = callback

    def _defaultPrint(self, text : str, progress: int):
        print("{}% {}".format(progress, text))

    def generateService(self):
        ''' Start Tokenizing
         here is the way to get token 
         link : https://developers.google.com/docs/api/quickstart/python
        '''
        SCOPES = ["https://www.googleapis.com/auth/forms.body",
                  "https://www.googleapis.com/auth/drive",
                  "https://www.googleapis.com/auth/drive.file",
                  "https://www.googleapis.com/auth/drive.appdata"]
        DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            self.infoPrint("token already exist",self.progress)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                self.infoPrint("refresh token",self.progress)
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './secret/client_secrets.json', SCOPES)
                creds = flow.run_local_server(port=0)
                self.infoPrint("generate token",self.progress)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            self.infoPrint("creating service",self.progress)
            service = build('docs', 'v1', credentials=creds)
            self.form_service, self.drive_service = \
                    build('forms', 'v1', credentials=creds, discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False),\
                    build('drive', 'v3', credentials=creds)

        except HttpError as err:
            print(err)
        ''' End Tokenizing
        '''

    def createForm(self, name):
        """ Create Form
            Args: 
            name : name form
        """
        try: 
            self.infoPrint("creating form",self.progress)
            self.main_form = self.form_service.forms().create(body={"info":{"title":name}}).execute()
        except HttpError as error:
            print('An error occurred: %s' % error)			

    def copyFile(self,origin_file_id, copy_title):
        """Copy an existing file.
        Args:
          service: Drive API service instance.
          origin_file_id: ID of the origin file to copy.
          copy_title: Title of the copy.

        Returns:
          The copied file if successful, None otherwise.
        """

        try:
            if((self.drive_service == None) or (self.form_service == None)):
                raise Exception('please generate service first')

            newFormId = self.drive_service.files().copy(\
                  fileId=origin_file_id, body={"name":copy_title})\
                  .execute()
            print(newFormId)
            self.main_form = self.form_service.forms().get(formId=newFormId["id"]).execute()

        except HttpError as error:
            print('An error occurred: %s' % error)

    def createOption(self, value, image=None):
        '''
        return {"value" : "A. option 1"}
        return {"value": "Option",
                "image": {
                    "sourceUri": "",
                    "properties": {
                        "alignment": "LEFT"
                    }
                }}
        '''
        self.infoPrint("creating option",self.progress)
        opt = {"value" : "{}".format(value)}
        if(image != None):
            self.infoPrint("uploading option image... ",self.progress)
            req = requests.post(self.image_temp_service_url,files={"file": open(image,'rb')})
            if(req.json()['status'] == 'error'):
                raise Exception("upload failed : {}".format(req.json()))
            time.sleep(3)
            self.infoPrint("uploading option image... ok",self.progress)
            u = urlparse(req.json()['data']['url'])
            opt.update({"image" : {
                        "sourceUri": u._replace(path="/dl"+u.path).geturl(),
                        "properties": {
                            "alignment": "LEFT"
                            }
                        }})
        time.sleep(3)
        return opt

    def createQuestion(self, title, description, options, indexAnswer, itemImage=None):
        '''
        Args: 
            "title"         : String
            "desc"          : String
            "indexAnswer"   : Integer, index for "options"
            "options"       : 
                  [{"value" : "A. option 1"},
                   {"value" : "B. option 2"},
                   {"value" : "C. option 3"},
                   {"value" : "D. option 4"},
                   {"value" : "E. option 5"},]
        '''
        item = {
            "title" : title,
            "description" : "{}".format(description),
            "questionItem" : {
                "question" : {
                    "grading" : {
                        "pointValue": 1,
                        "correctAnswers": {
                            "answers" : [ {"value": "{}".format(options[indexAnswer-1]["value"])} ]
                            }
                        },
                    "choiceQuestion" : {
                        "type" : "RADIO", 
                        "options" : options
                        }
                    }
                }
            }
        self.infoPrint("create question...",self.progress)
        if (itemImage != None):
            self.infoPrint("uploading question image...",self.progress)
            req = requests.post(self.image_temp_service_url,files={"file": open(itemImage,'rb')})
            if(req.json()['status'] == 'error'):
                raise Exception("upload failed : {}".format(req.json()))
            time.sleep(3)
            self.infoPrint("uploading question image... ok",self.progress)
            u = urlparse(req.json()['data']['url'])
            item['questionItem'].update(\
                    {"image": {
                        "sourceUri": u._replace(path="/dl"+u.path).geturl(),
                        "properties": {
                            "alignment": "CENTER"
                            }
                        }
                     })
        return item

    def submitQuestion(self, index, item):
        """ Submit item to submition
        Args: 
            index : location item in form
            item  : object item
        """
        self.submition['requests'].append({
            "createItem" : {
                "location": {"index": index},
                "item": item
                }
        })
        self.infoPrint("submit question",self.progress)
        print(self.submition)


    def update(self):
        self.infoPrint("Updating Form...",self.progress)
        # Adds the question to the form
        question_setting = self.form_service.forms().batchUpdate(formId=self.main_form["formId"], body=self.submition).execute()
        print(question_setting)

        # Prints the result to show the question has been added
        get_result = self.form_service.forms().get(formId=self.main_form["formId"]).execute()
        self.resultUri = get_result['responderUri']
        print(get_result)
        self.infoPrint("Updating Form... Done",self.progress)
