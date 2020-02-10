from rejseplan import RejseApi

def main(config):
    capi = RejseApi(config)
    while True:
        capi.get_departures()

main('config.yaml')