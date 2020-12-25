import argparse
import csv
import json
import random
import re

from typing import Optional

from faker import Faker

from conf import model

BOOKS = "books.txt"
AUTHORS = "authors.txt"


def main():
    """
    Main function
    :return:
    """
    parser = create_parser()
    args = parser.parse_args()
    list_of_books = []
    gen_book = books_generator(args.sale, args.authors)
    for _ in range(args.count):
        list_of_books.append(next(gen_book))
    if args.output_format == 'json':
        to_json_file(list_of_books, args.name, args.ind)
    elif args.output_format == 'csv':
        to_csv_file(list_of_books, args.name, args.deli)
    else:
        print(list_of_books)


def to_json_file(obj: list, filename, i):
    """
    Get .json file
    :param obj:
    :param filename:
    :param i:
    :return:
    """
    if not filename.endswith('.json'):
        filename += '.json'
    with open(filename, 'w', encoding='utf-8') as json_output_file:
        json.dump(obj, json_output_file, indent=i)


def to_csv_file(obj: list, filename: str, deli: str):
    """
    Get .csv file
    :param filename:
    :param obj:
    :param deli:
    :return:
    """
    if not filename.endswith('.csv'):
        filename += '.csv'
    with open(filename, 'w', newline='') as csv_output_file:
        wr = csv.writer(csv_output_file, delimiter=deli, quoting=csv.QUOTE_MINIMAL)
        wr.writerow(obj)


def get_book():
    """
    Get random book for dict
    :return:
    """
    books = []
    with open(BOOKS, 'r', encoding='utf-8') as books_file:
        for book in books_file:
            books.append(book.strip())
    return random.choice(books)


def get_authors():
    """
    Get list of authors for dict
    :return:
    """
    pattern_name = re.compile(r"(?P<name>[A-Z]\w+\s+[A-Z]\w+)")
    authors = []
    with open(AUTHORS, 'r', encoding='utf-8') as author_file:
        for k, author in enumerate(author_file):
            if not re.fullmatch(pattern_name, author.strip()):
                raise ValueError(f"String {k} doesnt match {pattern_name}")
            authors.append(author.strip())
    return authors


def get_rand_authors(list_: list, value: Optional[int] = None):
    """
    Get random authors
    :param list_:
    :param value:
    :return:
    """
    if value is None:
        value = random.randint(1, 3)
    return random.sample(list_, value)


def get_isbn13():
    """
    Get fake isbn13 number
    :return:
    """
    fake = Faker()
    return fake.isbn13()


def get_discount(value: bool):
    """
    Get discount for book
    :param value:
    :return:
    """
    return None if not value else random.randint(1, 100)


def books_generator(sale: bool, authors: Optional[int] = None):
    """
    Random dict generator
    :return:
    """
    i = 0
    while True:
        dict_ = dict()
        dict_["model"] = model
        dict_["pk"] = i + 1
        dict_["fields"] = {
            "title": get_book(),
            "year": random.randint(2000, 2020),
            "pages": random.randint(500, 1000),
            "isbn13": get_isbn13(),
            "rating": random.uniform(0, 5).__round__(3),
            "price": random.uniform(1000, 5000).__round__(3),
            "discount": get_discount(sale),
            "author": get_rand_authors(get_authors(), authors)
        }
        yield dict_
        i += 1


def create_parser():
    parser = argparse.ArgumentParser("These arguments add behavior to our script")
    parser.add_argument('-c', '--count', default=3, type=int,
                        help='Amount of dictionaries for output')
    parser.add_argument('-a', '--authors', default=None,
                        type=int, help='Amount of authors for output')
    parser.add_argument('-s', '--sale', action='store_true',
                        help='-s - Include a discount')
    subparsers = parser.add_subparsers(dest='output_format')

    # -------------------------------------json subparser create----------------------------------

    output_format_parser = subparsers.add_parser('json')
    output_format_parser.add_argument('-n', '--name', dest='name', required=False,
                                      type=str, default='test.json', help='-n <filename>')
    output_format_parser.add_argument('-i', '--ind', dest='ind', required=False, default=4,
                                      help='-i <indent>', type=int)

    # -------------------------------------csv subparser create----------------------------------

    output_format_parser = subparsers.add_parser('csv')
    output_format_parser.add_argument('-n', '--name', dest='name', required=False,
                                      type=str, default='test.csv', help='Set csv filename, -n <filename>, '
                                                                         'default test.csv')
    output_format_parser.add_argument('-d', '--deli', dest='deli', required=False, default='\n',
                                      help='Set delimiter, -d <one-character string>, default \\n', type=str)

    return parser


if __name__ == '__main__':
    main()
# C:\Python\Python39\python.exe
