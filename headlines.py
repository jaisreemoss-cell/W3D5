import requests
from bs4 import BeautifulSoup


def get_top_headlines():
    url = "https://www.bbc.com/news"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Target strictly the main story card headlines using BBC's data-testid attribute
    # and restrict to the main content area to avoid sidebars/footers.
    main_content = soup.find("main") or soup
    headline_elements = main_content.find_all(
        ["h2", "h3"], attrs={"data-testid": "card-headline"}
    )

    headlines = []
    seen = set()

    for element in headline_elements:
        text = element.get_text(strip=True)

        # Filter out empty strings, duplicates, or non-headline boilerplate
        if text and text not in seen:
            # Ensure we only take actual headline text (skip short badges like "LIVE")
            if len(text) > 10:
                seen.add(text)
                headlines.append(text)

        if len(headlines) == 5:
            break

    # Handle case where fewer than 5 headlines are found
    if headlines:
        for i, headline in enumerate(headlines, start=1):
            print(f"{i}. {headline}")
    else:
        print("No headlines found on the page.")


if __name__ == "__main__":
    get_top_headlines()