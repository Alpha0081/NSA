from os.path import isfile

from requests import get


class AlmanacDownloader:
    def __init__(
        self, root_path: str, satellite_system_name: str, url: str, update_almanac: bool
    ):
        if (
            not self.check_almanac_file(root_path, satellite_system_name.lower())
            or update_almanac
        ):
            self.download_almanac(root_path, url, satellite_system_name.lower())

    def download_almanac(
        self, root_path: str, url: str, file_name: str, file_type: str = ".json"
    ):
        almanac_request = get(url)
        with open(root_path + "data/" + file_name + file_type, "wb") as almanac_file:
            almanac_file.write(almanac_request.content)

    def check_almanac_file(
        self, root_path: str, file_name: str, file_type: str = ".json"
    ):
        return isfile(f"{root_path + 'data/' + file_name + file_type}")
