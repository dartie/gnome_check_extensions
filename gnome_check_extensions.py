import os
import sys
import time
import yaml
import argparse
from packaging.version import Version, parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from colorama import init as colorama_init, Fore, Back, Style
colorama_init()


# set version
__version__ = '1.0'

# I obtain the app directory
if getattr(sys, 'frozen', False):
    # frozen
    dirapp = os.path.dirname(sys.executable)
    dirapp_bundle = sys._MEIPASS
    executable_name = os.path.basename(sys.executable)
else:
    # unfrozen
    dirapp = os.path.dirname(os.path.realpath(__file__))
    dirapp_bundle = dirapp
    executable_name = os.path.basename(__file__)


def get_versions(url):
    # Set up Selenium options to run headless (without opening a browser window)
    options = Options()
    options.headless = True

    # # Replace the path with the actual path to your chromedriver executable
    # service = Service('/path/to/chromedriver')

    # # Create a WebDriver instance
    # driver = webdriver.Chrome(service=service, options=options)
    
    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize Chrome WebDriver with headless options
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)    

    try:
        # Open the page
        driver.get(url)

        # Wait for the page to fully load
        time.sleep(2)

        # Get the page source
        page_source = driver.page_source

        # # Wait for the page to fully load and find all version elements
        # version_elements = driver.find_elements(By.CSS_SELECTOR, '.version')
        # version_elements_ = driver.find_elements(By.XPATH, "//select[@class='shell-version']/option/@value")

        # # Extract and print the available versions
        # versions = [version.text for version in version_elements]

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the select element with class 'shell-version'
        select_element = soup.find('select', class_='shell-version')

        # Extract all option values
        versions = [option.get('value') for option in select_element.find_all('option') if option.get('value')]

        # Turn version into version
        versions = [parse(x) for x in versions]

        # Get name
        name_element = soup.find(id='extension_name').text


        return name_element, versions

    finally:
        # Close the browser
        driver.quit()


def check_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="""
    Check if the GNOME extensions you require are compatible with the latest GNOME DE version you require.

    """)

    # Options
    parser.add_argument("-S", "--settings", dest="settings", help="File containing all extensions", default=os.path.join(dirapp, "extensions.yml"))
    parser.add_argument("gnome_version", help="Set gnome version")

    args = parser.parse_args()  # it returns input as variables (args.dest)

    # end check args

    return args


def main(args=None):
    if args is None:
        args = check_args()
    version_required = parse(args.gnome_version)

    # Load extensions from file
    with open(args.settings) as yaml_stream:
        try:
            yaml_content = yaml.safe_load(yaml_stream)
        except yaml.YAMLError as exc:
            print(exc)

    extensions_urls = yaml_content["extensions"]

    for url in extensions_urls:
        name, versions = get_versions(url)
        latest_version_available = max(versions)

        if latest_version_available >= version_required:
            color = Fore.GREEN
        else:
            color = Fore.RED
        
        print(f"{color}{name}: {latest_version_available}")


if __name__ == '__main__':
    try:
        main(args=None)
    except KeyboardInterrupt:
        print('\n\nBye!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
