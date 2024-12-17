import county_demographics
import sys
import build_data
import reduced_data

full_data = build_data.get_data()

with open(sys.argv[0]) as operation:
    operation_contents = operation.readlines()
    new_data = []
    print(len(full_data), "records loaded")
    valid_counties = []
    line_num = 0

    for line in operation_contents:
        try:
            # Variables by file.
            total_population = 0
            line_num += 1

            line_strip = line.strip('\n')
            line_contents = line_strip.split(':')
            # Filter what state is being inquired (defaults to entire country).
            if "filter-state" == line_contents[0]:
                state = line_contents[1]
                for county in full_data:
                    if state == county.state:
                        new_data.append(county)
                print("Filter: state ==", state, "({} entries)".format(len(new_data)))

            # Filter if a county's attribute has greater than a specific percent.
            if 'filter-gt' == line_contents[0]:
                attributes = line_contents[1].split('.')
                att1 = attributes[0].lower()
                dictionary_att = attributes[1]
                percent = 0
                count = 0
                population = 0
                if len(new_data) > 0:
                    for county in new_data:
                        percent = getattr(county, att1)[dictionary_att]
                        if percent > int(line_contents[2]):
                            count += 1
                    print("Filter: {}.{} gt {} ({} entries)".format(attributes[0], dictionary_att, line_contents[2], count))
                if len(new_data) > 0:
                    for county in new_data:
                        percent = getattr(county, att1)[dictionary_att]
                        if percent > int(line_contents[2]):
                            valid_counties.append(county)
                else:
                    for county in full_data:
                        percent = getattr(county, att1)[dictionary_att]
                        if percent > int(line_contents[2]):
                            count += 1
                    print("Filter: {}.{} gt {} ({} entries)".format(attributes[0], dictionary_att, line_contents[2], count))
                    for county in full_data:
                        percent = getattr(county, att1)[dictionary_att]
                        if percent > int(line_contents[2]):
                            valid_counties.append(county)
            if 'filter-lt' == line_contents[0]:
                attributes = line_contents[1].split('.')
                att1 = attributes[0].lower()
                dictionary_att = attributes[1]
                percent = 0
                count = 0
                population = 0
                if len(new_data) > 0:
                    for county in new_data:
                        percent = getattr(county, att1)[dictionary_att]
                        if percent < int(line_contents[2]):
                            count += 1
                    print("Filter: {}.{} lt {} ({} entries)".format(attributes[0], dictionary_att, line_contents[2], count))
                if len(new_data) > 0:
                    for county in new_data:
                        percent = getattr(county, att1)[dictionary_att]
                        if percent < int(line_contents[2]):
                            valid_counties.append(county)
                else:
                    for county in full_data:
                        percent = getattr(county, att1)[dictionary_att]
                        if percent < int(line_contents[2]):
                            count += 1
                    print("Filter: {}.{} lt {} ({} entries)".format(attributes[0], dictionary_att, line_contents[2], count))
                    for county in full_data:
                        percent = getattr(county, att1)[dictionary_att]
                        if percent < int(line_contents[2]):
                            valid_counties.append(county)

        # Population-total throughout all counties (in country or specified state).
            if "population-total" == line_contents[0]:
                if len(valid_counties) > 0:
                    for county in valid_counties:
                        total_population += county.population["2014 Population"]
                    print("2014 population:", total_population)
                elif len(new_data) > 0:
                    for county in new_data:
                        total_population += county.population["2014 Population"]
                    print("2014 population:", total_population)
                else:
                    for county in full_data:
                        total_population += county.population["2014 Population"]
                    print("2014 population:", total_population)
                # Percentage stats of attributes.
            if "percent" == line_contents[0]:
                attributes = line_contents[1].split('.')
                att1 = attributes[0].lower()
                dictionary_att = attributes[1]
                percent = 0
                if len(valid_counties) > 0:
                    for county in valid_counties:
                        percent += getattr(county, att1)[dictionary_att]
                    print("2014 {}.{} percentage: {}".format(attributes[0], dictionary_att, percent / len(valid_counties)))
                elif len(new_data) > 0:
                    for county in new_data:
                        percent += getattr(county, att1)[dictionary_att]
                    print("2014 {}.{} percentage: {}".format(attributes[0], dictionary_att, percent / len(new_data)))
                else:
                    for county in full_data:
                        percent += getattr(county, att1)[dictionary_att]
                    print("2014 {}.{} percentage: {}".format(attributes[0], dictionary_att, percent / len(full_data)))

                # Population of attributes (does same as percent but finds population from that percent).
            if 'population' == line_contents[0]:
                attributes = line_contents[1].split('.')
                att1 = attributes[0].lower()
                dictionary_att = attributes[1]
                percent = 0
                population = 0
                if len(valid_counties) > 0:
                    for county in valid_counties:
                        percent += getattr(county, att1)[dictionary_att]
                        percent /= len(valid_counties)
                        population += county.population['2014 Population']
                    print("2014 {}.{} population: {}".format(attributes[0], dictionary_att, (population * percent)))
                elif len(new_data) > 0:
                    for county in new_data:
                        percent += getattr(county, att1)[dictionary_att]
                    percent /= len(new_data)
                    population += county.population['2014 Population']
                    print("2014 {}.{} population: {}".format(attributes[0], dictionary_att, (population * percent)))
                else:
                    for county in full_data:
                        percent += getattr(county, att1)[dictionary_att]
                    percent /= len(full_data)
                    population += county.population['2014 Population']
                    print("2014 {}.{} population: {}".format(attributes[0], dictionary_att, (population * percent)))

            # Prints all info about a county.
            if 'display' == line_contents[0]:
                for county in valid_counties:
                    print(
                        "{},{}".format(county.county, county.state), '\n',
                        '\t', "Population:", county.population['2014 Population'], '\n'
                                                                                   '\t', "Age:\n",
                        '\t', '\t', "< 5: {}%".format(county.age['Percent Under 5 Years']), '\n',
                        '\t', '\t', "< 18: {}%".format(county.age['Percent Under 18 Years']), '\n',
                        '\t', '\t', "> 65: {}%".format(county.age['Percent 65 and Older']), '\n',
                        '\t', "Education", '\n',
                        '\t', '\t', ">= High School: {}%".format(county.education['High School or Higher']), '\n',
                        '\t', '\t', ">= Bachelor's: {}% ".format(county.education["Bachelor's Degree or Higher"]), '\n',
                        '\t', "Ethnicity Percentages", '\n',
                        '\t', '\t', 'American Indian and Alaska Native Alone: {}%'.format(
                            county.ethnicities['American Indian and Alaska Native Alone']), '\n',
                        '\t', '\t', 'Asian Alone: {}%'.format(county.ethnicities['Asian Alone']), '\n',
                        '\t', '\t', 'Black Alone: {}%'.format(county.ethnicities['Black Alone']), '\n',
                        '\t', '\t', 'Hispanic or Latino: {}%'.format(county.ethnicities['Hispanic or Latino']), '\n',
                        '\t', '\t', 'Native Hawaiian and Other Pacific Islander Alone: {}%'.format(
                            county.ethnicities['Native Hawaiian and Other Pacific Islander Alone']), '\n',
                        '\t', '\t', 'Two or More Races: {}%'.format(county.ethnicities['Two or More Races']), '\n',
                        '\t', '\t', 'White Alone: {}%'.format(county.ethnicities['White Alone']), '\n',
                        '\t', '\t', 'White Alone, not Hispanic or Latino: {}%'.format(
                            county.ethnicities['White Alone, not Hispanic or Latino']), '\n',
                        '\t', "Income", '\n',
                        '\t', '\t', "Median Household: ", county.income['Median Household Income'], '\n',
                        '\t', '\t', "Per Capita: ", county.income['Per Capita Income'], '\n',
                        '\t', '\t', "Below Poverty Level: ", county.income['Persons Below Poverty Level'], '\n',
                    )
        except:
            print("line: ",line_num,"error")
