import requests

from utils import read_text_file


collection_urls = {
    "award-winners-and-nominees": "https://tensor-cdn.production-public.tubi.io/api/v7/containers/award_winners_and_nominees",
    "cult-classics": "https://tensor-cdn.production-public.tubi.io/api/v7/containers/cult_favorites",
    "most-popular": "https://tensor-cdn.production-public.tubi.io/api/v7/containers/most_popular",
    "recently-added": "https://tensor-cdn.production-public.tubi.io/api/v7/containers/recently_added",
    "trending-now": "https://tensor-cdn.production-public.tubi.io/api/v7/containers/trending",
}


def get_tubi_media_list(access_token, collection="recently-added"):
    """
    Fetch the list of media items from a Tubi collection.

    :param access_token: Tubi access token for authorization
    :param collection: Collection key from collection_urls
    :return: List of media items
    """
    url = collection_urls.get(collection)
    if not url:
        raise ValueError(f"Collection '{collection}' not found.")

    params = {
        "contents_limit": 200,
        "cursor": 0,
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US",
        "Authorization": f"Bearer {access_token}",
        "Cache-Control": "no-cache",
        "Origin": "https://tubitv.com",
        "Pragma": "no-cache",
        "Priority": "u=3, i",
        "Referrer": "https://tubitv.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0",
    }

    res = requests.get(url, params=params, headers=headers)
    res.raise_for_status()

    contents = res.json().get("contents", {})

    # save_to_json_file(res.json(), "output/tubi-api-response.json")
    # return []

    is_show = lambda item: item["type"] == "s"
    media_list = [
        {
            "mediaType": "show" if is_show(item) else "movie",
            "title": item["title"],
            "year": str(item.get("year")),
            "tubiURL": "https://tubitv.com/"
            + ("series" if is_show(item) else "movies")
            + "/"
            + item["id"],
        }
        for item in contents.values()
    ]

    print(f"Total media found from Tubi: {len(media_list)}")

    return media_list


if __name__ == "__main__":
    media_list = get_tubi_media_list(
        access_token=read_text_file("input/tubi_access_token.txt").strip()
    )
    print("media:", media_list)


