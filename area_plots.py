import os
import sys
from datetime import datetime

import matplotlib.pyplot as plt
import mpld3
import pandas as pd
from mpld3 import plugins


def trim_list(y1):
    back = 0
    while y1 and y1[-1] is 0:
        y1.pop()
        back += 1
    front = 0
    while y1 and y1[0] is 0:
        del y1[0]
        front += 1

    return y1, front, back


def string2date(date):
    return datetime.strptime(date, '%Y-%m-%d')


class AreaPlot:

    title = None

    def __init__(self):
        self.db_conn = dbc.DbConnectionHandler()

    def connect_RS_source(self, uname, pw):
        self.db_conn.load_profile('prod', os.getcwd())
        self.db_conn.establish_connection(user=uname, passw=pw)

    def create_plot(self, x, y1, y2):
        fig, ax = plt.subplots()

        y1, y1_b, y1_e = trim_list(y1)
        y2, y2_b, y2_e = trim_list(y2)

        x_dates = map(string2date, x)

        ax.set_xlim(left=min((x_dates[y1_b:-y1_e][0], x_dates[y2_b:-y2_e][0])),
                    right=max((x_dates[y1_b:-y1_e][-1], x_dates[y2_b:-y2_e][-1])))

        co = list()
        co.append(ax.plot(x_dates[y1_b:-y1_e], y1, 'b', label='One'))
        co.append(ax.plot(x_dates[y2_b:-y2_e], y2, 'r', label='Two'))

        handles, labels = ax.get_legend_handles_labels()  # return lines and labels
        interactive_legend = plugins.InteractiveLegendPlugin(zip(handles,
                                                                 co),
                                                             labels,
                                                             alpha_unsel=0.5,
                                                             alpha_over=1.5,
                                                             start_visible=True)
        plugins.connect(fig, interactive_legend)

        ax.fill_between(x_dates[y1_b:-y1_e], y1, facecolors='blue', alpha=0.5)
        ax.fill_between(x_dates[y2_b:-y2_e], y2, facecolors='red', alpha=0.5)
        ax.set_title(self.title)
        plt.subplots_adjust(right=.8)
        fig.set_size_inches(10, 8, forward=True)

        return mpld3.fig_to_html(fig)

    def get_data(self, movie):

        # Get data
        # return self.create_plot(x, y1, y2)
        pass