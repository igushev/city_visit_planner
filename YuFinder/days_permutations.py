import collections


def DaysPermutations(points, days_consider):
  # Deep copy of result except points.
  def _CopyResult(result):
    return collections.defaultdict(
        list, ((i, points[:]) for i, points in result.iteritems()))
    
  results = [collections.defaultdict(list)]
  for point in points:
    next_results = []
    for result in results:
      for i in range(len(days_consider)):
        if not days_consider[i]:
          continue
        next_result = _CopyResult(result)
        next_result[i].append(point)
        next_results.append(next_result)
    results = next_results
  return results