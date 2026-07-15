from excel_reader import ExcelReader

reader = ExcelReader(
    "../data/trainers.xlsx",
    "Technical trainer"
)

df = reader.read_data()

print()

print("Total Trainers :", len(df))

print()

print(df.head())