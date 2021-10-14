from bs4 import BeautifulSoup
import requests
import re


class ScrapeCSC:
    def __init__(self, url):
        self.url = url

    def _get_soup(self, page_url):
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    def _get_root(self):
        if '?' in self.url:
            return self.url.split('?')[0]
        else:
            return self.url

    def _pages_list(self):
        pages = []
        soup = self._get_soup(self.url)
        for ul in soup.findAll('ul', {'class': 'nav-pager align-left'}):
            for li in ul.findAll('li'):
                pages.append(li.a.text)

        try:
            pages = max([int(i) for i in pages if i.isdigit()])
        except:
            pages = 1

        return pages

    def _scrape_url_scores(self, page_url):
        score_list = []
        team_list = []
        games_list = []
        soup = self._get_soup(page_url)
        for div in soup.findAll('div', {'class': 'score score-only'}):
            score_list.append(div.text.strip())
        score_list_clean = [i for i in score_list if i is not None]

        for div in soup.findAll('div', {'class': 'schedule-team-name'}):
            team_list.append(div.a.text)

        for i in range(int(len(score_list)/2)):
            list_val = i * 2
            games_list.append([
                team_list[list_val],
                score_list_clean[list_val],
                team_list[list_val+1],
                score_list_clean[list_val+1]
            ])

        return games_list

    def _scrape_url_schedule(self, page_url):
        schedule_teams = []
        soup = self._get_soup(page_url)
        regex = re.compile("schedule-score-box with-score*")
        for div in soup.findAll('div', {'class': 'game-participant'}):
            score_list = div.findAll('div', {'class': regex})
            if len(score_list) == 0:
                for team_name in div.findAll('div', {'class': 'schedule-team-name'}):
                    schedule_teams.append(team_name.a.text)
        return schedule_teams

    def scrape_scores(self):
        final_games_list = []
        page_root = self._get_root()
        for page in range(self._pages_list()):
            page_url = page_root + f"?page={page+1}"
            temp_games = self._scrape_url_scores(page_url)
            final_games_list = final_games_list + temp_games
        return final_games_list

    def scrape_schedule(self):
        final_games_list = []
        page_root = self._get_root()
        for page in range(self._pages_list()):
            page_url = page_root + f"?page={page+1}"
            temp_games = self._scrape_url_schedule(page_url)
            final_games_list = final_games_list + temp_games
        return final_games_list
