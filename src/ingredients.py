import pandas as pd
import re
from collections import Counter
def process_ingredients_column(cocktail_df):
    print("\nPRZETWARZANIE KOLUMNY INGREDIENTS\n")
    print(cocktail_df.iloc[0]['ingredients'], "\n")

    print("Po oczyszczeniu")
    cocktail_df['ingredients'] = cocktail_df['ingredients'].apply(clean_ingredient_data)

    print_ingeredients(cocktail_df)


    cocktail_df['ingredients'] = cocktail_df['ingredients'].apply(lambda x: Quick_Fix(x, cocktail_df))


    print("")
    print("\n", cocktail_df.iloc[0]['ingredients'])


    cocktail_df['type_counts'] = cocktail_df['ingredients'].apply(count_types)
    print("")
    print(cocktail_df['type_counts'])

    print(amount_of_types(cocktail_df))
# Widać że będzie można pogrupować według głownego alkoholu znajdującego się w drinku
# Sprawdzamy nazwy składników by zobaczyć czy można je jakoś pogrupować
    ingredient_counts = get_ingredient_counts(cocktail_df)

    print("")
    for ingredient, count in ingredient_counts.most_common():
        print(f"{ingredient}: {count}")


#Drop bo juz niepotrzebna
    cocktail_df.drop(columns=['type_counts'], inplace=True)

#Podział według smaku
    cocktail_df[['sour_count', 'sweet_count', 'bitter_count', 'refreshing_count', 'creamy_count', 'herbal_count']] = \
    cocktail_df['ingredients'].apply(count_flavors)

    print("")
    print(cocktail_df.columns)


# Teraz podzielmy według głownego alkoholu znajdującego się w drinku
    main_alcohol_columns_df = cocktail_df['ingredients'].apply(categorize_main_alcohol_columns).apply(pd.Series)

    cocktail_df = pd.concat([cocktail_df, main_alcohol_columns_df], axis=1)

# Whiskey i Whisky to to samo zależna nazwa tylko od regionu nie potrzebujemy dwóch kolumn
    cocktail_df["Whiskey"] = cocktail_df[["Whiskey", "Whisky"]].max(axis=1)

    cocktail_df = cocktail_df.drop(columns=["Whisky"])

    print(cocktail_df.columns)
    print(cocktail_df['Whiskey'])
    print_ingeredients(cocktail_df)

# przeliczmy ilość alkoholowych składników
    cocktail_df['alcoholic_ingredient_count'] = cocktail_df['ingredients'].apply(count_alcoholic_ingredients)

# W Polu percentage jest wiele pustych miejsc  przypiszmy standardowe %  danych rodzajów alkoholu naszym składnikom
    cocktail_df["ingredients"] = cocktail_df["ingredients"].apply(
        lambda ingredients: [fill_missing_percentage(ingredient) for ingredient in ingredients]
    )

    print(cocktail_df.iloc[21]['ingredients'])

# Spróbujmy policzyć jak mocne są koktajle to pomoze w klasyfikacji
    display_unique_measures(cocktail_df)


#Sprawdzamy puste wartosci
    find_none_ingredients(cocktail_df)

    assign_default_measures(cocktail_df)

    print("")
    find_none_ingredients(cocktail_df)
    print("")
    find_none_ingredients_without_null(cocktail_df)

    apply_index_based_measures(cocktail_df, index_measure_updates)

    print(find_none_ingredients_without_null(cocktail_df))

#policzymy zawartości coktailu
    calculate_total_volume(cocktail_df)
#policzymy alkohol
    calculate_alcohol_content_per_ingredient(cocktail_df)

    find_missing_alcohol_content(cocktail_df)

    print(cocktail_df.iloc[0]['ingredients'])

    cocktail_df['total_alcohol'] = cocktail_df['ingredients'].apply(sum_total_alcohol)

    cocktail_df['total_alcohol_ml'] = cocktail_df['total_alcohol']

    cocktail_df = cocktail_df.drop('total_alcohol', axis=1)

#tworzymy kolumne liczaca moc drinka
    cocktail_df['strength_percentage'] = (cocktail_df['total_alcohol_ml'] / cocktail_df['total_volume_ml']) * 100

    cocktail_df['strength_percentage'] = cocktail_df['strength_percentage'].round(2)

    sorted_strength = cocktail_df['strength_percentage'].sort_values(ascending=False)

    print(sorted_strength)

    cocktail_df = cocktail_df.drop(columns=['total_alcohol_ml', 'ingredients'])

    print(cocktail_df.columns)

    return cocktail_df



