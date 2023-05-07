import sys
from manifiesto import SearchManifestClient, FulfillManifestClient

client = {
    'username': sys.argv[1],
    'password': sys.argv[2],
    'nit': sys.argv[3]
}

search = SearchManifestClient(client)
# response, is_valid = search.search_manifest(99999)
response, is_valid = search.search_active()
if not is_valid:
    print('no hay manifiestos por cumplir')
    sys.exit()

man = len(response)
print(f'hay {man} manifiestos sin cumplir')
manifests = []
for manifest, i in response:
    man_id = manifest.get('nummanifiestocarga')
    print(f'manifiesto {i}/{man} - {man_id}')
    to_fulfill = FulfillManifestClient(client)
    manifest.update({ 'fecha': manifest.get('fechaing') })
    to_fulfill.set_params(manifest)
    response, is_valid = to_fulfill.create()
    if is_valid:
        manifests.append({ 
            'id': man_id,
            'ingresoid': response.get('ingresoid'),
            'observacion': 'cumplido',
            'error': False
        })
        continue
    to_fulfill.set_suspension_params()
    response, is_valid = to_fulfill.create()
    if is_valid:
        manifests.append({ 
            'id': man_id,
            'ingresoid': response.get('ingresoid'),
            'observacion': 'cumplido en suspension',
            'error': False
        })
        continue
    manifests.append({ 
        'id': man_id,
        'ingresoid': None,
        'observacion': response,
        'error': True
    })

#cancelar los que no se cumplieron
