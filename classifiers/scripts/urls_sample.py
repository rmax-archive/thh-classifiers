# -*- coding: utf-8 -*-
import pandas as pd


if __name__ == '__main__':
    sample_size = 0
    min_class_size = 50
    test_sample_size = 0.3
    infile = "/media/sf_temp/func_class_items_texts.json"

    all_data = pd.read_json(infile)

    print all_data.columns

    for cat in all_data["category"].unique():
        print cat
        print all_data[all_data["category"] == cat].head(1)["url"]

