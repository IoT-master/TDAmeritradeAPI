import zipfile
import requests
from bs4 import BeautifulSoup
import sys
from pathlib import Path

current_platform = sys.platform

dir_platform = {
    'linux1': './ChromeDrivers/Linux',
    'linux2': './ChromeDrivers/Linux',
    'darwin': './ChromeDrivers/Mac',
    'win32': './ChromeDrivers/Windows'
}
save_dir = Path(dir_platform[current_platform])

chromedriver_platform = {
    'linux1': 'chromedriver',
    'linux2': 'chromedriver',
    'darwin': 'chromedriver',
    'win32': 'chromedriver.exe'
}
chromedriver = save_dir.joinpath(chromedriver_platform[current_platform])

if not chromedriver.exists():

    resp = requests.get(
        'https://chromedriver.storage.googleapis.com/?delimiter=/&prefix=')
    soup = BeautifulSoup(resp.text, features="lxml")
    newest_version = soup.find_all('commonprefixes')[-2].find('prefix').text

    url_platform = {
        'linux1': f'https://chromedriver.storage.googleapis.com/{newest_version}chromedriver_linux64.zip',
        'linux2': f'https://chromedriver.storage.googleapis.com/{newest_version}chromedriver_linux64.zip',
        'darwin': f'https://chromedriver.storage.googleapis.com/{newest_version}chromedriver_mac64.zip',
        'win32': f'https://chromedriver.storage.googleapis.com/{newest_version}chromedriver_win32.zip'
    }
    dir_platform = {
        'linux1': './ChromeDrivers/Linux',
        'linux2': './ChromeDrivers/Linux',
        'darwin': './ChromeDrivers/Mac',
        'win32': './ChromeDrivers/Windows'
    }
    url = url_platform[current_platform]

    zip_file = save_dir.joinpath('ChromeDriver.zip')
    file_resp = requests.get(url, allow_redirects=True)
    zip_file.write_bytes(file_resp.content)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(save_dir)
    zip_file.unlink()
