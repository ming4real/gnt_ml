#!/usr/bin/env python3

import csv\

import pandas as pd
import numpy as np
import ast


class TouchSensor():
    def __init__(self):
        self.data_set = []
        self.data_file = 'touch_events.csv'

    def process_features(self, dataframe):
        df = pd.DataFrame()
        df['event'] = dataframe['event'].apply(
            lambda x: np.array(ast.literal_eval(x)).flatten())

        new_columns = ["Input" + str(x) for x in range(800)]

        df2 = pd.DataFrame()
        df2[new_columns] = pd.DataFrame(
            df['event'].values.tolist(), columns=new_columns)
        df2 = df2.values
        return df2

    def readData(self):
        print("Reading data from {}".format(self.data_file))
        # src_df = pd.read_csv(self.data_file, sep=",")
        # training_examples = self.process_features(src_df)
        # print(type(training_examples))
        # print(training_examples.view())

        with open(self.data_file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            i = 0

            for row in reader:
                row_set = [[],[],[],[],[],[],[],[]]
                i += 1
                if i == 1:
                    continue

                timestamp = row[0]
                # Cope with [ or [[ at the start
                if row[1][1] == '[':
                    raw_data = row[1][2:-2]
                else:
                    raw_data = row[1][1:-2]
                known_class = row[2]

                tmp = raw_data.split('], [')
                # if i % 100 == 2:
                #     print("TMP: {}".format(tmp))
                for next_data in tmp:
                    tmp2 = next_data.split(', ')

                    for j in range(8):
                        row_set[j].append(tmp2[j])

                self.data_set.append([timestamp, row_set, known_class, []])

        csv_file.close()

    def writeData(self):
        print(self.data_set)

    def preProcess(self):
        row_count = 0
        for row in self.data_set:
            row_set = row[1]

            data_row_count = 0
            low_triggers = [[],[],[],[],[],[],[],[]]
            for data_rows in row_set:
                # print("Data: {}".format(data_rows))
                data_count = 0
                previous_point = 1
                for data_point in data_rows:
                    if float(data_point) > 0.5:
                        data_point = 1
                    else:
                        data_point = 0

                    self.data_set[row_count][1][data_row_count][data_count] = data_point
                    if previous_point != data_point:
                        if previous_point == 1:
                            # Transition between high and low
                            low_triggers[data_row_count].append(data_count)

                    previous_point = data_point

                    data_count += 1

                # if row_count % 100 == 0:
                #     print(self.data_set[row_count][1][data_row_count])
                #     print(low_triggers)
                data_row_count += 1
            self.data_set[row_count][3] = low_triggers

            row_count += 1

        print(self.data_set[0])

    def classifyData(self):
        row_count = 0
        number_correct = 0
        for row in self.data_set:
            touch_type = row[2]
            triggers = row[3]
            my_guess = ""

            # Detect double taps
            double_taps = 0
            for data in triggers:
                if len(data) > 1:
                    double_taps += 1

            if double_taps > 2:
                my_guess = "k"

            elif triggers[0] > triggers[1] > triggers[2] > triggers[3] or triggers[4] > triggers[5] > triggers[6] > triggers[7]:
                my_guess = "r"
            elif triggers[0] < triggers[1] < triggers[2] < triggers[3] or triggers[4] < triggers[5] < triggers[6] < triggers[7]:
                my_guess = "b"
            else:
                my_guess = "u"

            print("Row {} is {} ({})".format(row_count, my_guess, touch_type))
            if my_guess == touch_type:
                print("Correct")
                number_correct += 1
            else:
                print("!!! WRONG !!!")
            row_count += 1

        stats = (number_correct / row_count) * 100
        print("Stats\nCorrect: {}\nTotal: {}\nPercent: {}".format(number_correct, row_count, stats))

if __name__ == "__main__":
    sensor = TouchSensor()
    sensor.readData()
    # sensor.writeData()
    sensor.preProcess()
    sensor.classifyData()

