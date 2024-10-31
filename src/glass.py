import pandas as pd


def process_glass_column(cocktail_df):

    print("")
    print("PRZETWARZANIE KOLUMNY GLASS")
    print("")

    glass_unique_values = cocktail_df['glass'].unique()

    glass_value_counts = cocktail_df['glass'].value_counts()

    print(glass_unique_values, glass_value_counts)


    top_glasses = ['Cocktail glass', 'Old-fashioned glass', 'Highball glass', 'Whiskey sour glass', 'Collins glass',
                   'Champagne flute']

    cocktail_df['glass'] = cocktail_df['glass'].apply(lambda x: x if x in top_glasses else 'Other')

    cocktail_df = pd.get_dummies(cocktail_df, columns=['glass'], drop_first=True)

    cocktail_df.columns.tolist()

    cocktail_df = cocktail_df.applymap(lambda x: 1 if x is True else (0 if x is False else x))

    print("")
    print(cocktail_df.columns)
    print("")
    print(cocktail_df['glass_Highball glass'])




    return cocktail_df
