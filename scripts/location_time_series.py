import json
import csv
import requests
from dateutil.parser import parse
import os.path
from sliding_doors import slide_through_image

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
    num_cars = slide_through_image(path=img_path)
    if num_cars < 20:
        print("You can sleep in")
    else:
        print("Wakey wakey, need to go to work :)")
    print(num_cars)

#6703 is PIE x Thomson
def main(camera_id="6703", year="2018", month="09" , day="19", hour="09", minute="00", second="00", tz_hour="08", tz_minute="00"):
    # time_stamp = "2018-09-19T17:41:16+08:00"
    # time_stamp = "%s-%s-%sT%s%3A%s%3A%s%2B%s%3A%s" %(year, month, day, hour, minute, second, tz_hour, tz_minute)
    time_stamp = "2018-09-18T09%3A00%3A00%2B08%3A00"
    # print(time_stamp)
    get_traffic_camera_image(time_stamp, camera_id)

if __name__ == "__main__":
    print("Building time series for your location")
    main()
