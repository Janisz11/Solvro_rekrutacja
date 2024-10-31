import pandas as pd
from category import process_category_column
from glass import process_glass_column
from tags import process_tags_column
from instructions import process_instructions_column
from ingredients import process_ingredients_column
cocktail_df = pd.read_json('C:\\Users\\kjani\\PycharmProjects\\Solvro_Rekrutacja\\data\\cocktail_dataset.json')


# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_columns', None)
print(cocktail_df.head())

cocktail_df.info()

print(cocktail_df.shape)

print(cocktail_df['alcoholic'].value_counts())

# kolumna alkoholi zawiera same 1 wiec jest bezuzyteczna
cocktail_df = cocktail_df.drop(['id', 'name','imageUrl','alcoholic','createdAt', 'updatedAt'], axis=1)

print(cocktail_df.columns)

cocktail_df =process_category_column(cocktail_df)
print("")

cocktail_df = process_glass_column(cocktail_df)

cocktail_df = process_tags_column(cocktail_df)

cocktail_df = process_instructions_column(cocktail_df)

cocktail_df = process_ingredients_column(cocktail_df)


pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
print(cocktail_df.head(5))