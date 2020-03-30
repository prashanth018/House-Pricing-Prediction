import numpy as np
import pandas as pd
from pprint import pprint


class Data:
    TRAIN_PATH = "./data/train.csv"
    TEST_PATH = "./data/test.csv"
    # 42 Categorical Attributes which needs a table
    CATEGORICAL_FEATURES = ['MSZoning', 'Street', 'Alley', 'LotShape', 'LandContour', 'Utilities', 'LotConfig',
                            'LandSlope', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle',
                            'RoofStyle', 'RoofMatl', 'Exterior1st', 'Exterior2nd', 'MasVnrType', 'ExterQual',
                            'ExterCond', 'Foundation', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1',
                            'BsmtFinType2', 'Heating', 'HeatingQC', 'CentralAir', 'Electrical', 'KitchenQual',
                            'Functional', 'FireplaceQu', 'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond',
                            'PavedDrive', 'PoolQC', 'Fence', 'MiscFeature', 'SaleType', 'SaleCondition']

    # 12 Categorical Attributes which contains nan
    CATEGORICAL_FEATURES_WITH_NAN = ['MSZoning', 'Utilities', 'Exterior1st', 'Exterior2nd', 'MasVnrType', 'Electrical',
                                     'BsmtFullBath', 'BsmtHalfBath', 'KitchenQual', 'Functional', 'GarageCars',
                                     'SaleType']

    # 14 Categorical Attributes with genuine nan
    CATEGORICAL_FEATURES_WITH_GENUINE_NAN = ['Alley', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1',
                                             'BsmtFinType2', 'FireplaceQu', 'GarageType', 'GarageFinish', 'GarageQual',
                                             'GarageCond', 'PoolQC', 'Fence', 'MiscFeature']

    # 24 Continuous Attributes which needs normalization
    CONTINUOUS_FEATURES = ['MSSubClass', 'LotFrontage', 'LotArea', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea',
                           'BsmtFinSF1',
                           'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF',
                           'GrLivArea', 'GarageYrBlt', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch',
                           '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal', 'YrSold']

    # 8 Continuous Attributes which contains nan
    CONTINUOUS_FEATURES_WITH_NAN = ['LotFrontage', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF',
                                    'GarageYrBlt', 'GarageArea']

    def __init__(self, train_path=TRAIN_PATH, test_path=TEST_PATH):
        self.df_train = ""
        self.df_test = ""
        self.df_combined = ""
        self.load_data(train_path, test_path)
        self.features = self.load_features()
        self.df_combined = (self.df_train.iloc[:, 0:80]).append(self.df_test)
        self.feature_map = {}
        self.create_tables()
        # Replace NAN values observed in categorical features
        self.fillna_features(self.CATEGORICAL_FEATURES_WITH_NAN)
        self.replace()
        # Replace NAN values observed in continuous features
        self.fillna_features(self.CONTINUOUS_FEATURES_WITH_NAN, op="median")
        #        self.normalize(self.CONTINUOUS_FEATURES)
        self.normalize(self.features)
        self.clean()

    # Loads the train and test dataframes with the files present int the given path.
    def load_data(self, train_path, test_path):
        self.df_train = pd.read_csv(train_path)
        self.df_test = pd.read_csv(test_path)

    # Gets the features.
    def load_features(self):
        return self.df_test.keys()

    # Method to display the unique values corresponding to the set of features specified
    # to the method. Considers all the features if nothing specified to the method.
    def find_unique_values(self, features=[]):
        if len(features) == 0:
            features = self.features
        for key in features:
            classes = self.df_combined[key].unique()
            print(key, classes.shape, classes)

    # Method to find the number of missing values for all the features.
    def find_features_with_nan(self):
        for key in self.features:
            classes = self.df_combined[key]
            if classes.isna().any():
                print(key, str(classes.isna().sum()) + "/" + str(classes.shape[0]))

    # Given any column and the dataframe to this method, the method returns the dataframe
    # with the corresponding column normalized. Uses min-max normalization.
    def normalize(self, features_to_normalize):
        features_to_normalize = list(features_to_normalize)
        for idx in range(len(features_to_normalize)):
            if features_to_normalize[idx] == 'Id':
                del features_to_normalize[idx]
                break

        self.df_combined[features_to_normalize] = self.df_combined[features_to_normalize].apply(
            lambda x: (x - x.min()) / (x.max() - x.min()))

    # given a list of features in input.txt, the method give a list of these features.
    def get_list(self):
        f = open("input.txt", "r")
        ls = f.readlines()
        for i in range(len(ls)):
            ls[i] = ls[i].rstrip('\n')
        print(ls)
        f.close()

    # Method to create a map for the values of each categorical features to numbers. Includes
    # functionality to segregate the features with genuine NA values from the features with
    # few missing records. Populates the feature_map class attribute.
    def create_tables(self):
        for w in self.CATEGORICAL_FEATURES:
            self.feature_map[w] = {}
            vals = list(self.df_combined[w].unique())
            if w not in self.CATEGORICAL_FEATURES_WITH_GENUINE_NAN:
                for val_idx in range(len(vals)):
                    if vals[val_idx] != vals[val_idx]:
                        del vals[val_idx]
                        break
            for val_idx in range(len(vals)):
                self.feature_map[w][vals[val_idx]] = val_idx
        # pprint(self.feature_map)

    # Given a list of attributes, method populates the missing records with the either mean/median
    # if specified, else uses mode as the default operation.
    def fillna_features(self, ExtArr, op="mode"):
        for w in ExtArr:
            if op == "mode":
                self.df_combined[w].fillna(self.df_combined[w].mode()[0], inplace=True)
            elif op == "median":
                self.df_combined[w].fillna(self.df_combined[w].median(), inplace=True)
            elif op == "mean":
                self.df_combined[w].fillna(self.df_combined[w].mean(), inplace=True)

    # Method to selectively replace the values of the attributes in the dataframe with the values
    # corresponding to the attributes specified in the feature_map.
    def replace(self):
        self.df_combined.replace(self.feature_map, inplace=True)

    def clean(self):
        train_rows = self.df_train.shape[0]
        test_rows = self.df_test.shape[0]
        self.df_train[self.features[:80]] = self.df_combined[:train_rows]
        self.df_test = self.df_combined[-test_rows:]
        print(self.df_train.shape)
        print(self.df_test.shape)

    def save_to_file(self):
        self.df_train.to_csv("cleaned_train.csv")
        self.df_test.to_csv("cleaned_test.csv")


if __name__ == "__main__":
    dp = Data()
    # dp.find_unique_values()
    # dp.get_list()
    # findAttributesWithNan(attributes, df_test)
    # for w in attributes:
    # dp.create_tables()
    # dp.find_unique_values(dp.CONTINUOUS_FEATURES_WITH_NAN)
    # print("*************************************************************************************")
    # dp.find_unique_values(dp.CONTINUOUS_FEATURES_WITH_NAN)
    # dp.replace()
    # dp.find_unique_values()
    # dp.find_unique_values()
    # dp.clean()
    # print(dp.df_test)
    dp.save_to_file()
