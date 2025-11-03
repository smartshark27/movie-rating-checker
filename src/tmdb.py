import asyncio
import aiohttp

from utils import create_dir_if_not_exists, read_json_file, save_to_json_file

tmdb_movie_search_url = "https://api.themoviedb.org/3/search/movie"
tmdb_movie_lookup_url = "https://api.themoviedb.org/3/movie"
tmdb_show_search_url = "https://api.themoviedb.org/3/search/tv"
tmdb_show_lookup_url = "https://api.themoviedb.org/3/tv"


CONCURRENCY = 40  # Max concurrent requests to TMDB API


def get_tmdb_media_list(api_key, media_list):
    """
    Get TMDB details for a list of media items in parallel (up to 40 concurrent requests).
    Each item in media_list must be a dict with 'mediaType', 'title' and optional 'year'.
    """
    return asyncio.run(_get_tmdb_media_list_async(api_key, media_list))


async def _get_tmdb_media_list_async(api_key, media_list):
    cache = load_cache("cache/tmdb.json")
    semaphore = asyncio.Semaphore(CONCURRENCY)
    tmdb_media_list = []

    async with aiohttp.ClientSession() as session:

        async def process_media(media):
            tmdb_media = {}
            cache_key = (
                f"{media['mediaType']}-{media['title']}-{media.get('year', 'noyear')}"
            )
            cached = lookup_cache(cache, cache_key)
            if cached:
                print(f"Using cached TMDB data for key '{cache_key}'")
                tmdb_media = cached
            else:
                tmdb_media = await get_media_from_tmdb_async(
                    api_key, media, cache_key, session, semaphore
                )
                if tmdb_media:
                    cache.append(tmdb_media)
            return {**media, **(tmdb_media or {})}

        tasks = [process_media(media) for media in media_list]
        tmdb_media_list = await asyncio.gather(*tasks)

    # Save updated cache
    create_dir_if_not_exists("cache")
    save_to_json_file(cache, "cache/tmdb.json")
    return tmdb_media_list


def load_cache(filename):
    """
    Load cached TMDB data from a JSON file.
    """
    try:
        cache = read_json_file(filename)
        print(f"Loaded {len(cache)} items from cache")
        return cache
    except FileNotFoundError:
        print("Cache file not found, starting with empty cache")
        return []


def lookup_cache(cache, cache_key):
    """
    Lookup a movie in the cache using the cache key.
    """
    return next(
        (m for m in cache if m["cacheKey"] == cache_key),
        None,
    )


async def get_media_from_tmdb_async(api_key, media, cache_key, session, semaphore):
    """
    Async: Get TMDB movie/show details by title and optional year.
    """
    title = media["title"]
    year = media.get("year")
    search_results = await query_tmdb_async(api_key, media, session, semaphore)
    if not search_results:
        print(f"No TMDB results found for '{title}' ({year}) {media['mediaType']}")
        return {
            "cacheKey": cache_key,
            "title": title,
            "year": year,
            "tmdbPopularity": 0,
            "tmdbRating": 0,
            "tmdbRatingCount": 0,
            "imdbID": None,
        }

    # Use the first search result
    tmdb_id = search_results[0]["id"]
    tmdb_media = await lookup_tmdb_async(
        api_key, media["mediaType"], tmdb_id, session, semaphore
    )
    if not tmdb_media:
        return {
            "cacheKey": cache_key,
            "title": title,
            "year": year,
            "tmdbPopularity": 0,
            "tmdbRating": 0,
            "tmdbRatingCount": 0,
            "imdbID": None,
        }
    return {
        "cacheKey": cache_key,
        "title": (
            tmdb_media["title"] if media["mediaType"] == "movie" else tmdb_media["name"]
        ),
        "year": (
            tmdb_media["release_date"][:4] if tmdb_media.get("release_date") else None
        ),
        "tmdbPopularity": tmdb_media["popularity"],
        "tmdbRating": tmdb_media["vote_average"],
        "tmdbRatingCount": tmdb_media["vote_count"],
        "imdbID": tmdb_media.get("imdb_id", None),
    }


