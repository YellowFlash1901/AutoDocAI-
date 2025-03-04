import re
import urllib.parse
import requests

def parse_owner_repo(url: str):
    decoded_url = urllib.parse.unquote(url)
    pattern = r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)(/(?P<lastString>.+))?"
    match = re.match(pattern, decoded_url)
    if match:
        owner = match.group("owner")
        repo = match.group("repo")
        last_string = match.group("lastString") or ''

        return owner, repo, last_string
    return None, None, None

def fetch_repo_sha(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[-1].get('sha')
    return None

def fetch_repo_tree(owner: str, repo: str, sha: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{sha}?recursive=1"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("fetch repo",data)
        return data.get('tree')          
    return None