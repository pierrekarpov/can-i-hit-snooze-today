from os import listdir
from os.path import isfile, join
import csv
from PIL import Image, ImageDraw
import numpy as np
from car_detection import flatten_image
from count_clusters import count_clusters
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

def get_window(img, x=0, y=0, size=64, out_size=32):
    area = (x, y, x + size, y + size)
    cropped_img = img.crop(area)
    s = (out_size, out_size)

    resized_cropped_img = cropped_img.resize(s, Image.ANTIALIAS)

    return resized_cropped_img

def classify_window(img, x, y, size, out_size=32):
    window_image = get_window(img, x=x, y=y, size=size, out_size=out_size)
    np_flat, _ = flatten_image(window_image)
    clf = joblib.load('./image_data/models/car_detection_nn_model.pkl')
    pred = clf.predict(np_flat)

    return pred == [1]

def process_image(img, size=32, x_delta=4, y_delta=4, is_save=False):
    print("Processing image..")
    x_windows_count = int((img.size[0] - size) / x_delta)
    y_windows_count = int((img.size[1] - size) / y_delta)

    squares = []
    for yc in range(y_windows_count):
        for xc in range(x_windows_count):
            x = xc * x_delta
            y = yc * y_delta
            pred = classify_window(img, x, y, size, out_size=32)

            if pred:
                squares.append((x, y, size))

    if is_save:
        with open('./image_data/tmp_files/sliding_doors_squares3.csv', 'w') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for s in squares:
                datawriter.writerow(s)
    print("DONE")
    return squares


def show_boxes(img, squares):
    draw = ImageDraw.Draw(img)
    for (x, y, size) in squares:
        draw.line((x, y, x + size, y), fill="blue")
        draw.line((x, y, x, y + size), fill="blue")
        draw.line((x + size, y, x + size, y + size), fill="blue")
        draw.line((x, y + size, x + size, y + size), fill="blue")
    img.show()

def load_squares():
    squares = []

    with open('./image_data/tmp_files/sliding_doors_squares3.csv', 'r') as csvfile:
        datareader = csv.reader(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for d in datareader:
            s = tuple([int(el) for el in d])
            squares.append(s)

    return squares

def get_freq_map(img, squares):
    freq_array = np.zeros((img.size[1], img.size[0]))
    for (x, y, size) in squares:
        for y0 in range(y, y + size):
            for x0 in range(x, x + size):
                freq_array[y0][x0] = freq_array[y0][x0] + 1
    return freq_array

def show_freq_array(img, freq_array):
    freq_max = np.amax(freq_array)
    img2 = Image.new('RGB', img.size, "black")
    pixels2 = img2.load()

    for (j, row) in enumerate(freq_array):
        for (i, el) in enumerate(row):
            intensity = 0
            if el != 0:
                intensity = int((el * 105.0 / freq_max) + 150)
            pixels2[i, j] = (intensity, intensity, intensity)

    img2.show()

def slide_through_image(path="image_data/images/2018/08/1e0c1720-759d-4113-b3d2-e9257e020ae2.jpg", size=32, x_delta=4, y_delta=4, load_from_file=False, is_save=False):
    img = Image.open(path)
    squares = []

    if not load_from_file:
        squares = process_image(img, size=size, x_delta=x_delta, y_delta=y_delta, is_save=is_save)
    else:
        print("Loading squares from file")
        squares = load_squares()

    show_boxes(img, squares)
    num_clusters = count_clusters(img, squares, False)
    return num_clusters

if __name__ == "__main__":
    # num_clusters = slide_through_image(path="image_data/images/2018/08/b2433425-a3fa-4c05-b720-ce8c966df0fa.jpg", load_from_file=True) # tmp file number 3
    num_clusters = slide_through_image(path="image_data/images/2018/08/35b4b453-f4c9-4e21-ab5d-2468927bd8cd.jpg", load_from_file=False, is_save=False)
    print("Found %d clusters" %(num_clusters))
