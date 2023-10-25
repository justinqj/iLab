import requests
import time
import json

API_URL = 'https://api.lens.org/patent/search'
BATCH_SIZE = 100
DELAY = 1

# Fields to be included 
include = [
    "lens_id",
    "jurisdiction",
    "doc_number",
    "kind",
    "date_published",
    "lang",
    "biblio.publication_reference",
    "biblio.application_reference",
    "biblio.priority_claims",
    "biblio.invention_title.text",
    "biblio.parties.inventors.extracted_name",
    "biblio.parties.applicants.extracted_name",
    "biblio.classifications_cpc.classifications",
    "biblio.cited_by.patents",
    "abstract.text",
    "claims.claims",
    "description.text",
    "legal_status.granted",
    "legal_status.grant_date",
    "legal_status.patent_status",
    "biblio.parties.owners_all",
    "biblio.references_cited"
]

headers = {
    'Authorization': 'Bearer nGOk0QrJwwlTdrpCKlMbqEjA6ZdpIskMuSrE9uf6cnftVLO4Hw63', 
    'Content-Type': 'application/json'
}


all_results = []
offset = 0
YEAR = 2023  # You can change this each time you run the script for a different year
OUTPUT_FILE = f"raw_output_{YEAR}.json"

while True:
    request_body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"title": "technology"}},
                    {"match": {"lang": "en"}},
                    {"range": {"date_published": {"gte": f"{YEAR}-01-01", "lte": f"{YEAR}-12-31"}}}
                ]
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
        all_results.extend(results)
        offset += BATCH_SIZE

        # Check if we've retrieved all available results for the year
        if not results:
            break

        print(f"[INFO] Got {len(results)} results for {YEAR}, total so far: {len(all_results)}")

print(f"[INFO] Writing {len(all_results)} results to output file: {OUTPUT_FILE}")
with open(OUTPUT_FILE, "w") as f:
    f.write(json.dumps(all_results))
