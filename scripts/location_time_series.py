import json
import csv
import os.path
from dateutil.parser import parse
import requests
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from sliding_doors import slide_through_image
from time_series_prediction import make_predictions

def get_traffic_camera_api_data(date=None):
    res = {}
    api_url = "https://api.data.gov.sg/v1/transport/traffic-images"
    params = {
        "accept": "application/json"
    }
    date_param_str = ""
    if date is not None:
        date_param_str = "?date_time=" + date

    r = requests.get(api_url + date_param_str, params=params)
    res = r.json()

    return res

def get_image_link(cameras_data, selected_camera_id):
    camera_image_links = []

    for i_idx, i in enumerate(cameras_data["items"]):
        for c_idx, c in enumerate(i["cameras"]):
            c_id = cameras_data["items"][i_idx]["cameras"][c_idx]["camera_id"]
            if c_id == selected_camera_id:
                c_img = cameras_data["items"][i_idx]["cameras"][c_idx]["image"]
                c_time = cameras_data["items"][i_idx]["cameras"][c_idx]["timestamp"]
                camera_image_links.append((c_img, c_time))

    res = ("", "")
    if len(camera_image_links) == 0:
        print("No data for camera %s at that time" %(selected_camera_id))
    else:
        res = camera_image_links[0]

    return res

def get_image_path(img_link, img_timestamp, camera_id):
    d = parse(img_timestamp)
    file_name = d.strftime("%Y_%m_%d_T_%H_%M_%S") + ".jpg"
    path = "image_data/camera_images_time_series/%s/%s" %(camera_id, file_name)

    if not os.path.exists("image_data/camera_images_time_series/" + camera_id):
        os.makedirs("image_data/camera_images_time_series/" + camera_id)

    if not os.path.exists(path):
        print("Dowloading image %s and saving it as %s" %(img_link, file_name))
        r = requests.get(img_link, allow_redirects=True)
        with open(path, 'wb') as f:
            f.write(r.content)
    else:
        print("Loading image %s" %(file_name))

    return path

def get_traffic_camera_image(time_stamp, camera_id):
    traffic_camera_data = get_traffic_camera_api_data(time_stamp)
    img_link, img_timestamp = get_image_link(traffic_camera_data, camera_id)
    img_path = get_image_path(img_link, img_timestamp, camera_id)

    return img_path

def load_num_car(camera_id, year, month, day, hour, minute, second):
    num_cars = -1
    dt_val = "%s_%s_%sT%s:%s:%s" %(year, month, day, hour, minute, second)
    file_path = "image_data/camera_images_time_series/%s/time_series.csv" %(camera_id)
    if os.path.exists(file_path):
        with open(file_path, 'r') as csvfile:
            datareader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for dt, count in datareader:
                if dt == dt_val:
                    num_cars = int(count)
    return num_cars

def save_num_car(num_car, camera_id, year, month, day, hour, minute, second):
    dt_val = "%s_%s_%sT%s:%s:%s" %(year, month, day, hour, minute, second)
    file_path = "image_data/camera_images_time_series/%s/time_series.csv" %(camera_id)
    with open(file_path, 'a+') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow([dt_val, num_car])

def get_num_cars_for_traffic_camera(camera_id="6703", year="2018", month="09" , day="24", hour="09", minute="00", second="00", tz_hour="08", tz_minute="00"):
    num_cars = load_num_car(camera_id, year, month, day, hour, minute, second)
    if num_cars == -1:
        time_stamp = year + "-" + month + "-" + day + "T" + hour + "%3A" + minute + "%3A" + second + "%2B" + tz_hour + "%3A" + tz_minute
        img_path = get_traffic_camera_image(time_stamp, camera_id)
        num_cars = slide_through_image(path=img_path, is_show_imgs=False)
        save_num_car(num_cars, camera_id, year, month, day, hour, minute, second)

    return num_cars

def get_data_for_period(start_date_str="2018-09-24", end_date_str="2018-09-26"):
    data = {}

    start_date = parse(start_date_str)
    end_date = parse(end_date_str)

    diff = (end_date - start_date).days + 1
    for i in range(diff):
        delta = relativedelta(days=+i)
        dt = start_date + delta
        date_str = dt.strftime("%Y_%m_%d")
        month = dt.strftime("%m")
        day = dt.strftime("%d")
        num_cars = get_num_cars_for_traffic_camera(month=month, day=day)

        data[date_str] = num_cars

    return data

def plot_time_series(time_series):
    sorted_datetimes = sorted(time_series.keys())
    sorted_num_cars = [time_series[dt] for dt in sorted_datetimes]

    plt.plot(sorted_datetimes, sorted_num_cars)
    plt.xticks(rotation=-45)
    plt.show()

def predict(time_series):
    prediction = make_predictions()
    print("predicting: %f" %(prediction))
    return prediction

#6703 is PIE x Thomson
#6701 is PIE x CTE
def main():
    time_series = get_data_for_period()
    # plot_time_series(time_series)
    prediction = predict(time_series)
    if prediction < 20:
        print("You can sleep in")
    else:
        print("Wakey wakey, need to go to work :)")

if __name__ == "__main__":
    print("Building time series")
    main()
