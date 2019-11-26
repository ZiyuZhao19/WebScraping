import csv
import json
import math
import re
import requests
import pandas as pd
from pandas.io.json import json_normalize


def open_read_file(filename, title):

    """Opens and read a file under a particular title"""

    with open(filename) as in_file:
        file = pd.read_json(in_file)
        raw = file[title]
        df = json_normalize(raw)
    return df


def q1_yelp():
    print("Part 1")
    print("#Q1")

    # open and read files
    restaurant_df = open_read_file("PA_businesses.json", "businesses")
    review_df = open_read_file("PA_reviews_full.json", "reviews")
    rows_res, columns_res = restaurant_df.shape
    rows_rev, columns_rev = review_df.shape

    star_count_result = {}
    word_count_result = {}

    # set up the score to loop through
    i = 0.0
    while i < 5.5:
        count_res = 0
        count_rev = 0
        word_cont_star_amount = 0

        # 1.1-1 average percentage: business
        for star in restaurant_df.loc[:, 'stars']:
            if star == i:
                count_res += 1
        percentage_res = round(count_res / rows_res, 3) * 100

        # 1.1-1 average percentage: reviews
        for star in review_df.loc[:, 'stars']:
            if star == i:
                count_rev += 1
        percentage_rev = round(count_rev / rows_rev, 3) * 100

        percentage = round((percentage_res + percentage_rev) / 2, 2)
        star_count_result[i] = percentage

        # 1.1-2 average word count
        reviews_per_star_count = review_df.loc[review_df.stars == i]
        for review in reviews_per_star_count.loc[:, "text"]:
            space_count = 0
            review_line = review.strip()
            for char in review_line:
                if char in " ":
                    space_count += 1
            word_count = space_count + 1
            word_cont_star_amount += word_count
        if count_rev != 0:
            word_count_average = round(word_cont_star_amount / count_rev)
            word_count_result[i] = word_count_average

        i += 0.5

    print(f"Star: Percentage \n{star_count_result}")
    print(f"Star: Word Count \n{word_count_result}")
    return star_count_result


def q2_yelp():
    print("Part 1")
    print("#Q2")
    restaurant_df = open_read_file("PA_businesses.json", "businesses")
    category_list = []
    count_dict = {}
    star_dict = {}

    # 1.2-1 how many categories
    for categories_line in restaurant_df.loc[:, "categories"]:
        categories = categories_line.split(", ")
        for category in categories:
            if category not in category_list:
                category_list.append(category)

    # 1.2-2 how many restaurant each category
    for category in category_list:
        category_count = 0
        for categories_line in restaurant_df.loc[:, "categories"]:
            categories = categories_line.split(", ")
            if category in categories:
                category_count += 1
        count_dict[category] = category_count

    # 1.2-3 average star of each category
    category_and_star_df = restaurant_df.loc[:, ["categories", "stars"]]
    rows, columns = category_and_star_df.shape

    for category in category_list:
        star_sum = 0
        for i in range(rows):
            if category in category_and_star_df.loc[i, "categories"]:
                star_sum += category_and_star_df.loc[i, "stars"]
        star_dict[category] = round(star_sum / count_dict[category], 2)

    # with open('label.csv', 'w') as f1:
    #     [f1.write('{0},{1}\n'.format(key, value)) for key, value in count_dict.items()]
    # with open('label2.csv', 'w') as f2:
    #     [f2.write('{0},{1}\n'.format(key, value)) for key, value in star_dict.items()]

    print(f"label counts: {len(category_list)}")
    print(f"label: restaurant number \n{count_dict}")
    print(f"label: average score \n{star_dict}")
    return category_list


def keys_with_top_values(my_dict):

    """Retrives a key to the highest value in a dictionary"""

    return [key for (key, value) in my_dict.items() if value == max(my_dict.values())]


