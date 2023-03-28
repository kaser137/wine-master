import datetime
import os
import argparse
import dotenv
import pandas
import collections
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


def compute_age(birth_year):
    years = str(datetime.date.today().year - birth_year)
    if years[-1] == '1':
        years = f'{years} год'
    elif years[-1] in ('2', '3', '4'):
        years = f'{years} года'
    else:
        years = f'{years} лет'
    return years


def main():
    parser = argparse.ArgumentParser(description='Program start liquor shop site ')
    parser.add_argument('-f', '--fullname', help='Full name with path for .env', default='venv/.env')
    args = parser.parse_args()
    dotenv.load_dotenv(Path(args.fullname))
    birth_year = int(os.environ['BIRTH_YEAR'])
    file_fullname = os.environ['FILE_FULLNAME']
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    table_of_drinks = pandas.read_excel(Path(file_fullname)).fillna('')
    drinks = table_of_drinks.to_dict(orient='records')
    categories = collections.defaultdict(list)
    for drink in drinks:
        categories[drink['Категория']].append(drink)
    categories = collections.OrderedDict(sorted(categories.items()))
    rendered_page = template.render(
        vineyard_age=compute_age(birth_year),
        drink_categories=categories,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
