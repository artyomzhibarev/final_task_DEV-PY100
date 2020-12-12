import argparse
import csv
import json
import random
import re

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
    gen_book = books_generator()
    list_of_books = []
    for _ in range(args.count):
        list_of_books.append(next(gen_book))
    if args.json:
        get_json_file(list_of_books)
    elif args.csv:
        get_csv_file(list_of_books)
    else:
        print(list_of_books)


def get_json_file(obj: list):
    """
    Get .json file
    :param obj:
    :return:
    """
    with open('list_of_books.json', 'w', encoding='utf-8') as json_output_file:
        json.dump(obj, json_output_file, indent=4)


def get_csv_file(obj: list):
    """
    Get .csv file
    :param obj:
    :return:
    """
    with open('list_of_books.csv', 'w', encoding='utf-8') as csv_output_file:
        wr = csv.writer(csv_output_file, quoting=csv.QUOTE_ALL)
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
        k = 1
        for author in author_file:
            if not re.fullmatch(pattern_name, author.strip()):
                raise ValueError(f"String {k} doesnt match {pattern_name}")
            k += 1
            authors.append(author.strip())
    return authors


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
    if value:
        return random.randint(1, 100)
    else:
        return None


def books_generator():
    """
    Random dict generator
    :return:
    """
    parser = create_parser()
    args = parser.parse_args()
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
            "discount": get_discount(args.sale),
            "author": random.sample(get_authors(), args.authors)
        }
        yield dict_
        i += 1


def create_parser():
    parser = argparse.ArgumentParser("These arguments add behavior to our script")
    parser.add_argument('-c', '--count', default=3, type=int,
                        help='Amount of dictionaries for output')
    parser.add_argument('-a', '--authors', default=random.randint(1, 3),
                        type=int, help='Amount authors')
    parser.add_argument('-s', '--sale', action='store_true',
                        help='-s - Include a discount')
    parser.add_argument('--json', action='store_true',
                        help='Export list of dictionary\'s to json file')
    parser.add_argument('--csv', action='store_true',
                        help='Export list of dictionary\'s to csv file')

    return parser


# def universal_type_checker_decorator(fn):
#     def wrapper(*args, **kwargs):
#         print('Этот код будет выполняться перед каждым вызовом функции')
#         for key, value in dict_.items():
#             print(f'The key {key} value {value} is {type(value)}')
#         print('Этот код будет выполняться после каждого вызова функции')
#         return result
#
#     return wrapper


if __name__ == '__main__':
    main()
# C:\Python\Python39\python.exe
