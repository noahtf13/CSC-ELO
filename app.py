import scrape
import league_elo
import graphics
import pandas as pd
import os

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

URL =(
    'https://cscsports.com/e/sunday-mens-basketball-5v5-fall-2021/schedule/division/2%29+BRONZE/stage/139364?schedule_group_id=all_teams'
)

csc_scraper = scrape.ScrapeCSC(url=URL)
games_list = csc_scraper.scrape_scores()
schedule = csc_scraper.scrape_schedule()
elo_results = league_elo.Elo(games_list=games_list, schedule=schedule)

graphs = graphics.Tables(elo_results.elo_from_list(), elo_results.predictions())
predictions = graphs.predictions_tables()

app.layout = html.Div([
    html.H2('CSC Bronze Rankings'),
    dcc.Graph(figure=graphs.ratings()),
    html.H2('Upcoming Games'),
    dcc.Graph(figure=graphs.predictions_tables())
])

if __name__ == '__main__':
    app.run_server(debug=True)
