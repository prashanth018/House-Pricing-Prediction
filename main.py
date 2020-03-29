import numpy as np
import pandas as pd


class Data:
    TRAIN_PATH = "./data/train.csv"
    TEST_PATH = "./data/test.csv"

    def __init__(self, train_path=TRAIN_PATH, test_path=TEST_PATH):
        self.df_train = ""
        self.df_test = ""
        self.df_combined = ""
        self.load_data(train_path, test_path)
        self.features = self.load_features()
        self.df_combined = (self.df_train.iloc[:, 0:80]).append(self.df_test)

    # Loads the train and test dataframes with the files present int the given path.
    def load_data(self, train_path, test_path):
        self.df_train = pd.read_csv(train_path)
        self.df_test = pd.read_csv(test_path)

    def load_features(self):
        return self.df_test.keys()

    def find_unique_values(self):
        for key in self.features:
            classes = self.df_combined[key].unique()
            print(key, classes.shape, classes)

    def find_features_with_nan(self):
        for key in self.features:
            classes = self.df_combined[key]
            if classes.isna().any():
                print(key, str(classes.isna().sum()) + "/" + str(classes.shape[0]))

    # Given any column and the dataframe to this method, the method returns the dataframe with the corresponding column normalized.
    def normalize(self, df, column_name):
        return


if __name__ == "__main__":
    dp = Data()
    dp.find_unique_values()
    # findAttributesWithNan(attributes, df_test)
    # for w in attributes:
