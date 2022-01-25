import pandas as pd

df = pd.read_csv("Superstore.csv",encoding='windows-1254')

print(df.to_string()) 