#!/usr/bin/env python3
""" Deep Neural Network class: defines a deep neural network class
with private instances attributes
"""

import numpy as np
import matplotlib.pyplot as plt


class DeepNeuralNetwork:
    """ Class Deep Neural networks"""
    def __init__(self, nx, layers):
        """ Settings for class Deep Neural Networks"""
        if type(nx) is not int:
            raise TypeError("nx must be an integer")
        if nx < 1:
            raise ValueError("nx must be a positive integer")
        if type(layers) is not list:
            raise TypeError("layers must be a list of positive integers")
        self.nx = nx
        self.layers = layers
        self.__L = len(layers)
        self.__cache = {}
        self.__weights = {}
        ly = layers.copy()
        ly.insert(0, nx)
        for l in range(1, self.__L + 1):
            if type(ly[l-1]) is not int or ly[(l-1)] < 0:
                raise TypeError("layers must be a list of positive integers")
            temp = np.random.randn(ly[l], ly[l-1]) * (np.sqrt(2/ly[l-1]))
            self.__weights['W'+str(l)] = temp
            self.__weights['b'+str(l)] = np.zeros((ly[l], 1))

    @property
    def L(self):
        return self.__L

    @property
    def cache(self):
        return self.__cache

    @property
    def weights(self):
        return self.__weights

    def sigmoid(self, Z):
        """Function sigmoid"""
        sigm = 1 / (1 + np.exp(-Z))
        return sigm

    def forward_prop(self, X):
        """Function forward propoagation"""
        for i in range(self.__L + 1):
            if i == 0:
                self.__cache['A0'] = X
            else:
                A_tmp = (np.matmul(self.__weights['W' + str(i)],
                                   self.__cache['A' + str(i - 1)])
                         + self.__weights['b' + str(i)])
                H_tmp = self.sigmoid(A_tmp)
                self.__cache['A' + str(i)] = H_tmp
        return (self.__cache['A'+str(self.__L)], self.__cache)

    def cost(self, Y, A):
        """Function cost"""
        m = Y.shape[1]
        num_lreg = -1 * (Y * np.log(A) + (1 - Y) *
                         np.log(1.0000001 - A))
        cost = np.sum(num_lreg)/m
        return (cost)

    def evaluate(self, X, Y):
        """Function evauate"""
        self.forward_prop(X)
        A = self.__cache['A' + str(self.__L)]
        PRED = np.where(A >= 0.5, 1, 0)
        return (PRED, self.cost(Y, A))

    def gradient_descent(self, Y, cache, alpha=0.05):
        """Function gradient descent"""
        dW = {}
        dWT = {}
        db = {}
        dZ = {}
        m = Y.shape[1]
        wg = self.__weights.copy()
        posi = str(self.__L)
        dZ['dZ'+posi] = self.__cache['A' + posi] - Y
        db['db'+posi] = np.sum(dZ['dZ'+posi], axis=1, keepdims=True)/m
        dW['dW'+posi] = np.matmul(self.__cache['A'+str(self.__L - 1)],
                                  dZ['dZ'+posi].T) / m
        dWT['dWT'+posi] = dW['dW'+posi].T
        self.__weights['W'+posi] = wg['W'+posi] - alpha*dWT['dWT'+posi]
        self.__weights['b'+posi] = wg['b'+posi] - alpha*db['db'+posi]
        for i in range(self.__L - 1, 0, -1):
            posl = str(i-1)
            posm = str(i+1)
            pos = str(i)
            g_temp = self.__cache['A'+pos] * (1 - self.__cache['A'+pos])
            dZ['dZ'+pos] = np.matmul(wg['W'+posm].T, dZ['dZ'+posm]) * g_temp
            db['db'+pos] = np.sum(dZ['dZ'+pos], axis=1, keepdims=True)/m
            dW['dW'+pos] = np.matmul(self.__cache['A'+posl],
                                     dZ['dZ'+pos].T) / m
            dWT['dWT'+pos] = dW['dW'+pos].T
            self.__weights['W'+pos] = wg['W'+pos] - alpha*dWT['dWT'+pos]
            self.__weights['b'+pos] = wg['b'+pos] - alpha*db['db'+pos]
        return()

    def train(self, X, Y, iterations=5000, alpha=0.05, verbose=True,
              graph=True, step=100):
        """Function Train - with more args"""
        if type(iterations) is not int:
            raise TypeError("iterations must be an integer")
        if iterations <= 0:
            raise ValueError("iterations must be a positive integer")
        if type(alpha) is not float:
            raise TypeError("alpha must be a float")
        if alpha <= 0:
            raise ValueError("alpha must be positive")
        if verbose is True or graph is True:
            if type(step) is not int:
                raise TypeError("step must be an integer")
            if step <= 0 or step > iterations:
                raise ValueError("step must be positive and <= iterations")
        arr_cost = []
        arr_pos = []
        PRED, cost = self.evaluate(X, Y)
        iters = 0
        pos = 0
        arr_pos.append(0)
        arr_cost.append(cost)
        if verbose is True:
            print("Cost after {} iterations: {}".format(0, cost))
        for i in range(1, iterations + 1):
            self.gradient_descent(Y, self.__cache, alpha)
            PRED, cost = self.evaluate(X, Y)
            iters = iters + 1
            if iters == step:
                iters = 0
                pos = pos + 1
                arr_pos.append(i)
                arr_cost.append(cost)
                if verbose is True:
                    print("Cost after {} iterations: {}".format(i, cost))
        PRED, cost = self.evaluate(X, Y)
        pos = pos + 1
        arr_pos.append(iterations)
        arr_cost.append(cost)
        if verbose is True:
            print("Cost after {} iterations: {}".format(iterations, cost))
        if graph is True:
            plt.xlim(0, iterations)
            plt.xlabel('iteration')
            plt.ylabel('cost')
            plt.title("Training cost")
            plt.plot(arr_pos, arr_cost)
            plt.show()
        return(PRED, cost)
