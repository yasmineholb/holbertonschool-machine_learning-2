#!/usr/bin/env python3
""" Function Convolution Forward
Write a function  that performs forward propagation over a convolutional
layer of a neural network:

A_prev is a numpy.ndarray of shape (m, h_prev, w_prev, c_prev) containing
the output of the previous layer
m is the number of examples
h_prev is the height of the previous layer
w_prev is the width of the previous layer
c_prev is the number of channels in the previous layer
W is a numpy.ndarray of shape (kh, kw, c_prev, c_new) containing the kernels
for the convolution
kh is the filter height
kw is the filter width
c_prev is the number of channels in the previous layer
c_new is the number of channels in the output
b is a numpy.ndarray of shape (1, 1, 1, c_new) containing the biases applied
to the convolution
activation is an activation function applied to the convolution
padding is a string that is either same or valid, indicating the type of
padding used
stride is a tuple of (sh, sw) containing the strides for the convolution
sh is the stride for the height
sw is the stride for the width
you may import numpy as np
Returns: the output of the convolutional layer
"""
import numpy as np


def conv_forward(A_prev, W, b, activation, padding="same", stride=(1, 1)):
    """ Function Convolution Forward"""
    convolve_A = convolve(A_prev, W, padding, stride)
    convolve_B = np.sum(convolve_A + b)
    convolve_C = activation(convolve_A)
    return(convolve_C)


def convolve(X, W, padding, stride):
    """Function convolution"""
    m, h, w, c = X.shape
    kh, kw, kc, nc = W.shape
    sh = stride[0]
    sw = stride[1]
    if padding == 'same':
        ph = int(((h - 1)*sh + kh - h)/2) + 1
        pw = int(((w - 1)*sw + kw - w)/2) + 1
    else:
        ph, pw = 0, 0
    new_X = np.pad(X, ((0, 0), (ph, ph), (pw, pw), (0, 0)),
                   mode='constant', constant_values=0)
    ch = int(np.floor(((h - kh + 2*ph) / sh) + 1))
    cw = int(np.floor(((w - kw + 2*pw) / sw) + 1))
    new_conv = np.zeros((m, ch, cw, nc))
    m_o = np.arange(0, m)
    for row in range(ch):
        for col in range(cw):
            for n_k in range(nc):
                a = row*sh
                b = row*sh + kh
                c = col*sw
                d = col*sw + kw
                new_conv[m_o, row, col, n_k] = np.sum(np.multiply
                                                      (new_X[m_o, a:b,
                                                             c:d, ],
                                                       W[:, :, :, n_k]),
                                                      axis=(1, 2, 3))
    return(new_conv)
