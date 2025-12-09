import pandas as pd

lingas = pd.read_csv("Jyotirlingas.csv")

for index, row in lingas.iterrows():
    print(f"Row: {index + 1}")
    print(f"Name: {row.temple_name}")
    print(f"Latitude: {row.latitude}")
    print(f"Longitude: {row.longitude}")

