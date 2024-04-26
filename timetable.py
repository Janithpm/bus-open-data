from bus_API import fetchData

def getTimetableData(datasetID):
    url = f"https://data.bus-data.dft.gov.uk/api/v1/dataset/{datasetID}"
    return fetchData(url)
    