def clean_ingredient_data(ingredients_list):
    # Define keys to remove
    keys_to_remove = ['id', 'createdAt', 'updatedAt', 'imageUrl', 'description']

    # Remove specified keys from each dictionary in the ingredients list
    for ingredient in ingredients_list:
        for key in keys_to_remove:
            ingredient.pop(key, None)

    return ingredients_list

def print_ingeredients(cocktail_df):
    for i in range(5):
        print(cocktail_df.iloc[i]['ingredients'])
        print("")


def Quick_Fix(ingredients_list,cocktail_df):
    cocktail_df.loc[16, "ingredients"][0]["type"] = "Vodka"
    cocktail_df.loc[129, "ingredients"][0]["measure"] = "1 1/2 oz"
    for ingredient in ingredients_list:
        if ingredient['name'] == 'Soda water':
            ingredient['alcohol'] = 0
    return ingredients_list


def count_types(ingredients_list):
    type_counts = {}
    for ingredient in ingredients_list:
        if ingredient['type']:
            type_counts[ingredient['type']] = type_counts.get(ingredient['type'], 0) + 1
    return type_counts


def amount_of_types(cocktail_df):


    type_counter = Counter()

    for types in cocktail_df['type_counts']:
        type_counter.update(types)

    type_counts_total = dict(type_counter)

    return type_counts_total

def get_ingredient_counts(df):
    ingredient_counts = Counter()
    for row in df['ingredients']:
        for ingredient in row:
            ingredient_counts[ingredient['name']] += 1
    return ingredient_counts

def count_flavors(ingredients):
    flavor_mapping = {
    'sour': ['Lemon Juice', 'Lime Juice', 'Lemon', 'Lime', 'Cherry', 'Grapefruit Juice', 'Orange'],
    'sweet': ['Sugar', 'Powdered Sugar', 'Sugar Syrup', 'Grenadine', 'Orgeat Syrup', 'Honey', 'Amaretto', 'Maraschino Cherry', 'Kahlua', 'Blue Curacao', 'Triple Sec', 'Sweet Vermouth', 'Pineapple', 'Pineapple Juice', 'Strawberries', 'Banana', 'Coca-Cola', 'Orange Juice'],
    'bitter': ['Bitters', 'Orange Bitters', 'Angostura Bitters', 'Campari', 'Orange Peel', 'Lemon Peel', 'Orange Spiral'],
    'refreshing': ['Soda Water', 'Carbonated Water', 'Club Soda', 'Tonic Water', 'Lemon-lime Soda'],
    'creamy': ['Light Cream', 'Heavy Cream', 'Whipped Cream', 'Egg White', 'Egg Yolk', 'Milk'],
    'herbal': ['Mint', 'Nutmeg', 'Celery Salt', 'Green Chartreuse', 'Yellow Chartreuse', 'Tea']
}
    counts = {'sour_count': 0, 'sweet_count': 0, 'bitter_count': 0, 'refreshing_count': 0, 'creamy_count': 0, 'herbal_count': 0}
    for ingredient in ingredients:
        name = ingredient['name']
        for flavor, items in flavor_mapping.items():
            if name in items:
                counts[f"{flavor}_count"] += 1
    return pd.Series(counts)


def categorize_main_alcohol_columns(ingredients_list):
    main_alcohols = ["Whiskey", "Whisky", "Vodka", "Gin", "Rum", "Brandy", "Spirit"]
    alcohol_presence = {alcohol: 0 for alcohol in main_alcohols}

    for ingredient in ingredients_list:
        ingredient_type = ingredient.get("type")
        if ingredient_type in main_alcohols:
            alcohol_presence[ingredient_type] = 1

    return alcohol_presence

def count_alcoholic_ingredients(ingredients_list):

    return sum(1 for ingredient in ingredients_list if ingredient.get("alcohol") == 1)


def fill_missing_percentage(ingredient):
    standard_percentages = {
        "Vodka": 40,
        "Gin": 40,
        "Whiskey": 40,
        "Whisky": 40,
        "Rum": 40,
        "Brandy": 40,
        "Spirit": 40,
        "Liqueur": 20,
        "Liquer": 20,
        "Fortified Wine": 18,
        "Beer": 5,
        "Wine": 12,
    }

    if ingredient.get("percentage") is None and ingredient.get("alcohol") == 1:
        alcohol_type = ingredient.get("type")
        ingredient["percentage"] = standard_percentages.get(alcohol_type, 0)
    return ingredient


def display_unique_measures(df):
    unique_measures = set()
    for row in df['ingredients']:
        for ingredient in row:
            measure = ingredient.get('measure')
            if measure:
                unique_measures.add(measure)

    for measure in sorted(unique_measures):
        print(measure)


