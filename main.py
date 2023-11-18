from selenium import webdriver
import json
import csv


def measure_performance(url, number_of_measurements):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    performance_results = []
    for _ in range(number_of_measurements):
        driver.get(url)
        performance_timing = driver.execute_script(
            "return {'start': window.performance.timing.responseStart, 'end': window.performance.timing.loadEventEnd}")
        performance_results.append(performance_timing)

    driver.quit()
    return performance_results


def calculate_average(performance_data):
    total = sum(item['end'] - item['start'] for item in performance_data if item['end'] > 0 and item['start'] > 0)
    count = sum(1 for item in performance_data if item['end'] > 0 and item['start'] > 0)
    return total / count if count > 0 else 0


def write_to_json(data, average, filename):
    with open(filename, 'w') as file:
        json_data = {'measurements': data, 'average_duration': average}
        json.dump(json_data, file, indent=4)


def write_to_csv(average, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'duration'])
        writer.writerow(['Average Duration', average])


URL = 'https://en.wikipedia.org/wiki/Software_metric'
TIMES = 10

performance_data = measure_performance(URL, TIMES)
average_performance = calculate_average(performance_data)
write_to_json(performance_data, average_performance, 'performance.json')
write_to_csv(average_performance, 'performance.csv')
