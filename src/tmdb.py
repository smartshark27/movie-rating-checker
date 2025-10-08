import requests

from utils import create_dir_if_not_exists, read_json_file, save_to_json_file

tmdb_movie_search_url = "https://api.themoviedb.org/3/search/movie"


def get_tmdb_media_list(api_key, media_list):
    """
    Get TMDB details for a list of media items.
    Each item in media_list should be a dict with 'title' and 'year'.
    """
    cache = load_cache("cache/tmdb.json")
    tmdb_media_list = []
    for media in media_list:
        title = media.get("title")
        year = media.get("year")
        if not title:
            continue

        tmdb_media = {}

        # Lookup in cache first because TMDB is slow
        cached = lookup_cache(cache, title, year)
        if cached:
            print(f"Using cached TMDB data for '{title}' ({year})")
            tmdb_media = cached
        else:
            tmdb_media = get_media_from_tmdb(api_key, title, year)
            if tmdb_media:
                cache.append(tmdb_media)

        tmdb_media_list.append({**media, **(tmdb_media or {})})

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


def lookup_cache(cache, title, year=None):
    """
    Lookup a movie in the cache by title and year.
    """
    return next(
        (
            m
            for m in cache
            if m["searchTitle"] == title and (m["year"] == year or year is None)
        ),
        None,
    )


def get_media_from_tmdb(api_key, title, year=None):
    """
    Get TMDB movie details by title and optional year.
    """
    search_results = query_tmdb(api_key, title, year)
    if not search_results:
        print(f"No TMDB results found for '{title}' ({year})")
        return {
            "searchTitle": title,
            "title": title,
            "year": year,
            "tmdbPopularity": 0,
            "tmdbRating": 0,
            "tmdbRatingCount": 0,
            "imdbID": None,
        }

    # Use the first search result
    tmdb_id = search_results[0]["id"]
    movie = lookup_tmdb(api_key, tmdb_id)
    return {
        "searchTitle": title,
        "title": movie["title"],
        "year": movie["release_date"][:4] if movie.get("release_date") else None,
        "tmdbPopularity": movie["popularity"],
        "tmdbRating": movie["vote_average"],
        "tmdbRatingCount": movie["vote_count"],
        "imdbID": movie["imdb_id"],
    }


def query_tmdb(api_key, title, year=None):
    """
    Query TMDB for movies by title and optional year.
    """
    print(f"Searching TMDB for '{title}' ({year})...")

    params = {
        "api_key": api_key,
        "query": title,
    }
    if year:
        params["year"] = year

    return (
        requests.get(
            tmdb_movie_search_url,
            params=params,
        )
        .json()
        .get("results", [])
    )


def lookup_tmdb(api_key, tmdb_id):
    """
    Lookup a movie by its TMDB ID.
    """
    print(f"Looking up TMDB ID {tmdb_id}...")
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{tmdb_id}", params={"api_key": api_key}
    )
    if response.status_code != 200:
        print(f"TMDB lookup failed for ID {tmdb_id}: {response.status_code}")
        return None
    return response.json()
