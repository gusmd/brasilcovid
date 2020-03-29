
from data_provider import get_country_data 

if __name__ == "__main__":
    countries = ["Brazil", "Italy", "US", "Spain"]

    country_data = get_country_data(countries)

    print(country_data)