import csv
from pandas import read_csv
from pandas import datetime
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot
from sklearn.metrics import mean_squared_error

def format_time_series(path="image_data/camera_images_time_series/6703/"):
    in_file_path = path + "time_series.csv"
    out_file_path = path + "time_series_formatted.csv"
    data = []
    with open(in_file_path, 'r') as csvfile:
        datareader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for dt, count in datareader:
            data.append((dt, count))
    sorted_data = sorted(data, key=lambda o: o[0])
    with open(out_file_path, 'w') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(["\"timestamp\"", "\"Number of cars\""])
        for sd in sorted_data:
            datawriter.writerow(["\"" + sd[0] + "\"", sd[1]])

def parser(x):
    return datetime.strptime(x, '%Y_%m_%dT%H:%M:%S')


def test_time_series(size_to_test=5):
    series = read_csv('image_data/camera_images_time_series/6703/time_series_formatted.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
    X = series.values
    size = len(X) - size_to_test
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
    	model = ARIMA(history, order=(5,1,0))
    	model_fit = model.fit(disp=0)
    	output = model_fit.forecast()
    	yhat = output[0]
    	predictions.append(yhat)
    	obs = test[t]
    	history.append(obs)
    	print('predicted=%f, expected=%f' % (yhat, obs))
    error = mean_squared_error(test, predictions)

    print('Test MSE: %.3f' % error)
    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    pyplot.show()

def make_predictions():
    format_time_series()
    series = read_csv('image_data/camera_images_time_series/6703/time_series_formatted.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
    X = series.values
    model = ARIMA(X, order=(5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    return output[0][0]

if __name__ == "__main__":
    # format_time_series()
    # test_time_series()
    prediction = make_predictions()
