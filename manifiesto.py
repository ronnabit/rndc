from typing import Tuple
from rndc_client import RndcClient


class SearchManifestClient(RndcClient):
    """ Client to Search Manifest """
    variables = ['INGRESOID', 'FECHAING', 'FECHAEXPEDICIONMANIFIESTO', 'NUMMANIFIESTOCARGA']
    def __init__(self, client: dict):
        super().__init__()
        self._data = { 'numnitempresatransporte': client.get('nit') }
        self._payload.set_access(client.get('username'), client.get('password'))
        self._payload.set_process(3, 4)
        self._payload.set_variables(self.variables)

    def _search(self, data):
        """ search manifest given the data """
        self._data.update(data)
        self._payload.set_document(self._data)
        searched, is_valid = self.execute()
        response = searched['documento'] if is_valid else searched
        return response, is_valid

    def search_manifest(self, manifest_id) -> Tuple[dict, bool]:
        """ search a manifest given the id"""
        data= { 'NUMMANIFIESTOCARGA': manifest_id }
        return self._search(data)

    def search_active(self) -> Tuple[list, bool]:
        """ search all manifest active """
        data= { 'ESTADO': "'AC'" }
        return self._search(data)
