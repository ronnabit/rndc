import sys
import csv
from manifiesto import SearchManifestClient, FulfillManifestClient, CancelManifestClient

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
for i, manifest in enumerate(response):
    man_id = manifest.get('nummanifiestocarga')
    print(f'manifiesto {i+1}/{man} - {man_id}')
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

to_cancel = list(filter(lambda x: x['error'] is True, manifests))
man = len(to_cancel)
print(f'quedan {man} manifiestos por anular')
for i, manifest in enumerate(to_cancel):
    man_id = manifest.get('id')
    print(f'anulando manifiesto {i+1}/{man} - {man_id}')
    cancel = CancelManifestClient(client)
    cancel.set_params({ 'nummanifiestocarga': man_id })
    response, is_valid = cancel.create()
    if is_valid:
        manifest.update({
            'ingresoid': response.get('ingresoid'),
            'observacion': 'cancelado',
            'error': False
        })
        continue

csv_columns = ['id','ingresoid','observacion','error']
try:
    with open('manifiestos.csv', 'w', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in manifests:
            writer.writerow(data)
except IOError:
    print("error guardando archivo")
