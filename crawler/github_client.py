import requests
from requests import Request
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = 'https://api.github.com'
OWNER = 'facebook'
ACCESS_TOKEN = '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'

retries = Retry(total=3, backoff_factor=1, status_forcelist=[404, 429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
http = requests.Session()
http.mount("https://", adapter)


def do_get(url):
    req = Request('GET',  url)
    prepped = req.prepare()
    prepped.headers['Authorization'] = f'token {ACCESS_TOKEN}'
    response = http.send(prepped)

    if response.status_code != 200:
        raise Exception(f"Error handling request {url}: {response.reason}")

    return response


def get_api_rate_limit(): return do_get(f"{BASE_URL}/user").headers.get('X-RateLimit-Remaining')


def get_commits(repo): return do_get(f"{BASE_URL}/repos/{OWNER}/{repo.lower()}/commits")


def get_repos(): return do_get(f"{BASE_URL}/orgs/{OWNER}/repos")