def convert_to_ml(measure):
    conversion_to_ml = {
        'oz': 29.57,
        'tblsp': 14.79,
        'tsp': 4.93,
        'dash': 0.92,
        'cl': 10,
        'piece': 15,
        'slice': 15,
        'wedge': 15,
        'whole': 30,
        'cube': 4,
        'cup': 240,
        'chunk': 15,
        'drop': 0.05,
        '(Claret)': 150,
        'juice of 1': 45,
        'juice of 1/2': 22.5,
        'juice of 1/4': 11.25,
        '2 or 3': 30,
        '2-3 drops': 0.1,
        '2-4': 60,
        'Chilled': 60,
        'Coarse': 0,
        'Bourbon': 45,
        'Cherry': 5,
        'Olive': 5,
        'Maraschino Cherry': 5,
        'Lime': 15,
        'Egg White': 30,
        'Orange': 30,
        'Banana': 30,
        'Sugar': 5,
        'lemon': 15,
        'Egg Yolk': 15,
        'Pineapple': 15,
        'Strawberries': 5,
        # Ręczne przypisania
        "2-3 oz": 75,
        "1 oz": 29.57,
        "1/2 oz": 14.79,
        "1/2 oz white": 14.79,
        "1 oz white": 29.57,
        "1 1/2 oz": 44.36,
        "1/2 tsp": 2.46,
        "3/4 oz": 22.18,
        "1 1/2 tsp": 7.39,
        "3/4 oz white": 22.18
    }

    measure = re.sub(r'\s+', ' ', measure.strip())

    if measure in conversion_to_ml:
        return conversion_to_ml[measure]

    match = re.match(
        r'(\d+ \d+/\d+|\d+/\d+|\d+\.\d+|\d+)\s*(\w+)?(?:\s*(white|oz|tsp|tblsp|cl|dash|cup|drop|chunk|cube))?', measure)
    if match:
        amount = match.group(1)
        unit = match.group(2) or ""
        additional_unit = match.group(3)

        if " " in amount:
            whole, fraction = amount.split()
            numerator, denominator = map(int, fraction.split('/'))
            amount = int(whole) + (numerator / denominator)
        elif '/' in amount:
            numerator, denominator = map(int, amount.split('/'))
            amount = numerator / denominator
        else:
            amount = float(amount)

        if (unit and 'ml' in unit.lower()) or (additional_unit and 'ml' in additional_unit):
            return round(amount, 2)  # Jeśli już w mililitrach, nie trzeba przeliczać
        elif unit in conversion_to_ml:
            return round(amount * conversion_to_ml[unit], 2)
        elif additional_unit in conversion_to_ml:
            return round(amount * conversion_to_ml[additional_unit], 2)

    if "juice of 1" in measure.lower():
        return 45
    elif "juice of 1/2" in measure.lower():
        return 22.5
    elif "juice of 1/4" in measure.lower():
        return 11.25
    elif "dash" in measure.lower():
        dash_count = measure.split()[0] if measure.split()[0].isdigit() else 1
        return round(int(dash_count) * conversion_to_ml['dash'], 2)
    elif "twist" in measure.lower() or "splash" in measure.lower():
        return 5

    return None


def find_none_ingredients(df):
    results = {}
    for index, row in df.iterrows():
        none_ingredients = []
        for ingredient in row['ingredients']:
            measure = ingredient.get('measure')
            if measure in ['1', '2', '4', '4.5 cL', '2-3 oz', '3 chunks', '4 chunks', '6'] or measure is None:
                none_ingredients.append(ingredient['name'])
        if none_ingredients:
            results[index] = none_ingredients

    # Wyświetlenie wyników
    for index, ingredients in results.items():
        print(f"Index {index} - Missing measure values for ingredients: {', '.join(ingredients)}")


def assign_default_measures(df):
    default_measures = {
        "Carbonated Water": "60 ml",
        "Soda water": "60 ml",
        "Bourbon": "45 ml",
        "Salt": "1 ml",
        "Nutmeg": "1 ml",
        "Club Soda": "60 ml",
        "Lemon Peel": "1 ml",
        "Cherry": "5 ml",
        "Lemonade": "60 ml",
        "Coca-Cola": "60 ml",
        "Orange spiral": "1 ml",
        "Powdered Sugar": "5 ml",
        "Pineapple": "15 ml",
        "Gin": "45 ml",
        "Dry Vermouth": "15 ml",
        "Lemon": "15 ml",
        "Ginger Ale": "60 ml",
        "Lemon-lime soda": "60 ml"
    }

    for row in df['ingredients']:
        for ingredient in row:
            name = ingredient.get('name')
            if name in default_measures and (ingredient.get('measure') is None or ingredient['measure'] == ''):
                ingredient['measure'] = default_measures[name]

