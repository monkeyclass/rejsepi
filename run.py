from rejseplan import RejseApi

def main(config):
    capi = RejseApi(config)
    while True:
        capi.print_departures()

main('config.yaml')