import csv
from openpyxl import Workbook


class User:
    def __init__(self, user_info: dict):
        self.style_points = {1: [5, 8, 15, 34, 40], 2: [4, 12, 21, 26, 29], 3: [10, 14, 32, 36, 39],
                             4: [1, 7, 17, 22, 31], 5: [6, 13, 20, 24, 28], 6: [2, 9, 27, 35, 38],
                             7: [3, 16, 18, 25, 37],
                             8: [11, 19, 23, 30, 33]}
        self.user_styles = {}
        self.user_styles_percentage = {}
        self.area1_total = 0
        self.area2_total = 0
        self.area3_total = 0
        self.user_info = user_info
        self.name = "{} {}".format(self.user_info["NOME"], self.user_info["COGNOME"])
        self.parse_info()

    def parse_info(self):
        line = 0
        answers = []
        for key, item in self.user_info.items():
            if line < 5:  # Prime 5 righe di informazioni generali
                line += 1
            else:
                answers.append(item)
        for style, point in self.style_points.items():
            count = 0
            for p in point:
                count += int(answers[p - 1])
            self.user_styles[style] = count
        self.area1_total = self.user_styles[1] + self.user_styles[2] + self.user_styles[3] + self.user_styles[4]
        self.area2_total = self.user_styles[5] + self.user_styles[6]
        self.area3_total = self.user_styles[7] + self.user_styles[8]
        for style, count in self.user_styles.items():
            if style <= 4:
                self.user_styles_percentage[style] = round(count * 100 / self.area1_total, 2)
            elif style >= 5 and style <= 6:
                self.user_styles_percentage[style] = round(count * 100 / self.area2_total, 2)
            elif style >= 7:
                self.user_styles_percentage[style] = round(count * 100 / self.area3_total, 2)


def read_csv(f):
    rows = []
    with open(f) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line = 0
        for row in csv_reader:
            if line == 0:  # PRIMA RIGA CON PROPRIETA DEL CSV
                line += 1
            rows.append(row)
    return rows


def write_csv(f, users):
    with open(f, "w+", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            ["Cognome", "Nome", "Mail", "Classe", "Stile 1%", "Stile 2%", "Stile 3%", "Stile 4%", "Stile 5%",
             "Stile 6%", "Stile 7%", "Stile 8%"])
        for user in users:
            # print(user.user_info)
            to_write = [user.user_info["COGNOME"], user.user_info["NOME"], user.user_info["Indirizzo email"],
                        "1" + user.user_info["CLASSE PRIMA "]]
            for key, value in user.user_styles_percentage.items():
                # to_write.append(key)
                to_write.append(str(value) + "%")
            writer.writerow(to_write)


files = ["file.csv"]
users = []
for file in files:
    read = read_csv(file)
    for row in read:
        # print(row)
        users.append(User(row))

write_csv("f.csv", users)
