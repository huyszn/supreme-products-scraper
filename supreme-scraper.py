import requests, json, argparse
from datetime import datetime
import pandas as pd
from fp.fp import FreeProxy
from typing import List, Dict, Union

def category_dict(category_products_list_dict: List[Dict[str, int]]) -> Dict[str, List[Union[str, int]]]:
    """
    Parse products in a category to a dictionary

    Parameters
    ----------
    @category_products_list_dict: List[Dict[str, int]]: List of products in a dictionary based on their category

    Returns
    -------
    @category_results: Dict[str, List[Union[str, int]]]: Dictionary of all products and their attributes in a list for a category
    """
    c_name = [category_products_list_dict[item]['name'] for item in range(len(category_products_list_dict))]
    c_id = [int(category_products_list_dict[item]['id']) for item in range(len(category_products_list_dict))]
    c_mobile_url = [f'https://www.supremenewyork.com/mobile/#products/{id}' for id in c_id]
    c_image_url = [category_products_list_dict[item]['image_url'].replace("//", "https://") for item in range(len(category_products_list_dict))]
    c_image_url_hi = [category_products_list_dict[item]['image_url_hi'].replace("//", "https://") for item in range(len(category_products_list_dict))]
    c_price = [f"{float(category_products_list_dict[item]['price']/ 100.):.2f}" for item in range(len(category_products_list_dict))]
    c_sale_price = [f"{float(category_products_list_dict[item]['sale_price']/ 100.):.2f}" for item in range(len(category_products_list_dict))]
    # euros
    if 'price_euro' in category_products_list_dict[0]:
        c_price_euro = [f"{float(category_products_list_dict[item]['price_euro']/ 100.):.2f}" for item in range(len(category_products_list_dict))]
        c_sale_price_euro = [f"{float(category_products_list_dict[item]['sale_price_euro']/ 100.):.2f}" for item in range(len(category_products_list_dict))]
    c_new_item = [category_products_list_dict[item]['new_item'] for item in range(len(category_products_list_dict))]
    c_position = [int(category_products_list_dict[item]['position']) for item in range(len(category_products_list_dict))]
    c_category_name = [category_products_list_dict[item]['category_name'] for item in range(len(category_products_list_dict))]
    c_description = []
    c_colors = []
    c_mobile_url_colors = []
    c_sizes = []
    c_stock_levels = [[]]
    product_colors = []
    product_sizes = []
    product_mobile_url_colors = []
    # to do: get stock level from the below for loop like with description, color, and size
    for item in c_id:
        if PROXY:
            product_json = requests.get(f"https://www.supremenewyork.com/shop/{item}.json", headers=headers, proxies=free_proxy).json()
        else:
            product_json = requests.get(f"https://www.supremenewyork.com/shop/{item}.json", headers=headers).json()
        # get description for one product
        c_description.append(product_json['description'])
        # get all sizes for one product
        for i in range(len(product_json['styles'][0]['sizes'])):
            product_sizes.append(product_json['styles'][0]['sizes'][i]['name'])
        c_sizes.append(product_sizes)
        # get all colors, mobile URLs for each color, and stock levels for all sizes for each color for one product
        for color in range(len(product_json['styles'])):
            # colors
            product_colors.append(product_json['styles'][color]['name'])
            # mobile URLs for each color
            product_mobile_url_colors.append(f"https://www.supremenewyork.com/mobile/#products/{item}/{product_json['styles'][color]['id']}")
            # stock levels for all sizes for each color
            color_name = product_json['styles'][color]['name']
            # append stock levels for the color in the empty list created in c_stock_levels
            for size in range(len(product_json['styles'][color]['sizes'])):
                c_stock_levels[-1].append(product_json['styles'][color]['sizes'][size]['stock_level'])
            c_stock_levels[-1].append(f'END OF STOCK FOR {color_name}')
        c_colors.append(product_colors)
        c_mobile_url_colors.append(product_mobile_url_colors)
        # clear lists for next product
        product_colors = []
        product_mobile_url_colors = []
        product_sizes = []
        # append empty list for stock levels of next product
        c_stock_levels.append([])
    # remove the last empty list when iterated through all products in a category
    c_stock_levels = c_stock_levels[:-1]

    # EU
    if 'price_euro' in category_products_list_dict[0]:
        category_results = {'Name': c_name, 'ID': c_id, 'Mobile URL': c_mobile_url, 'Image URL': c_image_url, 'Image URL Hi': c_image_url_hi, 'Price': c_price, 'Sale Price': c_sale_price, 'Euro Price': c_price_euro, 'Euro Sale Price': c_sale_price_euro, 'New Item': c_new_item, 'Position': c_position, 'Category Name': c_category_name, 'Description': c_description, 'Colors': c_colors, 'Mobile URL Colors': c_mobile_url_colors, 'Sizes': c_sizes, 'Stock Levels': c_stock_levels}
    # NA / JP
    else:
        category_results = {'Name': c_name, 'ID': c_id, 'Mobile URL': c_mobile_url, 'Image URL': c_image_url, 'Image URL Hi': c_image_url_hi, 'Price': c_price, 'Sale Price': c_sale_price, 'New Item': c_new_item, 'Position': c_position, 'Category Name': c_category_name, 'Description': c_description, 'Colors': c_colors, 'Mobile URL Colors': c_mobile_url_colors, 'Sizes': c_sizes, 'Stock Levels': c_stock_levels}
    
    return category_results

