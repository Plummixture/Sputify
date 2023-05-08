import requests, json, os, random
from requests.auth import HTTPBasicAuth
from flask import Flask, request, redirect


app = Flask(__name__, static_url_path='/static')

clientID = os.environ['CLIENT_ID']
clientSecrect = os.environ['CLIENT_SECRECT']

url = 'https://accounts.spotify.com/api/token'
data = {'grant_type': 'client_credentials'}
auth = HTTPBasicAuth(clientID, clientSecrect)

response = requests.post(url, data=data, auth=auth)

accessToken = response.json()['access_token']
url = 'https://api.spotify.com/v1/search'
headers = {"Authorization": f"Bearer {accessToken}"}

#year = int(input("Year: ").strip().replace(" ", ''))
#print()

#print(json.dumps(data, indent=2))


body = ''
f = open('body.html', 'r')
body = f.read()
f.close()

bdy = ''
offset = 0

f = open("year.txt", "w")
f.write("")
f.close()

@app.route('/')
def index():
  global bdy, page
  entry = bdy
  page = ''
  f = open('app.html', 'r')
  page = f.read()
  f.close()
  page = page.replace("{body}", entry)
  bdy = ''
  return page

@app.route('/search', methods=['POST'])
def search():
  global body, bdy, offset, page
  form = request.form
  year = form['year']

  f = open("year.txt", "r")
  pg = f.read()
  f.close()

  if year == pg:
    offset += 10
  else:
    offset = 0
    
  search = f'?query=year%3A{year}&type=track&locale=en-US%2Cen%3Bq%3D0.9&offset={offset}&limit=10'
  pg = ''

  f = open("year.txt", 'w')
  f.write(year)
  f.close()
  fullURL = f"{url}{search}"
  response = requests.get(fullURL, headers=headers)
  data = response.json()
  #print(json.dumps(data, indent=2))
  for i in data['tracks']['items']:
    bodycpy = body
    bodycpy = bodycpy.replace("{title}", i['name'])
    bodycpy = bodycpy.replace("{link}", i['preview_url'])
    bodycpy = bodycpy.replace('{artist}', i['artists'][0]['name'])
    bdy += bodycpy
  return redirect('/')

app.run(host="0.0.0.0", port=81)
