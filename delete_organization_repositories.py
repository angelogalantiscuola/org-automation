import jwt
import time
import requests
from pathlib import Path

# curl -i -H "Authorization: Bearer YOUR_JWT" -H "Accept: application/vnd.github.machine-man-preview+json" https://api.github.com/app/installations

# Load private key
with open(Path("private-key.pem"), "r") as file:
    private_pem = file.read()

app_id = "889864"
installation_id = "50292267"

# Generate JWT
payload = {
    # issued at time
    "iat": int(time.time()),
    # JWT expiration time (10 minute maximum)
    "exp": int(time.time()) + (10 * 60),
    # GitHub App's identifier
    "iss": app_id,
}

jwt_token = jwt.encode(payload, private_pem, algorithm="RS256")

headers = {"Authorization": f"Bearer {jwt_token}", "Accept": "application/vnd.github.v3+json"}

# Use the JWT to obtain an installation access token
response = requests.post(f"https://api.github.com/app/installations/{installation_id}/access_tokens", headers=headers)

if response.status_code == 201:
    access_token = response.json()["token"]
    token_expires_at = response.json()["expires_at"]
else:
    print(f"Failed to get installation access token. Status code: {response.status_code}")
    exit(1)

# Use the access token to authenticate as the installation
headers = {"Authorization": f"token {access_token}", "Accept": "application/vnd.github.v3+json"}

response = requests.get(f"https://api.github.com/installation/repositories", headers=headers)

repo_name_starts_with = "22"

for repo in response.json()["repositories"]:
    repo_name = repo["name"]
    if repo_name.startswith(repo_name_starts_with):
        print(f"Skipping {repo_name}...")
    else:
        print(f"Deleting {repo_name}...")
        delete_response = requests.delete(f'https://api.github.com/repos/{repo["full_name"]}', headers=headers)
        if delete_response.status_code == 204:
            print(f"Successfully deleted {repo_name}")
        else:
            print(f"Failed to delete {repo_name}. Status code: {delete_response.status_code}")
