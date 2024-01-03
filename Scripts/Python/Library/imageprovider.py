import requests

class ImageProvides:
    def __init__(self):
        self.service_url = [ \
                "https://tmpfiles.org/api/v1/upload" ]
        self.service_use = 0
        self.successStatus = False
        self.urlImage = ""

    def upload(self, imagePath):
        try: 
            urlService = self.service_url[self.service_use]
            req = requests.post(urlService,files={"file": open(image,'rb')})
            if(req.json()['status'] == 'error'):
                self.successStatus = False
            self.successStatus = True


    def isSuccess(self):
        return self.successStatus

    def getUrl(self):
