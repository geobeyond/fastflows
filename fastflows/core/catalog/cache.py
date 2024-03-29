import json

from ...config import settings


class CatalogCache:

    separator = " >> "

    def __init__(self):
        self.data = self.read()

    def read(self) -> None:
        settings.FLOWS_HOME.mkdir(exist_ok=True, parents=True)
        try:
            with open(settings.CATALOG_CACHE, "r") as f:
                raw_data = f.read()
        except IOError:
            with open(settings.CATALOG_CACHE, "w+") as f:
                f.write("")
                raw_data = ""

        self.data = {}
        if raw_data:
            # get list with flow_name, flow_data
            data = raw_data.split("\n")
            flows_data_list = []
            for line in data:
                line = line.split(self.separator)
                if len(line) > 1:
                    flows_data_list.append(line[0])
                    flows_data_list.append(json.loads(line[1]))
            self.data = {
                flows_data_list[i]: flows_data_list[i + 1]
                for i in range(0, len(flows_data_list), 2)
            }
        return self.data

    def write(self, catalog_data: dict) -> None:
        data = self.catalog_dict_to_cache_str(catalog_data)

        with open(settings.CATALOG_CACHE, "w") as f:
            f.write(data)

    def catalog_dict_to_cache_str(self, data: dict) -> str:
        cache_str = ""
        for key, value in data.items():
            value = value.json()
            cache_str += f"{key}{self.separator}{value}\n"
        return cache_str
