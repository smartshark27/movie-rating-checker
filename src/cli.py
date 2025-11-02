import argparse
import os
import sys
from tenplay import get_10play_media_list
from abciview import get_abc_media_list
from sbs import get_sbs_media_list
from tmdb import get_tmdb_media_list
from utils import (
    create_dir_if_not_exists,
    delete_dir_if_exists,
    read_json_file,
    save_to_json_file,
)


def main():
    parser = argparse.ArgumentParser(description="Movie Rating Checker CLI")
    parser.add_argument(
        "media_sources",
        nargs="*",
        choices=[
            "10play-movies",
            "10play-shows-comedy",
            "10play-shows-drama",
            "10play-shows-kids",
            "abc-movies-a-z",
            "abc-movies-of-the-week",
            "abc-shows-best-of-british-tv",
            "abc-shows-comedy-gold",
            "abc-shows-time-for-a-rewatch",
            "abc-shows-timeless-tv-classics",
            "abc-shows-tv-shows-for-big-kids",
            "sbs-movies-all",
            "sbs-movies-recently-added",
            "sbs-shows-all",
            "sbs-shows-bingeable-box-sets",
            "sbs-shows-recently-added",
        ],
        help="The media sources to check. You can specify multiple sources separated by spaces.",
    )
    parser.add_argument(
        "--tmdb-api-key",
        type=str,
        help="The TMDB API key. If not provided, it will be fetched from the TMDB_API_KEY environment variable.",
    )
    parser.add_argument(
        "--movies-min-rating",
        type=float,
        default=7.0,
        help="Minimum TMDB rating for movies to include. Default is 7.0.",
    )
    parser.add_argument(
        "--movies-min-rating-count",
        type=int,
        default=300,
        help="Minimum TMDB rating count for movies to include. Default is 300.",
    )
    parser.add_argument(
        "--shows-min-rating",
        type=float,
        default=7.0,
        help="Minimum TMDB rating for shows to include. Default is 7.0.",
    )
    parser.add_argument(
        "--shows-min-rating-count",
        type=int,
        default=300,
        help="Minimum TMDB rating count for shows to include. Default is 300.",
    )
    parser.add_argument(
        "--sort-by",
        choices=["tmdb-rating", "tmdb-rating-count", "tmdb-popularity"],
        default="tmdb-rating",
        help="Sort the movies by 'tmdb-rating' or 'tmdb-popularity'. Default is 'tmdb-rating'.",
    )
    args = parser.parse_args()

    # Get the TMDB API key
    tmdb_api_key = args.tmdb_api_key or os.getenv("TMDB_API_KEY")
    if not tmdb_api_key:
        print(
            "Error: TMDB API key is required. Provide it via --tmdb-api-key or set the TMDB_API_KEY environment variable."
        )
        sys.exit(1)

    # Get media list from specified sources
    media_list = []
    for source in args.media_sources:
        if source.startswith("abc-"):
            media_list.extend(get_abc_media_list(source.replace("abc-", "")))
        elif source.startswith("sbs-"):
            media_list.extend(get_sbs_media_list(source.replace("sbs-", "")))
        elif source.startswith("10play-"):
            media_list.extend(get_10play_media_list(source.replace("10play-", "")))

    # Enrich media list with TMDB data
    tmdb_media_list = get_tmdb_media_list(tmdb_api_key, media_list)

    # Remove duplicates based on mediaType and title
    seen_media = set()
    unique_tmdb_media_list = []
    for media in tmdb_media_list:
        media_key = (media["mediaType"], media["title"])
        if media_key not in seen_media:
            unique_tmdb_media_list.append(media)
            seen_media.add(media_key)
    tmdb_media_list = unique_tmdb_media_list

    # Filter by minimum rating count
    tmdb_media_list = [
        m
        for m in tmdb_media_list
        if (
            m["mediaType"] == "movie"
            and m.get("tmdbRating", 0) >= args.movies_min_rating
            and m.get("tmdbRatingCount", 0) >= args.movies_min_rating_count
        )
        or (
            m["mediaType"] == "show"
            and m.get("tmdbRating", 0) >= args.shows_min_rating
            and m.get("tmdbRatingCount", 0) >= args.shows_min_rating_count
        )
    ]

    # Sort the movies
    if args.sort_by == "tmdb-rating":
        tmdb_media_list.sort(key=lambda x: x.get("tmdbRating", 0), reverse=True)
    elif args.sort_by == "tmdb-rating-count":
        tmdb_media_list.sort(key=lambda x: x.get("tmdbRatingCount", 0), reverse=True)
    elif args.sort_by == "tmdb-popularity":
        tmdb_media_list.sort(key=lambda x: x.get("tmdbPopularity", 0), reverse=True)

    # Save to output file
    output_dir = "output"
    delete_dir_if_exists(output_dir)
    create_dir_if_not_exists(output_dir)
    all_output_file = f"{output_dir}/all-media.json"
    save_to_json_file(tmdb_media_list, all_output_file)
    print(f"Saved {len(tmdb_media_list)} media to {all_output_file}")

    # Load previous output if exists
    previous_output_file = "cache/previous-media.json"
    if os.path.exists(previous_output_file):
        previous_media_list = []
        try:
            previous_media_list = read_json_file(previous_output_file)
            print(f"Loaded {len(previous_media_list)} items from previous output")
        except Exception as e:
            print(f"Error loading previous output: {e}")

        # Find new additions
        previous_titles = {m["title"] for m in previous_media_list}
        new_additions = [
            m for m in tmdb_media_list if m["title"] not in previous_titles
        ]
        if new_additions:
            new_output_file = f"{output_dir}/new-media.json"
            save_to_json_file(new_additions, new_output_file)
            print(f"Saved {len(new_additions)} new media to {new_output_file}")
        else:
            print("No new media found since last run.")
    else:
        print("No previous output found, skipping new media check.")

    # Save current output as previous for next run
    create_dir_if_not_exists("cache")
    save_to_json_file(tmdb_media_list, previous_output_file)

    print("Done.")


if __name__ == "__main__":
    main()
