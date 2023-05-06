import xml.etree.ElementTree as ET
import xmltodict

class RNDCXmlParser:
    """ this class allows make the body for rndc petitions and convert the response """
    xml_base = "<root><acceso><username /><password /></acceso><solicitud><tipo /><procesoid /></solicitud><variables /></root>"
    find = "./{http://schemas.xmlsoap.org/soap/envelope/}Body/{urn:BPMServicesIntf-IBPMServices}AtenderMensajeRNDCResponse/return"

    def __init__(self):
        self._root = ET.fromstring(self.xml_base)

    def set_access(self, username: str, password: str):
        """ set the credentials """
        self._root.find('./acceso/username').text = username
        self._root.find('./acceso/password').text = password

    def set_process(self, type_id: int, process_id: int):
        """ set the petition """
        self._root.find('./solicitud/tipo').text = str(type_id)
        self._root.find('./solicitud/procesoid').text = str(process_id)

    def set_variables(self, variables: list):
        """ set the variables that return the rndc system """
        self._root.find('./variables').text = ','.join(variables)

    def set_document(self, document: dict):
        """ add tag to find an specific document, only use when search data """
        documento = ET.Element('documento')
        for key, value in document.items():
            element = ET.Element(key)
            element.text = str(value)
            documento.append(element)
        self._root.append(documento)

    def set_document_range(self, initial: str, final: str):
        """ add tag to find data in specific range of dates, only use when search data """
        d_range = ET.fromstring('<documentorango><iniFECHAING /><finFECHAING /></documentorango>')
        d_range.find('./iniFECHAING').text = initial
        d_range.find('./finFECHAING').text = final
        self._root.append(d_range)

    def get(self):
        """ return the xml tree as str """
        return ET.tostring(self._root).decode()

    def parse_response(self, response):
        """ parse the data from str with xml format to dict """
        root = ET.fromstring(response)
        body = root.find(self.find)
        data = xmltodict.parse(body.text)
        return data