def category_dict_to_dfs(category_list_dict: List[Dict[str, List[Union[str, int]]]], name_list: List[str]) -> Dict[str, pd.DataFrame]:
    """
    Convert list of category dictionaries to dictionary of multiple dataframes of products based on their category

    Parameters
    ----------
    @category_list_dict: List[Dict[str, List[Union[str, int]]]]: Dictionary of all products and their attributes in a list for a category
    @name_list: List[str]: List of category names in strings
    Returns
    -------
    @category_dict_dfs: Dict[str, pd.DataFrame]: Dictionary of products dataframes based on their category
    """
    category_dict_dfs = {}
    category_name_idx = 0
    for c in category_list_dict:
        # get name of the category as string
        category_name = name_list[category_name_idx]
        # if the category is not empty (Ex. shoes don't always drop every week)
        if c:
            # EU
            if 'Euro Price' in c:
                category_dict_dfs[f"{category_name}"] = pd.DataFrame({'Name': c['Name'], 'ID': c['ID'], 'Mobile URL': c['Mobile URL'], 'Image URL': c['Image URL'], 'Image URL Hi': c['Image URL Hi'], 'Price': c['Price'], 'Sale Price': c['Sale Price'], 'Euro Price': c['Euro Price'], 'Euro Sale Price': c['Euro Sale Price'], 'New Item': c['New Item'], 'Position': c['Position'], 'Category Name': c['Category Name'], 'Description': c['Description'], 'Colors': c['Colors'], 'Mobile URL Colors': c['Mobile URL Colors'], 'Sizes': c['Sizes'], 'Stock Levels': c['Stock Levels']})
            # NA / JP
            else:
                category_dict_dfs[f"{category_name}"] = pd.DataFrame({'Name': c['Name'], 'ID': c['ID'], 'Mobile URL': c['Mobile URL'], 'Image URL': c['Image URL'], 'Image URL Hi': c['Image URL Hi'], 'Price': c['Price'], 'Sale Price': c['Sale Price'], 'New Item': c['New Item'], 'Position': c['Position'], 'Category Name': c['Category Name'], 'Description': c['Description'], 'Colors': c['Colors'], 'Mobile URL Colors': c['Mobile URL Colors'], 'Sizes': c['Sizes'], 'Stock Levels': c['Stock Levels']})
        category_name_idx += 1
    return category_dict_dfs

