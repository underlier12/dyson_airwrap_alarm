from cargo_status import CargoStatus
from slack_alert import SlackAlert

import time

def main():
    CHANNEL = 'dyson-alarm'
    
    cargo_status = CargoStatus()
    slack_alert = SlackAlert()

    while True:
        alert_candidate = cargo_status.check_inventory()

        for alert in alert_candidate:
            slack_alert.send_message(CHANNEL, alert)

        time.sleep(5*60)

if __name__ == "__main__":
    main()