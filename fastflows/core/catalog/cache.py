import os
from fastflows.config.app import configuration as cfg
from ast import literal_eval


class CatalogCache:

    separator = " >> "

    def __init__(self):
        self.data = self.read()

    def check_or_create_home_folder(self) -> None:

        if not os.path.exists(cfg.FLOWS_HOME):
            os.makedirs(cfg.FLOWS_HOME, exist_ok=True)

    def read(self) -> None:
        self.check_or_create_home_folder()
        try:
            with open(cfg.FASTFLOWS_CATALOG_CACHE, "r") as f:
                raw_data = f.read()
        except IOError:
            with open(cfg.FASTFLOWS_CATALOG_CACHE, "w+") as f:
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
                    flows_data_list.append(literal_eval(line[1]))

            self.data = dict(zip(flows_data_list[0::2], flows_data_list[1::2]))
        return self.data

    def write(self, catalog_data: dict) -> None:
        data = self.catalog_dict_to_cache_str(catalog_data)

        with open(cfg.FASTFLOWS_CATALOG_CACHE, "w") as f:
            f.write(data)

    def catalog_dict_to_cache_str(self, data: dict) -> str:
        cache_str = ""
        for key, value in data.items():
            value = value.dict()
            cache_str += f"{key}{self.separator}{value}\n"
        return cache_str