def convert_to_one_df(category_dict_dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Concatenate all products by row into one dataframe

    Parameters
    ----------
    @category_dict_dfs: Dict[str, pd.DataFrame]: Dictionary of products dataframes based on their category
    Returns
    -------
    @df: pd.DataFrame: One dataframe of all products
    """
    # get all products in each category into one list
    dfs_list = [v for k,v in category_dict_dfs.items()] 
    # concatenate all products by row into one dataframe
    df = pd.concat(dfs_list ,axis=0)
    return df

# Parse arguments
parser = argparse.ArgumentParser(description='Scrapes all supremenewyork.com products information')
parser.add_argument('--proxy', '-p', action='store_true', help='Use free proxies to scrape supremenewyork.com', required=False)
args = parser.parse_args()

# PROXY = True: Use free proxy for scraping
# PROXY = False: Do not use free proxy for scraping
PROXY = args.proxy

if PROXY:
    print('Using free proxy.')
else:
    print('Not using free proxy.')

free_proxy = {'https': (FreeProxy(country_id=['US', 'CA', 'MX'], rand=True)).get()}
#print(proxy)

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1'
}

def main():
    #### REQUEST JSON FROM URL
    if PROXY:
        r = requests.get("https://www.supremenewyork.com/mobile_stock.json", headers=headers, proxies=free_proxy)
    else:
        r = requests.get("https://www.supremenewyork.com/mobile_stock.json", headers=headers)
    json_r = r.json()
    with open('./stock/mobile_stock.json', 'w') as f:
        json.dump(json_r, f)

    #### LOAD DOWNLOADED JSON
    #r = open('./stock/mobile_stock_jp.json')
    #json_r = json.load(r)

    # create title for Excel and CSV files
    release_date = datetime.strptime(json_r["release_date"], "%m/%d/%Y").strftime('%B %d %Y')
    week_num = json_r["release_week"].split("F")[0]
    season = json_r["release_week"][1:]
    release_week = f"Week {week_num} of {season}"
    title = f"Supreme Products for the Week of {release_date} ({release_week})"

    categories = json_r['products_and_categories']
    # parse all products in a category to a dictionary
    Bags = category_dict(categories['Bags']) if 'Bags' in categories else []
    Skate = category_dict(categories['Skate']) if 'Skate' in categories else []
    Shirts = category_dict(categories['Shirts']) if 'Shirts' in categories else []
    Pants = category_dict(categories['Pants']) if 'Pants' in categories else []
    Shorts = category_dict(categories['Shorts']) if 'Shorts' in categories else []
    Tops_Sweaters = category_dict(categories['Tops/Sweaters']) if 'Tops/Sweaters' in categories else []
    T_Shirts = category_dict(categories['T-Shirts']) if 'T-Shirts' in categories else []
    Jackets = category_dict(categories['Jackets']) if 'Jackets' in categories else []
    Sweatshirts = category_dict(categories['Sweatshirts']) if 'Sweatshirts' in categories else []
    Hats = category_dict(categories['Hats']) if 'Hats' in categories else []
    Accessories = category_dict(categories['Accessories']) if 'Accessories' in categories else []
    Shoes = category_dict(categories['Shoes']) if 'Shoes' in categories else []

    category_list = [Bags, Skate, Shirts, Pants, Shorts, Tops_Sweaters, T_Shirts, Jackets, Sweatshirts, Hats, Accessories, Shoes]
    category_str_name_list = ['Bags', 'Skate', 'Shirts', 'Pants', 'Shorts', 'Tops_Sweaters', 'T-Shirts', 'Jackets', 'Sweatshirts', 'Hats', 'Accessories', 'Shoes']

    # make dictionaries in category_list into a dictionary of dataframes
    category_dfs = category_dict_to_dfs(category_list, category_str_name_list)

    # Excel file with separate sheets for each category
    writer = pd.ExcelWriter(f'./data/{title} - Sheets.xlsx', engine='xlsxwriter', engine_kwargs={'options': {'strings_to_numbers': True}})

    for category_name, df in category_dfs.items():
        # remove brackets from colors, sizes, and stock levels
        df['Colors'] = df['Colors'].str.join(',')
        df['Sizes'] = df['Sizes'].str.join(',')
        df['Stock Levels'] = df['Stock Levels'].apply(str).str.replace(r'\[','', regex=True)
        df['Stock Levels'] = df['Stock Levels'].apply(str).str.replace(r'\]','', regex=True)
        df['Mobile URL Colors'] = df['Mobile URL Colors'].apply(str).str.replace(r'\[','', regex=True)
        df['Mobile URL Colors'] = df['Mobile URL Colors'].apply(str).str.replace(r'\]','', regex=True)
        df.to_excel(writer, sheet_name=category_name, index=False)

    writer.save() 

    # Convert category_dfs into one dataframe of all products
    one_products_df = convert_to_one_df(category_dfs)

    # Excel file with all products on one sheet
    writer = pd.ExcelWriter(f'./data/{title} - One Sheet.xlsx', engine='xlsxwriter', engine_kwargs={'options': {'strings_to_numbers': True}})
    one_products_df.to_excel(writer, sheet_name='Products', index=False)
    writer.save() 

    # CSV file with all products
    one_products_df.to_csv(f'./data/{title} - CSV.csv', index=False)

    print('Finished exporting data to Excel and CSV files.')

if __name__ == '__main__':
    main()