def q3_yelp():
    print("Part 1")
    print("#Q3")
    restaurant_df = open_read_file("PA_businesses.json", "businesses")
    rows_all, columns_all = restaurant_df.shape
    column_list = []
    for column_name in restaurant_df.keys():
        if "attributes" in column_name:
            column_list.append(column_name)

    file = open('attributes.csv', 'w')

    high_score_df = restaurant_df.loc[restaurant_df.stars >= 4]
    rows, columns = high_score_df.shape

    # 1.3-1 business: general features
    print("# 1.3-1 business: general features\nMost popular choice for each attribute\n")
    for column in column_list:
        column_content = {}
        for i in range(rows_all):
            try:
                if high_score_df.loc[i, column] not in column_content:
                    column_content[high_score_df.loc[i, column]] = 1
                else:
                    column_content[high_score_df.loc[i, column]] += 1
            except KeyError:
                continue
        biggest_feature = keys_with_top_values(column_content)
        for (key, value) in column_content.items():
            if value == max(column_content.values()):
                percentage = round((value/rows)*100, 2)

        file.write('{0},{1},{2}\n'.format(column, biggest_feature, percentage))
        print(f"{column}: {biggest_feature}")
    file.close()

    # 1.3-2 business: detailed features
    print("\n# 1.3-2 business: detailed features\nTop 5 popular options for each attribute\n")

    # selected these five attributes for details
    detailed_attributes = ["attributes.BusinessParking","attributes.Ambience",
                           "attributes.GoodForMeal","attributes.Music",
                           "attributes.BestNights"]
    true_string = "True"
    true_regex = re.compile(true_string)
    for attribute in detailed_attributes:
        type_count = {}
        count = 1
        for i in range(rows_all):
            try:
                line = high_score_df.loc[i, attribute][1:-1]
                line = line.split(", ")
            except KeyError:
                pass
            except TypeError:
                pass
            for j in range(len(line)):
                try:
                    if re.search(true_regex,line[j]):
                        if line[j] not in type_count:
                            type_count[line[j]] = count
                        else:
                            type_count[line[j]] += 1
                except KeyError:
                    continue

        type_count_items = list(type_count.items())
        sort_type_count = sorted(type_count_items, key=lambda item: item[1], reverse=True)

        print(f"{attribute}: {sort_type_count[0:5]}")
    return column_content


def q3_yelp_3():

    """this function returns a list of word counts"""

    print("Part 1")
    print("#Q3")
    # 1.3-3 reviews: featured comments
    print("# 1.3-3 reviews: featured comments\nTop 100 most frequently used words")
    review_df = open_read_file("PA_reviews_full.json", "reviews")
    file = open('review_word.csv', 'w')
    file_out = csv.writer(file)
    rows_all, columns_all = review_df.shape
    word_count = {}
    high_score_df = review_df.loc[review_df.stars >= 4.0]
    for i in range(rows_all):
        try:
            review_line = high_score_df.loc[i, "text"]
            review = review_line.split()
            for word in review:
                if word not in word_count.keys():
                    word_count[word] = 1
                else:
                    word_count[word] += 1
        except KeyError:
            pass
    word_count_items = list(word_count.items())
    sort_word_count = sorted(word_count_items, key=lambda item: item[1], reverse=True)
    for k,v in sort_word_count[0:500]:
        file_out.writerow([k,v])
    file.close()
    print(sort_word_count[0:100])


# To import this function you will need to install the lxml library using Conda.
from wiki_api import page_text


def get_featured_biographies():

    # get the content of the list page
    website = "https://en.wikipedia.org/wiki/Wikipedia:Featured_articles"
    featured_list = requests.get(website)
    feature_text = featured_list.text.split("\n")
    featured_articles = {}
    featured_articles_list = []
    category_list = []
    bio_count = 0
    entry_sum = 0

    # 2.1-1 list of biographies in featured articles
    # print("\n# 2.1-1 list of biographies in featured articles")

    # identify a category of biographies by class="mw-headline"
    title_regex = re.compile(r'<span class="mw-headline" id=".*?">')
    for line in feature_text:
        # look for categories of biographies by reading <h3> headlines
        if "biographies" in line or "Biographies" in line:
            if "<h3>" in line:
                category = title_regex.search(line).group()[30:-2]
                if category != "":
                    category_list.append(category)

    # identify a name of an article by title=
    name_regex = re.compile(r'title=".*?"')
    for category in category_list:
        category_name = []
        for line in feature_text:
            # catch the category headline which marks the start point of a category of biographies
            if category in line:
                next_line_index = feature_text.index(line)+1
                # for every line after the category headline
                # if the line is not another headline or other functional lines
                # the line represents a featured article
                while "<h2>" not in feature_text[next_line_index]\
                        and "<h3>" not in feature_text[next_line_index]\
                        and "<h4>" not in feature_text[next_line_index]\
                        and "<p>" not in feature_text[next_line_index]:
                    if "title=" in feature_text[next_line_index]:
                        # look for the content in between the format
                        if name_regex.search(feature_text[next_line_index]) is not None:
                            # parse the name
                            name = name_regex.search(feature_text[next_line_index]).group()[7:-1]
                            featured_articles_list.append(name)
                            category_name.append(name)
                            # print(name)
                    next_line_index += 1
        # add the name to the dictionary of categories of biographies
        featured_articles[category] = category_name
        bio_count += len(featured_articles[category])

    # 2.1-2 percentage of biographies
    # as Architecture and archaeology is the first category
    # I'm only taking the articles after the headline as official festured articles
    for line in feature_text:
        if "Architecture and archaeology" in line:
            start_index = feature_text.index(line)
            break

    # calculate the amount of articles and the percentage of biographies
    for i in range(start_index, len(feature_text)):
        if "<li>" in feature_text[i] and "div id=" not in feature_text[i]:
            if name_regex.search(feature_text[i]):
                entry_sum += 1

    # print("\n# 2.1-2 percentage of biographies")
    # print(f"number of biographies: {bio_count}")
    # print(f"number of all articles: {entry_sum}")
    # print(f"bio percentage: {round(bio_count/entry_sum*100,2)}%")

    return featured_articles_list


