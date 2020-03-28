import numpy as np
import pandas as pd


def clean(attr, res, res1):
    for key in attr:
        # print(key)
        classes = res[key].unique()
        classes1 = res1[key].unique()
        # if classes.shape[0] < 26:
        print(key, classes.shape, classes1.shape, classes1)

def findAttributesWithNan(attr, res):
    for key in attr:
        classes = res[key]
        if classes.isna().any():
            print(key, str(classes.isna().sum()) + "/" + str(classes.shape[0]))


if __name__ == "__main__":
    df_train = pd.read_csv("./data/train.csv")
    df_test = pd.read_csv("./data/test.csv")
    df_train = df_train.iloc[:, 0:80]
    result = df_train.append(df_test)
    attributes = result.keys()
    # clean(attributes, df_train, result)
    findAttributesWithNan(attributes, df_test)
    # for w in attributes:
