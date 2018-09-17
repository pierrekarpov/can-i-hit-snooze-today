from os import listdir
from os.path import isfile, join
from PIL import Image
import numpy as np
import deep_nn_step_by_step as dnn
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib


def flatten_image(path="image_data/cropped_images/car/6b6777a5-ff5c-4f11-9f1c-8a98ba75e2f4_car_0.jpg", is_car=True, flat_image_size=3072):
    # path = "image_data/cropped_images/" + ("car/" if is_car else "not_car/")  + file_name
    im = Image.open(path)

    flat = list(im.getdata())
    label = 1 if is_car else 0

    np_flat = np.array(flat).reshape(1, flat_image_size)
    np_label = np.array([label]).reshape(1, 1)

    return np_flat, np_label

def flatten_images():
    flat_image_size = 32 *32 *3

    flatten_cars = [flatten_image(join("./image_data/cropped_images/car", f), True, flat_image_size) for f in listdir("./image_data/cropped_images/car") if isfile(join("./image_data/cropped_images/car", f))]
    flatten_cars_X = [fc[0][0] for fc in flatten_cars]
    flatten_cars_y = [fc[1][0] for fc in flatten_cars]
    flatten_cars_X = np.array(flatten_cars_X).reshape(len(flatten_cars), flat_image_size)
    flatten_cars_y = np.array(flatten_cars_y).reshape(len(flatten_cars), 1)

    flatten_not_cars = [flatten_image(join("./image_data/cropped_images/not_car", f), False, flat_image_size) for f in listdir("./image_data/cropped_images/not_car") if isfile(join("./image_data/cropped_images/not_car", f))]
    flatten_not_cars_X = [fc[0][0] for fc in flatten_not_cars]
    flatten_not_cars_y = [fc[1][0] for fc in flatten_not_cars]
    flatten_not_cars_X = np.array(flatten_not_cars_X).reshape(len(flatten_not_cars), flat_image_size)
    flatten_not_cars_y = np.array(flatten_not_cars_y).reshape(len(flatten_not_cars), 1)

    return flatten_cars_X, flatten_cars_y, flatten_not_cars_X, flatten_not_cars_y

def split_data(flatten_cars_X, flatten_cars_y, flatten_not_cars_X, flatten_not_cars_y, split_ratio=0.7):
    car_idx = int(flatten_cars_X.shape[0] * split_ratio)
    not_car_idx = int(flatten_not_cars_X.shape[0] * split_ratio)

    train_X = np.append(flatten_cars_X[:car_idx, :], flatten_not_cars_X[:not_car_idx, :], axis=0)
    test_X = np.append(flatten_cars_X[car_idx:, :], flatten_not_cars_X[not_car_idx:, :], axis=0)
    train_y = np.append(flatten_cars_y[:car_idx, :], flatten_not_cars_y[:not_car_idx, :], axis=0)
    test_y = np.append(flatten_cars_y[car_idx:, :], flatten_not_cars_y[not_car_idx:, :], axis=0)

    return train_X, train_y, test_X, test_y

def test_custom_model(train_X, train_y, test_X, test_y, layers, alpha):
    layers_dims = layers
    x_train_deep = np.array(train_X).T
    y_train_deep = np.array([train_y])

    parameters = dnn.L_layer_model(x_train_deep, y_train_deep, layers_dims, learning_rate = alpha, num_iterations=20000, print_cost=False, plot_cost=False)

    x_test_deep = np.array(test_X).T
    A_out, _ = dnn.L_model_forward(x_test_deep, parameters)
    res = [1 if y < 0.5 else 0 for y in A_out[0]]
    print("___")
    accuracy_deep = (1 / len(test_X)) * np.sum([1 if res[i] == test_y[i] else 0 for i in range(len(test_X))])
    print("Accuracy custom NN: " + str(accuracy_deep))
    print("___")

    return accuracy_deep

def get_model_accuracy(clf, test_X, test_y):
    pred = clf.predict(test_X)
    accuracy = (1 / len(test_X)) * np.sum([1 if pred[i] == test_y[i] else 0 for i in range(len(test_X))])

    return accuracy

def test_model(train_X, train_y, test_X, test_y, layers=(3, 3), alpha=0.0075, save=False):

    clf = MLPClassifier(solver='lbfgs', alpha=alpha, hidden_layer_sizes=layers, random_state=1)
    clf.fit(train_X, train_y)

    if save:
        joblib.dump(clf, './image_data/models/car_detection_nn_model.pkl')

    accuracy = get_model_accuracy(clf, test_X, test_y)

    return accuracy

def train_layer_size(train_X, train_y, test_X, test_y):
    for i in range(31):
        layers = (i + 1, )
        accuracy = test_model(train_X, train_y, test_X, test_y, layers)
        print(i, accuracy)
    # Best: 16: 0.88, 23: 0.90

def train_layer_depth(train_X, train_y, test_X, test_y):
    for i in [2, 5, 16, 23]:
        for j in [1, 2, 10, 20]:
            layers = ()
            for _ in range(j):
                layers = layers + (i,)
            accuracy = test_model(train_X, train_y, test_X, test_y, layers)
            print(layers, accuracy)
    # Best 16x10: 0.909, 23x10: 0.907

def train_alpha(train_X, train_y, test_X, test_y):
    for a in [0.00001, 0.00003, 0.00005,
              0.0001, 0.0003, 0.0005,
              0.001, 0.003, 0.005,
              0.01, 0.03, 0.05,
              0.1, 0.3, 0.5]:
        layers = (16, 16, 16, 16, 16, 16, 16, 16, 16, 16)
        accuracy = test_model(train_X, train_y, test_X, test_y, layers, a)
        print(a, accuracy)

    # Best: 0.0001: 0.911, 0.001: 0.903

def train_models(train_X, train_y, test_X, test_y):
    train_layer_size(train_X, train_y, test_X, test_y)
    train_layer_depth(train_X, train_y, test_X, test_y)
    train_alpha(train_X, train_y, test_X, test_y)

def load_and_test_model(test_X, test_y):
    clf = joblib.load('./image_data/models/car_detection_nn_model.pkl')
    accuracy = get_model_accuracy(clf, test_X, test_y)
    print(accuracy)

def classify_image(image_path="image_data/cropped_images/car/6b6777a5-ff5c-4f11-9f1c-8a98ba75e2f4_car_0.jpg"):
    X, _ = flatten_image(image_path)
    clf = joblib.load('./image_data/models/car_detection_nn_model.pkl')
    pred = clf.predict(X)
    print(pred)


def main():
    # split_ratio = 0.7
    # flatten_cars_X, flatten_cars_y, flatten_not_cars_X, flatten_not_cars_y = flatten_images()
    # train_X, train_y, test_X, test_y = split_data(flatten_cars_X, flatten_cars_y, flatten_not_cars_X, flatten_not_cars_y, split_ratio)

    # train_models(train_X, train_y, test_X, test_y)

    # layers = (16, 16, 16, 16, 16, 16, 16, 16, 16, 16)
    # alpha = 0.001
    # accuracy = test_model(train_X, train_y, test_X, test_y, layers, alpha, True)
    # print(accuracy)

    # load_and_test_model(test_X, test_y)

    car_image_file_names = ["6b6777a5-ff5c-4f11-9f1c-8a98ba75e2f4_car_0.jpg", "6b6777a5-ff5c-4f11-9f1c-8a98ba75e2f4_car_13.jpg", "047a3217-f379-48ee-80ee-d388aa3d48d2_car_16.jpg"]
    car_images = ["image_data/cropped_images/car/" + fn for fn in car_image_file_names]
    not_car_image_file_names = ["6b6777a5-ff5c-4f11-9f1c-8a98ba75e2f4_not_car_20.jpg", "35b4b453-f4c9-4e21-ab5d-2468927bd8cd_not_car_10.jpg", "35b4b453-f4c9-4e21-ab5d-2468927bd8cd_not_car_69.jpg"]
    not_car_images = ["image_data/cropped_images/not_car/" + fn for fn in not_car_image_file_names]
    images = car_images + not_car_images
    for i in images:
        classify_image(i)

if __name__ == "__main__":
    main()
