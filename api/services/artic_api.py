import requests

BASE_URL = "https://api.artic.edu/api/v1/artworks"


def get_artwork(external_id: int) -> dict | None:
    try:
        response = requests.get(f"{BASE_URL}/{external_id}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "external_id": external_id,
                "title": data["data"]["title"]
            }
        return None
    except requests.RequestException:
        return None