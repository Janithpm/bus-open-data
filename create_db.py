import sqlite3

def create_tables():
    queries = [
        '''CREATE TABLE IF NOT EXISTS Location (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            RecordedAtTime TEXT,
            ItemIdentifier TEXT,
            ValidUntilTime TEXT,
            LineRef INTEGER,
            DirectionRef TEXT,
            DataFrameRef TEXT,
            DatedVehicleJourneyRef INTEGER,
            PublishedLineName INTEGER,
            OperatorRef TEXT,
            OriginRef TEXT,
            OriginName TEXT,
            DestinationRef TEXT,
            DestinationName TEXT,
            OriginAimedDepartureTime TEXT,
            DestinationAimedArrivalTime TEXT,
            Longitude FLOAT,
            Latitude FLOAT,
            BlockRef INTEGER,
            VehicleRef TEXT,
            TicketMachineServiceCode INTEGER,
            JourneyCode TEXT,
            VehicleUniqueId INTEGER,
            Bearing FLOAT
        )''',
        '''CREATE TABLE IF NOT EXISTS LocationLogs (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            ResponseTimestamp TEXT,
            RequestMessageRef TEXT,
            ValidUntil TEXT,
            ShortestPossibleCycle TEXT,
            VehicleActivities INTEGER,
            TimeStamp TEXT
        )'''
    ]

    with sqlite3.connect('bus_data.db') as conn:
        c = conn.cursor()
        for query in queries:
            c.execute(query)
        conn.commit()

create_tables()
