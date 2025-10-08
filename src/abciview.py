import requests

# This script fetches a list of movies from the ABC iView catalogue.
# It uses the public API endpoint to retrieve movie data.

collection_urls = {
    "all-movies": "https://api.iview.abc.net.au/v3/collection/2711",
    "movies-of-the-week": "https://api.iview.abc.net.au/v3/collection/4028",
}
headers = {
    "User-Agent": "Mozilla/5.0",
}


def get_movies(collection="movies-of-the-week"):
    """
    Fetch all movies from the SBS On Demand catalogue.
    """
    if collection not in collection_urls:
        raise ValueError(
            f"Invalid collection '{collection}'. Must be one of {list(collection_urls.keys())}."
        )
    url = collection_urls[collection]

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    movies = [
        {
            "title": movie["title"],
            "abcURL": movie["shareUrl"],
        }
        for movie in response.json()["items"]
    ]

    print(f"Total movies found: {len(movies)}")
    return movies


if __name__ == "__main__":
    movies = get_movies()
    print("movies:", movies)


# Sample movie data structure from the API:
# {
#   "id": "ZX5993A001S00",
#   "type": "feature",
#   "houseNumber": "ZX5993A001S00",
#   "title": "Strictly Ballroom",
#   "showTitle": "Strictly Ballroom",
#   "displayTitle": "Strictly Ballroom",
#   "description": "When 21-year-old ballroom champion Scott Hastings commits the cardinal sin of dancing his own steps and not those of the all-powerful Dance Federation, the retribution is swift.",
#   "kickerTitle": "Classic Aussie Cinema",
#   "shortSynopsis": "Scott Hastings commits the misdeed of dancing his own steps and not those of the Dance Federation.",
#   "status": { "title": "MOVIE", "theme": "default" },
#   "duration": 5424,
#   "displayDuration": "1h 30m",
#   "displayDurationAccessible": "1 hour 30 minutes",
#   "classification": "PG",
#   "captions": true,
#   "shareUrl": "https://iview.abc.net.au/show/strictly-ballroom/video/ZX5993A001S00",
#   "images": [
#     {
#       "url": "https://cdn.iview.abc.net.au/thumbs/i/X0_5ee3114bc14c7_2000.jpg",
#       "name": "portraitTitledThumbnail",
#       "type": "portrait-titled",
#       "aspectRatio": "2:3",
#       "width": 2000,
#       "height": 3000,
#       "_source": "show",
#       "_entity": "image"
#     },
#     {
#       "url": "https://cdn.iview.abc.net.au/thumbs/i/X0_5ffbbf7616577_720.jpg",
#       "name": "portraitThumbnail",
#       "type": "portrait",
#       "aspectRatio": "2:3",
#       "width": 720,
#       "height": 1080,
#       "_source": "show",
#       "_entity": "image"
#     },
#     {
#       "url": "https://cdn.iview.abc.net.au/thumbs/i/zx/ZX5993A001S00_5ee323e7cfd7b_1280.jpg",
#       "name": "seriesThumbnail",
#       "type": "thumb",
#       "aspectRatio": "16:9",
#       "width": 1280,
#       "height": 720,
#       "_source": "series",
#       "_entity": "image"
#     },
#     {
#       "url": "https://cdn.iview.abc.net.au/thumbs/i/zx/ZX5993A001S00_5ee323e7cfd7b_1280.jpg",
#       "name": "episodeThumbnail",
#       "type": "thumb",
#       "aspectRatio": "16:9",
#       "width": 1280,
#       "height": 720,
#       "_source": "video",
#       "_entity": "image"
#     }
#   ],
#   "_entity": "video",
#   "_links": {
#     "self": { "href": "/video/ZX5993A001S00" },
#     "share": { "href": "https://iview.abc.net.au/video/ZX5993A001S00" },
#     "deeplink": {
#       "id": "ZX5993A001S00",
#       "href": "/show/strictly-ballroom/video/ZX5993A001S00"
#     },
#     "trailer": { "id": "MP2329H135C00GN1", "href": "/video/MP2329H135C00GN1" },
#     "show": { "id": 204199, "href": "/show/strictly-ballroom" }
#   }
# }
