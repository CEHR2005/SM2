from selenium import webdriver
import csv
from statistics import mean
from tabulate import tabulate
import json

def measure_load_time(url, number_of_measurements):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-cache')  # Disable cache
    detailed_results = []
    summary_results = []

    for _ in range(number_of_measurements):
        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
            navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
            load_event_end = driver.execute_script("return window.performance.timing.loadEventEnd")
            load_time = (load_event_end - navigation_start) / 1000  # Convert to seconds
            summary_results.append(load_time)

            resources = driver.execute_script("return window.performance.getEntriesByType('resource');")
            resources_data = [{'name': r['name'], 'duration': r['duration']} for r in resources]
            detailed_results.append({'test_number': _ + 1, 'load_time': load_time, 'resources': resources_data})

    return summary_results, detailed_results

def write_to_csv(data, filename, headers):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)

def write_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def prepare_summary_data(summary_results):
    return [[f"Test {i+1}", lt] for i, lt in enumerate(summary_results)] + [["Average", mean(summary_results)]]

URL = 'https://en.wikipedia.org/wiki/Software_metric'
TIMES = 10

# Measure load times
summary_results, detailed_results = measure_load_time(URL, TIMES)

# Writing summary results to CSV and JSON
summary_csv_filename = 'summary_load_times.csv'
summary_json_filename = 'summary_load_times.json'
summary_data = prepare_summary_data(summary_results)
write_to_csv(summary_data, summary_csv_filename, ["Measurement", "Load Time (seconds)"])
write_to_json(summary_results, summary_json_filename)

# Writing detailed results to CSV and JSON
detailed_csv_data = [(test['test_number'], test['load_time'], r['name'], r['duration'])
                     for test in detailed_results for r in test['resources']]
detailed_csv_filename = 'detailed_resource_load_times.csv'
detailed_json_filename = 'detailed_resource_load_times.json'
write_to_csv(detailed_csv_data, detailed_csv_filename, ["Test Number", "Load Time (seconds)", "Resource Name", "Duration (ms)"])
write_to_json(detailed_results, detailed_json_filename)

# Print summary load times table
print_table = [["Measurement", "Load Time (seconds)"]] + [[f"Test {i+1}", lt] for i, lt in enumerate(summary_results)]
print_table.append(["Average", mean(summary_results)])
print(tabulate(print_table, headers="firstrow", tablefmt="grid"))
