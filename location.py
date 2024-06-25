import xml.etree.ElementTree as ET
from Xml import getName, getText, typeCast, compare, find
from bus_API import fetchData

def getLocationData(datafeedId = ""):
    url = f"https://data.bus-data.dft.gov.uk/api/v1/datafeed?boundingBox=-1.360495,53.824031,-2.382224,53.428220"
    return fetchData(url)
    
    
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