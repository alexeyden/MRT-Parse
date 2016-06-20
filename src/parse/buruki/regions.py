import csv
import bisect
import heapq


class Regions:
    def __init__(self, csv_path):
        self.regions = dict()

        with open(csv_path, newline='') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            self.regions = {field:[] for field in reader.fieldnames}

            for row in reader:
                for field,value in row.items():
                    heapq.heappush(self.regions[field], value)

    def find(self, city):
        for region in self.regions.keys():
            cities = self.regions.get(region)
            i = bisect.bisect_left(cities, city)

            if i != len(cities) and cities[i] == city:
                return region

        return None