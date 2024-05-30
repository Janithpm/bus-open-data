from location import getLocationData, parse_location_xml
from timetable import getTimetableData
from sqlite import insertLocation, insertLocationLogs
import time

def main():
    # 14480, 14769, 14656
    datafeedId = 14656
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

total_duration = 10
interval = 10

iterations = total_duration // interval

for i in range(iterations):
    print(f"Start Iteration {i + 1} of {iterations}")
    main()
    print("Done with iteration. Sleeping...")
    time.sleep(interval)

print("Finished executing the script.")

    