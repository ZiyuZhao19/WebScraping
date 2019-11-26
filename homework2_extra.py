import math
import re
import pandas as pd

from homework2 import get_featured_biographies
from wiki_api import page_text


def get_infobox(page):

    """Returns a dictionary containing information extracted from infoboxes"""

    # to identify an infobox:
    # 1. find "table class=" in line
    # 2.parse the line and find the <tr> lables
    # 3. extract categorical label of the entries using e_c_r
    # 4. extract details following the label using e_a_r
    page_content = page_text(page, "html", include_tables = True).split("\\n")
    entry_regex = re.compile(r'<tr>.*?</tr>')
    entry_category_regex = re.compile(r'\">.*?</th>')
    entry_answer_regex = re.compile(r'\>.*?<')
    info_dict = {"Name": page}

    for line in page_content:
        if line == "":
            page_content.pop(page_content.index(line))
    for line in page_content:
        if "<table class=\"infobox" in line\
                and "vcard" in line:
            table_entries = entry_regex.findall(line)
            for i in table_entries:
                # print(i)
                entry_category = entry_category_regex.findall(i)
                entry_answer = entry_answer_regex.findall(i)
                entry_answer.pop(0)
                if len(entry_category) != 0:
                    answer = []
                    for j in entry_answer:
                        # to remove >< marks
                        j = j[1:-1]
                        if len(j.strip()) > 1:
                            try:
                                # to remove random punctuation marks
                                while j[0].isalpha() is False and j[0].isdigit() is False:
                                    j = j[1:]
                                while j[-1].isalpha() is False and j[-1].isdigit() is False:
                                    j = j[:-1]
                                answer.append(j)
                            except IndexError:
                                pass
                    # print(answer)
                    if len(answer) > 1:
                        # return the result in a joint string to improve readability
                        answer_value = ', '.join(answer[1:])
                        answer_key = answer[0]
                        if "(" in answer_key:
                            answer_key = answer_key.replace("(", "")
                        info_dict[answer_key] = answer_value

    # print(info_dict)
    return info_dict


def get_birth_and_death(infobox):

    """returns either an integer of age or a string describing life span, choose one and uncomment it"""

    # to identify a birth and death year:
    # 1. in the strings in infobox describing "Born" and "Death"
    # 2. find the first 3-4 digit number
    # 3. sincere apology to people in 1st century who were excluded
    # to avoid extracting a date rather than year
    year_pattern = "\d{3,4}"
    year_regex = re.compile(year_pattern)

    birth_year = None
    death_year = None
    try:
        born_year_text = infobox["Born"]
        died_year_text = infobox["Died"]

        if re.search(year_regex, born_year_text):
            birth_year = re.findall(year_pattern, born_year_text)[0]
        if re.search(year_regex, died_year_text):
            death_year = re.findall(year_pattern, died_year_text)[0]
    except KeyError:
        pass

    try:
        birth_year = int(birth_year)
        death_year = int(death_year)
        # if the age is unlikely, consider the calculation to be wrong
        if 0 < (death_year-birth_year) < 150:
            age = int(death_year-birth_year)
        else:
            age = None
    except TypeError:
        # if birth or death year were None
        # age is None
        age = None
        pass
    # print("Age: ", age)
    alive_duration = f"{birth_year}-{death_year}"
    # return alive_duration
    return age


def get_birth_death_for_all():

    """implements the get_birth_and_death to all articles in the list
    and returns a list that includes the string of people's recorded life duration"""

    bd_list_all = []
    for article in get_featured_biographies():
        bd_personal_dict = {}
        try:
            years = get_birth_and_death(get_infobox(article))
            bd_personal_dict[article] = years
            bd_list_all.append(bd_personal_dict)
        except UnboundLocalError:
            pass
    print(bd_list_all)


def count_duration():

    """Returns a list of count of life-span groups to study people's longevity"""

    duration_dict = {}
    for article in get_featured_biographies():
        try:
            duration = math.floor(get_birth_and_death(get_infobox(article))/10)
            if duration not in duration_dict:
                duration_dict[duration] = 1
            else:
                duration_dict[duration] += 1
        except UnboundLocalError:
            pass
        except TypeError:
            pass
    # print(duration_dict)
    duration_count_items = list(duration_dict.items())
    sort_duration_count = sorted(duration_count_items, key=lambda item: item[1], reverse=True)
    print("Age group: Number of people")
    print(sort_duration_count)


def output_df():

    """Prepares a dataframe for later output
    and counts the cases of failed extraction attempts"""

    df = []
    failed_count = 0
    no_info_box = 0

    for article in get_featured_biographies():
        try:
            info_box = get_infobox(article)

            if len(info_box) > 1:
                df.append(info_box)
            elif len(info_box) == 1:
                no_info_box += 1
        except IndexError:
            failed_count += 1
        except UnboundLocalError:
            failed_count += 1

    print(df)
    print(failed_count)
    print(no_info_box)
    return df


def export_dataset(df, name):

    """Outputs the df as a csv file"""

    pd.DataFrame(df).to_csv(name)


def test_df():

    # open and read the file; store it in a dataframe
    df = pd.read_csv('extra_infoboxes.csv')

    # get information about Bronwyn Bancroft
    # by name searching
    # using .dropna(axis=1, how='all') to clean columns with no value in it
    bronwyn_bancroft_info1 = df.loc[df.Name == "Bronwyn Bancroft"].dropna(axis=1, how='all')
    # or by index searching
    # using .dropna(axis=0, how='all') to clean rows with no value in it
    bronwyn_bancroft_info2 = df.iloc[0, :].dropna(axis=0, how='all')

    # to match the infobox picture included in the instructions
    # check the page for Ursula K. Le Guin
    ursula_le_guin_info = df.loc[df.Name == "Ursula K. Le Guin"].dropna(axis=1, how='all')

    # to print the result
    print("###  Bronwyn Bancroft 1  ###")
    print(bronwyn_bancroft_info1)
    print()
    print("###   Bronwyn Bancroft 2  ###")
    print(bronwyn_bancroft_info2)
    print()
    print("###  Ursula K. Le Guin  ###")
    print(ursula_le_guin_info)
    print()


def main():

    # get_infobox("Ursula K. Le Guin")
    # output_df()
    # get_birth_and_death(get_infobox("Ursula K. Le Guin"))
    # export_dataset(output_df(), 'extra_infoboxes.csv')
    # test_df()

    # two see the result of the two following functions
    # uncomment the right return type of get_birth_and_death(infobox)
    # 1. uncomment return alive_duration
    # get_birth_death_for_all()
    # 2. uncomment return age
    count_duration()


if __name__ == "__main__":
    main()