def get_first_paragraph(page):
    page_content = page_text(page, "text").split("\n")
    # remove empty lines in the list of content
    for line in page_content:
        if line == "":
            page_content.pop(page_content.index(line))
    i = 0;

    # criteria to search for first info paragraphs:
    # 1. the numbers of characters in line is greater than 100
    # 2. in the line, the person's family name is included
    # 3. the line is not starting with functional words such as "For" or "This"
    # if find the paragraph successfully based on rules about, return true
    # otherwise, return false
    while len(page_content[i].strip()) < 100:
        i += 1
    first_para = page_content[i].strip()
    first_word = first_para.split(" ")[0]
    try:
        if page[-1] in first_para:
            if first_word != "This" and first_word != "For" \
                    and first_word != "The" and first_word != "In" \
                    and first_para[0] != "\"" and first_para[0] != "(":
                print(first_para)
                return True
            else:
                first_para = page_content[i+1].strip()
                first_word = first_para.split(" ")[0]
                if len(first_para) > 100:
                    if first_word != "This" and first_word != "For"\
                            and first_word != "The" and first_word != "In" \
                            and first_para[0] != "\"" and first_para[0] != "(":
                        print(first_para)
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False
    except IndexError:
        return False


def p2_scraping_ds():

    """Implements get first paragraph function and count successful attempts"""

    print("Part 2")
    print("# 2.2 getting first paragraphs")
    success_count = 0
    for article in get_featured_biographies():
        try:
            if get_first_paragraph(article):
                success_count += 1
        except UnboundLocalError:
            pass
    print(success_count)


def get_pronouns(text):

    # add different cases of pronouns into the pattern
    # identify pronouns as single words
    male_pronouns = "(he|his|him|he's|he'd|He|His|Him|He's|He'd)"
    female_pronouns = "(she|her|hers|she's|she'd|She|Her|Hers|She's|She'd)"
    plural_or_non_binary = "(they|them|their|they're|they've|They|Them|Their|They're|They've)"
    space = " "

    # trying to include punctuation marks that follow the pronouns
    # failed
    punctuations = "[\"*.?,!]"

    # compile the pattern
    male_pattern = re.compile(f"{space}{male_pronouns}{space}")
    female_pattern = re.compile(f"{space}{female_pronouns}{space}")
    plural_pattern = re.compile(f"{space}{plural_or_non_binary}{space}")

    # look for all of the pronouns
    use_male_pronouns = re.findall(male_pattern, text)
    use_female_pronouns = re.findall(female_pattern, text)
    use_plural_pronouns = re.findall(plural_pattern, text)

    pronouns_using = {"Male Pronouns": len(use_male_pronouns),
                      "Female Pronouns": len(use_female_pronouns),
                      "Plural or Non-binary Pronouns": len(use_plural_pronouns)}

    # returns the pronoun type with most incidences
    most_common = max(pronouns_using, key=pronouns_using.get)
    # print(most_common)
    # print(pronouns_using)
    return most_common


