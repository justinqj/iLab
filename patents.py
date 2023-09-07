import requests
import time
import json

API_URL = 'https://api.lens.org/patent/search'
BATCH_SIZE = 100

DELAY = 1
OUTPUT_FILE = "output.json"

include = ["biblio.invention_title", "biblio.parties.inventors.extracted_name", "date_published"]
headers = {'Authorization': 'Bearer 02w63YLQJJRT3i8THxetpAJCvEO1883fymZIXxOzK2gP1N6UK3SN', 'Content-Type': 'application/json'}

all_results = []
offset = 0
while True:
  request_body = {
    "query": {
        "match":  {
            "title": "technology"
        }
    },
    "include": include,
    "from": offset,
    "size": BATCH_SIZE,
    "sort": [{"date_published": "desc"}]
  }
  response = requests.post(API_URL, json=request_body, headers=headers)

  if response.status_code == requests.codes.too_many_requests:
    print(f"[ERROR]: We are being rate limited, sleeping for {DELAY} and trying again.")
    time.sleep(DELAY)
    continue

  elif response.status_code != requests.codes.ok:
    print(f"[ERROR]: Request returned code {response.status_code}, aborting. Response was:")
    print(response.json())
    break

  else:
    response_json = response.json()
    results = response_json.get('data', [])
    total = response_json.get('total', 0)
    all_results.extend(results)
    offset += BATCH_SIZE

    if offset >= total:
      break
    print(f"[INFO] Got {len(results)}, currently: {offset} / {total} results")

print(f"[INFO] Writing {len(all_results)} results to output file: {OUTPUT_FILE}")
with open(OUTPUT_FILE, "w") as f:
  f.write(json.dumps(all_results))
