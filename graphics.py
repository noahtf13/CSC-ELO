import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import math


class Tables:
    def __init__(self, games_df, predictions_list):
        cols = ['Wins', 'Losses', 'Rating']
        games_df[cols] = games_df[cols].apply(pd.to_numeric, errors='coerce', axis=1)
        self.df = games_df.sort_values('Rating', ascending=False)
        self.predictions_list = predictions_list

    def _determine_color(self):
        max_color = px.colors.sequential.Oranges[-5]
        min_color = px.colors.sequential.Oranges[0]
        print()
        color_cols = ['Wins', 'Losses', 'Rating']
        color_dict = dict()
        for col in self.df.columns:
            if col in color_cols:
                int_col = pd.to_numeric(self.df[col]).astype(int)
                color_wheel = n_colors(min_color, max_color, (int_col.max() - int_col.min() + 1), colortype='rgb')
                column_above_min = (int_col - int_col.min()).tolist()
                print(column_above_min)
                color_dict[col] = [color_wheel[i] for i in column_above_min]
            else:
                color_dict[col] = ['white']*len(self.df)
        return color_dict

    def ratings(self):
        color_dict = self._determine_color()
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(self.df.columns),
                        line_color='black', fill_color='#bdbdbd',
                        align='left'),
            cells=dict(values=[self.df[col] for col in self.df.columns],
                       line_color='black',
                       fill_color=[color_dict[col] for col in self.df.columns],
                       align='left'))
        ])
        fig.update_layout(
            height=550,
            margin=dict(
                b=0
            )
        )

        return fig

    def predictions_tables(self):
        subplots = make_subplots(rows=2, cols=4, specs=[[{'type': 'domain'}]*4, [{'type': 'domain'}]*4])
        i = 0
        for game in self.predictions_list[0:8]:
            subplots.add_trace(go.Table(
                header=dict(values=['Team', 'Win Probability'],
                            line_color='black', fill_color='#bdbdbd',
                            align='left'),
                cells=dict(values=[[game[0], game[1]], [round(game[2] * 100, 0), round((1 - game[2]) * 100, 0)]],
                           align='left'))
            ,row=math.floor(i/4)+1, col=((i+4)%4+1))
            i = i+1

            subplots.update_layout(
                margin=dict(
                    t=0
                )
            )

        return subplots




