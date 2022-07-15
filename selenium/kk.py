import pandas as pd

url = 'save/reviews/경제경영.csv'
df = pd.read_csv(url)
df.drop_duplicates(inplace=True)
print(df)