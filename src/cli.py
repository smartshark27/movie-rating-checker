import argparse
import os
import sys
from abciview import get_abc_media_list
from sbs import get_sbs_media_list
from tmdb import get_tmdb_media_list
from utils import create_dir_if_not_exists, save_to_json_file


def main():
    parser = argparse.ArgumentParser(description="Movie Rating Checker CLI")
    parser.add_argument(
        "media_source",
        choices=[
            "abc-all-movies",
            "abc-movies-of-the-week",
            "sbs-recently-added-movies",
            "sbs-all-movies",
        ],
        help="The media source to check.",
    )
    parser.add_argument(
        "--tmdb-api-key",
        type=str,
        help="The TMDB API key. If not provided, it will be fetched from the TMDB_API_KEY environment variable.",
    )
    parser.add_argument(
        "--sort-by",
        choices=["tmdb-rating", "tmdb-rating-count", "tmdb-popularity"],
        default="tmdb-rating",
        help="Sort the movies by 'tmdb-rating' or 'tmdb-popularity'. Default is 'tmdb-rating'.",
    )
    parser.add_argument(
        "--min-rating",
        type=int,
        default=7,
        help="Minimum rating to include a movie in the output. Default is 7.",
    )
    parser.add_argument(
        "--min-rating-count",
        type=int,
        default=100,
        help="Minimum number of ratings to include a movie in the output. Default is 100.",
    )
    args = parser.parse_args()

    # Get the TMDB API key
    tmdb_api_key = args.tmdb_api_key or os.getenv("TMDB_API_KEY")
    if not tmdb_api_key:
        print(
            "Error: TMDB API key is required. Provide it via --tmdb-api-key or set the TMDB_API_KEY environment variable."
        )
        sys.exit(1)

    media_list = []
    if args.media_source == "abc-all-movies":
        media_list = get_abc_media_list("all-movies")
    if args.media_source == "abc-movies-of-the-week":
        media_list = get_abc_media_list("movies-of-the-week")
    elif args.media_source == "sbs-recently-added-movies":
        media_list = get_sbs_media_list("recently-added-movies")
    elif args.media_source == "sbs-all-movies":
        media_list = get_sbs_media_list("all-movies")

    tmdb_media_list = get_tmdb_media_list(tmdb_api_key, media_list)

    # Filter by minimum rating count
    tmdb_media_list = [
        m
        for m in tmdb_media_list
        if m.get("tmdbRatingCount", 0) >= args.min_rating_count
        and m.get("tmdbRating", 0) >= args.min_rating
    ]

    # Sort the movies
    if args.sort_by == "tmdb-rating":
        tmdb_media_list.sort(key=lambda x: x.get("tmdbRating", 0), reverse=True)
    elif args.sort_by == "tmdb-rating-count":
        tmdb_media_list.sort(key=lambda x: x.get("tmdbRatingCount", 0), reverse=True)
    elif args.sort_by == "tmdb-popularity":
        tmdb_media_list.sort(key=lambda x: x.get("tmdbPopularity", 0), reverse=True)

    # Save to output file
    create_dir_if_not_exists("output")
    output_file = "output/" + args.media_source.replace("-", "_") + "_with_tmdb.json"
    save_to_json_file(tmdb_media_list, output_file)
    print(f"Saved {len(tmdb_media_list)} movies to {output_file}")

    print("Done.")


if __name__ == "__main__":
    main()
