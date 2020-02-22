#!/usr/bin/env python3
""" Function One-hot encode"""
import numpy as np


def one_hot_encode(Y, classes):
    """Function one-hot encode"""
    matrix = np.zeros((classes, len(Y)))
    if len(Y) < 1:
        return (None)
    if classes < 1:
        return (None)
    for i in range(len(Y)):
        a = Y[i]
        matrix[a][i] = 1
    return (matrix)
