# Ziyu Zhao
# 71435169

# This function takes one object as input:
#   populations_file: A filename where the file contains a spreadsheet with
#                     exactly two columns: name in column 0, population in column 1
# 
# This function returns a dictionary as output:
#   states: Each key in this dictionary is a state name.
#           The value is the population for that state, as found in the data file. 
# 
def build_state_populations_dictionary(populations_file):
    states = {}
    with open(populations_file) as states_file:
        states_input = states_file.readlines()
        header_row = []
        i = 0
        for row in states_input:
            if i == 0:
                header_row = row.split(",")
            else:
                state_row = row.split(",")
                state_name = state_row[0].strip()
                state_population = int(state_row[1].strip())
                states[state_name] = state_population
            i += 1
    return states


# This function takes one object as input:
#   districts_filename: A filename where the file contains a spreadsheet with
#                       any number of columns.
#
# This header column is then followed by any number of rows. The function
# attempts to convert the values to integers, or defaults to strings if it cannot.
#
# This function returns a list as output:
#   districts_list: Each entry in this list is a dictionary representing
#                   a single school district from our input file. Each dictionary
#                   contains keys corresponding to the columns in the input file. 
#                   That means you can retrieve, for instance, the 
#                   total revenue of the first school district in the list:
# 
#                           districts_list[0]["revenue"]
# 
def build_districts_list(districts_filename):
    districts_list = []
    with open(districts_filename) as districts_file:
        districts_input = districts_file.readlines()
        row_number = 0
        header_row = []
        for row in districts_input:
            if row_number == 0:
                header_row = row.strip().split(",")
            else:
                district_row = row.split(",")
                district_facts = {}
                for column_number in range(len(district_row)):
                    column_name = header_row[column_number]
                    cell_value = district_row[column_number]
                    try:
                        cell_value = int(cell_value)
                    except ValueError:
                        pass
                    district_facts[column_name] = cell_value
                districts_list.append(district_facts)
            row_number += 1
    return districts_list


def q1_ten_million(districts_list):
    # set up a variable to store the count of more than ten million states
    more_than_ten_million = 0
    # loop through the districts list to look for local revenue more than ten million
    for district_dict in districts_list:
        if district_dict['local_revenue'] > 10000:
            # count + 1 if a district is noted
            more_than_ten_million += 1
    # calculate the percentage
    ten_million_percentage = round(more_than_ten_million / len(districts_list), 4) * 100
    # print the result
    print(f"Q1: {ten_million_percentage}%")
    return ten_million_percentage


def q2_shortest_billion_name(districts_list):
    # set up a variable to store the length of the shortest name
    # default be 10000, because it's extremely unlikely for any district name to be longer than 10000 char
    shortest_name_length = 10000
    # loop through the district lists for expenses more than 1 billion
    for district_dict in districts_list:
        if district_dict['expenses'] >= 1000000:
            # if the name is shorter than the existing shortest, update the shortest length
            if len(district_dict['name']) < shortest_name_length:
                shortest_name_length = len(district_dict['name'])
                # record the name of the district of shortest length
                shortest_name = district_dict['name']
                # record its state
                shortest_name_state = district_dict['state']
    # print the results
    print(f"Q2: {shortest_name} in {shortest_name_state}")
    return shortest_name


def q3_larger_than_hawaii(districts_list):
    # create a variable to store the count of more than Hawaii expenses
    more_than_hawaii_count = 0
    # loop through the list to look for Hawaii's expenses
    for district_dict in districts_list:
        if district_dict['state'] == "Hawaii":
            hawaii_expenses = district_dict['expenses']
    # loop through the list to find district with more expenses than Hawaii
    for district_dict in districts_list:
        # rule out Hawaii, to get districts other than Hawaii
        if district_dict['state'] != "Hawaii":
            if district_dict['expenses'] > hawaii_expenses:
                # add finding to the count
                more_than_hawaii_count += 1
    # print the results
    print(f"Q3: {more_than_hawaii_count}")
    return more_than_hawaii_count


def q4_biggest_pennsylvania_deficit(districts_list):
    # set up a variable to store the largest deficit
    # default as -10000000000000 because it's represents the smallest deficit practically
    largest_deficit = -10000000000000000
    # loop through the list to look for districts in Pennsylvania
    for district_dict in districts_list:
        if district_dict['state'] == "Pennsylvania":
            # calculate the deficit
            district_deficit = district_dict['expenses'] - district_dict['revenue']
            # update the largest, if the current one is larger than the record
            if district_deficit > largest_deficit:
                largest_deficit = district_deficit
                # record the district name
                district_of_largest_deficit = district_dict['name']
    # print results
    print(f"Q4: {district_of_largest_deficit}: {largest_deficit * 1000} USD")


