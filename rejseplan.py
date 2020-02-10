import yaml
import time
import requests
from xml.etree import ElementTree

class RejseApi:
    def __init__(self,config):
        with open(config, 'r') as ymlfile:
            self.cfg = yaml.safe_load(ymlfile)

        try:
            self.api_url = self.cfg['api']['url']
        except:
            raise ValueError('the url for the api needs to be set in the config file')
        
        try:
            self.api_params = self.cfg['api']['params']
        except:
            pass

        try:
            self.api_requestwait = self.cfg['api']['requestwait']
        except:
            pass

    def get_departures(self):
        try:
            if 'id' not in self.api_params:
                raise ValueError('Station ID must be included as parameter in the config file')
        except:
            raise ValueError('get_departures methods needs parameters set in the config file')

        request = requests.get(url = self.api_url, params = self.api_params)
        root = ElementTree.fromstring(request.text)
        
        for child in root:
            print(child.tag, child.attrib)
            try:
                print('waiting for', self.api_requestwait, 'seconds...')
                time.sleep(self.api_requestwait)
            except:
                raise ValueError("'requestwait' for request interval must be set for get_departures method in the config file")