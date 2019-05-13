import altair as alt
import pandas as pd
import numpy as np
from .visualizer import Visualizer


def get_sort_index(dataframe, sort_columns):
    sorted_dataframe = dataframe.sort_values(by=sort_columns)
    sorted_dataframe['sort_index'] = np.arange(len(dataframe.index))
    return sorted_dataframe['sort_index']


def create_scatter_plot(dataframe, x, y, label):
    return alt.Chart(dataframe).mark_point(size=100).encode(
        x=x,
        y=y,
        tooltip=label,
    ).properties(
        width=1000,
        height=1000,
    ).interactive()


def dataframe_preparation(gold_standard_df, similarity_log_df):
    dataframe = similarity_log_df
    dataframe['label'] = similarity_log_df['word1'] + ', ' + similarity_log_df['word2']
    dataframe['their_score'] = gold_standard_df['score']
    dataframe.dropna()
    dataframe['our_rank'] = get_sort_index(similarity_log_df, ['our_score'])
    dataframe['their_rank'] = get_sort_index(similarity_log_df, ['their_score'])
    return dataframe


class SimilarityVisualizer(Visualizer):

    log_file = 'similarities.csv'

    task_type = 'SimilarityTask'

    def __init__(self, output_dir, gold_standard, similarity_log):
        super().__init__(output_dir)
        gold_standard_df = pd.read_csv(gold_standard)
        similarity_log_df = pd.read_csv(similarity_log, names=['word1', 'word2', 'our_score'])
        self.dataframe = dataframe_preparation(gold_standard_df, similarity_log_df)

    def create_visualizations(self):
        create_scatter_plot(self.dataframe, 'our_rank', 'their_rank', 'label')\
            .save(str(self.output_dir.joinpath('rank_chart.html')))
        create_scatter_plot(self.dataframe, 'our_score', 'their_score', 'label')\
            .save(str(self.output_dir.joinpath('score_chart.html')))