# only for practice, please let me know if its wrong, but please don't grade on this
# thanks!
def q5_new_england_highest_per_capita(districts_list, state_populations):
    # create a list to store New England states
    new_england = ['Maine', 'Vermont', 'New Hampshire', 'Rhode Island', 'Massachusetts', 'Connecticut']
    # set up an empty dictionary to store states' non-federal funds
    non_federal_fund_each_state = {}
    # loop through New England states
    for i in new_england:
        district_amount = 0
        # for each state in New England, loop through the districts list to find matches
        for district_dict in districts_list:
            if district_dict['state'] == i:
                # calculate the amount of non-federal funds
                district_amount += (district_dict['state_revenue'] + district_dict['local_revenue'])
                # add the info to the dictionary
                non_federal_fund_each_state[i] = district_amount
    # get the max value in NE non-federal funds
    most_non_federal = max(non_federal_fund_each_state.values())
    # look for the key for the max value
    for key, val in non_federal_fund_each_state.items():
        if val == most_non_federal:
            most_non_federal_state = key
    # to get the state's population by looking for the key (the state name)
    for key, val in state_populations.items():
        if key == most_non_federal_state:
            state_population = val
    # calculate non-federal funds per capita
    fund_per_capita = round(most_non_federal * 1000 / state_population, 2)
    # print results
    print(f"Q5: {most_non_federal_state}: {fund_per_capita} USD per capita")


# same as q5, practice only
def q6_smallest_mean_district_size(districts_list, state_populations):
    # create an empty dictionary to store future data
    state_mean_sd_size = {}
    # loop through different states in state_population
    for key, val in state_populations.items():
        sd_count = 0
        # if the district is in the state in state_population
        for district_dict in districts_list:
            if district_dict['state'] == key:
                # add the count
                sd_count += 1
        # rule out states, statistic on which is not included in districts_list
        # specifically Puerto Rico in this case
        if sd_count > 0:
            # calculate the mean size of districts by dividing population by numbers of districts
            state_mean = round(val / sd_count)
            # store the info in the dictionary
            state_mean_sd_size[key] = state_mean
    # look for the smallest mean size
    smallest_size = min(state_mean_sd_size.values())
    # look for the key to the smallest value
    for k, v in state_mean_sd_size.items():
        if v == smallest_size:
            # store the key in smallest_sized_state
            smallest_sized_state = k
    # print the result
    print(f"Q6: {smallest_sized_state}: {smallest_size} people each district")
    return state_mean_sd_size


state_populations = build_state_populations_dictionary("state_sizes.csv")
districts_list = build_districts_list("district_statistics.csv")

print("P2")
q1_ten_million(districts_list)
q2_shortest_billion_name(districts_list)
q3_larger_than_hawaii(districts_list)
q4_biggest_pennsylvania_deficit(districts_list)
q5_new_england_highest_per_capita(districts_list, state_populations)
q6_smallest_mean_district_size(districts_list, state_populations)
print()


def p3_federal_state_sum(districts_list, state_populations):
    """this function returns a dictionary of states and their federal funding sum"""
    # create an empty dict
    state_federal = {}
    # calculate the sum of each state's federal revenue
    for k in state_populations:
        state_federal_sum = 0
        for district_dict in districts_list:
            if district_dict['state'] == k:
                state_federal_sum += district_dict['federal_revenue']
        # store the info in the dict
        state_federal[k] = state_federal_sum
    return state_federal


def p3_state_revenue_sum(districts_list, state_populations):
    """this function returns a dictionary of states and their revenue sum"""
    # create an empty dict
    state_revenue = {}
    # calculate the sum of each state's total revenue
    for k in state_populations:
        state_revenue_sum = 0
        for district_dict in districts_list:
            if district_dict['state'] == k:
                state_revenue_sum += district_dict['revenue']
        # update the dictionary for further use
        state_revenue[k] = state_revenue_sum
    return state_revenue


def p3_state_sd_count(districts_list, state_populations):
    """this function returns a dictionary of states and how many school districts each state has"""
    state_sd_count = {}
    # calculate the count of the school districts
    for k in state_populations:
        sd_count = 0
        for district_dict in districts_list:
            if district_dict['state'] == k:
                sd_count += 1
        # just in case the state in state_population is not included in districts_list
        if sd_count > 0:
            state_sd_count[k] = sd_count
    return state_sd_count


