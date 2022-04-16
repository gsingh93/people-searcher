# People Searcher

This script automatically opens a Chrome browser window and searches multiple people search sites for the given first and last name. The intended usecase for this script is to make it easier to find which people search sites have your own information, so you can more quickly identify which sites you need to request this information be removed from.

## Installation

1. Make sure [Google Chrome](https://www.google.com/chrome/downloads/) and [Python 3](https://www.python.org/downloads/) are installed
1. Install the `selenium` Python package: `pip install selenium`
1. Clone this repository with `git`: `git clone https://github.com/gsingh93/people-searcher`. Alternatively, you can download a zip file from [here](https://github.com/gsingh93/people-searcher/archive/refs/heads/main.zip).

## Usage

```
$ ./search.py -h
usage: search.py [-h] -f FIRST_NAME -l LAST_NAME [-c CITY] [-s STATE] [--min-age MIN_AGE] [--max-age MAX_AGE]
                 [--no-incognito NO_INCOGNITO] [--log-level {debug,info,warning,error,critical}]
                 URL_FILE

Search multiple people search sites for an individual

positional arguments:
  URL_FILE              File containing a list of newline separated template URLs

optional arguments:
  -h, --help            show this help message and exit
  -f FIRST_NAME, --first_name FIRST_NAME
  -l LAST_NAME, --last_name LAST_NAME
  -c CITY, --city CITY
  -s STATE, --state STATE
  --min-age MIN_AGE
  --max-age MAX_AGE
  --no-incognito NO_INCOGNITO
                        Don't use incognito mode when launching Chrome
  --log-level {debug,info,warning,error,critical}
```

The only required arguments are the first name, last name, and a file containing the template URLs for the people search sites. There is a [urls.txt](./urls.txt) file included in this repository that can be used as a starting point. Here's an example of some template URLs in this file:

```
https://radaris.com/ng/search?ff={first_name}&fl={last_name}&fs={state}&fc={city}
https://www.peoplefinders.com/people/{first_name}-{last_name}/{state_abbrev}/{city}
https://spokeo.com/{first_name}-{last_name}
https://www.intelius.com/search/?firstName={first_name}&lastName={last_name}&city={city}&state={state_abbrev}
```

The script will iterate through each URL, replace the template with the information provided through the command line arguments, and then open a new Chrome tab with that URL. Note that `state_abbrev` can't be set from the command line, setting the `--state` flag will automatically set `state_abbrev` to the correct state abbreviation.

If you leave out non-required information, like `city` or `state`, then those values will be replaced with empty strings in the URL. For some people search sites, this is fine. For others, this causes issues. To avoid these issues, you can either make sure to specify as much information as possible, or modify the URL template file and remove the template strings for information you're not planning to enter.

Here's an example of running the script:
```bash
./search.py -f Bob -l Smith -c Nashville -s Tennessee ./urls.txt
```

By default, Chrome will be launched in incognito mode. This may cause issues with some sites, so if you would like to change this, use the `--no-incognito` flag. Note that even when not using incognito mode, your personal Chrome profile will not be used.

## Limitations

- This script only searches for the information, but does not provide links to the opt-out pages. Support for optionally opening the opt-out URL may be added in the future, but for now you can always add the opt-out URL in the template URL file with no template parameters.
- Not all types of people search sites are supported. The only sites that work are ones where all of the search information can be encoded in the URL. Support for sites without the search information in the URL may be added in the future.
- As mentioned above, leaving out information may break the URL. Future versions may have better support for these optional parameters.
- Some sites will still require some manual interaction, such as solving a CAPTCHA. There are no plans to automate any interaction required to get to the results.
