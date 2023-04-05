import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.utils import plot_model
import numpy as np

square_state = np.ones((1,5,8,8))
input = layers.Input(shape=(5,8,8))

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
valueNet = layers.Flatten()(valueNet)
valueNet = layers.Dense(64, activation = 'relu')(valueNet)
valueNet = layers.Dense(1, activation = 'tanh')(valueNet)

model = Model(inputs = input, outputs = [policyNet, valueNet])
model.summary()

model.save('othelloZero.h5')
# plot_model(model, 'othelloZero.png')

# rlt = model.predict(square_state)
# for _ in rlt:
#     print(_.shape)
#     print(_)
    


# # import tensorflow.compat.v1 as tf
# # import numpy as np
# # square_state = np.zeros((1,5,8,8))
# # x = tf.constant(square_state)
# # y = tf.transpose(x,[0,2,3,1])
# # # print(x)
# # print(y)
# a = 1.4e768
# b = 1.0e54
