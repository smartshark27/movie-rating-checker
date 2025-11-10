import requests


program_id = "bluey"
season = 3
output_file = f"output/abc_{program_id}_{season}_episode_links.txt"


def get_abc_episode_links(url):
    """
    Fetch episode links from ABC iView API for a given program and season.

    :param url: API URL for the specific program and season
    :return: List of episode links
    """
    data = requests.get(url).json()
    episodes = data["_embedded"]["selectedSeries"]["_embedded"]["videoEpisodes"][
        "items"
    ]

    episode_links = [
        f"https://iview.abc.net.au/video/{episode['id']}" for episode in episodes
    ]

    print(f"Total episodes found: {len(episode_links)}")

    return episode_links


def save_links_to_file(episode_links):
    """
    Save episode links to a text file.

    :param episode_links: List of episode links
    """
    with open(output_file, "w", encoding="utf-8") as f:
        for link in episode_links:
            f.write(f"{link}\n")


if __name__ == "__main__":
    url = f"https://api.iview.abc.net.au/v3/show/{program_id}/series/{season}"
    episode_links = get_abc_episode_links(url)
    save_links_to_file(episode_links)
