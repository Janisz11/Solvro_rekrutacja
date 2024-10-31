import pandas as pd


def process_category_column(cocktail_df):

    print("")
    print("PRZETWARZANIE KOLUMNY CATEGORY")
    print("")

    print(cocktail_df['category'].unique())


    cocktail_df = pd.get_dummies(cocktail_df, columns=['category'], drop_first=True)


    cocktail_df = cocktail_df.applymap(lambda x: 1 if x is True else (0 if x is False else x))

    print("")
    print(cocktail_df.columns)
    print(" ")
    print("Punch/Party Column: ")
    print(cocktail_df['category_Punch / Party Drink'])



    return cocktail_df

