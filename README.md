# Movie Rating Checker

## Usage

The `movie-rating-checker` CLI allows you to fetch and sort movie data from SBS and enrich it with TMDB ratings and popularity.

### Prerequisites

1. **Python**: Ensure you have Python installed (version 3.7 or higher is recommended).
2. **TMDB API Key**: Obtain an API key from [The Movie Database (TMDB)](https://www.themoviedb.org/documentation/api).

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/movie-rating-checker.git
    cd movie-rating-checker
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Command-Line Arguments

Run the CLI script with the following options:

```bash
python src/cli.py <media_source> [--tmdb-api-key <key>] [--sort-by <criteria>] [--min-rating-count <count>]
```

#### Positional Arguments:
- `media_source`: The source of movies to check. Options:
  - `sbs-recently-added-movies`: Fetch recently added movies.
  - `sbs-all-movies`: Fetch all movies.

#### Optional Arguments:
- `--tmdb-api-key`: Your TMDB API key. If not provided, the script will use the `TMDB_API_KEY` environment variable.
- `--sort-by`: Criteria to sort the movies. Options:
  - `tmdb-rating` (default): Sort by TMDB rating.
  - `tmdb-rating-count`: Sort by the number of TMDB ratings.
  - `tmdb-popularity`: Sort by TMDB popularity.
- `--min-rating-count`: Minimum number of ratings required to include a movie in the output. Default is `100`.

### Examples

1. Fetch recently added movies and sort by TMDB rating:
    ```bash
    python src/cli.py sbs-recently-added-movies --tmdb-api-key YOUR_API_KEY
    ```

2. Fetch all movies, sort by popularity, and set a minimum rating count of 500:
    ```bash
    python src/cli.py sbs-all-movies --tmdb-api-key YOUR_API_KEY --sort-by tmdb-popularity --min-rating-count 500
    ```

3. Use the `TMDB_API_KEY` environment variable:
    ```bash
    export TMDB_API_KEY=YOUR_API_KEY
    python src/cli.py sbs-recently-added-movies
    ```

### Output

The script saves the enriched movie data as a JSON file in the `output/` directory. The file name is based on the `media_source` argument, e.g., `output/sbs_recently_added_movies_with_tmdb.json`.

### Notes

- Ensure the `TMDB_API_KEY` is valid and has sufficient permissions to access the TMDB API.
- The `output/` directory will be created automatically if it does not exist.

### Troubleshooting

- **Missing TMDB API Key**: Ensure you provide the `--tmdb-api-key` argument or set the `TMDB_API_KEY` environment variable.
- **Dependencies Not Installed**: Run `pip install -r requirements.txt` to install required packages.
