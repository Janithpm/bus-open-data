import xml.etree.ElementTree as ET
from Xml import getName, getText, typeCast, compare, find
from bus_API import fetchData
from sqlite import insert_location
class Location:
    locationData = {}
    location_xml = None
    datafeedId = 0

    def __init__ (self, datafeedId):
        self.datafeedId = datafeedId

    def get_location_data(self):
        return self.locationData

    def fetch(self):
        url = f"https://data.bus-data.dft.gov.uk/api/v1/datafeed/{self.datafeedId}"
        self.location_xml = fetchData(url)
    
    def extract(self, root):
        result = {}
        name = getName(root)
        text = getText(root)
        
        if text is not None:
            result[name] = typeCast(text)
        
        for child in root:
            child_result = self.extract(child)
            if child_result:
                if name in result:
                    if not isinstance(result[name], list):
                        result[name] = [result[name]]
                    result[name].append(child_result)
                else:
                    result.update(child_result)
        
        return result
        
    def parse(self):
        activities = {}
        vehicleActivity = []
        root = ET.fromstring(self.location_xml)
        ServiceDelivery = find(root, 'ServiceDelivery')
        VehicleMonitoringDelivery = find(ServiceDelivery, 'VehicleMonitoringDelivery')
        for child in VehicleMonitoringDelivery:
            if compare(child.tag, 'VehicleActivity'):
                vehicleActivity.append(self.extract(child))
            else:
                activities[getName(child)] = getText(child)    
        activities['VehicleActivity'] = vehicleActivity
        self.locationData = activities
    
    def save(self):
        insert_location(self.locationData.get('VehicleActivity', []))