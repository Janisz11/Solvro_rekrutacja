from collections import Counter

import pandas as pd
import re

def process_instructions_column(cocktail_df):
    print("")
    print("PRZETWARZANIE KOLUMNY INSTRUCTIONS")

    print("")
    show_instructions(cocktail_df)
    print("")

    cocktail_df = calculate_instruction_length(cocktail_df)
    print("")
    print(cocktail_df.columns)
    print("")
    print(cocktail_df['instruction_length'])
    print("")

    cocktail_df['cleaned_instructions'] = cocktail_df['instructions'].apply(clean_instruction)

    all_words = ' '.join(cocktail_df['cleaned_instructions']).split()

    word_counts = Counter(all_words)

    most_common_words = word_counts.most_common(20)
    print("Najczęściej używane słowa:")
    for word, count in most_common_words:
        print(f"{word}: {count}")

# Wydzielamy z instrukcji informacje o narzadziach potrzebnych do przygotowania drinka co takze nam powie o tym jak trudno jest wykonać danego drinka
# Oprócz tego sprawdzamy czy drink jest dekorowany sprawdzając zawartość słowa garnish
    cocktail_df['requires_shaker'] = cocktail_df['cleaned_instructions'].apply(lambda x: 1 if 'shake' in x else 0)
    cocktail_df['requires_stirring_spoon'] = cocktail_df['cleaned_instructions'].apply(
        lambda x: 1 if 'stir' in x else 0)
    cocktail_df['requires_strainer'] = cocktail_df['cleaned_instructions'].apply(lambda x: 1 if 'strain' in x else 0)
    cocktail_df['garnish'] = cocktail_df['cleaned_instructions'].apply(lambda x: 1 if 'garnish' in x else 0)

#Usuwamy kolumny już niepotrzbne
    cocktail_df = cocktail_df.drop(columns=['instructions', 'cleaned_instructions'])

    print(cocktail_df.columns)
    print("")
    print(cocktail_df['garnish'])

    return cocktail_df



def show_instructions(cocktail_df):
    for i in range(10):
        print("")
        print(cocktail_df.iloc[i]['instructions'])


def calculate_instruction_length(df):
    df['instruction_length'] = df['instructions'].apply(lambda x: len(x) if isinstance(x, str) else 0)
    return df


import re

unwanted_words = ['and', 'or', 'then', 'with', 'into', 'the', 'a', 'in', ' ']
unwanted_symbols = r'[.,]'


def clean_instruction(instruction):
    words = instruction.lower().split()
    cleaned_words = [word for word in words if word not in unwanted_words]

    cleaned_text = " ".join(cleaned_words)

    cleaned_text = re.sub(unwanted_symbols, '', cleaned_text)
    return cleaned_text


