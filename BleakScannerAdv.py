"""
Detection callback w/ scanner
--------------
Example showing what is returned using the callback upon detection functionality
Updated on 2020-10-11 by bernstern <bernie@allthenticate.net>
"""

import asyncio
import logging
import sys

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)

def simple_callback(device: BLEDevice, advertisement_data: AdvertisementData):
    logger.info(f"{device.address}: {advertisement_data}")
    AdvData = advertisement_data
    DevAddr = device.address
    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    
    Payload = {
      "Adevertisment Data": AdvData,
      "DeviceAddress": DevAddr,
      "date": date
    }

    OutData = json.dumps(payload)

    client.publish('GW02ADV/topic', payload=OutData, qos=0, retain=False)


async def main(service_uuids):
    scanner = BleakScanner(simple_callback, service_uuids)

    while True:
        print("(re)starting scanner")
        await scanner.start()
        await asyncio.sleep(5.0)
        await scanner.stop()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )
    service_uuids = sys.argv[1:]
    asyncio.run(main(service_uuids))