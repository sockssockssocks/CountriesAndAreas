import pandas as pd
import pickle
from os import path


def main():
    countries_file = "countriesFile"
    areas_file = "areasFile"

    # Checks if pickle file exists, read if True and write if False.
    if path.exists(countries_file and areas_file):
        countries = read(countries_file)
        areas = read(areas_file)
    else:
        countries, areas = get_and_format_data()
        write(countries_file, countries)
        write(areas_file, areas)

    intro_text()
    print(*countries, sep=", ")

    # Handles user input and ensures that only countries in the list will be looked up.
    while True:
        country_input = str(input("\nEnter a country: ")).title()
        try:
            country_key = countries.index(country_input)
            country_area = areas[country_key]
            print(country_input + " has the SQ KM area " + str(country_area))
        except ValueError:
            print("Error: The country you searched for doesn't exist. Please check your spelling and try again.")
            continue
        else:
            break

    # Variables used throughout iterating. Displayed to user once complete.
    total_countries = 0
    total_area = 0
    countries_that_fit = []

    # Looks through the areas list to see if the running total plus current index's area is less than user's
    # country to continue. Will stop once they are the same.
    for p in range(len(areas)):
        if total_area == country_area:
            break
        elif (total_area + areas[p]) < country_area:
            total_area += areas[p]
            countries_that_fit.append(countries[p])
            total_countries += 1

    print("\n-------------------------------------------------------------------------------------------------")
    print("The number of countries that fit inside of you country are: " + str(total_countries) + ".")
    print("Those countries are:")
    print(*countries_that_fit, sep=", ")
    print("The total area of these countries is: " + str(total_area) + " which is " + str(country_area - total_area)
          + " SQ KM off of " + country_input + " (" + str(country_area) + ").")
    print("-------------------------------------------------------------------------------------------------")


def get_and_format_data():
    # Get the data.
    url = "https://www.cia.gov/library/publications/the-world-factbook/rankorder/2147rank.html"
    df0 = pd.read_html(url)[0]

    # Remove unneeded columns.
    countries = df0.drop(columns=['Rank', '(SQ KM)', 'Date of Information'])
    areas = df0.drop(columns=['Rank', 'Country', 'Date of Information'])

    # Rename the area column.
    areas = areas.rename(columns={"(SQ KM)": "SQ KM"})

    # Flatten columns to make it easier to index then send to lists.
    countries_list = countries.to_numpy().flatten().tolist()
    areas_list = areas.to_numpy().flatten().tolist()

    return countries_list, areas_list


def write(file_name, data):
    if type(data) is list:
        outfile = open(file_name, 'wb')
        pickle.dump(data, outfile)
        outfile.close()
    elif type(data) is dict:
        df = pd.DataFrame(data)
        df.to_pickle(file_name)


def read(file_name):
    try:
        infile = open(file_name, 'rb')
        unpickled = pickle.load(infile)
        infile.close()
        return unpickled
    except:
        return print("Error. Could not retrieve data.")


def intro_text():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("This program scraps from the web a list of countries their SQ KM areas.")
    print("There are two modes:")
    print("    1. Choose one country and see how many other countries fit inside of it. In this mode\n"
          "       the largest countries are chosen first.")
    print("    2. Choose two countries and see how many times the second one fits into the first.")
    print("Beneath is a list of all countries to choose from ordered from largest to smallest.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


if __name__ == "__main__":
    main()
