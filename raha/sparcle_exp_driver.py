import argparse
import os
import time
import warnings

import raha
from correction import combine_xy, init_distance_matrix
from raha import Detection, Correction

warnings.simplefilter(action='ignore', category=FutureWarning)
from eval import do_eval

if __name__ == "__main__":
    start = time.perf_counter()

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--Dataset")
    parser.add_argument("-t", "--Times")
    args = parser.parse_args()
    dataset_name = args.Dataset
    times = int(args.Times)
    print(f"Dataset: {dataset_name}, Times: {times}")

    # Load the dataset
    dataset_dictionary = {
        "name": dataset_name,
        "path": os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "datasets", dataset_name, "dirty.csv")),
        "clean_path": os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "datasets", dataset_name, "clean.csv"))
    }
    data = raha.dataset.Dataset(dataset_dictionary)
    combine_xy(data)
    df_dm = init_distance_matrix(data)
    print("Done initializing distance matrix")

    for counter in range(times):
        # error detection
        app_detect = Detection()
        app_detect.VERBOSE = False
        app_detect.SAVE_RESULTS = False
        detection_dictionary = app_detect.run(dataset_dictionary)
        p, r, f = data.get_data_cleaning_evaluation(detection_dictionary)[:3]
        print("Raha's performance on {}:\nPrecision = {:.2f}\nRecall = {:.2f}\nF1 = {:.2f}".format(data.name, p, r, f))

        # error correction
        data.detected_cells = detection_dictionary
        app_correct = Correction()
        app_correct.VERBOSE = True
        app_correct.SAVE_RESULTS = False
        app_correct.distance_matrix = df_dm
        correction_dictionary = app_correct.run(data)
        p, r, f = data.get_data_cleaning_evaluation(correction_dictionary)[-3:]
        print("Baran's performance on {}:\nPrecision = {:.2f}\nRecall = {:.2f}\nF1 = {:.2f}".format(data.name, p, r, f))
        data.create_repaired_dataset(correction_dictionary=correction_dictionary)

        # attribute evaluation
        end = time.perf_counter()
        runtime = time.strftime("%Hh%Mm%Ss", time.gmtime(end - start))
        output_file = f'{dataset_dictionary["name"]}_eval_{counter}_{runtime}.csv'
        do_eval(data, data.dataframe.columns[3:].to_list(), output_file)
