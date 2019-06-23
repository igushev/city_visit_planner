# Description

The library was created for a travel service. Idea of travel service is that by
given days, constraints and various parameters chooses points of interests and
activities and optimizes time spent in given city. For example, family vacation
with kids for three full days in San Francisco, or, business trip with free
evening during one week in New York City. Service would create an optimal and
most efficient itinerary.  

Library approximates solution for [Travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem).

# Configuration

## Config
* `cost_accumulator_generator`. Various parameters which define cost of given
activity (driving, walking, waiting, etc.). Algorithm tries to minimize cost. 
* `day_visit_const_calculator_generator`. Various parameters which define users behaviour.
* `city_visit_router`. Various parameters which define algorithm behaviour. Please contact us for more details.

Following snippet can be used to load default config:
```python
import os
from config import config as config_
config = config_.GetConfig(os.path.join('config', 'runner.config'))
```

## Daily Parameters

Define a list of `DayVisitParameters` objects for each day of a trip.
`DayVisitParameters` has following arguments:
* `start_datetime`: (`datetime.datetime`) Beginning of the day.
* `end_datetime`: (`datetime.datetime`) End of the day.
* `lunch_start_datetime`: (`datetime.datetime`) Beginning of lunch.
* `lunch_hours`: (`float`) Duration of lunch in hours.
* `start_coordinates`: (`Coordinates`) Where day starts (hotel, office).
* `end_coordinates`: (`Coordinates`) Where day ends (hotel, specific location).

Following snippet shows an examples of defining such object:
```python
import datetime
from data import city_visit
from data import point

start_end_coordinates = point.Coordinates(40.763582, -73.988470)

day1 = city_visit.DayVisitParameters(
    start_datetime=datetime.datetime(2019, 7, 1, 10, 0, 0),
    end_datetime=datetime.datetime(2019, 7, 1, 19, 0, 0),
    lunch_start_datetime=datetime.datetime(2019, 7, 1, 14, 0, 0),
    lunch_hours=1.,
    start_coordinates=start_end_coordinates,
    end_coordinates=start_end_coordinates)

day2 = city_visit.DayVisitParameters(
    start_datetime=datetime.datetime(2019, 7, 2, 10, 0, 0),
    end_datetime=datetime.datetime(2019, 7, 2, 17, 0, 0),
    lunch_start_datetime=datetime.datetime(2019, 7, 1, 14, 0, 0),
    lunch_hours=1.,
    start_coordinates=start_end_coordinates,
    end_coordinates=start_end_coordinates)
```

## General Parameters

Define a `CityVisitParameters` object.
`CityVisitParameters` has following arguments:
* `visit_location`: (`VisitLocation`). General location parameters like name. The name might be used to retrieve points
from database.
* `day_visit_parameterss`: (`list(DayVisitParameters)`) List of `DayVisitParameters` objects described above.
* `point_type`: (`PointType`) For each type of a point (city_tours, landmarks, nature, museums,
shopping, dining) specifies a number from 0 to 100 how important this type to the user.
* `age_group:` (`AgeGroup`) For each age group (senior, adult, junior, child, toddlers) specifies
a number from 0 to 100 how tailored trip should be to the age group.

Following snippet shows an examples of defining such object:
```python
from data import city_visit
from data import point

visit_location = city_visit.VisitLocation('New York City')

parameters_point_types = point.PointType(
  city_tours=90,
  landmarks=90,
  nature=10,
  museums=10,
  shopping=50,
  dining=50)

parameters_age_groups = point.AgeGroup(
  senior=None,
  adult=90,
  junior=None,
  child=None,
  toddlers=10)

city_visit_parameters = city_visit.CityVisitParameters(
  visit_location=visit_location,
  day_visit_parameterss=[day1, day2],
  point_type=parameters_point_types,
  age_group=parameters_age_groups)
```

# Running

## Defining Input Points

