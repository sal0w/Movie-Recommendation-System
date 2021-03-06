#!/usr/bin/env python
# -*- coding: utf-8 -*-

# create a class called **Neural Network** which will create a network for a user to predict the score

# third party packages
import numpy as np

# library files
from random import shuffle

# local files
from . import convert

class Neural_Network:
    """
    It is a neural network to predict score for an item which may be given by an user.

    The index from 1 to :param nlayer: of :py:attr:`beta` and :py:attr:`W` contains ndarrays for the corresponding layers. The reason is we can flexibly change the number of layers.
    """
    def __init__(self, nlayer = 4):
        self.layerSize = [0, 19, 30, 15, 5]
        self.cost = float('inf')
        
        self.nlayer = nlayer
        self.beta   = [None for x in range(self.nlayer + 1)]
        self.alpha  = [None for x in range(self.nlayer + 1)]
        self.W      = [None for x in range(self.nlayer + 1)]
        self.delta  = [None for x in range(self.nlayer + 1)]
        for l in range(2, self.nlayer + 1):
            self.beta[l] = np.random.randn(self.layerSize[l])
            
            self.W[l] = np.random.randn(self.layerSize[l - 1], self.layerSize[l])
            
        # final hyperparameters
        self.final_beta = None
        self.final_alpha = None
        self.final_W = None
        self.final_delta = None
        self.final_error = float('inf')

    def feedforward(self, row):
        # set the input
        self.alpha[1] = np.array([row])
        #print(self.alpha[1])
        assert(len(row) == self.layerSize[1])

        # feedforward
        for l in range(2, self.nlayer + 1):
            assert(self.alpha[l - 1].shape[1] == self.W[l].shape[0])
            self.beta[l]  = self.alpha[l - 1].dot(self.W[l])
            self.alpha[l] = self.sigmoid(self.beta[l])

        assert(self.alpha[1].shape == (1, self.layerSize[1]))
        assert(self.alpha[2].shape == (1, self.layerSize[2]))
        assert(self.alpha[3].shape == (1, self.layerSize[3]))
        assert(self.beta[2].shape == (1, self.layerSize[2]))
        assert(self.beta[3].shape == (1, self.layerSize[3]))

        return self.alpha[self.nlayer]

    def calculate_error(self, training_examples):
        """
        """
        error = 0
        for feature, y in training_examples:
            error += abs(convert.f_inverse_cap(list(self.feedforward(feature)[0])) - convert.f_inverse(list(y))) ** 2


        cur_error = (error / len(training_examples)) ** .5
        
        # update the final hyperparamters
        if cur_error < self.final_error:
            self.final_beta = self.beta
            self.final_alpha = self.alpha
            self.final_W = self.W
            self.final_delta = self.delta
            self.final_error = cur_error
            print('Error', cur_error)
            
    def backpropagation(self, training_examples, epoch, eta):
        """
        backpropagation using stochastic gradient descent
        
        :param movie_info: one row of this array contains 40 ratings given by similar users and genre information
        :type movie_info:  ndarray

        :todo: the feature and y are not ndarrays, so convert those to ndarrays so that it will be easier to manipulate and watch the dimensions in your derivation.
        """
        for times in range(epoch):

            # randomly shuffle the training examples in the training set
            shuffle(training_examples)

            self.calculate_error(training_examples)
            
            for feature, y in training_examples:
                self.feedforward(feature)

                # compute the error for the last level
                self.delta[self.nlayer] = (self.alpha[self.nlayer] - y.ravel().reshape(self.alpha[self.nlayer].shape)) * self.sigmoidPrime(self.beta[self.nlayer])

                # backpropagate the error
                for l in range(self.nlayer - 1, 1, -1):
                    self.delta[l] = (self.W[l + 1].dot(self.delta[l + 1].T) * self.sigmoidPrime(self.beta[l].T)).T

                # update weights
                for l in range(self.nlayer, 1, -1):
                    self.W[l] -= (eta / len(training_examples)) * (self.alpha[l - 1].T).dot(self.delta[l])


        # load the optimal hyperparameters
        self.beta = self.final_beta
        self.alpha = self.final_alpha
        self.W = self.final_W
        self.delta = self.final_delta

        
    @staticmethod
    def sigmoid(beta):
        """function for sigmoid activation"""
        return 1 / (1 + np.exp(-beta))

    @staticmethod
    def sigmoidPrime(beta):
        """derivative of sigmoid function w.r.t val"""
        return (1 * np.exp(-beta)) / ((1 + np.exp(-beta)) ** 2)
