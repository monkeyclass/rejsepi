import time
from rejseplan import RejseApi
def main(config):
    while True:
        RejseApi(config).get_departures()
        print('waiting')
        time.sleep(20)

main('config.yaml')