import requests

TIMESERIES_URL = "https://pomber.github.io/covid19/timeseries.json"
CONFIRMED_KEY = "confirmed"
DEATHS_KEY = "deaths"
DATE_KEY = "date"

COUNTRY_KEY = "country"
HUNDREDTH_DATE_KEY = "hundredth_date"
HUNDREDTH_INDEX_KEY = "hundredth_idx"

DEATHS_DATE_KEY = "deaths_date"
DEATHS_INDEX_KEY = "deaths_idx"


def get_dataset(url):
    return requests.get(TIMESERIES_URL).json()


def get_idx_before_ith_case(dataset, country, cutoff, parameter_key):
    for i, day in enumerate(dataset[country]):
        if day[parameter_key] > cutoff:
            return i
    return None


def get_date_for_idx(dataset, country, idx):
    return dataset[country][idx][DATE_KEY]


def get_field_for_country(dataset, country, field, start_idx):
    return [x[field] for x in dataset[country][start_idx:]]


def get_country_data(countries):
    dataset = get_dataset(TIMESERIES_URL)

    country_data = {}
    for country in countries:
        hundredth_case_idx = get_idx_before_ith_case(
            dataset, country, 100, CONFIRMED_KEY
        )
        first_death_idx = get_idx_before_ith_case(dataset, country, 1, DEATHS_KEY)
        this_country = {
            HUNDREDTH_INDEX_KEY: hundredth_case_idx,
            HUNDREDTH_DATE_KEY: get_date_for_idx(dataset, country, hundredth_case_idx),
            CONFIRMED_KEY: get_field_for_country(
                dataset, country, CONFIRMED_KEY, hundredth_case_idx
            ),
            DEATHS_INDEX_KEY: first_death_idx,
            DEATHS_DATE_KEY: get_date_for_idx(dataset, country, first_death_idx),
            DEATHS_KEY: get_field_for_country(
                dataset, country, DEATHS_KEY, first_death_idx
            ),
        }
        country_data[country] = this_country

    return country_data