async def query_tmdb_async(api_key, media, session, semaphore):
    """
    Async: Query TMDB for movies/shows by title and optional year.
    """
    title = media["title"]
    media_type = media["mediaType"]
    if media_type not in ["movie", "show"]:
        print(f"Unknown media type '{media_type}' for item '{title}'")
        return []
    year = media.get("year")
    print(f"Searching TMDB for '{title}' ({year})...")

    params = {
        "api_key": api_key,
        "query": title,
    }
    if year:
        params["year"] = year

    url = tmdb_movie_search_url if media_type == "movie" else tmdb_show_search_url
    async with semaphore:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                print(f"TMDB search failed for '{title}': {resp.status}")
                return []
            data = await resp.json()
            return data.get("results", [])


async def lookup_tmdb_async(api_key, media_type, tmdb_id, session, semaphore):
    """
    Async: Lookup a movie/show by its TMDB ID.
    """
    url = tmdb_movie_lookup_url if media_type == "movie" else tmdb_show_lookup_url
    url += f"/{tmdb_id}"

    print(f"Looking up TMDB ID {tmdb_id} at URL {url}...")
    async with semaphore:
        async with session.get(url, params={"api_key": api_key}) as resp:
            if resp.status != 200:
                print(f"TMDB lookup failed for ID {tmdb_id}: {resp.status}")
                return None
            return await resp.json()


# Sample TMDB TV show data structure from the API:
# {
#   "adult": false,
#   "backdrop_path": "/A23065a99kzX6LN3tt9nQzq6QNe.jpg",
#   "created_by": [],
#   "episode_run_time": [],
#   "first_air_date": "2002-01-01",
#   "genres": [],
#   "homepage": "",
#   "id": 122965,
#   "in_production": false,
#   "languages": ["el"],
#   "last_air_date": "2002-06-25",
#   "last_episode_to_air": {
#     "id": 2864238,
#     "name": "Episode 26",
#     "overview": "",
#     "vote_average": 0.0,
#     "vote_count": 0,
#     "air_date": "2002-06-25",
#     "episode_number": 26,
#     "episode_type": "finale",
#     "production_code": "",
#     "runtime": null,
#     "season_number": 1,
#     "show_id": 122965,
#     "still_path": "/la5bf37O4N08jdgKC1rKYugQLCQ.jpg"
#   },
#   "name": "Mother and Son",
#   "next_episode_to_air": null,
#   "networks": [
#     {
#       "id": 2474,
#       "logo_path": "/mR0SoE9l7rq8nsmjeuMhv05CVoh.png",
#       "name": "ERT1",
#       "origin_country": "GR"
#     }
#   ],
#   "number_of_episodes": 26,
#   "number_of_seasons": 1,
#   "origin_country": ["GR"],
#   "original_language": "el",
#   "original_name": "Μαμά και Γιος",
#   "overview": "Pericles lives with his controlling mother Ioulia, who is starting to show signs of dementia.",
#   "popularity": 0.9838,
#   "poster_path": "/skCmZa6oVzMS1fbcgfEvFWS8uJk.jpg",
#   "production_companies": [],
#   "production_countries": [{ "iso_3166_1": "GR", "name": "Greece" }],
#   "seasons": [
#     {
#       "air_date": "2002-01-01",
#       "episode_count": 26,
#       "id": 189991,
#       "name": "Season 1",
#       "overview": "",
#       "poster_path": "/v3jnl45UDgH6MWoEJvWiBS9VXjE.jpg",
#       "season_number": 1,
#       "vote_average": 0.0
#     }
#   ],
#   "spoken_languages": [
#     { "english_name": "Greek", "iso_639_1": "el", "name": "ελληνικά" }
#   ],
#   "status": "Ended",
#   "tagline": "",
#   "type": "Scripted",
#   "vote_average": 10.0,
#   "vote_count": 2
# }
