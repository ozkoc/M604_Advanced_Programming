import openpyxl

#read_Dataset_from_excel
file_path = "Reports/Rostock.xlsx"
wb = openpyxl.load_workbook(file_path)
sheet = wb.active

# Define column ranges based on main topics
column_ranges = {
    'Age': range(4, 27),
    'Overall Movement': range(27, 30),
    'Natural Movement': range(30, 37),
    'Spatial Movement': range(37, 43),
    'Marital Status': range(43, 47),
    'Gender': range(47, 51),
    'Household Structure': range(51, 56),
    'Overall': range(56, 58),
    'Nationality': range(58, 60)
}

# Define dummy points at the top level
map_points = [
    (200, 550), # Hansaviertel
    (450, 180), # Rostock-Heide
    (100, 430), # Evershagen
    (300, 550), # Stadtmitte
    (155, 570), # Gartenstadt/Stadtweide
    (175, 400), # Schmarl
    (320, 480), # Dierkow-West
    (100, 330), # Lichtenhagen
    (250, 540), # Kröpeliner-Tor-Vorstadt
    (108, 375), # Lütten Klein
    (250, 480), # Gehlsdorf
    (170, 500), # Reutershagen
    (300, 330), # Rostock-Ost
    (370, 465), # Dierkow-Neu
    (200, 630), # Biestow
    (350, 500), # Dierkow-Ost
    (300, 430), # Toitenwinkel
    (160, 350), # Groß Klein
    (380, 540), # Brinckmansdorf
    (250, 590), # Südstadt
    (180, 300)  # Warnemünde
]

# City points dictionary
city_points = {
    'I': 'Hansaviertel',
    'B': 'Rostock-Heide',
    'F': 'Evershagen',
    'N': 'Stadtmitte',
    'J': 'Gartenstadt/Stadtweide',
    'G': 'Schmarl',
    'R': 'Dierkow-West',
    'C': 'Lichtenhagen',
    'K': 'Kröpeliner-Tor-Vorstadt',
    'E': 'Lütten Klein',
    'T': 'Gehlsdorf',
    'H': 'Reutershagen',
    'U': 'Rostock-Ost',
    'P': 'Dierkow-Neu',
    'M': 'Biestow',
    'Q': 'Dierkow-Ost',
    'S': 'Toitenwinkel',
    'D': 'Groß Klein',
    'O': 'Brinckmansdorf',
    'L': 'Südstadt',
    'A': 'Warnemünde'
}

def read_cities_from_excel():

    cities = {}
    for row in sheet.iter_rows(min_row=2, values_only=True):
        city_code = row[1]
        city_name = row[2]
        cities[city_code] = city_name
    sorted_cities = {k: v for k, v in sorted(cities.items(), key=lambda item: item[1])}
    return sorted_cities

global city_names
city_names = read_cities_from_excel()
