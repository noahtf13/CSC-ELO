import numpy as np
import pandas as pd

import scrape
import math

url = 'https://cscsports.com/e/sunday-mens-basketball-5v5-fall-2021/schedule/stage/139364/division/2%29+BRONZE'
scraper = scrape.ScrapeCSC(url=url)
list_of_games = scraper.scrape_games()


class Elo:
    def __init__(self, games_list, k):
        self.games_list = games_list
        self.K = k
        self.med_margin = np.median(
            [abs(int(game[1]) - int(game[3])) for game in self.games_list if game[1].isdigit()]
        )

    def _distinct_teams(self):
        gl = self.games_list
        teams = []
        for game in gl:
            teams = teams + [game[0], game[2]]
        return list(set(teams))

    def _initial_dict(self):
        teams = self._distinct_teams()
        teams_dict = dict()
        for team in teams:
            teams_dict[team] = dict()
            teams_dict[team]['wins'] = 0
            teams_dict[team]['losses'] = 0
            teams_dict[team]['elo'] = 1000
        self.elo_dict = teams_dict
        return teams_dict

    def _elo_change(self, winner, loser, margin):
        teams_dict = self.elo_dict
        total_games = 0

        for team in [winner, loser]:
            for result in ['wins', 'losses']:
                total_games = total_games + teams_dict[team][result]
        temp_k = self.K / math.log(self.med_margin + 1)
        win_elo = teams_dict[winner]['elo']
        loser_elo = teams_dict[loser]['elo']
        elo_diff = win_elo - loser_elo
        prior_win_prob = 1/(10**(-elo_diff/400) + 1)
        mov_multiple = math.log(margin + 1) * 2.2/(elo_diff*0.001+2.2)
        elo_change = prior_win_prob*temp_k*mov_multiple
        teams_dict[winner]['elo'] = win_elo + elo_change
        teams_dict[loser]['elo'] = loser_elo - elo_change
        teams_dict[winner]['wins'] += 1
        teams_dict[loser]['losses'] += 1

    def elo_from_list(self):
        self._initial_dict()
        gl = self.games_list
        for game in gl:
            if game[1] == "W":
                self._elo_change(winner=game[0], loser=game[2], margin=1)
            elif game[1] == "L":
                self._elo_change(winner=game[2], loser=game[0], margin=1)
            elif int(game[1]) > int(game[3]):
                self._elo_change(winner=game[0], loser=game[2], margin=int(game[1]) - int(game[3]))
            elif int(game[3]) > int(game[1]):
                self._elo_change(winner=game[2], loser=game[0], margin=int(game[3]) - int(game[1]))
        return self.elo_dict


elo_json = Elo(games_list=list_of_games, k=34).elo_from_list()
print(pd.DataFrame(elo_json).transpose().sort_values('elo', ascending=False))
