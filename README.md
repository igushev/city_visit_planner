# Description

Idea of travel service is that by given days, constraints and various parameters
chooses points of interests and activities and optimizes time spent in given
city. For example, family vacation with kids for three full days in
San Francisco, or, business trip with free evening during one week in
New York City. Service would create an optimal and most efficient itinerary.  

Library approximates solution for [Travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem).

# Configuration

## Config
* `cost_accumulator_generator`. Various parameters which define cost of given
activity (driving, walking, waiting, etc.). Algorithm tries to minimize cost. 
* `day_visit_const_calculator_generator`. Various parameters which define users behaviour.
* `city_visit_router`. Various parameters which define algorithm behaviour. Please contact us for more details.

Following snippet can be used to load default config:
```
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

# Running

## Defining Input Points

Define a list of `Point` objects. Each `Point` represents point of interest or activity (city_tours, landmarks, nature,
museums, shopping, dining). Order in the list does not matter.

## Running

Following snippet can be used to run the algorithm:
```
city_visit_finder = config_.GetCityVisitFinder(config)
city_visit_accumulator_generator = config_.GetCityVisitAccumulatorGenerator(config)
city_visit = self.city_visit_finder.FindCityVisit(points_input, city_visit_parameters, city_visit_accumulator_generator)
```