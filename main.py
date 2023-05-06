import sys
from manifiesto import SearchManifestClient

client = {
    'username': sys.argv[1],
    'password': sys.argv[2],
    'nit': sys.argv[3]
}
print(client)

search = SearchManifestClient(client)
response, is_valid = search.search_manifest(99999)
print(response)
