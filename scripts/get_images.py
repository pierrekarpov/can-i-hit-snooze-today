import json
import csv
import requests
import os.path

def get_camera_data(data):
    file_path = "image_data/camera_locations.csv"
    indices_to_add = []
    with open(file_path, 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        camera_ids = [r[0] for r in datareader]
        for i_idx, i in enumerate(data["items"]):
            for c_idx, c in enumerate(i["cameras"]):
                if c["camera_id"] not in camera_ids and (i_idx, c_idx) not in indices_to_add:
                    indices_to_add.append((i_idx, c_idx))


    if len(indices_to_add):
        with open(file_path, 'a') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for (i_idx, c_idx) in indices_to_add:
                c_id = data["items"][i_idx]["cameras"][c_idx]["camera_id"]
                c_lat = data["items"][i_idx]["cameras"][c_idx]["location"]["latitude"]
                c_lon = data["items"][i_idx]["cameras"][c_idx]["location"]["longitude"]
                print "Writing ", c_id, c_lat, c_lon
                datawriter.writerow([c_id, c_lat, c_lon])

def get_image_data(data):
    file_path = "image_data/image_links.csv"
    data_to_add = []
    with open(file_path, 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        img_links = [r[2] for r in datareader]
        for i_idx, i in enumerate(data["items"]):
            for c_idx, c in enumerate(i["cameras"]):
                if c["image"] not in img_links:
                    c_id = data["items"][i_idx]["cameras"][c_idx]["camera_id"]
                    c_time = data["items"][i_idx]["cameras"][c_idx]["timestamp"]
                    c_img = data["items"][i_idx]["cameras"][c_idx]["image"]

                    data_to_add.append([c_id, c_time, c_img])

    if len(data_to_add):
        with open(file_path, 'a') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for d in data_to_add:
                print "Writing ", d
                datawriter.writerow(d)

def parse_response(res):
    get_camera_data(res)
    get_image_data(res)
    # print json.dumps(res, indent=4, sort_keys=True)
    # for k in res["items"][0]["cameras"][0]:
    #     print k, res["items"][0]["cameras"][0][k]

def make_request(date=None, is_load=False):
    res = {}
    response_file_name = "image_data/api_response_sample.json"

    if not is_load:
        params = {
            "accept": "application/json"
        }
        date_param_str = ""
        if date is not None:
            date_param_str = "?date_time=" + date

        r = requests.get("https://api.data.gov.sg/v1/transport/traffic-images" + date_param_str, params=params)
        res = r.json()

        with open(response_file_name, "w") as f:
            json.dump(res, f, indent=4)
    else:
        with open(response_file_name, 'r') as fp:
            res = json.load(fp)
    return res

def get_images():
    image_links_file_path = "image_data/image_links.csv"
    with open(image_links_file_path, 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        img_urls = [r[-1] for r in datareader]

        for url in img_urls:
            url_parts = url.split('/')
            file_name = url_parts[-1]
            month = url_parts[-2]
            year = url_parts[-3]
            file_path = "image_data/images/" + year + "/" + month + "/" + file_name
            if not os.path.exists(file_path):
                if not os.path.exists("image_data/images/" + year):
                    os.makedirs("image_data/images/" + year)
                if not os.path.exists("image_data/images/" + year + "/" + month):
                    os.makedirs("image_data/images/" + year + "/" + month)

                print "Need to add file ", file_path
                r = requests.get(url, allow_redirects=True)
                open(file_path, 'wb').write(r.content)

if __name__ == "__main__":
    is_generate_csv_file = True
    is_load_from_api = True
    timestamp = "2018-08-27T09%3A00%3A00%2B08%3A00"

    if is_generate_csv_file:
        json_resonse = make_request(timestamp, is_load_from_api)
        parse_response(json_resonse)

    get_images()
