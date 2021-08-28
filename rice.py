#!/bin/python

import requests
import wget
import os
from bs4 import BeautifulSoup
from argparse import ArgumentParser, RawDescriptionHelpFormatter


class Rice:

    def __init__(self, environment):
        self.environment = environment

    def mk_request(self):
        try:
            url = f"https://www.reddit.com/r/unixporn/search/?q={self.environment}&restrict_sr=1&t=all&sort=hot"
            with requests.get(url) as response:
                if response.status_code == 200:
                    print("[OK]")

                    return BeautifulSoup(response.text, 'html.parser')
                else:
                    print("[FAILED]")

        except requests.exceptions.HTTPError as err:
            print(f'Something went wrong! {err}')

    def download(self):
        images = []

        req = 0
        print(f'\nSelcted Environment: {self.environment}')
        while images == []:
            page_soup = Rice(self.environment).mk_request()

            req += 1
            for content in page_soup.findAll('div', {'class': '_1poyrkZ7g36PawDueRza-J'}):
                for image in content.findAll('a'):
                    if image['href'].endswith(('.png', 'jpg')) and not image['href'] in images:
                        images.append(image['href'])

            if req == 10:
                print(f'Could not find anything for: "{self.environment}"')
                break

        if not os.path.exists(self.environment):
            os.mkdir(self.environment)
        
        print(f'Requests made: {req}')
        print(f'Number of {self.environment} rices found: {len(images)}')
        for rice in images:
            dir_path = os.path.join(os.getcwd(), self.environment)
            
            if not rice.split('/')[-1] in os.listdir(dir_path):
                wget.download(rice, dir_path)


if __name__ == '__main__':
    parser = ArgumentParser(description="Download rice according to DE/WM name",
                            formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('de_wm',
                    nargs='+', metavar='DE_WM',
                    type=str, action='store',
                    help="Enter the DE or WM name (./main.py kde xmonad i3 bspwm)")
    
    args = parser.parse_args()
    for i in args.de_wm:
        Rice(i).download()
