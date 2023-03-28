import datetime
import pandas
import collections
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


def age_in_years():
    years = str(datetime.date.today().year - 1920)
    if years[-1] == '1':
        years = years + ' год'
    elif years[-1] in ('2', '3', '4'):
        years = years + ' года'
    else:
        years = years + ' лет'
    return years


table_of_drinks = pandas.read_excel('wine3.xlsx').fillna('')
drinks = table_of_drinks.to_dict(orient='records')
categories = collections.defaultdict(list)
for drink in drinks:
    categories[drink['Категория']].append(drink)
categories = collections.OrderedDict(sorted(categories.items()))
rendered_page = template.render(
    vineyard_age=age_in_years(),
    drink_categories=categories,

)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