Define a list of `Point` objects. Each `Point` represents point of interest or activity (city_tours, landmarks, nature,
museums, shopping, dining). Order in the list does not matter.

Following snippet loads list of `Point` from CSV file:
```python
from data import test_util as point_test_util
points_input = list(point_test_util.GetPointsInput('data', 'test_nyc_1.csv').values())
```

## Running

To run the algorithm, one needs to create a `CityVisitFinder` object and helper objects. 

Following snippet can be used to run the algorithm:
```python
from config import config as config_
city_visit_finder = config_.GetCityVisitFinder(config)
city_visit_accumulator_generator = config_.GetCityVisitAccumulatorGenerator(config)
city_visit = city_visit_finder.FindCityVisit(points_input, city_visit_parameters, city_visit_accumulator_generator)
```

## Result

Result of runnig the algorithm is `CityVisit` which represents entire trip and
has list of `DayVisit` objects which represents individual days.

`CityVisit` object can be printed to console:
```python
print('Your schedule:')
print(city_visit)
```

It would print:
```
Your schedule:
Date: 2019-07-01
Walking from 40.7636:-73.9885 to 40.7587:-73.9787 from 10:00:00 to 10:25:58.080801
Visiting point "Rockefeller Center" from 10:25:58.080801 to 11:55:58.080801
Walking from 40.7587:-73.9787 to 40.7527:-73.9772 from 11:55:58.080801 to 12:13:50.395826
Visiting point "Grand Central Terminal" from 12:13:50.395826 to 13:43:50.395826
Walking from 40.7527:-73.9772 to 40.7517:-73.9753 from 13:43:50.395826 to 13:49:06.950449
Visiting point "Chrysler Building" from 13:49:06.950449 to 14:01:06.950449
Having lunch from 14:01:06.950449 to 15:01:06.950449
Walking from 40.7517:-73.9753 to 40.7503:-73.9883 from 15:01:06.950449 to 15:30:21.503593
Visiting point "Macy's Herald Square" from 15:30:21.503593 to 17:30:21.503593
Walking from 40.7503:-73.9883 to 40.7577:-73.9857 from 17:30:21.503593 to 17:52:58.126602
Visiting point "Times Square" from 17:52:58.126602 to 18:34:58.126602
Walking from 40.7577:-73.9857 to 40.7636:-73.9885 from 18:34:58.126602 to 18:53:11.255089
Cost: 2.05
Price: 20.00
Date: 2019-07-02
Using PTT from 40.7636:-73.9885 to 40.7358:-74.0036 from 10:00:00 to 10:26:45.062003
Visiting point "West Village" from 10:26:45.062003 to 12:26:45.062003
Walking from 40.7358:-74.0036 to 40.7339:-74.0011 from 12:26:45.062003 to 12:34:32.015399
Visiting point "Greenwich Village" from 12:34:32.015399 to 14:34:32.015399
Using PTT from 40.7339:-74.0011 to 40.7056:-74.0134 from 14:34:32.015399 to 15:01:11.148649
Visiting point "Charging Bull" from 15:01:11.148649 to 15:07:11.148649
Using PTT from 40.7056:-74.0134 to 40.7411:-73.9897 from 15:07:11.148649 to 15:37:44.058580
Visiting point "Flatiron Building" from 15:37:44.058580 to 15:49:44.058580
Using PTT from 40.7411:-73.9897 to 40.7636:-73.9885 from 15:49:44.058580 to 16:13:32.684885
Cost: 14.05
Price: 0.00
Total cost: 91016.10
Total price: 20.00
```

The two day trip has been found. First day is mostly focused on must-see points of
interest in Midtown area, while second day is lower Manhattan.

# Examples

Two more examples can be found in following scripts:
* `finder/runner_nyc_1.py` - 3 day trip in New York City;
*  `finder/runner_sf_1.py` - 3 day trip in San Francisco.

All snippets above formed as script can be found in file `finder/runner_doc.py`