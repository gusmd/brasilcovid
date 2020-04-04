import itertools

from bokeh.plotting import figure
from bokeh.palettes import Dark2_8 as palette
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.models import PrintfTickFormatter

from jinja2 import Template

from data_provider import get_country_data

HIGHLIGHT_COUNTRY = "Brazil"
curdoc().theme = "dark_minimal"


def get_plot(country_data, field, title, x_label, y_label):
    TOOLTIPS = [("País", "$name"), (y_label, "$y{0}")]
    p = figure(
        title=title,
        y_axis_type="log",
        border_fill_alpha=0.0,
        background_fill_alpha=0.0,
        plot_height=500,
        sizing_mode="stretch_width",
        tooltips=TOOLTIPS,
        toolbar_location=None,
    )

    colors = itertools.cycle(palette)

    for country, color in zip(country_data.keys(), colors):
        label = country_data[country]["display_name"]
        data = country_data[country][field]
        x = range(len(data))
        if country == HIGHLIGHT_COUNTRY:
            line_width = 5
            line_alpha = 1
        else:
            line_width = 1
            line_alpha = 0.8

        p.line(
            x,
            data,
            legend_label=label,
            color=color,
            line_width=line_width,
            line_alpha=line_alpha,
            name=label,
        )

    p.legend.location = "bottom_right"
    p.xaxis.axis_label = x_label
    p.yaxis.axis_label = y_label
    p.yaxis.formatter = PrintfTickFormatter(format="%5f")

    return p


def render_template(confirmed_plot, deaths_plot):
    template_file = "templates/index.html"
    with open(template_file) as file:
        template = Template(file.read())

    script, div = components({"confirmed": confirmed_plot, "deaths": deaths_plot})
    page = template.render({"bokeh_divs": div, "bokeh_script": script})

    with open("page/index.html", "w") as file:
        file.write(page)


def add_display_name(country_data, countries):
    for country in country_data.keys():
        country_data[country]["display_name"] = countries[country]


if __name__ == "__main__":
    countries = {
        "Brazil": "Brasil",
        "Italy": "Itália",
        "US": "Estados Unidos",
        "Spain": "Espanha",
        "United Kingdom": "Reino Unido",
        "Korea, South": "Coreia do Sul",
        "Japan": "Japão",
        "Mexico": "México",
    }

    country_data = get_country_data(countries.keys())
    add_display_name(country_data, countries)

    confirmed = get_plot(
        country_data, "confirmed", "", "Dias desde o caso #100", "Casos Confirmados"
    )
    deaths = get_plot(
        country_data, "deaths", "", "Dias desde a primeira morte", "Mortes"
    )

    render_template(confirmed, deaths)
