import pandas as pd
from collections import Counter
from itertools import chain
def process_tags_column(cocktail_df):
    print("")
    print("PRZETWARZANIE KOLUMNY TAGS")



    print("")
    print(cocktail_df.iloc[0]['tags'])
    print("")
    print(cocktail_df['tags'].apply(type).value_counts())
#Widać dużo none wartości
    tag_count(cocktail_df)

    cocktail_df = add_tag_columns(cocktail_df)
    cocktail_df = cocktail_df.drop(['tags'], axis=1)

    print("")
    print(cocktail_df.columns)
    print(cocktail_df['IBA'])

    return cocktail_df

def tag_count(cocktail_df):
    tags_not_null_df = cocktail_df[cocktail_df['tags'].notnull()]


    total_tags = tags_not_null_df['tags'].apply(len).sum()



    all_tags = list(chain.from_iterable(tags_not_null_df['tags']))

    unique_tags = set(all_tags)

    num_unique_tags = len(unique_tags)

    print(f"Number of unique tags: {num_unique_tags}")



    tag_counts = Counter(all_tags)


    tag_counts_df = pd.DataFrame.from_dict(tag_counts, orient='index', columns=['count'])
    tag_counts_df = tag_counts_df.sort_values(by='count', ascending=False)

    print(tag_counts_df)


def add_tag_columns(df):
    tags_to_add = ['IBA', 'Classic', 'ContemporaryClassic']

    # Add binary columns for each tag
    for tag in tags_to_add:
        df[tag] = df['tags'].apply(lambda x: 1 if isinstance(x, list) and tag in x else 0)

    return df