def p3_top5_federal_funding(state_federal_sum):
    """returns the sorted list of states and their federal funding sum and prints the top 5"""
    # turn the key-value tuples in the dictionary into a list to sort
    state_fed_sum_items = list(state_federal_sum.items())
    # sort the list from highest federal funding to the lowest
    sort_fed_sum = sorted(state_fed_sum_items, key=lambda item: item[1], reverse=True)
    # print the top 5
    print(f"P3#1 top 5 most federal funded states (k USD): \n{sort_fed_sum[0:5]}")
    print("-" * 100)
    return sort_fed_sum


def p3_top5_federal_per_sd(state_sum, sd_count):
    """returns the top 5 states that have highest federal funding per school district"""
    federal_sd = {}
    # for the values in the federal sum dict and district count dict that have same state as key
    for k1 in state_sum:
        for k2 in sd_count:
            if k1 == k2:
                # calculate the fed fund per district
                federal_per_sd = round(state_sum[k1] / sd_count[k2], 2)
        # update the info into a dictionary
        federal_sd[k1] = federal_per_sd
    # create a list of key-value items in the dict
    federal_sd_items = list(federal_sd.items())
    # sort the list top down
    sort_fed_sd = sorted(federal_sd_items, key=lambda item: item[1], reverse=True)
    # print the top 5
    print(f"P3#2 top 5 states of highest federal funding per district (k USD): \n{sort_fed_sd[0:5]}")
    print("-" * 100)
    return sort_fed_sd[0:5]


def p3_top5_fed_per_capita(state_sum, state_population):
    """returns the top 5 states that have highest federal funding per capita"""
    fed_capita = {}
    for k1 in state_sum:
        for k2 in state_population:
            # for the values in the federal sum dict and population dict that have same state as key
            if k1 == k2:
                # calculate the fed fund per capita
                fed_per_capita = round(state_sum[k1] / state_population[k2], 2) * 1000
        # update the dict
        fed_capita[k1] = fed_per_capita
    # create a list of items
    fed_capita_items = list(fed_capita.items())
    # sort the items list top down
    sort_fed_cap = sorted(fed_capita_items, key=lambda item: item[1], reverse=True)
    # print the top 5
    print(f"P3#3 top 5 states of highest federal funding per capita (USD): \n{sort_fed_cap[0:5]}")
    print("-" * 100)
    return sort_fed_cap[0:5]


def p3_top5_fed_proportion(state_fed_sum, state_revenue_sum):
    """returns the top 5 states that have highest federal funding proportion"""
    fed_prop = {}
    for k1 in state_revenue_sum:
        for k2 in state_fed_sum:
            # for the values in the federal sum dict and revenue sum dict that have same state as key
            if k1 == k2:
                # rule out the case where the state in population dict not mentioned in district list
                if state_revenue_sum[k1] != 0:
                    # calculate the percentage
                    fed_proportion = round((state_fed_sum[k2] / state_revenue_sum[k1]) * 100, 2)
        # update the dict
        fed_prop[k1] = fed_proportion
    # create a list of items to sort
    fed_prop_items = list(fed_prop.items())
    # sort the list top down
    sort_fed_prop = sorted(fed_prop_items, key=lambda item: item[1], reverse=True)
    # print the top 5
    print(f"P3#4 top 5 state of highest federal funding proportion (%): \n{sort_fed_prop[0:5]}")
    print("-" * 100)
    return sort_fed_prop[0:5]


def p3_best_deal(t5_fed_per_sd, t5_fed_per_cap, t5_fed_ratio):
    """this function evaluates which state is top 5 in all three perspectives above"""
    # create a list of best deal candidates just in case there is more than one
    best_deal = []
    # if a top 5 state of highest fed fund per district also in top 5 fed funds per capita
    for item1 in t5_fed_per_sd:
        for item2 in t5_fed_per_cap:
            if item1[0] == item2[0]:
                # treat it as a potential candidate
                best_deal_candidate = item1[0]
                # if the candidate also in top 5 proportional rate
                for item3 in t5_fed_ratio:
                    if best_deal_candidate == item3[0]:
                        # it's then officially a great deal of fed funding
                        best_deal.append(best_deal_candidate)
    # print the result
    print(f"P3#5 best deal candidate(s): \n{best_deal}")
    return best_deal


# call the function for top 5 federal funding sum
p3_top5_federal_funding(p3_federal_state_sum(districts_list, state_populations))
# call the best deal function, taking per sd, per cap, and proportion rate into consideration
p3_best_deal(p3_top5_federal_per_sd(p3_federal_state_sum(districts_list, state_populations),
                                    p3_state_sd_count(districts_list, state_populations)),
             p3_top5_fed_per_capita(p3_federal_state_sum(districts_list, state_populations), state_populations),
             p3_top5_fed_proportion(p3_federal_state_sum(districts_list, state_populations),
                                    p3_state_revenue_sum(districts_list, state_populations)))
