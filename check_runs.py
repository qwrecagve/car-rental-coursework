import urllib.request
import json

try:
    url = 'https://api.github.com/repos/qwrecagve/car-rental-coursework/actions/runs'
    req = urllib.request.urlopen(url)
    data = json.loads(req.read())
    runs = data.get('workflow_runs', [])[:3]
    for r in runs:
        print(f"Status: {r['status']}, Conclusion: {r['conclusion']}, Commit: {r['head_commit']['message']}")
except Exception as e:
    print("Error:", e)
