from __future__ import division
import numpy as np
from sklearn import datasets
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt

# NOTE:
# took about 8 hours to build (vs 10 min with sklearn)
# results not satisfying, maybe the data set is no good?
# spent a long time because of python 2 division
# still sometimes problem with exploding/vanishing weights

def ReLU(x):
    cache = x
    return x * (x > 0), cache

def dReLU(x):
    return 1. * (x > 0)

def ReLU_backward(dA, activation_cache):
    Z = activation_cache
    return dA *  dReLU(Z)

def sigmoid(x):
    cache = x
    return 1. / (1 + np.exp(-x)), cache

def dsigmoid(x):
    return x * (1. - x)

def sigmoid_backward(dA, activation_cache):
    Z = activation_cache
    return dA *  dsigmoid(Z)

def load_data(params, train_ration=0.7):
    iris = datasets.load_iris()
    l = list(zip(iris.data, iris.target))
    l = l[:100]
    np.random.shuffle(l)

    train_size = round(len(l) * train_ration)
    x_train = [x for x, _ in l[:train_size]]
    y_train = [y % 2 for _, y in l[:train_size]]
    x_test = [x for x, _ in l[train_size:]]
    y_test = [y % 2 for _, y in l[train_size:]]

    params["m"] = len(x_train)
    params["n_x"] = len(x_train[0])

    return x_train, y_train, x_test, y_test

def extract_data(data, params):
    m = len(data)
    n_x = len(data[0]) - 1
    params["m"] = m
    params["n_x"] = n_x

    X = np.array([np.array(x[:-1]) for x in data]).T.reshape((n_x, m))
    Y = np.array([np.array(x[-1]) for x in data]).T.reshape((m, 1))

    return X, Y

def initialize_layers(layers, params):
    n_x = params["n_x"]
    for i, l in enumerate(layers):
        num_row = l["num_units"]
        num_col = layers[i - 1]["num_units"]
        if i == 0:
            num_col = n_x
        params["Wl" + str(i+1)] = np.random.randn(num_row, num_col) * 0.01
        params["bl" + str(i+1)] = np.zeros((num_row, 1))

def linear_forward(A, W, b):
    Z = np.dot(W, A) + b
    cache = (A, W, b)

    return Z, cache

def linear_activation_forward(A, W, b, activation_func="relu"):
    Z, linear_cache = linear_forward(A, W, b)
    A_temp, W_temp, b_temp = linear_cache

    if activation_func == "relu":
        A, activation_cache = ReLU(Z)
    else:
        A, activation_cache = sigmoid(Z)

    Z_temp = activation_cache

    cache = (linear_cache, activation_cache)
    return A, cache


def compute_cost(A, Y, params):
    m = params["m"]
    AL = A.reshape((m, 1))

    cost = (-1 / m) * np.sum(np.multiply(Y, np.log(AL)) + np.multiply((1 - Y), np.log(1 - AL)))

    return cost

def linear_backward(dZ, cache, params):
    m = params["m"]
    (A_prev, W, b) = cache

    dW = (1 / m) * np.dot(dZ, A_prev.T)
    db = (1 / m) * np.sum(dZ, axis=1, keepdims=True)
    dA_prev = np.dot(W.T, dZ)

    return dA_prev, dW, db

def linear_activation_backward(dA, cache, layer, params):
    linear_cache, activation_cache = cache
    if layer["activation_func"] == "relu":
        dZ = ReLU_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache, params)

    elif layer["activation_func"] == "sigmoid":
        dZ = sigmoid_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache, params)

    return dA_prev, dW, db

def run_forward_prop(X, layers, params):
    caches = []
    A = X

    for i, _ in enumerate(layers):
        A, cache = linear_activation_forward(A, params["Wl" + str(i+1)], params["bl" + str(i+1)], layers[i]["activation_func"])
        caches.append(cache)

    return A, caches

def run_backward_prop(AL, Y, caches, params):
    grads = {}
    L = len(caches)
    m = params["m"]
    AL = AL.reshape((1, m))
    Y = Y.reshape(AL.shape)

    dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))

    current_cache = caches[L-1]

    grads["dA" + str(L-1)], grads["dW" + str(L)], grads["db" + str(L)] = linear_activation_backward(dAL, current_cache, layers[L-1], params)

    for l in reversed(range(L-1)):
        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads["dA" + str(l + 1)], current_cache, layers[l], params)
        grads["dA" + str(l)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp
        grads["db" + str(l + 1)] = db_temp

    return grads

def update_params(params, grads, layers, learning_rate):
    for i in range(len(layers)):
        params["Wl" + str(i+1)] = params["Wl" + str(i+1)] - learning_rate * grads["dW" + str(i + 1)]
        params["bl" + str(i+1)] = params["bl" + str(i+1)] - learning_rate * grads["db" + str(i + 1)]

    return params

def train_nn(data, layers, num_iterations=200, learning_rate=0.0075):
    params = {}
    X, Y = extract_data(data, params)
    x_train, y_train, x_test, y_test = load_data(params)
    x_train_deep = np.array(x_train).T
    y_train_deep = np.array(y_train)

    initialize_layers(layers, params)
    for i in range(num_iterations):
        AL, caches = run_forward_prop(x_train_deep, layers, params)
        if i % 100 == 0:
            cost = compute_cost(AL, y_train_deep, params)
            print(cost)
        grads = run_backward_prop(AL, y_train_deep, caches, params)
        params = update_params(params, grads, layers, learning_rate)

    x_test_deep = np.array(x_test).T
    y_test_deep = np.array(y_test)
    A_out, _ = run_forward_prop(x_test_deep, layers, params)
    print(A_out)
    print(y_test_deep)
    res = [1 if y < 0.5 else 0 for y in A_out[0]]
    res2 = [1 if y >= 0.5 else 0 for y in A_out[0]]
    accuracy_deep = (1 / len(x_test)) * np.sum([1 if res[i] == y_test[i] else 0 for i in range(len(x_test))])
    accuracy_deep2 = (1 / len(x_test)) * np.sum([1 if res2[i] == y_test[i] else 0 for i in range(len(x_test))])

    clf = MLPClassifier(solver='lbfgs', max_iter=5000, alpha=0.75, hidden_layer_sizes=(1, 4), random_state=1)
    clf.fit(x_train, y_train)
    pred = clf.predict(x_test)
    accuracy_skl = (1 / len(x_test)) * np.sum([1 if pred[i] == y_test[i] else 0 for i in range(len(x_test))])
    print("___")
    print("Accuracy custom NN: " + str(accuracy_deep))
    print("Accuracy2 custom NN: " + str(accuracy_deep2))
    print("Accuracy sklearn: " + str(accuracy_skl))
    print("___")

if __name__ == "__main__":
    print("Neural Network")

    layers = [
        {"num_units": 3, "activation_func": "relu"},
        {"num_units": 2, "activation_func": "relu"},
        {"num_units": 3, "activation_func": "relu"},
        {"num_units": 1, "activation_func": "sigmoid"}
    ]
    data = [
        [0, 1, 2, 3, 4, 0],
        [0, 1, 0, 3, 0, 1],
        [0, 1, 2, 3, 4, 0],
        [0, 1, 0, 3, 0, 1],
        [0, 1, 2, 3, 4, 0],
        [0, 1, 1, 3, 1, 1],
        [0, 1, 2, 3, 4, 0],
        [0, 1, 0, 3, 0, 1],
        [0, 1, 2, 3, 4, 0],
        [0, 1, 0, 3, 0, 1]
    ]

    train_nn(data, layers)


# started 1230
