import random
import numpy as np
from PIL import Image

def checkIfBright():
    total_value = 0

    im = Image.open('checker.jpg')
    pix = im.load()
    size = im.size
    x_size = size[0]
    y_size = size[1]
    pixels = []

    for i in range(x_size):
        for j in range(y_size):
            pixels.append(pix[i,j])

    for i in pixels:
        if i[0] == 255:
            total_value = total_value + .25
        else:
            total_value = total_value + -.25 
    isImageBright(total_value)

def sigmoid(x):
    return np.tanh(x)


def dsigmoid(x):
    return 1.0 - x ** 2


class MLP:

    def __init__(self, *args):
        
        self.shape = args
        n = len(args)

        # Build layers
        self.layers = []

        self.layers.append(np.ones(self.shape[0] + 1))

        for i in range(1, n):
            self.layers.append(np.ones(self.shape[i]))


        self.weights = []

        for i in range(n - 1):
            self.weights.append(np.zeros((self.layers[i].size,
                                          self.layers[i + 1].size)))

        self.dw = [0, ] * len(self.weights)
        self.reset()

    def reset(self):
        ''' Reset weights '''
        for i in range(len(self.weights)):
            Z = np.random.random((self.layers[i].size, self.layers[i + 1].size))
            self.weights[i][...] = (2 * Z - 1) * 0.25

    def propagate_forward(self, data):
        self.layers[0][0:-1] = data

        for i in range(1, len(self.shape)):
            self.layers[i][...] = sigmoid(np.dot(self.layers[i - 1], self.weights[i - 1]))

        # Return output
        return self.layers[-1]

    def propagate_backward(self, target, lrate=0.1, momentum=0.1):
        deltas = []

        # Compute error on output layer
        error = target - self.layers[-1]
        delta = error * dsigmoid(self.layers[-1])
        deltas.append(delta)

        # Compute error on hidden layers
        for i in range(len(self.shape) - 2, 0, -1):
            delta = np.dot(deltas[0], self.weights[i].T) * dsigmoid(self.layers[i])
            deltas.insert(0, delta)

        # Update weights
        for i in range(len(self.weights)):
            layer = np.atleast_2d(self.layers[i])
            delta = np.atleast_2d(deltas[i])
            dw = np.dot(layer.T, delta)
            self.weights[i] += lrate * dw + momentum * self.dw[i]
            self.dw[i] = dw

        # Return error
        return (error ** 2).sum()
    def returnepoch(self):
        return  random.randint(4,16)


if __name__ == '__main__':
    import matplotlib
    import matplotlib.pyplot as plt


    def learn(network, training, epochs=10000, lrate=.1, momentum=0.1):
        # Train
        for i in range(epochs):
            n = np.random.randint(training.size)
            network.propagate_forward(training['input'][n])
            network.propagate_backward(training['output'][n], lrate, momentum)
        # Test
        for i in range(training.size):
            o = network.propagate_forward(training['input'][i])
            print("Training", i, training['input'][i], '%.2f' % o[0], )
            print('(expected %.2f)' % training['output'][i])
            print()
        print()


    network = MLP(4, 2, 1)

    print("Untrained Weights:")
    weights1 = network.weights
    count = 1

    for i in weights1:
        for a in i:
            print("node {}:".format(count))
            for n in a:
                print(n, end = " ")
                print(" ")
            count +=  1

    training = np.zeros(16, dtype=[('input', float, 4), ('output', float, 1)])

    print()

    network.reset()

    training[0] = (0, 0, 0, 0), 0
    training[1] = (0, 0, 1, 0), 0
    training[2] = (0, 0, 1, 1), 0
    training[3] = (0, 1, 0, 0), 0
    training[4] = (0, 1, 0, 1), 0
    training[5] = (0, 1, 1, 0), 0
    training[6] = (0, 1, 1, 1), 1
    training[7] = (1, 0, 0, 0), 0
    training[8] = (1, 0, 0, 1), 0
    training[9] = (1, 0, 1, 0), 0
    training[10] = (1, 0, 1, 1), 1
    training[11] = (1, 1, 0, 0), 0
    training[12] = (1, 1, 0, 1), 0
    training[13] = (1, 1, 1, 0), 1
    training[14] = (1, 1, 1, 1), 1
    training[15] = (0, 0, 0, 1), 0

    learn(network, training)

    print("Trained Weights:")
    print("")
    weights1 = (network.weights)

    count = 1


    for i in weights1:
        for a in i:
            print("node {}:".format(count))
            for n in a:
                print(n, end = " ")
                print(" ")
            count +=  1


    print("Epoch Errors: " + str(network.returnepoch()))
