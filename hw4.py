import sys
from build_data import get_data

DATA = get_data()

def display_data(data):
    """Displays all county data in a user-friendly format."""
    for county in data:
        print(f"{county.State} - {county.County}: Population {county.Population['2014 Population']}")

def filter_state(data, state):
    """Filters counties by state abbreviation."""
    filtered = [county for county in data if county.State == state]
    print(f"Filter: state == {state} ({len(filtered)} entries)")
    return filtered

def filter_gt(data, field, value):
    """Filters counties where the field is greater than the given value."""
    filtered = [
        county for county in data
        if field in county_to_dict(county) and county_to_dict(county)[field] > value
    ]
    print(f"Filter: {field} gt {value} ({len(filtered)} entries)")
    return filtered

def filter_lt(data, field, value):
    """Filters counties where the field is less than the given value."""
    filtered = [
        county for county in data
        if field in county_to_dict(county) and county_to_dict(county)[field] < value
    ]
    print(f"Filter: {field} lt {value} ({len(filtered)} entries)")
    return filtered

def population_total(data):
    """Calculates the total population for 2014."""
    total = sum(county.Population['2014 Population'] for county in data)
    print(f"2014 population: {total}")
    return total

def population_field(data, field):
    """Calculates the total sub-population for a given percentage field."""
    total = sum(
        county.Population['2014 Population'] * (county_to_dict(county).get(field, 0) / 100)
        for county in data
    )
    print(f"2014 {field} population: {total}")
    return total

def percent(data, field):
    """Calculates the percentage of the total population within a given sub-population."""
    total_population = population_total(data)
    sub_population = population_field(data, field)
    percentage = (sub_population / total_population) * 100 if total_population > 0 else 0
    print(f"2014 {field} percentage: {percentage}")
    return percentage

def county_to_dict(county):
    """Converts a CountyDemographics object to a flattened dictionary."""
    return {
        **county.Education,
        **county.Ethnicities,
        **county.Income,
    }

def process_operations_file(file_path):
    """Processes the operations file and performs the requested operations."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: Could not open file {file_path}")
        sys.exit(1)

    current_data = DATA
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        try:
            parts = line.split(':')
            operation = parts[0]
            if operation == 'display':
                display_data(current_data)
            elif operation == 'filter-state':
                state = parts[1]
                current_data = filter_state(current_data, state)
            elif operation == 'filter-gt':
                field, value = parts[1], float(parts[2])
                current_data = filter_gt(current_data, field, value)
            elif operation == 'filter-lt':
                field, value = parts[1], float(parts[2])
                current_data = filter_lt(current_data, field, value)
            elif operation == 'population-total':
                population_total(current_data)
            elif operation == 'population':
                field = parts[1]
                population_field(current_data, field)
            elif operation == 'percent':
                field = parts[1]
                percent(current_data, field)
            else:
                print(f"Error: Unsupported operation '{operation}' on line {line_num}")
        except (IndexError, ValueError) as e:
            print(f"Error: Malformed line {line_num} - {line}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python hw4.py <operations_file>")
        sys.exit(1)

    process_operations_file(sys.argv[1])
