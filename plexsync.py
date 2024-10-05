import dotenv
import requests
import os
import glob
from xml.etree import ElementTree

dotenv.load_dotenv()
base_url = os.environ["BASE_URL"]

def etree_to_dict(t):
    if type(t) is ElementTree: return etree_to_dict(t.getroot())
    return {
        **t.attrib,
        'text': t.text,
        **{e.tag: etree_to_dict(e) for e in t}
    }

def to_dict(r):
    return etree_to_dict(ElementTree.fromstring(r.content))

# get this from the plex_tv_auth cookie under authentication_token
# is this ok to use? i mean it works but still...not documented anywhere lol
s = requests.Session()
s.headers = {
	"X-Plex-Token": os.environ["TOKEN"],
}

# https://plexapi.dev/api-reference/playlists/upload-playlist
for p in glob.glob("E:\MusicBee\Playlists\*.m3u"):
    print("updating playlist "+p)
    response = s.post(
        base_url+"/playlists/upload",
        params={"path":p, "sectionID": 1},
	)
    print(response.status_code)
    if not response:
        print(response.content)
