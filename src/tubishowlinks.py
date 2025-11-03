from utils import read_text_file

# 1. Open TV show link on Tubi. E.g. https://tubitv.com/series/2067/yu-gi-oh/season-5
# 2. Inspect and copy the "web-ui-grid-container" div HTML into input/tubishow.html
# 3. Run this script to extract episode links and save to output/tubi_episode_links.txt

INPUT_FILE = "input/tubi_show.html"
OUTPUT_FILE = "output/tubi_episode_links.txt"
TUBI_URL_PREFIX = "https://tubitv.com"


def run():
    episode_links = get_tubi_episode_links()
    save_links_to_file(episode_links)


def get_tubi_episode_links():
    """
    Extract Tubi episode links from a saved HTML file.

    :return: List of episode links
    """
    from bs4 import BeautifulSoup

    html_content = read_text_file(INPUT_FILE)
    soup = BeautifulSoup(html_content, "html.parser")

    episode_links = []
    grid_container = soup.find("div", {"data-test-id": "web-ui-grid-container"})
    if grid_container:
        grid_items = grid_container.find_all(
            "div", {"data-test-id": "web-ui-grid-item"}
        )
        for item in grid_items:
            title_anchor = item.find("a", class_="web-content-tile__title")
            if title_anchor and "href" in title_anchor.attrs:
                episode_links.append(TUBI_URL_PREFIX + title_anchor["href"])

    return episode_links


def save_links_to_file(episode_links):
    """
    Save episode links to a text file.

    :param episode_links: List of episode links
    """
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for link in episode_links:
            f.write(f"{link}\n")


if __name__ == "__main__":
    run()


