import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_TOKEN")

base_url = os.getenv("BASE_URL")

proxies = {
        'http': os.getenv("PROXY"),
        'https': os.getenv("PROXY"),
    }


def get_media(media_type: str, id_genre: str, page: str):
    params = {
        'api_key': api_key,
        'language': 'ru-RU',
        'with_genres': str(id_genre),
        'page': page,
    }

    try:
        response = requests.get(base_url + media_type, params=params, proxies=proxies)
        response.raise_for_status()

        data = response.json()
        media = data.get('results', [])
        if media:
            return media
        if media is None:
            return get_media(media_type, id_genre, page)
        else:
            return get_media(media_type, id_genre, page)

    except requests.exceptions.RequestException:
        return get_media(media_type, id_genre, page)

    except Exception:
        pass


def get_poster(poster_path: str):
    poster_base_url = "https://image.tmdb.org/t/p/"
    poster_size = "w500"  # Выберите размер постера
    poster_path = poster_path
    full_poster_url = f"{poster_base_url}{poster_size}{poster_path}"
    return full_poster_url
