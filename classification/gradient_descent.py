"""
Date    : 15/5/29
Author  : baylor
"""
__author__ = 'baylor'


class GradientDescent(object):

    __param_vector = {}
    __learning_rate = 1.0
    __sum_of_data = 0

    # def gradient(self, data_set):
    #     return {}

    def next_iter(self):
        return False

    def get_param_vector(self):
        return self.__param_vector

    def get_learning_rate(self):
        return self.__learning_rate

    def get_sum_of_data(self):
        return self.__sum_of_data

    def set_sum_of_data(self, s):
        self.__sum_of_data = s

    def update_param(self, param, value):
        self.__param_vector[param] = value

    def get_param(self, param):
        return self.__param_vector[param]

    def compute(self, data_set):

        self.set_sum_of_data(len(data_set))

        while True:
            gradient_vector = self.gradient(data_set)

            for param, value in gradient_vector.items():
                self.update_param(param, self.get_param(param) + -1 * self.get_learning_rate())

            if not self.next_iter():
                break

        return self.__param_vector


class StochasticGradientDescent(GradientDescent):

    def compute(self, data_set):
        self.set_sum_of_data(len(data_set))

        while True:
            for feature_list in data_set:
                gradient_vector = self.gradient(feature_list)

                for param, value in gradient_vector.items():
                    self.update_param(param, self.get_param(param) + -1 * self.get_learning_rate())

                if not self.next_iter():
                    break