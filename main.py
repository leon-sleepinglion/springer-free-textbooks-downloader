import os
import csv
import argparse
from pathlib import Path

import wget
import requests

PATH = Path(os.path.dirname(os.path.abspath(__file__))) / "Textbooks"
CATEGORIES = [
    'Literature, Cultural and Media Studies', 
    'Biomedical and Life Sciences', 
    'Earth and Environmental Science', 
    'Humanities, Social Sciences and Law', 
    'Law and Criminology', 
    'Computer Science', 
    'Religion and Philosophy', 
    'Behavioral Science', 
    'Business and Economics', 
    'Behavioral Science and Psychology', 
    'Chemistry and Materials Science', 
    'Engineering', 'Mathematics and Statistics', 
    'Business and Management', 
    'Physics and Astronomy', 
    'Medicine', 
    'Intelligent Technologies and Robotics', 
    'Energy', 
    'Social Sciences', 
    'Economics and Finance', 
    'Education'
]

f = open('textbooks.csv', encoding='utf-8')
csv_reader = csv.reader(f, delimiter=',')
BOOKS = list(csv_reader)[1:] 
f.close()

def main(categories, inverse=False):
    if inverse:
        categories = [c for c in range(21) if c not in categories]

    for c in categories:
        c_package = CATEGORIES[c]
        directory = str(PATH / c_package)
        Path(directory).mkdir(parents=True, exist_ok=True)
        for book in [book for book in BOOKS if book[11] == c_package]:
            r = requests.get(book[18])
            # download pdf
            pdf_url = r.url.replace('/book/', '/content/pdf/') + '.pdf'
            if requests.head(pdf_url).status_code == 200:
                wget.download(pdf_url, out=f'{directory}/{book[0]} - {book[1]}.pdf')

            # download epub
            epub_url = r.url.replace('/book/', '/download/epub/') + '.epub'
            if requests.head(epub_url).status_code == 200:
                wget.download(epub_url, out=f'{directory}/{book[0]} - {book[1]}.epub')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Download Springer Textbooks by Categories',
        epilog='[0] **Download all categories\n' + ''.join([f'[{i+1}] {c}\n' for i, c in enumerate(CATEGORIES)]),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.set_defaults(inverse=False)
    parser.add_argument(
        '-c',
        '--category',
        type=int,
        nargs='+',
        required=True,
        help='specify the categories to download, separated by space, i.e. -c 1 3 5',
    )
    parser.add_argument(
        '-i',
        '--inverse',
        dest='inverse',
        action='store_true',
        help='download all categories that are not specified in -c',
    )
    args = parser.parse_args()

    for c in args.category:
        if c < 0 or c > 21:
            raise ValueError('Categories index out of range')

    categories = []
    if 0 in args.category:
        if len(args.category) != 1:
            raise ValueError('You can only download all or specific categories')
        elif 0 in args.category and args.inverse:
            raise ValueError('You can not use inverse with the download all argument')
        else:
            categories = [c for c in range(21)]
    else:
        categories = [c-1 for c in args.category]

    main(categories, args.inverse)
