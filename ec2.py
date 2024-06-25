import time
import logging
import requests
import ast
import xml.etree.ElementTree as ET
import sqlite3
import datetime

namespaces = {
    'siri': 'http://www.siri.org.uk/siri'
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

file_handler = logging.FileHandler('script.log')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

Number_of_days = 3
start_time = time.time()
end_time = start_time + Number_of_days * 24 * 60 * 60

def compare(tag, other):
    return tag == '{%s}%s' % (namespaces['siri'], other)

def getName(ele):
    return ele.tag.split('}')[-1]

def getText(ele):
    return ele.text

def find(root, tag):
    return root.find('siri:' + tag, namespaces)

def findall(root, tag):
    return root.findall('siri:' + tag, namespaces)

def typeCast(text):
    try:
        return ast.literal_eval(text)
    except (SyntaxError, ValueError):
        return text

def insertLocation(data_list):
    conn = sqlite3.connect('bus_data.db')
    c = conn.cursor()
    sql = '''INSERT INTO Location (
                 RecordedAtTime, ItemIdentifier, ValidUntilTime, LineRef, DirectionRef,
                 DataFrameRef, DatedVehicleJourneyRef, PublishedLineName, OperatorRef,
                 OriginRef, OriginName, DestinationRef, DestinationName,
                 OriginAimedDepartureTime, DestinationAimedArrivalTime,
                 Longitude, Latitude, BlockRef, VehicleRef, TicketMachineServiceCode,
                 JourneyCode, VehicleUniqueId, Bearing
             )
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    
    try:
        c.executemany(sql, [
        (
            data.get('RecordedAtTime', None),
            data.get('ItemIdentifier', None),
            data.get('ValidUntilTime', None),
            data.get('LineRef', None),
            data.get('DirectionRef', None),
            data.get('DataFrameRef', None),
            data.get('DatedVehicleJourneyRef', None),
            data.get('PublishedLineName', None),
            data.get('OperatorRef', None),
            data.get('OriginRef', None),
            data.get('OriginName', None),
            data.get('DestinationRef', None),
            data.get('DestinationName', None),
            data.get('OriginAimedDepartureTime', None),
            data.get('DestinationAimedArrivalTime', None),
            data.get('Longitude', None),
            data.get('Latitude', None),
            data.get('BlockRef', None),
            data.get('VehicleRef', None),
            data.get('TicketMachineServiceCode', None),
            data.get('JourneyCode', None),
            data.get('VehicleUniqueId', None),
            data.get('Bearing', None)
        ) for data in data_list
    ])
        conn.commit()
    except sqlite3.Error as e:
        print("Error inserting data:", e)
        conn.rollback()
    finally:
        conn.close()

def insertLocationLogs(data):
    conn = sqlite3.connect('bus_data.db')
    c = conn.cursor()
    sql = '''INSERT INTO LocationLogs (
                 ResponseTimestamp, RequestMessageRef, ValidUntil, ShortestPossibleCycle, VehicleActivities, TimeStamp
             )
             VALUES (?, ?, ?, ?, ?, ?)'''
    try:
        c.execute(sql, (
            data.get('ResponseTimestamp', None),
            data.get('RequestMessageRef', None),
            data.get('ValidUntil', None),
            data.get('ShortestPossibleCycle', None),
            data.get('VehicleActivities', 0),
            datetime.datetime.now()
        ))
        conn.commit()
    except sqlite3.Error as e:
        print("Error inserting data:", e)
        conn.rollback()
    finally:
        conn.close()

def fetchData(url):
    response = requests.get(url + '&api_key=c7f9574084c5817d26ebe99fe521b4a6e97d28fb')
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch data from API. Status code: {response.status_code}")
        return None

def extractRecursively(root):
    result = {}
    name = getName(root)
    text = getText(root)
    
    if text is not None:
        result[name] = typeCast(text)
    
    for child in root:
        child_result = extractRecursively(child)
        if child_result:
            if name in result:
                if not isinstance(result[name], list):
                    result[name] = [result[name]]
                result[name].append(child_result)
            else:
                result.update(child_result)
    
    return result
    
def parse_location_xml(xml_data):
    locationData = {}
    vehicleActivity = []
    root = ET.fromstring(xml_data)
    ServiceDelivery = find(root, 'ServiceDelivery')
    VehicleMonitoringDelivery = find(ServiceDelivery, 'VehicleMonitoringDelivery')
    for child in VehicleMonitoringDelivery:
        if compare(child.tag, 'VehicleActivity'):
           vehicleActivity.append(extractRecursively(child))
        else:
            locationData[getName(child)] = getText(child)    
    locationData['VehicleActivity'] = vehicleActivity
    return locationData

def main():
    try:
        xml_data = fetchData(f"https://data.bus-data.dft.gov.uk/api/v1/datafeed?boundingBox=-1.360495,53.824031,-2.382224,53.428220")
        locationData = parse_location_xml(xml_data)
        insertLocation(locationData.get('VehicleActivity', []))
        insertLocationLogs({
            'ResponseTimestamp': locationData.get('ResponseTimestamp', None),
            'RequestMessageRef': locationData.get('RequestMessageRef', None),
            'ValidUntil': locationData.get('ValidUntil', None),
            'ShortestPossibleCycle': locationData.get('ShortestPossibleCycle', None),
            'VehicleActivities': len(locationData.get('VehicleActivity', []))
        })
        logger.info("Data fetched and inserted successfully")
    except Exception as e:
        logger.error(f"An error occurred in main: {e}")

while time.time() < end_time:
    try:
        logger.info(f"Start data fetching...")
        main()
        logger.info("Done with iteration. Sleeping...")
    except Exception as e:
        logger.error(f"An error occurred in the loop: {e}")
    finally:
        time.sleep(10)

logger.info("Finished executing the script.")