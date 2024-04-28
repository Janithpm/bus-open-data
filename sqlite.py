import sqlite3
import datetime

def insert_location(data_list):
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

def insert_location_logs(data):
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