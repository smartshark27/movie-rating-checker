
# Movie Rating Checker

## Overview

The `movie-rating-checker` CLI fetches movie lists from ABC iView and SBS, enriches them with TMDB ratings and popularity, and saves the results as JSON files. You can filter and sort the output using various criteria.

## Prerequisites

1. **Python**: Version 3.7 or higher is recommended.
2. **TMDB API Key**: Get an API key from [The Movie Database (TMDB)](https://www.themoviedb.org/documentation/api).

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/movie-rating-checker.git
cd movie-rating-checker
pip install -r requirements.txt
```

## Usage

Run the CLI script with:

```bash
python src/cli.py <media_source> [--tmdb-api-key <key>] [--sort-by <criteria>] [--min-rating-count <count>]
```

### Positional Arguments

- `media_source`: The source of movies to check. Options:
    - `abc-all-movies`: All movies from ABC iView
    - `abc-movies-of-the-week`: ABC iView Movies of the Week
    - `sbs-recently-added-movies`: Recently added movies from SBS
    - `sbs-all-movies`: All movies from SBS

### Optional Arguments

- `--tmdb-api-key`: Your TMDB API key. If not provided, the script uses the `TMDB_API_KEY` environment variable.
- `--sort-by`: Sort criteria. Options:
    - `tmdb-rating` (default): Sort by TMDB rating
    - `tmdb-rating-count`: Sort by number of TMDB ratings
    - `tmdb-popularity`: Sort by TMDB popularity
- `--min-rating-count`: Minimum number of ratings required to include a movie in the output. Default is `100`.

## Examples

1. Fetch all ABC iView movies and sort by TMDB rating:
        ```bash
        python src/cli.py abc-all-movies --tmdb-api-key YOUR_API_KEY
        ```

2. Fetch SBS recently added movies, sort by popularity, and set a minimum rating count of 500:
        ```bash
        python src/cli.py sbs-recently-added-movies --tmdb-api-key YOUR_API_KEY --sort-by tmdb-popularity --min-rating-count 500
        ```

3. Use the `TMDB_API_KEY` environment variable:
        ```bash
        export TMDB_API_KEY=YOUR_API_KEY
        python src/cli.py abc-movies-of-the-week
        ```

## Output

The script saves the enriched movie data as a JSON file in the `output/` directory. The file name is based on the `media_source` argument, e.g., `output/abc_all_movies_with_tmdb.json`.

## Notes

- The `output/` directory is created automatically if it does not exist.
- Ensure your TMDB API key is valid and has sufficient permissions.

## Troubleshooting

- **Missing TMDB API Key**: Provide the `--tmdb-api-key` argument or set the `TMDB_API_KEY` environment variable.
- **Dependencies Not Installed**: Run `pip install -r requirements.txt` to install required packages.
