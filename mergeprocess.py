import os
import pandas as pd

# Define the directories for each year containing the files
directories = ['Reports/Datasets/2016', 'Reports/Datasets/2017', 'Reports/Datasets/2018', 'Reports/Datasets/2019']

# List all the file names without the year prefix
file_names = [
    'alter.xlsx',
    'bewegung_gesamt.xlsx',
    'bewegung_natuerlich.xlsx',
    'bewegung_raeumlich.xlsx',
    'familienstand.xlsx',
    'geschlecht.xlsx',
    'haushaltsstruktur.xlsx',
    'insgesamt.xlsx',
    'staatsangehoerigkeit.xlsx'
]

# Function to read and prepare data from each file
def read_and_prepare_data(file_path):
    df = pd.read_excel(file_path)
    # Drop any potential unnamed columns caused by merged cells in Excel
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # Drop duplicate rows based on column A and B (assuming these are the main keys)
    df.drop_duplicates(subset=['stadtbereich_code', 'stadtbereich_bezeichnung'], keep='first', inplace=True)
    return df

# List to hold all the data frames for each year
all_years_data = {}

# Iterate over each year's directory
for directory in directories:
    year = int(os.path.basename(directory))  # Convert directory name to integer
    all_dfs = []
    stadtbereich_code = None
    stadtbereich_bezeichnung = None
    
    # Iterate over each file and read data
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        df = read_and_prepare_data(file_path)
        
        # Extract stadtbereich_code and stadtbereich_bezeichnung from the first sheet
        if len(all_dfs) == 0:  # Only extract once from the first sheet
            stadtbereich_code = df.iloc[:, 0].rename('stadtbereich_code')  # Assuming the first column is stadtbereich_code
            stadtbereich_bezeichnung = df.iloc[:, 1].rename('stadtbereich_bezeichnung')  # Assuming the second column is stadtbereich_bezeichnung
            first_sheet_data = df.iloc[:, 2:]  # Exclude the first two columns for the first sheet
            all_dfs.append(first_sheet_data)
        else:
            all_dfs.append(df.iloc[:, 2:])  # Exclude the first two columns for other sheets
    
    # Concatenate all data frames along columns
    final_data = pd.concat(all_dfs, axis=1)
    
    # Insert 'year' column with value from directory name as integer
    final_data.insert(0, 'year', year)
    
    # Add stadtbereich_code and stadtbereich_bezeichnung columns from the first sheet at the desired positions
    final_data.insert(1, 'area_code', stadtbereich_code)
    final_data.insert(2, 'area_name', stadtbereich_bezeichnung)
    
    # Store final_data in the dictionary with year as the key
    all_years_data[year] = final_data

# Concatenate data from all years into a single DataFrame
combined_data = pd.concat(all_years_data.values(), ignore_index=True)

# Rename columns as specified
column_rename_map = {
    'durchschnittsalter': 'average_age',
    'jugendquotient': 'youth_ratio',
    'altenquotient': 'old_age_ratio',
    'anzahl_juenger_3': 'number_younger_3',
    'anteil_juenger_3': 'percentage_younger_3',
    'anzahl_3_6': 'number_3_6',
    'anteil_3_6': 'percentage_3_6',
    'anzahl_6_15': 'number_6_15',
    'anteil_6_15': 'percentage_6_15',
    'anzahl_15_25': 'number_15_25',
    'anteil_15_25': 'percentage_15_25',
    'anzahl_25_35': 'number_25_35',
    'anteil_25_35': 'percentage_25_35',
    'anzahl_35_45': 'number_35_45',
    'anteil_35_45': 'percentage_35_45',
    'anzahl_45_55': 'number_45_55',
    'anteil_45_55': 'percentage_45_55',
    'anzahl_55_65': 'number_55_65',
    'anteil_55_65': 'percentage_55_65',
    'anzahl_65_75': 'number_65_75',
    'anteil_65_75': 'percentage_65_75',
    'anzahl_75_aelter': 'number_75_older',
    'anteil_75_aelter': 'percentage_75_older',
    'abs_bestandsveraenderung': 'absolute_population_change',
    'rel_bestandsveraenderung': 'relative_population_change',
    'bestandsveraaenderung_je_1000': 'population_change_per_1000',
    'anzahl_zuzuege': 'number_in_migrants',
    'zuzuege_je_1000': 'in_migrants_per_1000',
    'anzahl_wegzuege': 'number_out_migrants',
    'wegzuege_je_1000': 'out_migrants_per_1000',
    'wanderungssaldo': 'migration_balance',
    'wanderungssaldo_je_1000': 'migration_balance_per_1000',
    'anteil_ledige': 'percentage_single',
    'anteil_verheiratete': 'percentage_married',
    'anteil_verwitwete': 'percentage_widowed',
    'anteil_geschiedene': 'percentage_divorced',
    'anzahl_maennlich': 'number_male',
    'anteil_maennlich': 'percentage_male',
    'anzahl_weiblich': 'number_female',
    'anteil_weiblich': 'percentage_female',
    'einwohnerzahl': 'population',
    'bevoelkerungsdichte': 'population_density',
    'anteil_deutsch': 'percentage_german',
    'anteil_auslaendisch': 'percentage_foreign',
    'anzahl_haushalte': 'number_households',
    'anteil_single': 'percentage_single',
    'anteil_single_juenger_30': 'percentage_single_younger_30',
    'anteil_single_65_aelter': 'percentage_single_65_older',
    'anteil_mit_kindern': 'percentage_with_children',
    'anzahl_lebendgeborene': 'number_live_births',
    'lebendgeborene_je_1000': 'live_births_per_1000',
    'geburtenrate': 'birth_rate',
    'anzahl_gestorbene': 'number_deaths',
    'gestorbene_je_1000': 'deaths_per_1000',
    'geburten_sterbesaldo': 'birth_death_balance',
    'geburten_sterbesaldo_je_1000': 'birth_death_balance_per_1000'
}

combined_data.rename(columns=column_rename_map, inplace=True)

# Save the combined data to an Excel file
combined_data.to_excel('Reports/Rostock.xlsx', index=False)