import re
import urllib.parse

def parse_owner_repo(url: str):
    decoded_url = urllib.parse.unquote(url)
    pattern = r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)"
    match = re.match(pattern, decoded_url)
    if match:
        owner = match.group("owner")
        repo = match.group("repo")
        return owner, repo
    return None, None

