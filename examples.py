import scrape
import league_elo

URL =(
    'https://cscsports.com/e/sunday-mens-basketball-5v5-fall-2021/schedule/division/2%29+BRONZE/stage/139364'
    '?schedule_group_id=all_teams'
)

csc_scraper = scrape.ScrapeCSC(url=URL)
games_list = csc_scraper.scrape_games()
print(league_elo.Elo(games_list=games_list, k=32).elo_from_list())

