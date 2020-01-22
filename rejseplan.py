import yaml
import requests
from xml.etree import ElementTree

class RejseApi:
    def __init__(self,config):
        with open(config, 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)

        self.api_url = cfg['api']['url']
        self.api_params = cfg['api']['params']

    def get_departures(self):
        request = requests.get(url = self.api_url, params = self.api_params)
        print(request.url)
        root = ElementTree.fromstring(request.text)
        for child in root:
            print(child.tag, child.attrib)