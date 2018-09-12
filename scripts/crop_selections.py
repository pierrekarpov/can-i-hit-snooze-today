from PIL import Image
from os import listdir
from os.path import isfile, join
import csv
from time import time

def crop(data, in_file_path, out_file_path, out_size=32, rewrite=False):
    if not rewrite and isfile(out_file_path):
        return 0

    x, y, size = [int(d) for d in data]
    img = Image.open(in_file_path)
    area = (x - size, y - size, x + size, y + size)
    cropped_img = img.crop(area)

    s = (out_size, out_size)
    cropped_img.thumbnail(s, Image.ANTIALIAS)
    cropped_img.save(out_file_path)
    return 1


def process_file(file_name):
    written_pics_per_file = 0
    file_path = "image_data/image_selections/" + file_name + ".jpg.csv"
    with open(file_path, 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        cars_idx = 0
        not_cars_idx = 0
        for d in datareader:
            in_file_path = "image_data/images/2018/08/" + file_name + ".jpg"
            out_file_path = "image_data/cropped_images"

            if d[0] == "1":
                out_file_path = out_file_path + "/car/" + file_name + "_car_" + str(cars_idx) + ".jpg"
                cars_idx = cars_idx + 1
            else:
                out_file_path = out_file_path + "/not_car/" + file_name + "_not_car_" + str(not_cars_idx) + ".jpg"
                not_cars_idx = not_cars_idx + 1

            pic_written = crop(d[1:], in_file_path, out_file_path)
            written_pics_per_file = written_pics_per_file + pic_written
    return written_pics_per_file

def generate_selections():
    written_files = 0
    image_selection_files = [f for f in listdir("./image_data/image_selections") if isfile(join("./image_data/image_selections", f))]
    for f in image_selection_files:
        file_name = f.split(".")[0]
        written_pics_per_file = process_file(file_name)
        written_files = written_files + written_pics_per_file
    return written_files

def count_cropped_files():
    car_files = [f for f in listdir("./image_data/cropped_images/car") if isfile(join("./image_data/cropped_images/car", f))]
    not_car_files = [f for f in listdir("./image_data/cropped_images/not_car") if isfile(join("./image_data/cropped_images/not_car", f))]
    return len(car_files), len(not_car_files)

if __name__ == "__main__":
    t0 = time()
    written_files = generate_selections()
    t1 = time()

    print  "Wrote %d cropped selections in %f s" %(written_files, (t1 - t0))
    cs, ncs = count_cropped_files()
    print "There are %d cars and %d not cars cropped selections" %(cs, ncs)