# Example HTML structure to parse:
# <div
#   data-test-id="web-ui-grid-container"
#   class="web-grid-container web-grid-container--no-margin web-carousel CT_Zj web-carousel--enable-transition"
#   style="transform: translate3d(0px, 0px, 0px)"
# >
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/2FX-e1DtbDUQsg==/8e9ebd61-846b-4a3f-ac35-97b150caab7a/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E01 - Unwanted Guest (Pt. 1)"
#                 role="img"
#               />
#             </div>
#           </div>
#           <div class="web-content-tile__poster-overlay">
#             <div class="web-play-button">
#               <div class="web-play-button__play-icon-container">
#                 <svg
#                   class="web-play-button__circle"
#                   viewBox="0 0 48 48"
#                   fill="none"
#                   stroke="currentColor"
#                   xmlns="http://www.w3.org/2000/svg"
#                 >
#                   <rect
#                     x="1"
#                     y="1"
#                     width="46"
#                     height="46"
#                     rx="23"
#                     stroke-width="2"
#                   ></rect></svg
#                 ><svg
#                   xmlns="http://www.w3.org/2000/svg"
#                   width="1em"
#                   height="1em"
#                   fill="none"
#                   data-test-id="icons-play"
#                   viewBox="0 0 24 24"
#                   role="img"
#                   class="web-play-button__play-icon"
#                 >
#                   <title>Play Icon</title>
#                   <path
#                     fill="currentColor"
#                     d="M19.622 10.393A105.98 105.98 0 0 0 6.419 3.176c-1.2-.55-2.572.25-2.663 1.558-.167 2.4-.256 4.82-.256 7.262 0 2.444.088 4.868.256 7.27.092 1.307 1.464 2.108 2.663 1.558a106.112 106.112 0 0 0 13.203-7.217 1.91 1.91 0 0 0 0-3.214"
#                   ></path>
#                 </svg>
#               </div>
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365683/s05-e01-unwanted-guest-pt-1"
#               ><h2>S05:E01 - Unwanted Guest (Pt. 1)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Yugi and the gang have saved the world from Dartz and his Grand
#               Dragon Leviathan, but they’re about to face their biggest
#               challenge yet.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/7b4JOGfGzS-HfQ==/c53060ca-41ff-4e26-951d-928e4df06c51/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E02 - Unwanted Guest (Pt. 2)"
#                 role="img"
#               />
#             </div>
#           </div>
#           <div class="web-content-tile__poster-overlay">
#             <div class="web-play-button">
#               <div class="web-play-button__play-icon-container">
#                 <svg
#                   class="web-play-button__circle"
#                   viewBox="0 0 48 48"
#                   fill="none"
#                   stroke="currentColor"
#                   xmlns="http://www.w3.org/2000/svg"
#                 >
#                   <rect
#                     x="1"
#                     y="1"
#                     width="46"
#                     height="46"
#                     rx="23"
#                     stroke-width="2"
#                   ></rect></svg
#                 ><svg
#                   xmlns="http://www.w3.org/2000/svg"
#                   width="1em"
#                   height="1em"
#                   fill="none"
#                   data-test-id="icons-play"
#                   viewBox="0 0 24 24"
#                   role="img"
#                   class="web-play-button__play-icon"
#                 >
#                   <title>Play Icon</title>
#                   <path
#                     fill="currentColor"
#                     d="M19.622 10.393A105.98 105.98 0 0 0 6.419 3.176c-1.2-.55-2.572.25-2.663 1.558-.167 2.4-.256 4.82-.256 7.262 0 2.444.088 4.868.256 7.27.092 1.307 1.464 2.108 2.663 1.558a106.112 106.112 0 0 0 13.203-7.217 1.91 1.91 0 0 0 0-3.214"
#                   ></path>
#                 </svg>
#               </div>
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365684/s05-e02-unwanted-guest-pt-2"
#               ><h2>S05:E02 - Unwanted Guest (Pt. 2)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Yugi is trapped inside the Duel Dome, and the only way to escape
#               is by defeating the Duel Computer, programmed with the skills of
#               the world’s top duelists. Since the Duel Computer has access to
#               thousands of cards, how can Yugi win?
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/t7KnLeBjNlckLQ==/fe4960a6-a487-42ab-aa98-ff648c8e5bc9/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E03 - Let the Games Begin! (Pt. 1)"
#                 role="img"
#               />
#             </div>
#           </div>
#           <div class="web-content-tile__poster-overlay">
#             <div class="web-play-button">
#               <div class="web-play-button__play-icon-container">
#                 <svg
#                   class="web-play-button__circle"
#                   viewBox="0 0 48 48"
#                   fill="none"
#                   stroke="currentColor"
#                   xmlns="http://www.w3.org/2000/svg"
#                 >
#                   <rect
#                     x="1"
#                     y="1"
#                     width="46"
#                     height="46"
#                     rx="23"
#                     stroke-width="2"
#                   ></rect></svg
#                 ><svg
#                   xmlns="http://www.w3.org/2000/svg"
#                   width="1em"
#                   height="1em"
#                   fill="none"
#                   data-test-id="icons-play"
#                   viewBox="0 0 24 24"
#                   role="img"
#                   class="web-play-button__play-icon"
#                 >
#                   <title>Play Icon</title>
#                   <path
#                     fill="currentColor"
#                     d="M19.622 10.393A105.98 105.98 0 0 0 6.419 3.176c-1.2-.55-2.572.25-2.663 1.558-.167 2.4-.256 4.82-.256 7.262 0 2.444.088 4.868.256 7.27.092 1.307 1.464 2.108 2.663 1.558a106.112 106.112 0 0 0 13.203-7.217 1.91 1.91 0 0 0 0-3.214"
#                   ></path>
#                 </svg>
#               </div>
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365685/s05-e03-let-the-games-begin-pt-1"
#               ><h2>S05:E03 - Let the Games Begin! (Pt. 1)</h2></a
#             >
#             <div class="web-content-tile__description">
#               It’s the start of the KC Grand Championship! Sixteen of the
#               world’s greatest duelists vie for a chance to challenge Yugi as
#               the King of Games!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition web-carousel__item--masked"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/KQyoMkASEuuSTQ==/5a8aec34-f67e-4952-9fd6-ad07099cafd4/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E04 - Let the Games Begin! (Pt. 2)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365686/s05-e04-let-the-games-begin-pt-2"
#               ><h2>S05:E04 - Let the Games Begin! (Pt. 2)</h2></a
#             >
#             <div class="web-content-tile__description">
#               How does Apdnarg Otum know all of Joey’s strategies? How can Joey
#               stop Apdnarg when he gathers his ancient cards to unleash the
#               fiercest monster from the great past? But the biggest mystery...
#               how can Joey not know who Apdnarg Otum is?
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/ti8YeSMthgeb4w==/68d10bb5-7273-4c22-bb02-17551c941c5f/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E05 - Child’s Play"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365687/s05-e05-child-s-play"
#               ><h2>S05:E05 - Child’s Play</h2></a
#             >
#             <div class="web-content-tile__description">
#               It’s the second match of the KC Grand Championship as Rebecca
#               faces the kung-fu kicking Asia champion Vivian Wong. However,
#               there’s more at stake than just winning the duel – Yugi’s heart is
#               on the line, whether he likes it or not.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/f_9FWR7y3-CEZg==/74bd68b0-3bce-4057-ad8f-7d25ae1d022f/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E06 - Down in Flames (Pt. 1)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365688/s05-e06-down-in-flames-pt-1"
#               ><h2>S05:E06 - Down in Flames (Pt. 1)</h2></a
#             >
#             <div class="web-content-tile__description">
#               The first round is over, leaving eight duelists to compete for the
#               right to face Yugi for the KC Grand Championship. Unfortunately
#               for Joey, his next opponent is Zigfried Lloyd, who defeated both
#               Weevil and Rex Raptor in one turn.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/Tv65FRYvI9BNxQ==/f241515f-b87e-4c44-940b-ba57e31488ef/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E07 - Down in Flames (Pt. 2)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365689/s05-e07-down-in-flames-pt-2"
#               ><h2>S05:E07 - Down in Flames (Pt. 2)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Zigfried activates Ride of the Valkyries, the same card that
#               defeated both Weevil and Rex Raptor at the same time.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/B1-rwJPnBsx2rg==/d22a2b8c-3af7-49a5-886d-efe45cefed1d/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E08 - A Brawl in Small Town (Pt. 1)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365690/s05-e08-a-brawl-in-small-town-pt-1"
#               ><h2>S05:E08 - A Brawl in Small Town (Pt. 1)</h2></a
#             >
#             <div class="web-content-tile__description">
#               In the semifinals of the KC Grand Championship, it’s a duel
#               between child prodigies as Rebecca faces Leon Wilson and his fairy
#               tale faction.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/EBveD1SjEloNkQ==/9bc8ffa7-9608-4b45-8658-f29e96787450/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E09 - A Brawl in Small Town (Pt. 2)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365691/s05-e09-a-brawl-in-small-town-pt-2"
#               ><h2>S05:E09 - A Brawl in Small Town (Pt. 2)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Yugi finds Grandpa’s kidnapper, but is it really a kidnapping?
#               While Yugi unravels the truth, Rebecca starts to unravel when her
#               dragons fall prey to Leon’s fervent fables. Rebecca must think of
#               a new plan quickly or there will be no happy ending.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/DWiUdPSX1VFSkw==/28dcebd6-4c96-41a6-a56b-02493fe9ca3e/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E10 - One Step Ahead (Pt. 1)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365692/s05-e10-one-step-ahead-pt-1"
#               ><h2>S05:E10 - One Step Ahead (Pt. 1)</h2></a
#             >
#             <div class="web-content-tile__description">
#               It’s Zigfried vs. Leon for the right to challenge Yugi in the KC
#               Grand Championship Finals... but Kaiba stops the duel!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/m96K0-xMlOZTow==/9630c69c-86c6-4a76-b5f4-7d63dad092f2/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E11 - One Step Ahead (Pt. 2)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365693/s05-e11-one-step-ahead-pt-2"
#               ><h2>S05:E11 - One Step Ahead (Pt. 2)</h2></a
#             >
#             <div class="web-content-tile__description">
#               It’s a battle between Zigfried and Kaiba. Zigfried quickly gains
#               the advantage by destroying Kaiba’s monsters before he can even
#               draw them!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/kk2Fp2Urubk6rg==/a2f8047e-2cf7-4248-9452-d4661382ae76/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E12 - Sinister Secrets (Pt. 1)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365694/s05-e12-sinister-secrets-pt-1"
#               ><h2>S05:E12 - Sinister Secrets (Pt. 1)</h2></a
#             >
#             <div class="web-content-tile__description">
#               It’s Yugi vs. Leon for the title of King of Games at the KC Grand
#               Championship! Something sinister lurks in the shadows, for this
#               duel is more than just getting the crown. Zigfried’s greatest
#               revenge will commence as his real plan is unleashed.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/5TnkGjPR0YO5gw==/09e2b110-bdd3-4b72-ba83-d03acdf7d87b/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E13 - Sinister Secrets (Pt. 2)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365695/s05-e13-sinister-secrets-pt-2"
#               ><h2>S05:E13 - Sinister Secrets (Pt. 2)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Leon is Zigfried’s younger brother, and he’ll avenge his family’s
#               loss. Leon’s fairy tales are giving Yugi nightmares but the worst
#               is yet to come as Leon has Zigfried’s mysterious and special card.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/9lOSNAkA2H2uQQ==/bf956eb0-d830-4420-8413-9e6117f163b2/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E14 - Sinister Secrets (Pt. 3)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365696/s05-e14-sinister-secrets-pt-3"
#               ><h2>S05:E14 - Sinister Secrets (Pt. 3)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Golden Castle of Stromberg is infecting the world’s Duel Disks
#               with a virus that will destroy KaibaCorp. If Yugi doesn’t destroy
#               the card, the virus program can’t be stopped.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/GiRPwBlcfO4Qew==/4a37ef94-cb72-4025-9014-02d8f4ad64f3/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E15 - Getting Played"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365697/s05-e15-getting-played"
#               ><h2>S05:E15 - Getting Played</h2></a
#             >
#             <div class="web-content-tile__description">
#               The gang goes on an exotic trip to India, but when their plane
#               crashes in a deserted forest, their vacation turns into a
#               dangerous game of survival.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/2UKF06FISJUuNQ==/dacd7d06-827d-4df8-9d20-b4165e395f54/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E16 - Divide and Conquer"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365698/s05-e16-divide-and-conquer"
#               ><h2>S05:E16 - Divide and Conquer</h2></a
#             >
#             <div class="web-content-tile__description">
#               Realizing that they’ve become part of a real-life version of the
#               Capsule Monsters board game, the gang struggles to find a way out.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/DTMg3U6Txo8lkg==/86067352-aaef-4140-be3d-0fc2c1fd3044/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E17 - Reunited at Last"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365699/s05-e17-reunited-at-last"
#               ><h2>S05:E17 - Reunited at Last</h2></a
#             >
#             <div class="web-content-tile__description">
#               Reunited at last, Yugi and his friends rejoice. But their
#               celebration is soon interrupted by a pack of man-eating wolves, a
#               giant turtle and an angry Genie!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/nZqjklG2qVwZLw==/c357c774-6da2-44f9-bcea-8623623cb6ab/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E18 - Fortress of Fear"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365700/s05-e18-fortress-of-fear"
#               ><h2>S05:E18 - Fortress of Fear</h2></a
#             >
#             <div class="web-content-tile__description">
#               Grandpa translates an ancient stone tablet which directs the gang
#               to locate the “Fortress of Fear.” Now they have until sunset to
#               find this mysterious structure or they’ll be trapped in the world
#               of Capsule Monsters forever.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/kBjFbgx7PDyTzA==/89db21fc-c6fd-49c1-b46b-4a15283bf5cf/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E19 - Eye of the Storm"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365701/s05-e19-eye-of-the-storm"
#               ><h2>S05:E19 - Eye of the Storm</h2></a
#             >
#             <div class="web-content-tile__description">
#               Yugi and his friends discover that in order to return home to the
#               real world they must pass a series of tests: the Five Sacred
#               Trials. The first of which pits them against enormous sand worms
#               and a mysterious voice that travels with the desert wind.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/9RHb_dtvpqEUHQ==/7724361d-198e-4180-8139-4d2624116492/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E20 - Trial of Light and Shadow"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365702/s05-e20-trial-of-light-and-shadow"
#               ><h2>S05:E20 - Trial of Light and Shadow</h2></a
#             >
#             <div class="web-content-tile__description">
#               After narrowly escaping their battle in the desert, the gang finds
#               themselves stranded on a mysterious floating island, where they
#               face a monster that derives its strength from the sun.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/S6jHuqkaUSE62g==/25d501c1-76af-42eb-83d2-97e4f9a3ef17/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E21 - Red-Eyes Black Curse"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365703/s05-e21-red-eyes-black-curse"
#               ><h2>S05:E21 - Red-Eyes Black Curse</h2></a
#             >
#             <div class="web-content-tile__description">
#               It’s on to level three as Yugi and his friends are transported to
#               a lava-covered wasteland. To make matters worse, Joey is possessed
#               by an evil force, and destroying it may mean destroying Joey as
#               well.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/HAYXjt85he1n8A==/3af6b4c8-f95e-4759-ae09-107bf280bb3b/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E22 - Fruits of Evolution"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365704/s05-e22-fruits-of-evolution"
#               ><h2>S05:E22 - Fruits of Evolution</h2></a
#             >
#             <div class="web-content-tile__description">
#               Yugi and his friends are faced with an impossible task: locating a
#               magical apple in a forest full of apple trees.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/HfYoi82q--dpUw==/560cfd42-a274-479b-b650-8b5a7821f4c7/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E23 - The Fiendish Five (Pt. 1)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365705/s05-e23-the-fiendish-five-pt-1"
#               ><h2>S05:E23 - The Fiendish Five (Pt. 1)</h2></a
#             >
#             <div class="web-content-tile__description">
#               The gang stumbles upon a small kingdom dominated by a clan of
#               fierce dragons known as The Fiendish Five. If they fail to slay
#               these beasts, one of Yugi’s friends must give up his soul!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/qA6pGmPh6R3Q7A==/32712992-93ae-4f44-9a93-1e0bdb2010db/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E24 - The Fiendish Five (Pt. 2)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365706/s05-e24-the-fiendish-five-pt-2"
#               ><h2>S05:E24 - The Fiendish Five (Pt. 2)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Yugi and his friends defeat the Fiendish Five…or so they think.
#               These ferocious dragons have merged together and are now more
#               powerful than ever!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/ZLcsbWu4pEaslA==/956eb49d-13e6-4995-92e8-697e4c2a110f/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E25 - The True King (Pt. 1)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365707/s05-e25-the-true-king-pt-1"
#               ><h2>S05:E25 - The True King (Pt. 1)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Although the gang has passed the five sacred trials, the most
#               dangerous test is yet to come. Now Yugi must face the spirit of
#               Alexander the Great in an all-out Capsule Monsters war with the
#               ultimate stakes!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/NBi08nzL-xTWzQ==/6ae0be0e-3030-4468-bd49-f34d62a27992/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E26 - The True King (Pt. 2)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365708/s05-e26-the-true-king-pt-2"
#               ><h2>S05:E26 - The True King (Pt. 2)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Yugi’s friends are unconscious, leaving him to defeat Alexander
#               the Great on his own!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/GD8VaLJe-Rj5Iw==/e5c255f6-a6c3-43d0-9471-3185d9515bfe/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E27 - Tomb of the Nameless Pharaoh"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365709/s05-e27-tomb-of-the-nameless-pharaoh"
#               ><h2>S05:E27 - Tomb of the Nameless Pharaoh</h2></a
#             >
#             <div class="web-content-tile__description">
#               Grandpa found the Millennium Puzzle decades ago, but little is
#               known about the terrors, traps, turmoil and treachery he faced to
#               find the ancient artifact! See how it all began as we learn how
#               Grandpa unearthed the Millennium Puzzle.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/2sRtr-gj3sQPvA==/6727ab29-624c-4e71-ba2e-090efe963944/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E28 - Spiritual Awakening"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365710/s05-e28-spiritual-awakening"
#               ><h2>S05:E28 - Spiritual Awakening</h2></a
#             >
#             <div class="web-content-tile__description">
#               The evil spirit within the Millennium Ring has reunited with
#               Bakura, prepped with a new monster to create the ultimate Shadow
#               Game. And his first target is Kaiba!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/ZDQyFSP069Q3Yw==/d77f6f9d-bfcb-40d2-9fa0-9ae9fb99c698/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E29 - Memoirs of a Pharaoh"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365711/s05-e29-memoirs-of-a-pharaoh"
#               ><h2>S05:E29 - Memoirs of a Pharaoh</h2></a
#             >
#             <div class="web-content-tile__description">
#               Yugi and friends go to the dawn of the duel, to the place where it
#               all began, to the land where the Pharaoh’s mysteries lie: Egypt.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/P2c9WvS3jCP-EA==/e7c4ce2c-d075-480e-b920-584854f374f5/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E30 - The Intruder (Pt. 1)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365712/s05-e30-the-intruder-pt-1"
#               ><h2>S05:E30 - The Intruder (Pt. 1)</h2></a
#             >
#             <div class="web-content-tile__description">
#               The past is quickly becoming perilous as the fearless bandit king
#               Bakura has invaded the Pharaoh’s palace to take down the keepers
#               of the seven Millennium Items single-handedly!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/qWQQXbJ8na22Yw==/6b671383-e3ea-4a57-949c-c34b5118ea56/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E31 - The Intruder (Pt. 2)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365713/s05-e31-the-intruder-pt-2"
#               ><h2>S05:E31 - The Intruder (Pt. 2)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Even with the potent power of Obelisk the Tormentor, the Pharaoh
#               couldn’t prevent the bandit Bakura from escaping. Everyone knows
#               that thief will return for a rematch, so Seto has a plan to create
#               a powerful army.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/zXxbGH0RTSsdog==/8c15e37b-bd0b-460c-805e-1a1136a71cc8/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E32 - Makings of a Magician"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365714/s05-e32-makings-of-a-magician"
#               ><h2>S05:E32 - Makings of a Magician</h2></a
#             >
#             <div class="web-content-tile__description">
#               Mahad vows to stop the bandit king Bakura’s sneak attacks once and
#               for all, but he may have made a promise he can’t keep!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/uOs5VqQfNXV_VQ==/4539b81d-1b9c-4c96-a014-453dde8593d7/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E33 - Birth of the Blue-Eyes"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365715/s05-e33-birth-of-the-blue-eyes"
#               ><h2>S05:E33 - Birth of the Blue-Eyes</h2></a
#             >
#             <div class="web-content-tile__description">
#               Mahad, the first of the Pharaoh’s guardians, has fallen. Even
#               worse, the bandit king Bakura now has the Millennium Ring, making
#               his Diabound even more unstoppable!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/wj8TuHCrjBMDhA==/4b133ed1-e09d-49cc-8645-650cd3fc4c30/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E34 - Village of Lost Souls"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365716/s05-e34-village-of-lost-souls"
#               ><h2>S05:E34 - Village of Lost Souls</h2></a
#             >
#             <div class="web-content-tile__description">
#               The origins of the Millennium Items are revealed! Who forged these
#               powerful artifacts, and why were they created? Though the
#               Millennium Items are powerful, such power comes with a heavy
#               price... a debt that may never be able to be repaid!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/1IXtrK-pjdMpOg==/491e3376-2cf7-45b8-b045-2b431bcd0138/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E35 - A Reversal of Fortune"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365717/s05-e35-a-reversal-of-fortune"
#               ><h2>S05:E35 - A Reversal of Fortune</h2></a
#             >
#             <div class="web-content-tile__description">
#               The Pharaoh calls forth the mighty Egyptian God Slifer the Sky
#               Dragon to fight the bandit Bakura’s Diabound, but when Diabound
#               starts attacking the townspeople, the Pharaoh must protect them,
#               even if it means sacrificing himself!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/Y9Ss_wCbv8UUOg==/25f8de00-8de3-47f3-a726-1f8ea46a1f9a/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E36 - In Search of a King"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365718/s05-e36-in-search-of-a-king"
#               ><h2>S05:E36 - In Search of a King</h2></a
#             >
#             <div class="web-content-tile__description">
#               The bandit Bakura has stolen the Millennium Puzzle and sent the
#               Pharaoh plummeting into the abyss. Now he’s another step closer to
#               obtaining all seven Millennium Items and resurrecting the
#               malevolent Zorc, the greatest evil of all time!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/3Ryh_Kqkz8SdeQ==/a89cdde6-9588-4d5c-9533-0dd292434816/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E37 - Village of Vengeance (Pt. 1)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365719/s05-e37-village-of-vengeance-pt-1"
#               ><h2>S05:E37 - Village of Vengeance (Pt. 1)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Yugi and the Pharaoh are reunited, but the Pharaoh is powerless
#               without the Millennium Puzzle! However, that won’t stop the
#               Pharaoh from a final showdown against the bandit king Bakura.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/UiSCZ_rEiR_2hQ==/cc9a952e-686f-423c-aa90-364cb3d510e7/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E38 - Village of Vengeance (Pt. 2)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365720/s05-e38-village-of-vengeance-pt-2"
#               ><h2>S05:E38 - Village of Vengeance (Pt. 2)</h2></a
#             >
#             <div class="web-content-tile__description">
#               It’s the showdown in the sands between the bandit Bakura and his
#               ever-growing Diabound versus the Pharaoh, Mahad the Dark Magician
#               and the remaining guardians of the Pharaoh!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/5pzKTC4ULt64hA==/2401af58-8243-4976-b9a4-1e340dbc85b5/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E39 - Village of Vengeance (Pt. 3)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365721/s05-e39-village-of-vengeance-pt-3"
#               ><h2>S05:E39 - Village of Vengeance (Pt. 3)</h2></a
#             >
#             <div class="web-content-tile__description">
#               With the help of his father’s spirit, the Pharaoh and his
#               guardians defeated the bandit Bakura’s Diabound and stopped the
#               horrible Zorc from resurrecting... or did they?
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/Zl2NdJdl2G3-2Q==/c23f5b07-d4b6-465b-bdfe-46721c1c0c76/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E40 - Village of Vengeance (Pt. 4)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365722/s05-e40-village-of-vengeance-pt-4"
#               ><h2>S05:E40 - Village of Vengeance (Pt. 4)</h2></a
#             >
#             <div class="web-content-tile__description">
#               The Pharaoh’s journey was more than a trip to the past, it’s the
#               greatest Shadow Game ever created. Yami Yugi and Yami Bakura’s
#               Shadow Game has already reached apocalyptic proportions, but it’s
#               only the beginning of cataclysmic events!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/SOaXOQpc67C63w==/c9afa205-33bd-40d6-8e50-ab7002e874d6/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E41 - Village of Vengeance (Pt. 5)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365723/s05-e41-village-of-vengeance-pt-5"
#               ><h2>S05:E41 - Village of Vengeance (Pt. 5)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Zorc’s incredible shadow energies have resurrected the bandit
#               Bakura and his Diabound. With a second chance at revenge, the
#               bandit king has broken up the Pharaoh’s team so that he can divide
#               and conquer them one at a time!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/2PE0C0KoQA5ctA==/ed67c3e8-97de-4425-86a6-bdcac855d7d8/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E42 - Name of the Game"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365724/s05-e42-name-of-the-game"
#               ><h2>S05:E42 - Name of the Game</h2></a
#             >
#             <div class="web-content-tile__description">
#               The hope of mankind rests on Yugi’s shoulders as he arrives at the
#               final temple chamber where the Pharaoh’s name is located, but
#               something unexpected is waiting for them – a sinister surprise
#               that can cost them their lives!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/QajwcRp9yKnmzA==/e48a9845-4d11-42d3-9125-f40446e73d95/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E43 - The Dark One Cometh (Pt. 1)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365725/s05-e43-the-dark-one-cometh-pt-1"
#               ><h2>S05:E43 - The Dark One Cometh (Pt. 1)</h2></a
#             >
#             <div class="web-content-tile__description">
#               After a nearly eternal slumber, the all-powerful Zorc has
#               resurrected, plunging the world into darkness!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/7k3-P-4VV2vbRg==/276be7bb-2f19-4387-8089-746c69e10b53/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E44 - The Dark One Cometh (Pt. 2)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365726/s05-e44-the-dark-one-cometh-pt-2"
#               ><h2>S05:E44 - The Dark One Cometh (Pt. 2)</h2></a
#             >
#             <div class="web-content-tile__description">
#               The Pharaoh and his guardians are down to their last line of
#               defense as Shada falls victim to Zorc. The Pharaoh desperately
#               wants to summon the three Egyptian Gods, but he can’t without his
#               Millennium Puzzle!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/j6gqStRFpM_P3Q==/58d97ba9-67a1-498f-a714-eda0e730aaa4/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E45 - The Dark One Cometh (Pt. 3)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365727/s05-e45-the-dark-one-cometh-pt-3"
#               ><h2>S05:E45 - The Dark One Cometh (Pt. 3)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Exodia the Forbidden One couldn't defeat Zorc! Exodia was able to
#               buy enough time for the Pharaoh to get his Millennium Puzzle
#               back–he can now summon the almighty Egyptian Gods! It’s time for
#               the Pharaoh’s counterattack in the biggest brawl in history!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/aC3Ajva_FVDAvQ==/19f1a977-f083-482a-8165-11ddb9df88a5/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E46 - The Dark One Cometh (Pt. 4)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365728/s05-e46-the-dark-one-cometh-pt-4"
#               ><h2>S05:E46 - The Dark One Cometh (Pt. 4)</h2></a
#             >
#             <div class="web-content-tile__description">
#               The three Egyptian Gods have been defeated. The Pharaoh is
#               severely hurt and unable to stop Zorc from setting fire to the
#               city, but our heroes aren’t giving up. It’s not double vision when
#               Seto and Kaiba transcend time to confront Zorc.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/2WZnrFVo-JjgLQ==/2ec28915-07b9-4751-b978-cf3b57349061/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E47 - In the Name of the Pharaoh"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365729/s05-e47-in-the-name-of-the-pharaoh"
#               ><h2>S05:E47 - In the Name of the Pharaoh</h2></a
#             >
#             <div class="web-content-tile__description">
#               The Pharaoh and Kaiba’s combined strength couldn’t defeat Zorc.
#               Yugi must give the Pharaoh his name, but Yugi doesn’t know how to
#               read ancient Egyptian text. All bets are off in the final clash
#               where Yugi must protect the past to save the future!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/g0tIAgxYrTH-bg==/96197d4d-51ce-40cf-a5de-08073df96ae2/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E48 - The Final Journey"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365730/s05-e48-the-final-journey"
#               ><h2>S05:E48 - The Final Journey</h2></a
#             >
#             <div class="web-content-tile__description">
#               Pharaoh Atem, Yugi and friends have defeated the bandit Bakura and
#               Zorc, but the final test still awaits! Yugi must duel Atem! As
#               they set sail to the final dueling grounds, everyone realizes this
#               may be the final night Yugi and Atem have together.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/3vTIKllHDx3FaQ==/b7e8ee17-d180-4e53-b35d-4838cfef1314/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E49 - The Final Duel (Pt. 1)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365731/s05-e49-the-final-duel-pt-1"
#               ><h2>S05:E49 - The Final Duel (Pt. 1)</h2></a
#             >
#             <div class="web-content-tile__description">
#               If Yugi defeats Atem, Yugi will prove he’s ready to stand on his
#               own, and Atem can join his friends in the world beyond. But Yugi
#               and Atem will be separated forever.
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/_p0B9ZFw4Rt0TA==/eceb4eb9-a21c-47ab-bdcc-4941f9943a81/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E50 - The Final Duel (Pt. 2)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365732/s05-e50-the-final-duel-pt-2"
#               ><h2>S05:E50 - The Final Duel (Pt. 2)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Atem has summoned all three Egyptian Gods! What chance does Yugi
#               have against these powerful creatures that no one has been able to
#               defeat? Yugi better think of a strategy quickly or this duel will
#               be over soon!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/zy6c9TGney8KAA==/18aa14db-c96b-4b38-af09-07e2aa943ba9/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E51 - The Final Duel (Pt. 3)"
#                 role="img"
#               />
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365733/s05-e51-the-final-duel-pt-3"
#               ><h2>S05:E51 - The Final Duel (Pt. 3)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Atem still has all three Egyptian God Cards, Yugi doesn’t have a
#               single monster on the field! Yugi claims that he has a combo that
#               will defeat the Egyptian Gods, but is he simply bragging or does
#               he actually have a plan?
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
#   <div
#     data-test-id="web-ui-grid-item"
#     class="web-col web-col--6 web-col--lg-4 web-carousel__item web-carousel__item--enable-transition"
#   >
#     <div data-test-id="web-ui-content-tile" class="web-content-tile">
#       <div class="web-content-tile__container">
#         <div class="web-content-tile__poster">
#           <div class="web-poster">
#             <div
#               class="web-poster__image-container web-poster__image-container--landscape"
#             >
#               <img
#                 class="web-poster__image-element"
#                 src="//canvas-lb.tubitv.com/opts/hFi95C0Sek6rrQ==/5c7c6117-6341-4db2-9a62-fb0dddfb2126/CIAFEOgCOgUxLjEuOA=="
#                 alt="S05:E52 - The Final Duel (Pt. 4)"
#                 role="img"
#               />
#             </div>
#           </div>
#           <div class="web-content-tile__poster-overlay">
#             <div class="web-play-button">
#               <div class="web-play-button__play-icon-container">
#                 <svg
#                   class="web-play-button__circle"
#                   viewBox="0 0 48 48"
#                   fill="none"
#                   stroke="currentColor"
#                   xmlns="http://www.w3.org/2000/svg"
#                 >
#                   <rect
#                     x="1"
#                     y="1"
#                     width="46"
#                     height="46"
#                     rx="23"
#                     stroke-width="2"
#                   ></rect></svg
#                 ><svg
#                   xmlns="http://www.w3.org/2000/svg"
#                   width="1em"
#                   height="1em"
#                   fill="none"
#                   data-test-id="icons-play"
#                   viewBox="0 0 24 24"
#                   role="img"
#                   class="web-play-button__play-icon"
#                 >
#                   <title>Play Icon</title>
#                   <path
#                     fill="currentColor"
#                     d="M19.622 10.393A105.98 105.98 0 0 0 6.419 3.176c-1.2-.55-2.572.25-2.663 1.558-.167 2.4-.256 4.82-.256 7.262 0 2.444.088 4.868.256 7.27.092 1.307 1.464 2.108 2.663 1.558a106.112 106.112 0 0 0 13.203-7.217 1.91 1.91 0 0 0 0-3.214"
#                   ></path>
#                 </svg>
#               </div>
#             </div>
#           </div>
#         </div>
#         <div class="web-content-tile__content-info">
#           <div class="web-content-tile__content-digest">
#             <a
#               class="web-content-tile__title"
#               href="/tv-shows/365734/s05-e52-the-final-duel-pt-4"
#               ><h2>S05:E52 - The Final Duel (Pt. 4)</h2></a
#             >
#             <div class="web-content-tile__description">
#               Yugi and Atem – more than friends, closer than brothers. Will they
#               stay together, or is it time to say goodbye? It’s the final
#               answers, the final duel and the final time we will see our friends
#               in the rousing conclusion to Yu-Gi-Oh!
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
# </div>
