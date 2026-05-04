import urllib.request
import json
try:
    req = urllib.request.urlopen("https://car-rental-uz-8749-hhg9e4cmdzhndycg.westeurope-01.azurewebsites.net/api/debug", timeout=10)
    print(req.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)
