import csv
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans
import numpy as np

def load_squares():
    squares = []

    with open('./image_data/tmp_files/sliding_doors_squares.csv', 'r') as csvfile:
        datareader = csv.reader(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for d in datareader:
            # print(tuple(d))
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
    img2 = Image.new( 'RGB', img.size, "black") # Create a new black image
    pixels2 = img2.load() # Create the pixel map

    for (j, row) in enumerate(freq_array):
        for (i, el) in enumerate(row):
            intensity = 0
            if el != 0:
                intensity = int((el * 105.0 / freq_max) + 150)
            pixels2[i,j] = (intensity, intensity, intensity)

    img2.show()

def prep_cluster_data(freq_array):
    cluster_data = []
    for (j, row) in enumerate(freq_array):
        for (i, el) in enumerate(row):
            for _ in range(int(el)):
                cluster_data.append((i, j))

    return cluster_data


def knn(cluster_data):
    X = np.array(cluster_data)

    min_inertia = 1000000000000000
    clusters = []
    for i in range(20):
        kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
        if kmeans.inertia_ < min_inertia:
            min_inertia = kmeans.inertia_
            clusters = kmeans.cluster_centers_


    # print(kmeans.cluster_centers_)
    # print(kmeans.inertia_)

    return clusters

def show_clusters(img, clusters):
    draw = ImageDraw.Draw(img)

    for x, y in clusters:
        offset = 5
        draw.ellipse((x - offset, y - offset, x + offset, y + offset), fill = 'blue', outline ='blue')

    img.show()

def count_clusters(img, squares):
    freq_array = get_freq_map(img, squares)
    show_freq_array(img, freq_array)

    cluster_data = prep_cluster_data(freq_array)
    clusters = knn(cluster_data)

    show_clusters(img, clusters)

def main(path="./image_data/images/2018/08/1e0c1720-759d-4113-b3d2-e9257e020ae2.jpg"):
    img = Image.open(path)
    print(img.size)
    squares = load_squares()
    count_clusters(img, squares)

if __name__ == "__main__":
    print("knn")
    main()
