"""
Date    : 15/5/27
Author  : baylor
"""
from learning.gradient_descent import GradientDescent, StochasticGradientDescent
from regression import Regression

__author__ = 'baylor'


class LinearRegressionComputer(object):
    @staticmethod
    def compute_gradient(self, feature_list, param_vector, learning_rate, sum_of_data, gradient_vector):
        features, target = feature_list

        predict = self.predict(features, param_vector)

        error_value = learning_rate * (predict - target) / sum_of_data

        for word, field, value in features:
            gradient_vector[word] = error_value * value

    @staticmethod
    def predict(features, param_vector):
        predict = 0
        for word, field, value in features:
            predict += param_vector[word] * value
        return predict


class LinearGradientDescent(GradientDescent):

    def gradient(self, data_set):
        gradient_vector = {}
        for feature_list in data_set:
            LinearRegressionComputer.compute_gradient(feature_list,
                                                      self.get_param_vector(),
                                                      self.get_learning_rate(),
                                                      gradient_vector)
        return gradient_vector


class LinearStochasticGradientDescent(StochasticGradientDescent):

    def gradient(self, feature_list):
        gradient_vector = {}
        LinearRegressionComputer.compute_gradient(feature_list,
                                                  self.get_param_vector(),
                                                  self.get_learning_rate(),
                                                  gradient_vector)
        return gradient_vector

    def next_iter(self):
        # |gradient|
        # |weight|
        return True


class LinearRegression(Regression):

    __weight_dict = {}
    __gradient_dict = {}
    __lambda = 1.0
    __m = 100
    __common_w0_feature = '__w0__'

    def feature_extract(self, features):
        feature_list = self.__feature_extraction.process(features)
        feature_list.append(self.__common_w0_feature, self.__common_w0_feature, 1)
        return feature_list

    def process(self, data):
        features = data[0]
        target = data[1]

        gradient_dict = self.gradient(features, target)

    def compute_predict(self, features, param_vector):
        return LinearRegressionComputer.predict(features, param_vector)

if __name__ == '__main__':
    regress = LinearRegression()