import urllib.request
import json

try:
    url = 'https://api.github.com/repos/qwrecagve/car-rental-coursework/actions/runs'
    req = urllib.request.urlopen(url)
    data = json.loads(req.read())
    run_id = data['workflow_runs'][0]['id']
    
    url_jobs = f'https://api.github.com/repos/qwrecagve/car-rental-coursework/actions/runs/{run_id}/jobs'
    req_jobs = urllib.request.urlopen(url_jobs)
    jobs_data = json.loads(req_jobs.read())
    
    for job in jobs_data['jobs']:
        if job['conclusion'] == 'failure':
            print(f"Failed Job: {job['name']}")
            for step in job['steps']:
                if step['conclusion'] == 'failure':
                    print(f"Failed Step: {step['name']}")
except Exception as e:
    print("Error:", e)
