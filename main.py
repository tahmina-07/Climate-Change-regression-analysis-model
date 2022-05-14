#python libaray
import numpy as np 
import pylab 
import re 

#21 cities in our data.csv file 
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

#list of dates in data.csv file
INTERVAL_1 = list(range(1961, 2006))
INTERVAL_2 = list(range(2006, 2016))

class Climate(object):
    """This class contains tempture records loaded from data.cvs file"""
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        #dict for raw data
        self.rawdata = {}
        #read the file data.csv
        f = open(filename, 'r')
        #create heading 
        header = f.readline().strip().split(',')
        #iterate over the rest of the items 
        for line in f:
            item = line.strip().split(',')
            #store the complete date 
            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', item[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            #store a signle city 
            city = item[header.index('CITY')]
            #store the temperature 
            temperature = float(item[header.index('TEMP')])
            #checking if the data is in the file or not
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature 

        #close the file
        f.close()

    def get_yearly_temp(self, city, year):
         """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a numpy 1-d array of daily temperatures for the specified year and
            city
        """
        temperature = []
        #check if the city and year is in the data.cvs file 
        assert city in self.rawdata, "Provided city is not avaliable"
        assert year in self.rawdata[city], "Provided year is not avaliable"
        #adding the temperature for that city and year 
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperature.append(self.rawdata[city][year][month][day])
        return np.array(temperature)
    def get_daily_temp(self, city, month, year, day):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        #check if the city, month, year, day is in data.cvs file
        assert city in self.rawdata, "Provided city is not avaliable"
        assert year in self.rawdata[city], "Provided year is not avaliable"
        assert month in self.rawdata[city][year], "Provided month is not avaliable"
        assert day in self.rawdata[city][year][month], "Provided day is not avaliable"
        return self.rawdata[city][year][month][day]

#start of modeling the data 
#create numpy array of coefficiens to min the sum of squared errors 
def generate_models(x, y, degree):
     """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).
    Args:
        x: a list with length N, representing the x-coords of N sample points
        y: a list with length N, representing the y-coords of N sample points
        degs: a list of degrees of the fitting polynomial
    Returns:
        a list of numpy arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    model = []
    for degree in deg:
        model.append(np.polyfit(x, y, degree))
    return model 

#find the best fit using r^2 values 
def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    Args:
        y: list with length N, representing the y-coords of N sample points
        estimated: a list of values estimated by the regression model
    Returns:
        a float for the R-squared error term
    """
    numerator = 0
    denomenator = 0
    mean = sum(y) / len(y)
    for i in range(len(y)):
        numerator += (y[i] - estimated[i])**2
        denomenator += (y[i] - mean)**2
    return 1 - (numerator / denomenator)

#ploting
def evaluate_models_on_training(x, y, models):
    """
    Args:
        x: a list of length N, representing the x-coords of N sample points
        y: a list of length N, representing the y-coords of N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.
    Returns:
        None
    """
    xCoord = np.array(x)
    yCoord = np.array(y)

    for model in models:
        pylab.plot(xCoord, yCoord, 'bo', label = "Samples Data points")
        pylab.title("")
        pylab.xlabel("Year")
        pylab.ylabel("Temperature Celcuis")
        estVals = np.polyval(model, xCoord)
        Rsquared = r_squared(yCoord, estVals)
        pylab.plot(xCoord, yCoord, "r-", label = "R^2 = " + str(Rsquared))
        pylab.legend(loc = "best")
        pylab.show()

### Begining of program
raw_data = Climate('data.csv')


y = []
x = INTERVAL_1
for year in INTERVAL_1:
    y.append(raw_data.get_daily_temp('BOSTON', 1, 10, year))
models = generate_models(x, y, [1])
evaluate_models_on_training(x, y, models)




