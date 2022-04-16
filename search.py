#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from argparse import ArgumentParser
import logging
import os

logging.basicConfig()
logger = logging.getLogger(os.path.basename(__file__))

us_state_to_abbrev = {
    'alabama': 'AL',
    'alaska': 'AK',
    'arizona': 'AZ',
    'arkansas': 'AR',
    'california': 'CA',
    'colorado': 'CO',
    'connecticut': 'CT',
    'delaware': 'DE',
    'florida': 'FL',
    'georgia': 'GA',
    'hawaii': 'HI',
    'idaho': 'ID',
    'illinois': 'IL',
    'indiana': 'IN',
    'iowa': 'IA',
    'kansas': 'KS',
    'kentucky': 'KY',
    'louisiana': 'LA',
    'maine': 'ME',
    'maryland': 'MD',
    'massachusetts': 'MA',
    'michigan': 'MI',
    'minnesota': 'MN',
    'mississippi': 'MS',
    'missouri': 'MO',
    'montana': 'MT',
    'nebraska': 'NE',
    'nevada': 'NV',
    'new hampshire': 'NH',
    'new jersey': 'NJ',
    'new mexico': 'NM',
    'new york': 'NY',
    'north carolina': 'NC',
    'north dakota': 'ND',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'rhode island': 'RI',
    'south carolina': 'SC',
    'south dakota': 'SD',
    'tennessee': 'TN',
    'texas': 'TX',
    'utah': 'UT',
    'vermont': 'VT',
    'virginia': 'VA',
    'washington': 'WA',
    'west virginia': 'WV',
    'wisconsin': 'WI',
    'wyoming': 'WY',
    'district of columbia': 'DC',
    'american samoa': 'AS',
    'guam': 'GU',
    'northern mariana islands': 'MP',
    'puerto rico': 'PR',
    'united states minor outlying islands': 'UM',
    'u.s. virgin islands': 'VI',
}


def parse_args():
    argparser = ArgumentParser(
        description='Search multiple people search sites for an individual',
    )

    argparser.add_argument(
        'url_file',
        metavar='URL_FILE',
        help='File containing a list of newline separated template URLs',
    )

    argparser.add_argument('-f', '--first_name', required=True)
    argparser.add_argument('-l', '--last_name', required=True)
    argparser.add_argument('-c', '--city', default='')
    argparser.add_argument('-s', '--state', default='')
    argparser.add_argument('--min-age', default='')
    argparser.add_argument('--max-age', default='')

    argparser.add_argument(
        '--no-incognito',
        help="Don't use incognito mode when launching Chrome",
    )
    argparser.add_argument(
        '--log-level',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        default='notset',
    )

    return argparser.parse_args()


def main():
    args = parse_args()
    logger.setLevel(getattr(logging, args.log_level.upper()))

    if args.state != '' and args.state.lower() not in us_state_to_abbrev:
        raise ValueError('Invalid state: {}'.format(args.state))

    # Some sites require lowercase names, but no sites require capitalized
    # names, so make `first_name` and `last_name` lowercase. If a site is added
    # in the future that requires a capitalized first name, we can add
    # `first_name_capitalized` and `last_name_capitalized` then
    format_args = {
        'first_name': args.first_name.lower(),
        'last_name': args.last_name.lower(),
        'city': args.city,
        'state': args.state,
        'state_abbrev': us_state_to_abbrev.get(args.state, ''),
        'min_age': args.min_age,
        'max_age': args.max_age,
    }

    logger.info('Reading file "{0}"'.format(args.url_file))

    with open(args.url_file) as f:
        lines = f.read().strip().split('\n')

    template_urls = []
    for line in lines:
        logger.debug(f'Processing line: {line}')

        # Strip leading and trailing whitespace
        line = line.strip()

        # Skip empty lines and comments
        if line == '' or line[0] == '#':
            logger.debug('Skipping line')
            continue

        template_urls.append(line)

    chrome_options = Options()

    # Leave the browser open after the script is finished
    chrome_options.add_experimental_option('detach', True)
    chrome_options.add_argument('incognito')
    driver = webdriver.Chrome(options=chrome_options)

    for i, template_url in enumerate(template_urls):
        logger.info(f'Formating template URL {template_url}')
        url = template_url.format(**format_args)

        # Navigate to the URL
        logger.info(f'Navigating to URL {url}')
        driver.get(url)

        # Create a new tab unless this is the last URL
        if i != len(template_urls) - 1:
            tabName = f'tab{i}'
            driver.execute_script(f"window.open('about:blank', '{tabName}');")
            driver.switch_to.window(tabName)


if __name__ == '__main__':
    main()
