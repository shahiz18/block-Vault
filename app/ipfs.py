import os, requests

PINATA_ENDPOINT = "https://api.pinata.cloud/pinning/pinFileToIPFS"
GATEWAY = "https://violet-giant-goldfish-635.mypinata.cloud/ipfs/{}"


def upload_to_ipfs(file_path: str, jwt_token: str) -> str:
    headers = {"Authorization": f"Bearer {jwt_token}"}
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as fp:
        files = {"file": (file_name, fp)}  # default mime → application/octet-stream
        r = requests.post(PINATA_ENDPOINT, headers=headers, files=files, timeout=60)

    if r.status_code == 200:
        return r.json()["IpfsHash"]
    raise Exception(f"IPFS upload failed {r.status_code}: {r.text[:120]}")


def fetch_from_pinata(cid: str) -> bytes:
    """Download raw bytes for a CID from Pinata’s gateway."""
    url = GATEWAY.format(cid)
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.content