def find_none_ingredients_without_null(df):
    results = {}
    for index, row in df.iterrows():
        none_ingredients = []
        for ingredient in row['ingredients']:
            measure = ingredient.get('measure')
            if measure in ['1 ', '2 ', '4', '4.5 cL', '2-3 oz', '3 chunks', '4 chunks', '6'] :
                none_ingredients.append(ingredient['name'])
        if none_ingredients:
            results[index] = none_ingredients


    for index, ingredients in results.items():
        print(f"Index {index} - Missing measure values for ingredients: {', '.join(ingredients)}")


def apply_index_based_measures(df, updates):


    for index, ingredients in updates.items():
        for ingredient in df.at[index, 'ingredients']:
            name = ingredient.get('name')
            if name in ingredients:
                ingredient['measure'] = ingredients[name]


index_measure_updates = {
        1: {"Bourbon": "45 ml"},
        4: {"Cherry": "5 ml"},
        5: {"Olive": "5 ml"},
        8: {"Maraschino Cherry": "5 ml"},
        10: {"Lime": "15 ml"},
        20: {"Egg White": "30 ml"},
        23: {"Lime": "15 ml"},
        29: {"Egg White": "30 ml", "Orange": "15 ml"},
        30: {"Lime": "15 ml"},
        35: {"Banana": "30 ml", "Cherry": "5 ml"},
        44: {"Maraschino Cherry": "5 ml"},
        46: {"Maraschino Cherry": "5 ml"},
        48: {"Cherry": "5 ml", "Egg White": "30 ml"},
        49: {"Maraschino Cherry": "5 ml", "Orange": "15 ml", "Sugar": "5 ml"},
        51: {"Maraschino Cherry": "5 ml", "Orange": "15 ml"},
        52: {"Egg White": "30 ml"},
        53: {"lemon": "15 ml", "Maraschino Cherry": "5 ml", "Orange": "15 ml"},
        55: {"Cherry": "5 ml"},
        56: {"Lime": "15 ml"},
        59: {"Egg Yolk": "15 ml"},
        62: {"Egg White": "30 ml"},
        67: {"Lime": "15 ml"},
        71: {"Cherry": "5 ml"},
        76: {"Cherry": "5 ml"},
        80: {"Lime": "15 ml"},
        82: {"Maraschino Cherry": "5 ml", "Orange": "15 ml"},
        85: {"Cherry": "5 ml"},
        86: {"Maraschino Cherry": "5 ml", "Orange": "15 ml"},
        87: {"Pineapple": "45 ml", "Strawberries": "10 ml"},  # 3 chunks of Pineapple, 2 Strawberries
        93: {"Pineapple": "15 ml"},
        97: {"Olive": "5 ml"},
        99: {"Cherry": "5 ml"},
        101: {"Egg White": "30 ml"},
        103: {"Maraschino Cherry": "5 ml", "Orange": "15 ml"},
        107: {"Egg White": "30 ml"},
        113: {"Cherry": "5 ml"},
        114: {"Cherry": "5 ml"},
        115: {"Olive": "5 ml"},
        123: {"Egg White": "30 ml"}
    }


def calculate_total_volume(df):
    total_volumes = []

    for index, row in df.iterrows():
        total_volume = 0
        for ingredient in row['ingredients']:
            measure = ingredient.get('measure')
            if measure:
                # Przypisanie wielkości w ml
                volume = convert_to_ml(measure)
                if volume is not None:
                    total_volume += volume

        total_volumes.append(total_volume)

    df['total_volume_ml'] = total_volumes


def calculate_alcohol_content_per_ingredient(df):
    for row in df['ingredients']:
        for ingredient in row:
            if ingredient.get('alcohol') == 1:

                measure = ingredient.get('measure')
                percentage = ingredient.get('percentage')

                if measure and percentage:

                    volume_ml = convert_to_ml(measure)
                    if volume_ml:

                        ingredient['total_alcohol_content'] = round(volume_ml * (percentage / 100), 2)
                    else:
                        ingredient['total_alcohol_content'] = None
                else:
                    ingredient['total_alcohol_content'] = None


def find_missing_alcohol_content(df):
    for index, row in df.iterrows():
        missing_details = []
        for ingredient in row['ingredients']:
            if ingredient.get('alcohol') == 1 and ingredient.get('total_alcohol_content') is None:
                missing_details.append(f"{ingredient['name']} (Measure: {ingredient.get('measure')})")

        if missing_details:
            print(f"Index {index} - Ingredients with missing alcohol content:")
            for detail in missing_details:
                print(f"  {detail}")
            print()
def sum_total_alcohol(ingredients):
    total = 0
    for ingredient in ingredients:
        tac = ingredient.get('total_alcohol_content', 0)
        if tac is None:
            tac = 0
        total += tac
    return total

