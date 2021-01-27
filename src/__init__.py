# -*- coding: utf-8 -*-

# Copyright 2021 Francisco Dans
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from anki.stats import CollectionStats


def time_per_card_graph(self):
    start, days, chunk = self.get_start_end_chunk()
    data = self._done(days, chunk)
    [DAY_INDEX, LEARN_INDEX, YOUNG_INDEX, MATURE_INDEX, RELEARN_INDEX] = [0, 1, 2, 3, 4]
    [LEARN_TIME_INDEX, YOUNG_TIME_INDEX, MATURE_TIME_INDEX, RELEARN_TIME_INDEX] = [6, 7, 8, 9]

    def calculate_time_per_day(row):
        total_reps = row[LEARN_INDEX] + row[YOUNG_INDEX] + row[MATURE_INDEX] + row[RELEARN_INDEX]
        total_time = row[LEARN_TIME_INDEX] + row[YOUNG_TIME_INDEX] + row[MATURE_TIME_INDEX] + row[RELEARN_TIME_INDEX]
        return 60 * total_time / total_reps

    time_per_card_data = list(map(lambda dayRow: (dayRow[DAY_INDEX], calculate_time_per_day(dayRow)), data))
    output = {'data': time_per_card_data, 'color': '#FF7F00'}
    conf: Dict[str, Any] = dict(
        xaxis=dict(tickDecimals=0, max=0.5),
        yaxes=[dict(min=0)],
    )
    txt1 = self._title("Time per card", "The average number of seconds spent on each card.")
    txt1 += self._graph(
        'timepercard', data=[output], conf=conf, xunit=chunk, ylabel='Seconds per card'
    )
    return self._section(txt1)


def new_reps_graphs(self):
    return originalRepsGraphs(self) + time_per_card_graph(self)


originalRepsGraphs = CollectionStats.repsGraphs
CollectionStats.repsGraphs = new_reps_graphs
