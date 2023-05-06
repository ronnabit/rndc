import requests
from rndc_parser import RNDCXmlParser


class RndcClient:
    """ This class manage the petitions to RNDC system """
    url = "http://plc.mintransporte.gov.co:8080/soap/IBPMServices"
    headers = {
        'Content-Type': 'text/xml',
        'SOAPAction': 'urn:BPMServicesIntf-IBPMServices#AtenderMensajeRNDC'
    }
    raw_body = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<soapenv:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:urn=\"urn:BPMServicesIntf-IBPMServices\">\n    <soapenv:Header/>\n    <soapenv:Body>\n        <urn:AtenderMensajeRNDC soapenv:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">\n            <Request xsi:type=\"xsd:string\">\n  {payload}    </Request>\n        </urn:AtenderMensajeRNDC>\n    </soapenv:Body>\n</soapenv:Envelope>"

    def __init__(self):
        self._payload = RNDCXmlParser()

    def execute(self):
        """ execute a petition to rndc """
        body = self.raw_body.format(payload=self._payload.get())
        response = requests.request("POST", self.url, headers=self.headers, data=body, timeout=10)
        return self.validate(response)

    def validate(self, response):
        """ validate if not errors ocurred """
        data = self._payload.parse_response(response.text)
        response = data['root']
        is_valid = False if 'ErrorMSG' in response else True
        return response, is_valid
