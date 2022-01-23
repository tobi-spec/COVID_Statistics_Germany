from src.deprecated import FetchService
from pathlib import Path

'''
This class enables the download and handle of COVID-19 epidemiological data provides by the german RKI Institut (www.RKI.de)
All data is gathereed into a single csv file, which makes the file very large (> 1.8million columns)

RKI.fetch allows the download of the whole file, saved in a seperated folder (./data/rki)

'''


def fetch():
    url = "https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data"
    directory = Path("data/rki")
    print("this will need a while...")
    FetchService.save_csv(directory, url)
    print("Finished!")


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def save_csv(directory, link):
    response = requests.get(link)
    with open(Path(directory), 'w', encoding="utf-8", newline='') as file:
        file.write(response.text)

if __name__ == "__main__":
    fetch()
