# import json
from location import getLocationData, parse_location_xml
from timetable import getTimetableData
from sqlite import insertLocation, insertLocationLogs

def main():
    datafeedId = 14480
    datasetId = 2023

    xml_data = getLocationData(datafeedId)
    locationData = parse_location_xml(xml_data)
    insertLocation(locationData.get('VehicleActivity', []))
    insertLocationLogs({
        'ResponseTimestamp': locationData.get('ResponseTimestamp', None),
        'RequestMessageRef': locationData.get('RequestMessageRef', None),
        'ValidUntil': locationData.get('ValidUntil', None),
        'ShortestPossibleCycle': locationData.get('ShortestPossibleCycle', None),
        'VehicleActivities': len(locationData.get('VehicleActivity', []))
    })
    
    timetable = getTimetableData(datasetId)
    with open('data/timetable.json', 'w') as tf:
        tf.write(timetable)

if __name__ == "__main__":
    main()