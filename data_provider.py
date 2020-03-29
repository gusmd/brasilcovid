import requests

TIMESERIES_URL = "https://pomber.github.io/covid19/timeseries.json"
CONFIRMED_KEY = "confirmed"
DEATHS_KEY = "deaths"
DATE_KEY = "date"

COUNTRY_KEY = "country"
HUNDREDTH_DATE_KEY = "hundredth_date"
HUNDREDTH_INDEX_KEY = "hundredth_idx"


def get_dataset(url):
    return requests.get(TIMESERIES_URL).json()


def get_idx_before_hundredth_case(dataset, country):
    for i, day in enumerate(dataset[country]):
        if day[CONFIRMED_KEY] > 100:
            return i - 1 if i > 0 else 0
    return None


def get_date_for_idx(dataset, country, idx):
    return dataset[country][idx][DATE_KEY]


def get_field_for_country(dataset, country, field, start_idx):
    return [x[field] for x in dataset[country][start_idx:]]


def get_country_data(countries):
    dataset = get_dataset(TIMESERIES_URL)

    country_data = {}
    for country in countries:
        hundredth_idx = get_idx_before_hundredth_case(dataset, country)
        this_country = {
            HUNDREDTH_INDEX_KEY: hundredth_idx,
            HUNDREDTH_DATE_KEY: get_date_for_idx(dataset, country, hundredth_idx),
            CONFIRMED_KEY: get_field_for_country(
                dataset, country, CONFIRMED_KEY, hundredth_idx
            ),
        }
        country_data[country] = this_country

    return country_data
