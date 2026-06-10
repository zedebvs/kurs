from bs4 import BeautifulSoup
from itertools import zip_longest


KEYS = ["№", "MAC", "SSID", "Тип", "Подключений", "Трафик байт", "Уровень дБм", "Используемые каналы", "Шифрование", "Первое обнаружение", "Последнее обнаружение"]
    

class Parse():
    def __init__(self) -> None:
        self.all_data = []
        self.stationary = []
        self.intruders = []
        self.randoms = []
        self.summary = 0
        self.filenames = []
        self.keys = KEYS
        self.files_ui = 'Файлы не загружены'

    @staticmethod
    def parse_html_file(filename) -> list:
        with open(filename, "r", encoding="CP1251") as f:
            soup = BeautifulSoup(f.read(), "lxml")
            
        data = []
        
        table = soup.find_all("table")
        for t in table:
            for rid, row in enumerate(t.find_all("tr")  ): #type: ignore
                if rid == 0:
                    continue 
                cols = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
                if cols:
                    data.append(cols)
        return data

    def discover(self, data: list[list[list]]) -> None:
        devices = {}

        for file_index, file_data in enumerate(data):
            seen_in_file = set()

            for row in file_data:
                if len(row) < 2:
                    continue

                mac = row[1]

                if mac in seen_in_file:
                    continue

                seen_in_file.add(mac)

                if mac not in devices:
                    devices[mac] = {
                        "row": row,
                        "files": set(),
                    }

                devices[mac]["files"].add(file_index)

        files_count = len(data)

        for mac, device in devices.items():
            count = len(device["files"])

            item = {
                "row": device["row"],
                "count": count,
            }

            if count == 1:
                self.randoms.append(item)
            elif count == 5:
                self.stationary.append(item)
            else:
                self.intruders.append(item)

    def parse_all_files(self) -> None:
        for filename in self.filenames:
            data = self.parse_html_file(filename)
            self.all_data.append(data)
            
    def summary_(self) -> None:
        for i in self.all_data:
            self.summary += len(i)
    
    def string_(self, key: int, data: list):
        string = ''
        for i in data:
            string+=f'{i[key]}\n'
        return string

        
    def parse_ui(self):
        self.all_data = []
        self.stationary = []
        self.intruders = []
        self.randoms = []
        self.summary = 0
        
        self.parse_all_files()
        self.summary_()
        self.discover(self.all_data)
            
    
    def reset(self) -> None:
        self.all_data = []
        self.stationary = []
        self.intruders = []
        self.randoms = []
        self.summary = 0
        self.filenames = []
        self.keys = KEYS
        self.files_ui = 'Файлы не загружены'