# Example API response
# {
#     "container": {
#         "background": null,
#         "children": [
#             "689248",
#             "643370",
#             "643397",
#             "609201",
#             "630357",
#             "100012887",
#             "0300008092",
#             "0334",
#             "617695",
#             "618737"
#         ],
#         "container_images": null,
#         "cursor": 60,
#         "description": "Fresh out of the oven — hot new movies and shows just for you, added weekly so check in often!",
#         "id": "recently_added",
#         "logo": null,
#         "needs_login": false,
#         "reaction": "none",
#         "slug": "recently_added",
#         "sponsorship": null,
#         "tags": [
#             "For You",
#             "Popular"
#         ],
#         "thumbnail": "http://images.adrise.tv/KCfHoo4h7QNPGEqN7bkxF1i2bLg=/640x360/smart/img.adrise.tv/6c7aae80-f77b-4a83-9c89-09e7b699cb44.jpg",
#         "title": "Recently Added",
#         "type": "regular",
#         "ui_customization": null,
#         "valid_duration": null
#     },
#     "contents": {
#         "0300008092": {
#             "video_resources": [],
#             "schedule_data": null,
#             "has_trailer": false,
#             "num_seasons": 4,
#             "video_previews": [
#                 {
#                     "url": "https://video-preview-lb.production-public.tubi.io/videopreview/a9868f97-32bf-48e0-ab89-8cf0a4eaaa49-start91.861-end193.878.mp4",
#                     "uuid": "d89a2dbb-8883-46cc-826c-ba6917b4884a"
#                 }
#             ],
#             "description": "As gene therapy, transplants and cloning offer hope for humanity, a dark side of evolution produces monsters a select few are brave enough to take on.",
#             "availability_duration": null,
#             "league": null,
#             "needs_login": false,
#             "is_recurring": false,
#             "landscape_images": [
#                 "https://canvas-lb.tubitv.com/opts/DTAg9NPcHWx6Mg==/e5790053-dccc-4cde-9eba-78bffaf9ca3a/CMADEPwBOgUxLjEuOA=="
#             ],
#             "publisher_id": "",
#             "availability_ends": null,
#             "images": {},
#             "directors": [],
#             "backgrounds": [
#                 "https://canvas-lb.tubitv.com/opts/mv3z7wzkKDElbw==/101b3434-3d1d-4ac2-baa3-a9d151cc17de/CIAPELgIOgUxLjEuOA=="
#             ],
#             "gracenote_id": "SH010854210000",
#             "availability_starts": null,
#             "tags": [
#                 "Sci-Fi",
#                 "Action",
#                 "Drama"
#             ],
#             "video_renditions": [],
#             "genres": [],
#             "posterarts": [
#                 "https://canvas-lb.tubitv.com/opts/E4Z4dSaoBGqMgg==/6101c4db-69a5-4f55-b00b-0d5008160959/CJADEL4EOgUxLjEuOA=="
#             ],
#             "competitors": null,
#             "content_tags": {
#                 "imdb_highly_rated": null,
#                 "poster_labels": null,
#                 "rotten_tomatoes_certified_fresh": null,
#                 "tubi_most_liked": null,
#                 "vibes": null
#             },
#             "ad_languages": [],
#             "login_reason": "UNKNOWN",
#             "player_type": "tubi",
#             "has_subtitle": false,
#             "gn_fields": null,
#             "vibes": null,
#             "year": 2008,
#             "video_metadata": null,
#             "lang": "English",
#             "epg_feed": null,
#             "hero_images": [
#                 "https://canvas-lb.tubitv.com/opts/7-5OdvIhdmplgA==/a7435802-cb93-4b8a-a75b-23cfc65ecfb7/CIAPEKQFOgUxLjEuOA=="
#             ],
#             "air_datetime": null,
#             "type": "s",
#             "actors": [
#                 "Amanda Tapping",
#                 "Robin Dunne",
#                 "Christopher Heyerdahl",
#                 "Ryan Robbins",
#                 "Agam Darshi"
#             ],
#             "teams": null,
#             "thumbnails": [
#                 "https://canvas-lb.tubitv.com/opts/uNOjz3HQgG6-Vg==/a7435802-cb93-4b8a-a75b-23cfc65ecfb7/CIAFEOgCOgUxLjEuOA=="
#             ],
#             "import_id": "filmrise",
#             "video_preview_url": "https://video-preview-lb.production-public.tubi.io/videopreview/a9868f97-32bf-48e0-ab89-8cf0a4eaaa49-start91.861-end193.878.mp4",
#             "ratings": [
#                 {
#                     "code": "TV-14",
#                     "system": "tvpg",
#                     "value": "TV-14",
#                     "descriptors": []
#                 }
#             ],
#             "id": "300008092",
#             "title": "Sanctuary",
#             "is_cdc": false
#         },
#         "0334": {
#             "video_resources": [],
#             "schedule_data": null,
#             "has_trailer": false,
#             "num_seasons": 1,
#             "video_previews": [
#                 {
#                     "url": "https://video-preview-lb.production-public.tubi.io/videopreview/8dbaa8a9-7346-45f9-9b82-bb620be4fccd/8dbaa8a9-7346-45f9-9b82-bb620be4fccd-start615-end691_v2.mp4",
#                     "uuid": "46dd2ec7-4aa4-48c3-a6ca-fc001de8718c"
#                 }
#             ],
#             "description": "Daisy De La Hoya has 18 hot guys to choose from, from all walks of life, as she allows them to move into a Hollywood Mansion and fight for her love.",
#             "availability_duration": null,
#             "league": null,
#             "needs_login": false,
#             "is_recurring": false,
#             "landscape_images": [
#                 "https://canvas-lb.tubitv.com/opts/_Tphguz-QDAoaQ==/05ae9c91-45f1-42e7-b758-da45a2f0bf7f/CMADEPwBOgUxLjEuOA=="
#             ],
#             "publisher_id": "",
#             "availability_ends": null,
#             "images": {},
#             "directors": [
#                 "Cris Abrego",
#                 "Mark Cronin"
#             ],
#             "backgrounds": [
#                 "https://canvas-lb.tubitv.com/opts/LhM846HllbgShQ==/00608fca-ffd3-4e01-8de9-40fe2062bb95/CIAPELgIOgUxLjEuOA=="
#             ],
#             "gracenote_id": "SH011449440000",
#             "availability_starts": null,
#             "tags": [
#                 "Reality",
#                 "Romance"
#             ],
#             "video_renditions": [],
#             "genres": [],
#             "posterarts": [
#                 "https://canvas-lb.tubitv.com/opts/j-mt8DPlzpkyFg==/37af6e81-b7ea-4167-a21d-2f9341b061a7/CJADEL4EOgUxLjEuOA=="
#             ],
#             "competitors": null,
#             "content_tags": {
#                 "imdb_highly_rated": null,
#                 "poster_labels": null,
#                 "rotten_tomatoes_certified_fresh": null,
#                 "tubi_most_liked": null,
#                 "vibes": null
#             },
#             "ad_languages": [],
#             "login_reason": "UNKNOWN",
#             "player_type": "tubi",
#             "has_subtitle": false,
#             "gn_fields": null,
#             "vibes": null,
#             "year": 2009,
#             "video_metadata": null,
#             "lang": "English",
#             "epg_feed": null,
#             "hero_images": [
#                 "https://canvas-lb.tubitv.com/opts/znJQAF0po8A9WA==/209f0d2e-0d3a-43c5-a441-b31743e364fc/CIAPEKQFOgUxLjEuOA=="
#             ],
#             "air_datetime": null,
#             "type": "s",
#             "actors": [
#                 "Riki Rachtman",
#                 "Daisy De La Hoya"
#             ],
#             "teams": null,
#             "thumbnails": [
#                 "https://canvas-lb.tubitv.com/opts/s_a7BBArv9krZg==/196f0097-675c-4b53-a78f-3f48c5e1f289/CIAFEOgCOgUxLjEuOA=="
#             ],
#             "import_id": "endemol",
#             "video_preview_url": "https://video-preview-lb.production-public.tubi.io/videopreview/8dbaa8a9-7346-45f9-9b82-bb620be4fccd/8dbaa8a9-7346-45f9-9b82-bb620be4fccd-start615-end691_v2.mp4",
#             "ratings": [
#                 {
#                     "code": "TV-MA",
#                     "system": "tvpg",
#                     "value": "TV-MA",
#                     "descriptors": []
#                 }
#             ],
#             "id": "334",
#             "title": "Daisy of Love",
#             "is_cdc": false
#         },
#         "100012887": {
#             "video_resources": [],
#             "schedule_data": null,
#             "has_trailer": true,
#             "video_previews": [
#                 {
#                     "url": "https://video-preview-lb.production-public.tubi.io/videopreview/e10aeffd-6b7a-45a4-a75a-05ec69f5ec1c-start1411.538-end1497.032.mp4",
#                     "uuid": "1d6935c6-85a3-4ebb-ae37-55b1a8cd9cd0"
#                 }
#             ],
#             "description": "When Luke is attacked and his fiancée is murdered, he pledges to train himself in combat and use it against anyone who dares to cross his path.",
#             "availability_duration": 31536000,
#             "league": null,
#             "needs_login": false,
#             "landscape_images": [
#                 "https://canvas-lb.tubitv.com/opts/c8h6SlRPY2INuA==/044758fe-600b-4e04-8bb9-16dd15a229b2/CMADEPwBOgUxLjEuOA=="
#             ],
#             "publisher_id": "95c4f7da4bfefb2d4f78fea1b0046ed6",
#             "trailers": [
#                 {
#                     "id": "600008586",
#                     "duration": 165,
#                     "url": "https://aka2.tubi.video/2d1f2fef-bb04-4a24-93b4-0ae74c8223bd/z2jpv2rx9z.m3u8?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjZG5fcHJlZml4IjoiaHR0cHM6Ly9ha2EyLnR1YmkudmlkZW8iLCJleHAiOjE3NjI3MjU2MDAsIm1lZGlhX3NpZyI6OTcwMzY3NjN9.ds5nW5tnXnSOBle-xXNe4fI2pGDUHTKhA2pqqbHEads"
#                 }
#             ],
#             "availability_ends": null,
#             "images": {},
#             "directors": [
#                 "Aash Aaron"
#             ],
#             "backgrounds": [
#                 "https://canvas-lb.tubitv.com/opts/Bjq_F6BJrKXSfQ==/e766a9ef-6a04-4704-a0ab-d052b426443b/CIAPELgIOgUxLjEuOA=="
#             ],
#             "gracenote_id": "MV003401140000",
#             "availability_starts": "2018-07-30T00:00:00.000Z",
#             "tags": [
#                 "Action",
#                 "Thriller",
#                 "Crime"
#             ],
#             "video_renditions": [],
#             "genres": [],
#             "posterarts": [
#                 "https://canvas-lb.tubitv.com/opts/JQTkm5OY7d4YpQ==/3a2a7dd1-e383-4a83-ab6c-0bd33eca794a/CJADEL4EOgUxLjEuOA=="
#             ],
#             "competitors": null,
#             "content_tags": {
#                 "imdb_highly_rated": null,
#                 "poster_labels": null,
#                 "rotten_tomatoes_certified_fresh": null,
#                 "tubi_most_liked": null,
#                 "vibes": null
#             },
#             "ad_languages": [],
#             "login_reason": "UNKNOWN",
#             "player_type": "tubi",
#             "has_subtitle": true,
#             "gn_fields": null,
#             "vibes": null,
#             "year": 2008,
#             "duration": 5622,
#             "video_metadata": [],
#             "lang": "English",
#             "epg_feed": null,
#             "hero_images": [
#                 "https://canvas-lb.tubitv.com/opts/5ZFLViqhibv8Kg==/7f1043f0-9ba0-4988-aab1-ad928e8abc9e/CIAPEKQFOgUxLjEuOA=="
#             ],
#             "air_datetime": null,
#             "type": "v",
#             "actors": [
#                 "Margot Robbie",
#                 "Robert Díaz",
#                 "Kazuya Wright",
#                 "Lexie Symon"
#             ],
#             "teams": null,
#             "thumbnails": [
#                 "https://canvas-lb.tubitv.com/opts/xGReh1j2pUFbHw==/8aeb4045-473a-4cee-8661-24f32e5d533b/CIAFEOgCOgUxLjEuOA=="
#             ],
#             "import_id": "all-channel-films",
#             "video_preview_url": "https://video-preview-lb.production-public.tubi.io/videopreview/e10aeffd-6b7a-45a4-a75a-05ec69f5ec1c-start1411.538-end1497.032.mp4",
#             "ratings": [
#                 {
#                     "code": "R",
#                     "system": "mpaa",
#                     "value": "R",
#                     "descriptors": []
#                 }
#             ],
#             "id": "100012887",
#             "title": "Vigilante",
#             "is_cdc": false
#         },
#         "609201": {
#             "video_resources": [],
#             "schedule_data": null,
#             "has_trailer": false,
#             "video_previews": [
#                 {
#                     "url": "https://video-preview-lb.production-public.tubi.io/videopreview/de525315-6ece-4039-9c46-51b3d5e5b1ce/de525315-6ece-4039-9c46-51b3d5e5b1ce-start221-end281_v2.mp4",
#                     "uuid": "602fbaf9-4324-4b9a-b78f-ce61253c4314"
#                 }
#             ],
#             "description": "The true story of the inspiring singer who overcame her years as a homeless teenager and went on to change the R&B music scene forever.",
#             "availability_duration": 31536000,
#             "league": null,
#             "needs_login": false,
#             "landscape_images": [
#                 "https://canvas-lb.tubitv.com/opts/4oNN3_L9JHWQ0Q==/4b2b51fe-4a91-4a1d-911f-562724728acf/CMADEPwBOgUxLjEuOA=="
#             ],
#             "publisher_id": "cb24c07ebda918a000eb2a550063458f",
#             "availability_ends": null,
#             "images": {},
#             "directors": [
#                 "Christine Swanson"
#             ],
#             "backgrounds": [
#                 "https://canvas-lb.tubitv.com/opts/EYQgsYSGJWczEg==/a43f8731-1697-4204-95e9-135c7c2bca19/CIAPELgIOgUxLjEuOA=="
#             ],
#             "gracenote_id": "MV008951540000",
#             "availability_starts": "2014-01-01T00:00:00.000Z",
#             "tags": [
#                 "Drama",
#                 "Music"
#             ],
#             "video_renditions": [],
#             "genres": [],
#             "posterarts": [
#                 "https://canvas-lb.tubitv.com/opts/Ny70_EBnjj4e1w==/cf5e3985-528f-4779-b05f-cb40f917b8de/CJADEL4EOgUxLjEuOA=="
#             ],
#             "competitors": null,
#             "content_tags": {
#                 "imdb_highly_rated": null,
#                 "poster_labels": null,
#                 "rotten_tomatoes_certified_fresh": null,
#                 "tubi_most_liked": null,
#                 "vibes": null
#             },
#             "ad_languages": [],
#             "login_reason": "UNKNOWN",
#             "player_type": "tubi",
#             "has_subtitle": true,
#             "gn_fields": null,
#             "vibes": null,
#             "year": 2016,
#             "duration": 4935,
#             "video_metadata": [],
#             "lang": "English",
#             "epg_feed": null,
#             "hero_images": [
#                 "https://canvas-lb.tubitv.com/opts/5jlP9iZE0R9L-A==/49c9feb9-2422-4a2f-aa34-b6c874c98599/CIAPEKQFOgUxLjEuOA=="
#             ],
#             "air_datetime": null,
#             "type": "v",
#             "actors": [
#                 "Teyonah Parris",
#                 "Gary Dourdan",
#                 "Darius McCrary"
#             ],
#             "teams": null,
#             "thumbnails": [
#                 "https://canvas-lb.tubitv.com/opts/-UnrnnHoY6GHFA==/85ae5909-818d-4cc9-b7ff-d9e98ec39d66/CIAFEOgCOgUxLjEuOA=="
#             ],
#             "import_id": "tv-one",
#             "video_preview_url": "https://video-preview-lb.production-public.tubi.io/videopreview/de525315-6ece-4039-9c46-51b3d5e5b1ce/de525315-6ece-4039-9c46-51b3d5e5b1ce-start221-end281_v2.mp4",
#             "ratings": [
#                 {
#                     "code": "TV-14",
#                     "system": "tvpg",
#                     "value": "TV-14",
#                     "descriptors": []
#                 }
#             ],
#             "id": "609201",
#             "title": "Love Under New Management: The Miki Howard Story",
#             "is_cdc": false
#         },
#         "617695": {
#             "video_resources": [],
#             "schedule_data": null,
#             "has_trailer": true,
#             "video_previews": [
#                 {
#                     "url": "https://video-preview-lb.production-public.tubi.io/videopreview/f0c23949-d4d3-4609-8ac3-4e3d9a9cdb88-start15.456-end70.279.mp4",
#                     "uuid": "b4e252ea-b521-40fd-80b0-099e0aac520b"
#                 }
#             ],
#             "description": "The romance of pop star Gwen Stefani and country rocker Blake Shelton is shown, from their music careers to falling in love on the show “The Voice.”",
#             "availability_duration": 31536000,
#             "league": null,
#             "needs_login": false,
#             "landscape_images": [
#                 "https://canvas-lb.tubitv.com/opts/z4NEAlvT_PixaQ==/2d5222ef-ec88-4b47-b46b-065797da8886/CMADEPwBOgUxLjEuOA=="
#             ],
#             "publisher_id": "aa4cefde9ba4469e051f935624aff54f",
#             "trailers": [
#                 {
#                     "id": "617699",
#                     "duration": 117,
#                     "url": "https://aka.tubi.video/1d12da1d-b176-41ad-a3b0-be70d27c5d5b/ovd4e6g5fu.m3u8?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjZG5fcHJlZml4IjoiaHR0cHM6Ly9ha2EudHViaS52aWRlbyIsImV4cCI6MTc2MjU2NzIwMCwibWVkaWFfc2lnIjozNzY1MTY4NX0.EVNhlFXjR2kd7jdzO0yF5nljBUJUffc5nsb_xveQmK0"
#                 }
#             ],
#             "availability_ends": null,
#             "images": {},
#             "directors": [
#                 "Danielle WInter"
#             ],
#             "backgrounds": [
#                 "https://canvas-lb.tubitv.com/opts/hwC6uK-19HrE9A==/44c4448d-567c-41bb-b93b-9e1b3c2afc91/CIAPELgIOgUxLjEuOA=="
#             ],
#             "gracenote_id": "SH041683220000",
#             "availability_starts": "2014-01-01T00:00:00.000Z",
#             "tags": [
#                 "Documentary",
#                 "Music",
#                 "Romance"
#             ],
#             "video_renditions": [],
#             "genres": [],
#             "posterarts": [
#                 "https://canvas-lb.tubitv.com/opts/ocbu_9SxeHXsXA==/48c9740c-3363-42a3-b28a-3187de2697db/CJADEL4EOgUxLjEuOA=="
#             ],
#             "competitors": null,
#             "content_tags": {
#                 "imdb_highly_rated": null,
#                 "poster_labels": null,
#                 "rotten_tomatoes_certified_fresh": null,
#                 "tubi_most_liked": null,
#                 "vibes": null
#             },
#             "ad_languages": [],
#             "login_reason": "UNKNOWN",
#             "player_type": "tubi",
#             "has_subtitle": true,
#             "gn_fields": null,
#             "vibes": null,
#             "year": 2021,
#             "duration": 3242,
#             "video_metadata": [],
#             "lang": "English",
#             "epg_feed": null,
#             "hero_images": [
#                 "https://canvas-lb.tubitv.com/opts/r5VVP2d07D20PA==/8a896ccd-206d-40de-8670-872ec051dc9f/CIAPEKQFOgUxLjEuOA=="
#             ],
#             "air_datetime": null,
#             "type": "v",
#             "actors": [
#                 "Gwen Stefani",
#                 "Blake Shelton",
#                 "Sharon Feingold"
#             ],
#             "teams": null,
#             "thumbnails": [
#                 "https://canvas-lb.tubitv.com/opts/tUVP6hBCM6iEYg==/39edc900-27b7-46f4-b03b-323d8ef7422b/CIAFEOgCOgUxLjEuOA=="
#             ],
#             "import_id": "legacy-distribution",
#             "video_preview_url": "https://video-preview-lb.production-public.tubi.io/videopreview/f0c23949-d4d3-4609-8ac3-4e3d9a9cdb88-start15.456-end70.279.mp4",
#             "ratings": [
#                 {
#                     "code": "TV-14",
#                     "system": "tvpg",
#                     "value": "TV-14",
#                     "descriptors": []
#                 }
#             ],
#             "id": "617695",
#             "title": "Blake & Gwen: Now & Then",
#             "is_cdc": false
#         },
#         "618737": {
#             "video_resources": [],
#             "schedule_data": null,
#             "has_trailer": false,
#             "video_previews": [
#                 {
#                     "url": "https://video-preview-lb.production-public.tubi.io/videopreview/0cee3209-a56d-413e-b178-79419317177f-start1272.813-end1341.730.mp4",
#                     "uuid": "bd341adf-c2ef-4cc4-951c-b64b6bab6c36"
#                 }
#             ],
#             "description": "Jodie Foster plays an orphaned young woman living in 1900’s New Zealand. After she marries an older businessman, he desires to play an unusual game.",
#             "availability_duration": 31536000,
#             "league": null,
#             "needs_login": false,
#             "landscape_images": [
#                 "https://canvas-lb.tubitv.com/opts/04kOw2v4IC1QOg==/943bc7bd-5715-4116-97b4-cffe167711f9/CMADEPwBOgUxLjEuOA=="
#             ],
#             "publisher_id": "fce9d37fc5c71c2f4bd5e2847e766e55",
#             "availability_ends": "2041-12-31T23:59:59.000Z",
#             "images": {},
#             "directors": [
#                 "Michael Laughlin"
#             ],
#             "backgrounds": [
#                 "https://canvas-lb.tubitv.com/opts/H-x893LyD5nbSA==/29d2124d-b355-4876-8ed3-d5ecea41761b/CIAPELgIOgUxLjEuOA=="
#             ],
#             "gracenote_id": "MV000213320000",
#             "availability_starts": "2021-09-03T00:00:00.000Z",
#             "tags": [
#                 "Drama",
#                 "Romance"
#             ],
#             "video_renditions": [],
#             "genres": [],
#             "posterarts": [
#                 "https://canvas-lb.tubitv.com/opts/kkyWdPmdRWDdTQ==/d222e48b-aa3a-4a97-b466-1db6dd3c9923/CJADEL4EOgUxLjEuOA=="
#             ],
#             "competitors": null,
#             "content_tags": {
#                 "imdb_highly_rated": null,
#                 "poster_labels": null,
#                 "rotten_tomatoes_certified_fresh": null,
#                 "tubi_most_liked": null,
#                 "vibes": null
#             },
#             "ad_languages": [],
#             "login_reason": "UNKNOWN",
#             "player_type": "tubi",
#             "has_subtitle": true,
#             "gn_fields": null,
#             "vibes": null,
#             "year": 1984,
#             "duration": 5391,
#             "video_metadata": [],
#             "lang": "English",
#             "epg_feed": null,
#             "hero_images": [
#                 "https://canvas-lb.tubitv.com/opts/KgrO7-WPRxmalA==/b9800376-7113-4990-96f5-ef17f4600c82/CIAPEKQFOgUxLjEuOA=="
#             ],
#             "air_datetime": null,
#             "type": "v",
#             "actors": [
#                 "Jodie Foster",
#                 "John Lithgow",
#                 "Michael Murphy"
#             ],
#             "teams": null,
#             "thumbnails": [
#                 "https://canvas-lb.tubitv.com/opts/HUq3SVMh3Ljq1A==/dabf6701-52a1-4f58-9a5d-37d295c0319f/CIAFEOgCOgUxLjEuOA=="
#             ],
#             "import_id": "filmrise",
#             "video_preview_url": "https://video-preview-lb.production-public.tubi.io/videopreview/0cee3209-a56d-413e-b178-79419317177f-start1272.813-end1341.730.mp4",
#             "ratings": [
#                 {
#                     "code": "PG",
#                     "system": "mpaa",
#                     "value": "PG",
#                     "descriptors": []
#                 }
#             ],
#             "id": "618737",
#             "title": "Mesmerized",
#             "is_cdc": false
#         },
#         "630357": {
#             "video_resources": [],
#             "schedule_data": null,
#             "has_trailer": true,
#             "video_previews": [
#                 {
#                     "url": "https://video-preview-lb.production-public.tubi.io/videopreview/9452049d-ac9a-4ffe-b97a-4cabd69bc8c7-start15.734-end84.630.mp4",
#                     "uuid": "afa6b92d-c6a5-4ca1-a091-ec05f186ff76"
#                 }
#             ],
#             "description": "A major feature-length documentary that corrects the misconceptions of Diana as a victim of the Royal family and shows how she changed them forever.",
#             "availability_duration": 31536000,
#             "league": null,
#             "needs_login": false,
#             "landscape_images": [
#                 "https://canvas-lb.tubitv.com/opts/Ue7JkYWtOayZfA==/75c67a71-1512-418f-9826-6a30729392a6/CMADEPwBOgUxLjEuOA=="
#             ],
#             "publisher_id": "e6d457189261018d9566b039aebcbc75",
#             "trailers": [
#                 {
#                     "id": "630358",
#                     "duration": 264,
#                     "url": "https://fa.tubi.video/ac86355f-bcbb-4301-966d-6a1f3d51c82e/sxucddlpfa.m3u8?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjZG5fcHJlZml4IjoiaHR0cHM6Ly9mYS50dWJpLnZpZGVvIiwiZXhwIjoxNzYyNjg2MDAwLCJtZWRpYV9zaWciOjQyMzE5OTcyfQ.2KnqCiQT1_ekNRYIUPe2e3ot7M0D7jc10pYOxoMmEyY"
#                 }
#             ],
#             "availability_ends": null,
#             "images": {},
#             "directors": [
#                 "Sonia Anderson"
#             ],
#             "backgrounds": [
#                 "https://canvas-lb.tubitv.com/opts/uSfu06P93oPbtA==/5e522217-1d83-4dba-a306-353ca2fd3f6e/CIAPELgIOgUxLjEuOA=="
#             ],
#             "gracenote_id": "SH030393460000",
#             "availability_starts": "2014-01-01T00:00:00.000Z",
#             "tags": [
#                 "Documentary"
#             ],
#             "video_renditions": [],
#             "genres": [],
#             "posterarts": [
#                 "https://canvas-lb.tubitv.com/opts/W7SXG6Qo14FaGA==/6c04df0a-d4e6-4e4c-b9f9-ad472ba48fd1/CJADEL4EOgUxLjEuOA=="
#             ],
#             "competitors": null,
#             "content_tags": {
#                 "imdb_highly_rated": null,
#                 "poster_labels": null,
#                 "rotten_tomatoes_certified_fresh": null,
#                 "tubi_most_liked": null,
#                 "vibes": null
#             },
#             "ad_languages": [],
#             "login_reason": "UNKNOWN",
#             "player_type": "tubi",
#             "has_subtitle": true,
#             "gn_fields": null,
#             "vibes": null,
#             "year": 2021,
#             "duration": 5620,
#             "video_metadata": [],
#             "lang": "English",
#             "epg_feed": null,
#             "hero_images": [
#                 "https://canvas-lb.tubitv.com/opts/slitLUDeYqJ9Pg==/9a57b53a-a993-49db-8f0c-c15b8363a42a/CIAPEKQFOgUxLjEuOA=="
#             ],
#             "air_datetime": null,
#             "type": "v",
#             "actors": [
#                 "Louise Barrett"
#             ],
#             "teams": null,
#             "thumbnails": [
#                 "https://canvas-lb.tubitv.com/opts/8EzIzTbsc9Z32Q==/a7834443-722b-4632-bfda-b93b5ad4a0e6/CIAFEOgCOgUxLjEuOA=="
#             ],
#             "import_id": "screenbound",
#             "video_preview_url": "https://video-preview-lb.production-public.tubi.io/videopreview/9452049d-ac9a-4ffe-b97a-4cabd69bc8c7-start15.734-end84.630.mp4",
#             "ratings": [
#                 {
#                     "code": "TV-PG",
#                     "system": "tvpg",
#                     "value": "TV-PG",
#                     "descriptors": []
#                 }
#             ],
#             "id": "630357",
#             "title": "Princess Diana: The Woman Inside",
#             "is_cdc": false
#         },
#         "643370": {
#             "video_resources": [],
#             "schedule_data": null,
#             "has_trailer": false,
#             "video_previews": [
#                 {
#                     "url": "https://video-preview-lb.production-public.tubi.io/videopreview/c6318d00-c830-40b8-9519-472c867ce055-start931.536-end969.398.mp4",
#                     "uuid": "25e192e4-ff81-4a5f-9e47-e264e143ad89"
#                 }
#             ],
#             "description": "Based on Nick Hornby's eponymous autobiographical bestseller, this British rom-com tackles the love triangle of a man, a woman, and a football team.",
#             "availability_duration": 31536000,
#             "league": null,
#             "needs_login": false,
#             "landscape_images": [
#                 "https://canvas-lb.tubitv.com/opts/6Q_v4PV7YRMaXQ==/47e4238e-49b9-42d4-9206-eb155458a32d/CMADEPwBOgUxLjEuOA=="
#             ],
#             "publisher_id": "239b1a0696748c0b931642a1dfefbd9e",
#             "availability_ends": null,
#             "images": {},
#             "directors": [
#                 "David Evans"
#             ],
#             "backgrounds": [
#                 "https://canvas-lb.tubitv.com/opts/E9AH76YhVZAY6w==/02dd0942-7aa5-46c4-ad3d-d0fb6355b450/CIAPELgIOgUxLjEuOA=="
#             ],
#             "gracenote_id": "MV000807390000",
#             "availability_starts": "2022-01-18T00:00:00.000Z",
#             "tags": [
#                 "Comedy",
#                 "Drama",
#                 "Romance"
#             ],
#             "video_renditions": [],
#             "genres": [],
#             "posterarts": [
#                 "https://canvas-lb.tubitv.com/opts/5yH-qAT94zmAfQ==/e4f140fb-9165-42e8-8f20-20b61d13990b/CJADEL4EOgUxLjEuOA=="
#             ],
#             "competitors": null,
#             "content_tags": {
#                 "imdb_highly_rated": null,
#                 "poster_labels": null,
#                 "rotten_tomatoes_certified_fresh": null,
#                 "tubi_most_liked": null,
#                 "vibes": null
#             },
#             "ad_languages": [],
#             "login_reason": "UNKNOWN",
#             "player_type": "tubi",
#             "has_subtitle": false,
#             "gn_fields": null,
#             "vibes": null,
#             "year": 1997,
#             "duration": 6189,
#             "video_metadata": [],
#             "lang": "English",
#             "epg_feed": null,
#             "hero_images": [
#                 "https://canvas-lb.tubitv.com/opts/49iU9iSXD4984A==/c5f203b4-bb9e-45ae-995a-b6f925643a8e/CIAPEKQFOgUxLjEuOA=="
#             ],
#             "air_datetime": null,
#             "type": "v",
#             "actors": [
#                 "Colin Firth",
#                 "Ruth Gemmell",
#                 "Luke Aikman",
#                 "Mark Strong"
#             ],
#             "teams": null,
#             "thumbnails": [
#                 "https://canvas-lb.tubitv.com/opts/j2v-dAWOXxTbqg==/aa67e5bc-7a90-41a5-ba5f-fff47a3bca7c/CIAFEOgCOgUxLjEuOA=="
#             ],
#             "import_id": "signature-entertainment",
#             "video_preview_url": "https://video-preview-lb.production-public.tubi.io/videopreview/c6318d00-c830-40b8-9519-472c867ce055-start931.536-end969.398.mp4",
#             "ratings": [
#                 {
#                     "code": "R",
#                     "system": "mpaa",
#                     "value": "R",
#                     "descriptors": []
#                 }
#             ],
#             "id": "643370",
#             "title": "Fever Pitch",
#             "is_cdc": false
#         },
#         "643397": {
#             "video_resources": [],
#             "schedule_data": null,
#             "has_trailer": true,
#             "video_previews": [
#                 {
#                     "url": "https://video-preview-lb.production-public.tubi.io/videopreview/4002351f-bdc0-412d-b507-e2112246b363-start247.974-end324.402.mp4",
#                     "uuid": "be2041ba-c82b-4ff8-8a35-d6c1c83d8ee7"
#                 }
#             ],
#             "description": "In this wicked, sexy cult classic, based on the book Dangerous Liaisons, venomous step-siblings make a bet involving the deflowering of a schoolmate.",
#             "availability_duration": 31536000,
#             "league": null,
#             "needs_login": false,
#             "landscape_images": [
#                 "https://canvas-lb.tubitv.com/opts/tzSDFfcUUaKYzQ==/5e1226a3-3735-44a4-b605-80c26207b215/CMADEPwBOgUxLjEuOA=="
#             ],
#             "publisher_id": "239b1a0696748c0b931642a1dfefbd9e",
#             "trailers": [
#                 {
#                     "id": "643398",
#                     "duration": 141,
#                     "url": "https://aka.tubi.video/98e984b5-09df-4bfa-8011-359fcd867280/u82zn02bdi.m3u8?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjZG5fcHJlZml4IjoiaHR0cHM6Ly9ha2EudHViaS52aWRlbyIsImV4cCI6MTc2MjY4NjAwMCwibWVkaWFfc2lnIjo2NDMwMTkwMX0.TkSG7KQir0a69Ok85sPkuhkh--ZY6Hn6uk_-d1iQIlM"
#                 }
#             ],
#             "availability_ends": null,
#             "images": {},
#             "directors": [
#                 "Roger Kumble"
#             ],
#             "backgrounds": [
#                 "https://canvas-lb.tubitv.com/opts/n1zigJm3JP-b6A==/45de43c0-dbd6-44d2-b7db-fe449cdea960/CIAPELgIOgUxLjEuOA=="
#             ],
#             "gracenote_id": "MV000711510000",
#             "availability_starts": "2022-01-18T00:00:00.000Z",
#             "tags": [
#                 "Drama",
#                 "Romance"
#             ],
#             "video_renditions": [],
#             "genres": [],
#             "posterarts": [
#                 "https://canvas-lb.tubitv.com/opts/yfRQMsIN0mp7UQ==/0a4324b6-f827-4de8-ac88-4562476c48e6/CJADEL4EOgUxLjEuOA=="
#             ],
#             "competitors": null,
#             "content_tags": {
#                 "imdb_highly_rated": null,
#                 "poster_labels": null,
#                 "rotten_tomatoes_certified_fresh": null,
#                 "tubi_most_liked": null,
#                 "vibes": null
#             },
#             "ad_languages": [],
#             "login_reason": "UNKNOWN",
#             "player_type": "tubi",
#             "has_subtitle": false,
#             "gn_fields": null,
#             "vibes": null,
#             "year": 1999,
#             "duration": 5866,
#             "video_metadata": [],
#             "lang": "English",
#             "epg_feed": null,
#             "hero_images": [
#                 "https://canvas-lb.tubitv.com/opts/sDywZuZ75ujIZA==/eaec4da7-4be8-4ca1-9305-98648b5366df/CIAPEKQFOgUxLjEuOA=="
#             ],
#             "air_datetime": null,
#             "type": "v",
#             "actors": [
#                 "Sarah Michelle Gellar",
#                 "Ryan Phillippe",
#                 "Reese Witherspoon",
#                 "Selma Blair",
#                 "Joshua Jackson",
#                 "Tara Reid",
#                 "Christine Baranski"
#             ],
#             "teams": null,
#             "thumbnails": [
#                 "https://canvas-lb.tubitv.com/opts/bv0GYFKfgMJ-WA==/1aa6644f-d196-4884-96fa-9777414de071/CIAFEOgCOgUxLjEuOA=="
#             ],
#             "import_id": "signature-entertainment",
#             "video_preview_url": "https://video-preview-lb.production-public.tubi.io/videopreview/4002351f-bdc0-412d-b507-e2112246b363-start247.974-end324.402.mp4",
#             "ratings": [
#                 {
#                     "code": "R",
#                     "system": "mpaa",
#                     "value": "R",
#                     "descriptors": []
#                 }
#             ],
#             "id": "643397",
#             "title": "Cruel Intentions",
#             "is_cdc": false
#         },
#         "689248": {
#             "video_resources": [],
#             "schedule_data": null,
#             "has_trailer": false,
#             "video_previews": [
#                 {
#                     "url": "https://video-preview-lb.production-public.tubi.io/videopreview/30f0d944-74b1-43ba-b7f8-d385724d4edc/30f0d944-74b1-43ba-b7f8-d385724d4edc-start681-end740_v2.mp4",
#                     "uuid": "05625869-2fe4-4a70-ae2b-72d8e967e574"
#                 }
#             ],
#             "description": "When the victim of a home robbery kills her intruder in self defense, his girlfriend sets out to destroy her life by infiltrating her support group.",
#             "availability_duration": 31536000,
#             "league": null,
#             "needs_login": false,
#             "landscape_images": [
#                 "https://canvas-lb.tubitv.com/opts/ZSRn080iMDug6w==/218ba0f0-7a63-40cd-8311-31b078361a97/CMADEPwBOgUxLjEuOA=="
#             ],
#             "publisher_id": "9fb073304145fad6aa220922cb970104",
#             "availability_ends": null,
#             "images": {},
#             "directors": [
#                 "Doug Campbell"
#             ],
#             "backgrounds": [
#                 "https://canvas-lb.tubitv.com/opts/VLznGvUAN_Ff4Q==/dcaec89f-bb1b-45ad-81bf-773f8ee3f595/CIAPELgIOgUxLjEuOA=="
#             ],
#             "gracenote_id": "MV003887370000",
#             "availability_starts": "2014-01-01T00:00:00.000Z",
#             "tags": [
#                 "Thriller",
#                 "Drama"
#             ],
#             "video_renditions": [],
#             "genres": [],
#             "posterarts": [
#                 "https://canvas-lb.tubitv.com/opts/8T2qPmQKGSTZHw==/e48fd15d-2523-4186-b06d-accbc1f270b0/CJADEL4EOgUxLjEuOA=="
#             ],
#             "competitors": null,
#             "content_tags": {
#                 "imdb_highly_rated": null,
#                 "poster_labels": null,
#                 "rotten_tomatoes_certified_fresh": null,
#                 "tubi_most_liked": null,
#                 "vibes": null
#             },
#             "ad_languages": [],
#             "login_reason": "UNKNOWN",
#             "player_type": "tubi",
#             "has_subtitle": true,
#             "gn_fields": null,
#             "vibes": null,
#             "year": 2012,
#             "duration": 5481,
#             "video_metadata": [],
#             "lang": "English",
#             "epg_feed": null,
#             "hero_images": [
#                 "https://canvas-lb.tubitv.com/opts/gZKHaY8QKoztCA==/867cf659-d5c0-4dc6-a42f-c39e021783fa/CIAPEKQFOgUxLjEuOA=="
#             ],
#             "air_datetime": null,
#             "type": "v",
#             "actors": [
#                 "Haylie Duff",
#                 "Lisa Sheridan",
#                 "Jason Brooks",
#                 "C. Thomas Howell",
#                 "Barbara Niven",
#                 "Al Sapienza",
#                 "Kyla Dang",
#                 "Taymour Ghazi",
#                 "Jason Stuart",
#                 "Veralyn Jones"
#             ],
#             "teams": null,
#             "thumbnails": [
#                 "https://canvas-lb.tubitv.com/opts/WjOXNy5f09u8Xw==/f3f768e6-15a7-49c3-ae0a-bf3b1733fca5/CIAFEOgCOgUxLjEuOA=="
#             ],
#             "import_id": "johnson-production-group",
#             "video_preview_url": "https://video-preview-lb.production-public.tubi.io/videopreview/30f0d944-74b1-43ba-b7f8-d385724d4edc/30f0d944-74b1-43ba-b7f8-d385724d4edc-start681-end740_v2.mp4",
#             "ratings": [
#                 {
#                     "code": "TV-14",
#                     "system": "tvpg",
#                     "value": "TV-14",
#                     "descriptors": []
#                 }
#             ],
#             "id": "689248",
#             "title": "Home Invasion",
#             "is_cdc": false
#         }
#     },
#     "personalization_id": "rn_pid:50be6838-f094-4083-8968-21b7c4a717cd",
#     "valid_duration": 5521
# }
