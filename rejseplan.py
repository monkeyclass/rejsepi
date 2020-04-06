import yaml
import time
import requests
from datetime import datetime
from xml.etree import ElementTree

class RejseApi:
    def __init__(self,config_file):
        with open(config_file, 'r') as ymlfile:
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
        try:
            self.display_lines = self.cfg['display']['lines']
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
        
        return root
        #for child in root:
        #    print(child.tag, child.attrib)
        
    def print_departures(self):
        """ Built for displays and intended to print to these
            using specific parameters set in the config file """
        root = self.get_departures()
        for child in root[:self.display_lines]:
            a = child.attrib

            # create the transportation type string
            try:
                transtype = a['type']
            except:
                transtype = 'U'
            
            # creating the line info
            try:
                line = a['line']
            except:
                line = 'unknown line'
            
            # creating the direction info
            try:
                direction = a['direction']
            except:
                direction = 'unknown direction'

            # creating the track information
            try:
                track = a['rtTrack']
            except:
                try:
                    track = a['track']
                except:
                    track = 'track unkown'

            # creating the departure in time string
            try:
                depart_time_str = a['rtTime']
            except:
                try:
                    depart_time_str = a['time']
                except:
                    depart_time_str = ''
            
            try:
                depart_date_str = a['rtDate']
            except:
                try:
                    depart_date_str = a['date']
                except:
                    depart_date_str = ''
            
            try:
                # converting string dates to python dates
                depart_datetime_str = depart_date_str + ' ' + depart_time_str
                depart_datetime = datetime.strptime(depart_datetime_str, '%d.%m.%y %H:%M')

                # getting difference between now and departure
                current_time = datetime.now()
                total_seconds = (depart_datetime - current_time).total_seconds()

                # creates readable dateparts of either:
                #  > 1 hour
                if total_seconds // 3600 > 0:
                    hours = total_seconds // 3600
                    minutes = total_seconds % 3600 // 60
                    depart_in = str(int(hours)).zfill(2) + ' hour ' + str(int(minutes)).zfill(2) + ' min.'
                # > 1 minute
                elif total_seconds // 60 > 0:
                    minutes = total_seconds // 60
                    depart_in = str(int(minutes)).zfill(2) + ' min.'
                # > 30 seconds
                elif total_seconds > 30:
                    depart_in = '½ min.'
                # < 30 seconds
                else:
                    depart_in = '0 min.'
            except:
                depart_in = 'no time info'
            
            # printing the line to command line
            if transtype == 'S':
                print('Line', line, '>', f"{direction:<15}", 'track', track, 'in', depart_in)
        try:
            print('waiting for', self.api_requestwait, 'seconds...')
            time.sleep(self.api_requestwait)
        except:
            raise ValueError("'requestwait' for request interval must be set for get_departures method in the config file")
