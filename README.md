
# Movie Rating Checker

The **Movie Rating Checker** is a command-line tool designed to fetch and filter movies and TV shows from various media sources based on their ratings and popularity. It integrates with TMDB to enrich media data and allows users to customize filtering and sorting criteria.

## Features

- Fetch media lists from sources like 10play, ABC, SBS, and Tubi.
- Enrich media data with TMDB ratings, popularity, and other metadata.
- Filter media by minimum rating, rating count, and type (movies or shows).
- Sort results by TMDB rating, rating count, or popularity.
- Save results to JSON files for further analysis.

## Usage

The main script for this project is [`cli.py`](src/cli.py). To use it, run:

```bash
python src/cli.py [media_sources] [options]
```

### Example

```bash
python src/cli.py abc-movies-a-z sbs-movies-all --tmdb-api-key YOUR_API_KEY
```

### Options

- `--tmdb-api-key`: TMDB API key (required).
- `--tubi-access-token`: Tubi access token (if using Tubi sources).
- `--movies-min-rating`: Minimum rating for movies (default: 7.0).
- `--shows-min-rating`: Minimum rating for shows (default: 7.0).
- `--sort-by`: Sort results by `tmdb-rating`, `tmdb-rating-count`, or `tmdb-popularity`.

## Output

Results are saved in the `output` directory:
- `all-media.json`: Contains all filtered media.
- `new-media.json`: Contains new media since the last run (if applicable).

## Prerequisites

- Python 3.7+
- Install dependencies using `pip install -r requirements.txt`.