def p2_extracting_info():

    """Implements get_pronouns(text) function to all of the biographies and print the result"""

    print("Part 2")
    print("#2.3 extracting common pronouns")
    common_male = 0
    common_female = 0
    common_plural = 0

    for article in get_featured_biographies():
        try:
            page_content = page_text(article, "text")
            if get_pronouns(page_content) == "Male Pronouns":
                common_male += 1
            elif get_pronouns(page_content) == "Female Pronouns":
                common_female += 1
            elif get_pronouns(page_content) == "Plural or Non-binary Pronouns":
                common_plural += 1
            else:
                print(article)
        except UnboundLocalError:
            pass

    print(f"male common number: {common_male}\n"
          f"male common percentage: {round(common_male / len(get_featured_biographies())*100, 2)}%")
    print(f"female common number: {common_female}\n"
          f"female common percentage: {round(common_female / len(get_featured_biographies()) * 100, 2)}%")
    print(f"plural common number: {common_plural}\n"
          f"plural common percentage: {round(common_plural / len(get_featured_biographies()) * 100, 2)}%")


def additional_analysis():

    """Returns a list of century counts"""

    # look for year information by 3-4 digits (2 digits were omitted)
    # check if the year is BC or not
    year_pattern = "\d{3,4}\)*\s"
    bc_str = "\sBC\s\)*"
    bc_pattern = re.compile(bc_str)
    century_count = {}

    for article in get_featured_biographies():
        print(article)
        try:
            page_content = page_text(article, "text")
            try:
                birth_year = re.findall(year_pattern, page_content)[0]
                try:
                    birth_year = int(birth_year)
                    # if the ) is not parse out of the string, it causes an error
                except ValueError:
                    birth_year = birth_year[:-2]
                    birth_year = int(birth_year)
                print(birth_year)
                birth_year_century = math.floor(birth_year/100)+1
                if bc_pattern.search(page_content):
                    birth_year_century = -birth_year_century

                    if birth_year_century not in century_count:
                        century_count[birth_year_century] = 1
                    else:
                        century_count[birth_year_century] += 1
            except IndexError:
                pass
        except UnboundLocalError:
            pass

    century_count_items = list(century_count.items())
    sorted_century_count = sorted(century_count_items, key=lambda item: item[0], reverse=True)

    # write the count into a csv file
    # with open('century_count.csv', 'w') as f3:
    #     [f3.write('{0},{1}\n'.format(key, value)) for key, value in century_count.items()]
    print(sorted_century_count)
    return sorted_century_count


def additional_analysis_q5(text):

    """This function takes a parameter and returns the person's year of birth only"""

    year_pattern = "\d{3,4}\)*\s"
    bc_str = "\sBC\s\)*"
    bc_pattern = re.compile(bc_str)

    try:
        birth_year = re.findall(year_pattern, text)[0]
        try:
            birth_year = int(birth_year)
        except ValueError:
            birth_year = birth_year[:-2]
            birth_year = int(birth_year)
        birth_year_century = math.floor(birth_year/100)+1
        if bc_pattern.search(text):
            birth_year_century = -birth_year_century
            # if the century errously out of bounds, consider the data missing
            if 21 < birth_year_century or birth_year_century < -25:
                birth_year = None
                pass
    except IndexError:
        birth_year = None
        pass
    return birth_year


def q5_addtional():

    """This function tests additional_analysis_q5(text) before using it in q5"""

    for article in get_featured_biographies():
        try:
            page_content = page_text(article, "text")
            print(additional_analysis_q5(page_content))
        except UnboundLocalError:
            pass


def df_summary_list():

    """This function creates a list of dictionaries that store people's info"""

    summary_list = []
    for article in get_featured_biographies():
        try:
            page_content = page_text(article, "text")
            sub_dict = {"Name": article,
                        "Year_of_Birth": additional_analysis_q5(page_content),
                        "Most_Common_Pronoun": get_pronouns(page_content),
                        }
            i = get_featured_biographies().index(article)
            print(i)
            print(sub_dict)
            summary_list.append(sub_dict)
        except UnboundLocalError:
            pass
    df = pd.DataFrame(summary_list)
    return df


def export_dataset(df):

    """Outputs the df as a csv file"""

    pd.DataFrame(df).to_csv('p2_5.csv')


def main():

    """Please uncomment the function that you want to call"""

    # q1_yelp()
    # q2_yelp()
    # q3_yelp()
    # q3_yelp_3()
    # get_featured_biographies()
    # p2_scraping_ds()
    # p2_extracting_info()
    # additional_analysis()
    export_dataset(df_summary_list())

if __name__ == "__main__":
    main()
