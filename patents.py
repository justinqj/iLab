import requests
import time
url = 'https://api.lens.org/patent/search'

# include fields
include = '''["biblio.invention_title", "biblio.parties.inventors.extracted_name", "date_published"]'''
# request body with scroll time of 1 minute
request_body = '''{
    "query": {
        "match":  {
            "title": "technology"
        }
    },
    "include": %s,
    "scroll": "1m",
    "size": 20,
    "sort": [{"date_published": "desc"}]
}''' % include
headers = {'Authorization': 'Bearer 02w63YLQJJRT3i8THxetpAJCvEO1883fymZIXxOzK2gP1N6UK3SN', 'Content-Type': 'application/json'}

# Recursive function to scroll through paginated results
def scroll(scroll_id):
  # Change the request_body to prepare for next scroll api call
  # Make sure to append the include fields to make faster response
  if scroll_id is not None:
    global request_body
    request_body = '''{"scroll_id": "%s", "include": %s}''' % (scroll_id, include)

  # make api request
  response = requests.post(url, data=request_body, headers=headers) 

  # If rate-limited, wait for n seconds and proceed the same scroll id
  # Since scroll time is 1 minutes, it will give sufficient time to wait and proceed
  if response.status_code == requests.codes.too_many_requests:
    time.sleep(8)
    scroll(scroll_id)
  # If the response is not ok here, better to stop here and debug it
  elif response.status_code != requests.codes.ok:
    print(response.json())
  # If the response is ok, do something with the response, take the new scroll id and iterate
  else:
    json = response.json()
    if json.get('results') is not None and json['results'] > 0:
        scroll_id = json['scroll_id'] # Extract the new scroll id from response
        print(json['data']) #DO something with your data
        scroll(scroll_id)

# start recursive scrolling
scroll(scroll_id=None)
