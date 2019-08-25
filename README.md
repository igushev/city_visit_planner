Table of Contents
=================

   * [Description](#description)
      * [Travel Service](#travel-service)
      * [Business model](#business-model)
      * [Library](#library)
      * [Testing](#testing)
      * [Further development](#further-development)
   * [Configuration](#configuration)
      * [Config](#config)
      * [Daily Parameters](#daily-parameters)
      * [General Parameters](#general-parameters)
   * [Running](#running)
      * [Defining Input Points](#defining-input-points)
      * [Running](#running-1)
      * [Result](#result)
   * [Examples](#examples)
      * [New York City - 3 day](#new-york-city---3-day)
      * [San Francisco - 3 day](#san-francisco---3-day)

# Description

## Travel Service

A travel service that by given dates, constraints and various parameters
chooses points of interests and activities and creates a schedule optimizing
time spent in given city. For example, family vacation with kids for three full
days in San Francisco, or, business trip with free evenings during one week in
New York City. Service would create an optimal and most efficient itinerary.

Interesting, that as of 2019, no such service still exists, which would be a
household name.

## Business model
* Reselling tickets for points of interests and activities;
* Advertising of businesses near user's trip (like restaurants);

## Library

This library was created as backend for the service. It can be deployed to the
cloud and an iOS/Android/Web application can send requests to it to provide
the service to its users.

Library approximates solution for [Travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem).

## Testing

Output and efficiently of trips were tested in New York City and San Francisco.

## Further development
The service is supposed to be interactive, for example, track user if they
follow the schedule and, if needed, adjust correspondently, for example, user
cannot make it to a museum, move the visit to next day and substitute with
something else. The service also should learn from user things, like speed of
walk, duration of lunch, etc.

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

`PTT` means "Public Transportation or Taxi".

The two day trip has been found. First day is mostly focused on must-see points of
interest in Midtown area, while second day is lower Manhattan.

Script with all snippets above can be found file `finder/runner_doc.py`

# Examples

## New York City - 3 day

Script to create a 3 day trip to New York City can be found in `finder/runner_nyc_1.py`.

Resulting trip is:
```
Your schedule:
Date: 2015-07-13
Walking from 40.7636:-73.9885 to 40.7587:-73.9787 from 10:00:00 to 10:25:58.080801
Visiting point "Rockefeller Center" from 10:25:58.080801 to 11:55:58.080801
Walking from 40.7587:-73.9787 to 40.7527:-73.9772 from 11:55:58.080801 to 12:13:50.395826
Visiting point "Grand Central Terminal" from 12:13:50.395826 to 13:43:50.395826
Walking from 40.7527:-73.9772 to 40.7517:-73.9753 from 13:43:50.395826 to 13:49:06.950449
Visiting point "Chrysler Building" from 13:49:06.950449 to 14:01:06.950449
Having lunch from 14:01:06.950449 to 15:01:06.950449
Walking from 40.7517:-73.9753 to 40.7503:-73.9883 from 15:01:06.950449 to 15:30:21.503593
Visiting point "Macy's Herald Square" from 15:30:21.503593 to 17:30:21.503593
Walking from 40.7503:-73.9883 to 40.7411:-73.9897 from 17:30:21.503593 to 17:57:32.933379
Visiting point "Flatiron Building" from 17:57:32.933379 to 18:09:32.933379
Using PTT from 40.7411:-73.9897 to 40.7636:-73.9885 from 18:09:32.933379 to 18:33:21.559684
Cost: 5.00
Price: 20.00
Date: 2015-07-14
Using PTT from 40.7636:-73.9885 to 40.7358:-74.0036 from 10:00:00 to 10:26:45.062003
Visiting point "West Village" from 10:26:45.062003 to 12:26:45.062003
Walking from 40.7358:-74.0036 to 40.7339:-74.0011 from 12:26:45.062003 to 12:34:32.015399
Visiting point "Greenwich Village" from 12:34:32.015399 to 14:34:32.015399
Having lunch from 14:34:32.015399 to 15:34:32.015399
Using PTT from 40.7339:-74.0011 to 40.7115:-74.0133 from 15:34:32.015399 to 15:59:00.475593
Visiting point "National September 11 Memorial And Museum" from 15:59:00.475593 to 16:59:00.475593
Walking from 40.7115:-74.0133 to 40.7056:-74.0134 from 16:59:00.475593 to 17:16:19.583403
Visiting point "Charging Bull" from 17:16:19.583403 to 17:22:19.583403
Using PTT from 40.7056:-74.0134 to 40.7577:-73.9857 from 17:22:19.583403 to 17:59:18.157762
Visiting point "Times Square" from 17:59:18.157762 to 18:41:18.157762
Walking from 40.7577:-73.9857 to 40.7636:-73.9885 from 18:41:18.157762 to 18:59:31.286249
Cost: 11.74
Price: 24.00
Date: 2015-07-15
Using PTT from 40.7636:-73.9885 to 40.7484:-73.9857 from 10:00:00 to 10:20:58.781754
Visiting point "Empire State Building" from 10:20:58.781754 to 13:20:58.781754
Using PTT from 40.7484:-73.9857 to 40.7630:-73.9740 from 13:20:58.781754 to 13:42:38.231343
Having lunch from 13:42:38.231343 to 14:42:38.231343
Visiting point "Fifth Avenue (Shopping)" from 14:42:38.231343 to 16:42:38.231343
Using PTT from 40.7630:-73.9740 to 40.7812:-73.9814 from 16:42:38.231343 to 17:05:06.510163
Visiting point "Broadway" from 17:05:06.510163 to 18:05:06.510163
Using PTT from 40.7812:-73.9814 to 40.7636:-73.9885 from 18:05:06.510163 to 18:27:19.060887
Cost: 11.23
Price: 32.00
Total cost: 87027.96
Total price: 76.00
```

## San Francisco - 3 day

Script to create a 3 day trip to New York City can be found in `finder/runner_sf_1.py`.

Resulting trip is:
```
Your schedule:
Date: 2015-07-01
Walking from 37.7881:-122.4075 to 37.7881:-122.4075 from 10:00:00 to 10:00:00
Visiting point "Union Square" from 10:00:00 to 11:00:00
Walking from 37.7881:-122.4075 to 37.7947:-122.4072 from 11:00:00 to 11:19:21.647349
Visiting point "China Town" from 11:19:21.647349 to 13:19:21.647349
Using PTT from 37.7947:-122.4072 to 37.7764:-122.4347 from 13:19:21.647349 to 13:45:27.977177
Having lunch from 13:45:27.977177 to 14:45:27.977177
Visiting point "Alamo Square" from 14:45:27.977177 to 15:45:27.977177
Using PTT from 37.7764:-122.4347 to 37.7516:-122.4477 from 15:45:27.977177 to 16:10:57.560841
Visiting point "Twin Peaks" from 16:10:57.560841 to 16:40:57.560841
Using PTT from 37.7516:-122.4477 to 37.7792:-122.4191 from 16:40:57.560841 to 17:09:54.301642
Visiting point "San Francisco City Hall" from 17:09:54.301642 to 18:39:54.301642
Using PTT from 37.7792:-122.4191 to 37.7881:-122.4075 from 18:39:54.301642 to 18:59:53.960923
Cost: 12.87
Price: 0.00
Date: 2015-07-02
Using PTT from 37.7881:-122.4075 to 37.8019:-122.4189 from 10:00:00 to 10:21:26.497490
Visiting point "Lombard Street" from 10:21:26.497490 to 10:51:26.497490
Using PTT from 37.8019:-122.4189 to 37.8100:-122.4104 from 10:51:26.497490 to 11:10:33.263750
Visiting point "Pier 39" from 11:10:33.263750 to 14:10:33.263750
Having lunch from 14:10:33.263750 to 15:10:33.263750
Walking from 37.8100:-122.4104 to 37.8025:-122.4058 from 15:10:33.263750 to 15:34:59.197464
Visiting point "Coit Tower" from 15:34:59.197464 to 16:34:59.197464
Using PTT from 37.8025:-122.4058 to 37.7955:-122.3937 from 16:34:59.197464 to 16:54:37.099985
Visiting point "Ferry Building" from 16:54:37.099985 to 17:54:37.099985
Walking from 37.7955:-122.3937 to 37.7937:-122.3961 from 17:54:37.099985 to 18:02:17.012584
Visiting point "Cable Car" from 18:02:17.012584 to 18:17:17.012584
Walking from 37.7850:-122.4072 to 37.7881:-122.4075 from 18:17:17.012584 to 18:26:23.875557
Cost: 8.54
Price: 14.00
Date: 2015-07-03
Walking from 37.7881:-122.4075 to 37.7956:-122.4075 from 10:00:00 to 10:21:59.203016
Visiting point "Cable Car Museum" from 10:21:59.203016 to 12:21:59.203016
Using PTT from 37.7956:-122.4075 to 37.8028:-122.4483 from 12:21:59.203016 to 12:49:53.906889
Visiting point "Palace of Fine Arts" from 12:49:53.906889 to 13:49:53.906889
Having lunch from 13:49:53.906889 to 14:49:53.906889
Using PTT from 37.8028:-122.4483 to 37.8197:-122.4786 from 14:49:53.906889 to 15:16:21.125200
Visiting point "Golden Gate Bridge" from 15:16:21.125200 to 15:46:21.125200
Using PTT from 37.8197:-122.4786 to 37.7932:-122.4840 from 15:46:21.125200 to 16:11:50.619571
Visiting point "Baker Beach" from 16:11:50.619571 to 17:11:50.619571
Using PTT from 37.7932:-122.4840 to 37.7786:-122.3892 from 17:11:50.619571 to 17:56:40.755743
Visiting point "Att Park" from 17:56:40.755743 to 18:26:40.755743
Using PTT from 37.7786:-122.3892 to 37.7881:-122.4075 from 18:26:40.755743 to 18:48:26.579609
Cost: 18.76
Price: 0.00
Total cost: 7040.18
Total price: 14.00
```
