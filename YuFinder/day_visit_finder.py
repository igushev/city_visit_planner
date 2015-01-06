from collections import namedtuple
import copy


PointsCalculator = namedtuple('PointsCalculator', 'Points Calculator')


# TODO(igushev): Use set instead of list for Points.
def FindDayVisit(all_points, day_visit_parameters, calculator_generator):
  """Find maximum number of point with minimum cost for a particular day."""
  points_calculator_queue = [
      PointsCalculator(all_points, calculator_generator.Generate(day_visit_parameters))]
  results = []
  while points_calculator_queue:
    next_points_calculator_queue = []
    for points, calculator in points_calculator_queue:
      for i, point in enumerate(points):
        next_calculator = copy.deepcopy(calculator)
        if (next_calculator.PushPoint(point) and next_calculator.CanFinalize()):
          next_points = points[:i] + points[i+1:]  # -= point
          if next_points:
            next_points_calculator_queue.append(
              PointsCalculator(next_points, next_calculator))
          else:
            results.append(next_calculator)
    # Keep record of previous step.
    prev_points_calculator_queue = points_calculator_queue
    points_calculator_queue = next_points_calculator_queue

  if results:
    # We can fit all points to the day at least with one combination.
    # Return the best.
    calculator_best = sorted(
        results, key=lambda calculator: calculator.FinalizedCost())[0]
    return [], calculator_best.FinalizedDayVisit()
  else:
    # We cannot fit all points to the day.
    # Return the best with the rest of points.
    assert len(prev_points_calculator_queue) >= 1
    points_left, calculator_best = (
        sorted(prev_points_calculator_queue,
               key=lambda points_calculator: (
                   points_calculator.Calculator.FinalizedCost()))[0])
    return points_left, calculator_best.FinalizedDayVisit()
