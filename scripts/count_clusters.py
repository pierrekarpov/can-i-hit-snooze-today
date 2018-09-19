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
    img2 = Image.new('RGB', img.size, "black") # Create a new black image
    pixels2 = img2.load() # Create the pixel map

    for (j, row) in enumerate(freq_array):
        for (i, el) in enumerate(row):
            intensity = 0
            if el > 0:
                intensity = int((el * 105.0 / freq_max) + 150)
            pixels2[i, j] = (intensity, intensity, intensity)

    img2.show()

def color_neighbors(freq_array, i, j, i_max, j_max, threshold=0):
    scan_i = i
    scan_j = j
    neighbors = []
    colored_neighbors = []
    did_find_neighborhood = False

    freq_array[j, i] = -1
    colored_neighbors.append((scan_j, scan_i))

    if scan_i - 1 >= 0 and freq_array[scan_j, scan_i - 1] > threshold:
        neighbors.append((scan_j, scan_i - 1))
    if scan_i + 1 < i_max and freq_array[scan_j, scan_i + 1] > threshold:
        neighbors.append((scan_j, scan_i + 1))
    if scan_j - 1 >= 0 and freq_array[scan_j - 1, scan_i] > threshold:
        neighbors.append((scan_j - 1, scan_i))
    if scan_j + 1 < j_max and freq_array[scan_j + 1, scan_i] > threshold:
        neighbors.append((scan_j + 1, scan_i))

    count = i_max * j_max * 100
    while len(neighbors) != 0 and count > 0:
        (scan_j, scan_i) = neighbors.pop()
        freq_array[scan_j, scan_i] = -1
        colored_neighbors.append((scan_j, scan_i))

        if scan_i - 1 >= 0 and freq_array[scan_j, scan_i - 1] > threshold and (scan_j, scan_i - 1) not in neighbors:
            neighbors.append((scan_j, scan_i - 1))
        if scan_i + 1 < i_max and freq_array[scan_j, scan_i + 1] > threshold and (scan_j, scan_i + 1) not in neighbors:
            neighbors.append((scan_j, scan_i + 1))
        if scan_j - 1 >= 0 and freq_array[scan_j - 1, scan_i] > threshold and (scan_j - 1, scan_i) not in neighbors:
            neighbors.append((scan_j - 1, scan_i))
        if scan_j + 1 < j_max and freq_array[scan_j + 1, scan_i] > threshold and (scan_j + 1, scan_i) not in neighbors:
            neighbors.append((scan_j + 1, scan_i))

    did_find_neighborhood = len(colored_neighbors) > 0

    return freq_array, did_find_neighborhood

def remove_neighborhood(freq_array):
    for (j, row) in enumerate(freq_array):
        for (i, el) in enumerate(row):
            if el < 0:
                freq_array[j, i] = 0
    return freq_array

def color_clusters(img, freq_array, is_show_imgs=False, threshold_ratio=0.29):
    num_clusters = 0
    freq_max = np.amax(freq_array)
    threshold = int(freq_max * threshold_ratio)

    for (j, row) in enumerate(freq_array):
        for (i, el) in enumerate(row):
            if el > threshold:
                freq_array, did_find_cluster = color_neighbors(freq_array, i, j, img.size[0], img.size[1], threshold)
                if did_find_cluster:
                    if is_show_imgs:
                        show_colored_clusters(img, freq_array)
                    freq_array = remove_neighborhood(freq_array)
                    if is_show_imgs:
                        show_colored_clusters(img, freq_array)
                    num_clusters = num_clusters + 1

    return freq_array, num_clusters

def show_colored_clusters(img, freq_array):
    img2 = Image.new('RGB', img.size, "black")
    pixels2 = img2.load()

    for (j, row) in enumerate(freq_array):
        for (i, el) in enumerate(row):
            if el > 0:
                pixels2[i, j] = (255, 255, 255)
            elif el < 0:
                pixels2[i, j] = (255, 0, 0)
            else:
                pixels2[i, j] = (0, 0, 0)

    img2.show()

def count_clusters(img, squares, is_show_imgs=False):
    freq_array = get_freq_map(img, squares)
    if is_show_imgs:
        show_freq_array(img, freq_array)
    freq_array, num_clusters = color_clusters(img, freq_array, is_show_imgs)
    return num_clusters

def main(path="./image_data/images/2018/08/1e0c1720-759d-4113-b3d2-e9257e020ae2.jpg", is_show_imgs=False):
    img = Image.open(path)
    if is_show_imgs:
        img.show()
    squares = load_squares()
    num_clusters = count_clusters(img, squares, True)
    print("Found %d clusters" %(num_clusters))


if __name__ == "__main__":
    print("Counting clusters")
    main()
