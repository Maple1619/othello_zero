import tensorflow as tf
from tensorflow.keras import layers, Model
import numpy as np

from Env import Board
class OthelloZero:
    def __init__(self, n: int, model_file = None):
        self.n = n
        self.l2_const = 1e-4

        input = layers.Input(shape=(5,self.n,self.n))

        '''
        AlphaGO zeoro는 
        1 convolutional layer,
        40개의 residual layers
        1 value layer and 1 policy layer.

        각 residual layer는 
        Conv layer -> batch norm -> ReLU -> Conv layer -> batch norm -> skip connection -> ReLU
            │                                                                    ↑
            └────────────────────────────────────────────────────────────────────┘

        skip connection의 경우에는 
        f(x) + x

        로 이뤄져있다.
        즉, 총 40*2+1개의 convolution layer로 이뤄져 있다. (policy와 value에서 1회 convolution이 있긴 하나, 1,2개의 filter에 size도 1x1이라 무시함)

        바둑의 경우의수 : 1.4e768
        오셀로 경우의수 : 1.0e54
        10*714배 차이..

        따라서 1개의 conv layer, 1개의 residual layer, 1개의 value layer, 1개의 policy layer로 Model 구성.

        filter 개수는 32개로 고정.
        '''
        # Convolution layer
        ConvNet = layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same',data_format = 'channels_first')(input)
        ConvNet = layers.BatchNormalization()(ConvNet)
        ConvNet = layers.Activation('relu')(ConvNet)

        # Residual layer
        ResNet = layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same',data_format = 'channels_first')(ConvNet)
        ResNet = layers.BatchNormalization()(ResNet)
        ResNet = layers.Activation('relu')(ResNet)
        ResNet = layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same',data_format = 'channels_first')(ResNet)
        ResNet = layers.BatchNormalization()(ResNet)
        # Skip Connection
        ResNet = layers.Add()([ResNet,ConvNet])
        ResNet = layers.Activation('relu')(ResNet)

        # action policy network
        policyNet = layers.Conv2D(filters=2, kernel_size=(1, 1), padding='same', data_format = 'channels_first')(ResNet)
        policyNet = layers.BatchNormalization()(policyNet)
        policyNet = layers.Activation('relu')(policyNet)

        # state value layers
        valueNet = layers.Conv2D(filters=1, kernel_size=(1, 1), padding='same', data_format = 'channels_first')(ResNet)
        valueNet = layers.BatchNormalization()(valueNet)
        valueNet = layers.Activation('relu')(valueNet)
        valueNet = layers.Dense(64, activation = 'relu')(valueNet)
        valueNet = layers.Dense(1, activation = 'tanh')(valueNet)
        self.model = Model(inputs = input, outputs = [policyNet, valueNet])

    def saveModel():
        pass
