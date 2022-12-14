'''
This script is a minimal example of using a data generator that works with Keras.
'''
from keras.models import Model, Sequential
from keras.layers import Input, Dense
import tensorflow as tf
import numpy as np

# Make some random data
N = 300
M = N//4
X = np.random.randint(M, size=(N,))
Y = (X + 1) % N  # target will be next number in sequence (modulo N)
BSIZE = N//10

xtf = tf.one_hot(X, M)
ytf = tf.one_hot(Y, M)

# Define model
model = Sequential()
model.add(Dense(M, input_shape=(M,), activation='softmax'))
model.add(Dense(M, activation='linear'))
model.add(Dense(M, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print(model.summary())
print(f'Model input shape: {model.input_shape}')

# Define generator
def makeBatch(i, N=BSIZE):
    x = xtf[i:i+N]
    y = ytf[i:i+N]
    return (x, y)

from keras.utils import Sequence
class DataGenerator(Sequence):
    def __init__(self, x, y, batch_size=32):
        self.x = x
        self.y = y
        self.batch_size = batch_size

    def __len__(self):
        return len(self.x)//self.batch_size

    def __getitem__(self, index):
        return makeBatch(index)

# Train model
dgen = DataGenerator(xtf, ytf, batch_size=BSIZE)
print(f'Sample shape: {dgen[0][0].shape}')
print(f'Training on {len(dgen)} batches of size {BSIZE} (total size of {len(dgen)*BSIZE}))\n')
model.fit(dgen, epochs=5, batch_size=BSIZE)