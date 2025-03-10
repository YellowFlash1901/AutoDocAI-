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
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('tree')          
    return None


def parse_github_tree(tree_data):
    """
    Convert GitHub API tree data to a readable file structure representation.
    
    Args:
        tree_data (dict): The GitHub API tree response with owner, repo, and tree.
        
    Returns:
        str: A formatted string showing the file structure.
    """
    owner = tree_data.get('owner', 'unknown')
    repo = tree_data.get('repo', 'unknown')
    tree = tree_data.get('tree', [])
    
    # Create directory structure
    root_dir = f"{owner}/{repo}/"
    directories = {}
    
    # Initialize root directory
    directories[root_dir] = []
    
    # Sort tree items by path depth
    sorted_tree = sorted(tree, key=lambda x: (x['path'].count('/'), x['path']))
    # Build the directory structure
    for item in sorted_tree:
        path = item['path']
        parts = path.split('/')
        
        if len(parts) == 1:
            # Root level item
            directories[root_dir].append({
                'name': parts[0],
                'is_dir': item['type'] == 'tree',
                'path': path
            })
        else:
            # Nested item
            filename = parts[-1]
            dir_path = '/'.join(parts[:-1])
            dir_key = f"{owner}/{repo}/{dir_path}/"
            
            # Ensure parent directory exists in our structure
            if dir_key not in directories:
                directories[dir_key] = []
            
            # Add item to its parent directory
            directories[dir_key].append({
                'name': filename,
                'is_dir': item['type'] == 'tree',
                'path': path
            })
    
    # Generate the formatted output
    result = [f"{root_dir}"]
    
    def build_structure(dir_key, prefix=""):
        # Sort items: directories first, then files, both alphabetically
        items = sorted(
            directories.get(dir_key, []),
            key=lambda x: (not x['is_dir'], x['name'].lower())
        )
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            new_prefix = "    " if is_last else "│   "
            
            result.append(f"{prefix}{connector}{item['name']}{'/' if item['is_dir'] else ''}")
            
            if item['is_dir']:
                new_dir_key = f"{dir_key}{item['name']}/"
                build_structure(new_dir_key, prefix + new_prefix)
    
    build_structure(root_dir)
    return "\n".join(result)


def get_file_structure(url: str):
    #first is to get owner then repo name then sha then repo json.
    #then get the tree sha from the repo json
    owner, repo, last_string = parse_owner_repo(url)
    sha = fetch_repo_sha(owner, repo)
    tree = fetch_repo_tree(owner, repo, sha)
    file_structure = parse_github_tree({"owner": owner, "repo": repo, "tree": tree})

    return {"file_structure": file_structure}