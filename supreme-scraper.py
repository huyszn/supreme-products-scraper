import requests, json
from datetime import datetime
import pandas as pd
from fp.fp import FreeProxy

def category_dict(category_items):
    """
    Parse products in a category to a dictionary

    Parameters
    ----------
    @results_items [list]: List of products in a category

    Returns
    -------
    [dictionary] all products and their attributes for a category
    """
    c_name = [category_items[item]['name'] for item in range(len(category_items))]
    c_id = [int(category_items[item]['id']) for item in range(len(category_items))]
    c_image_url = [category_items[item]['image_url'].replace("//", "") for item in range(len(category_items))]
    c_image_url_hi = [category_items[item]['image_url_hi'].replace("//", "") for item in range(len(category_items))]
    c_price = [float(f"{category_items[item]['price']/ 100.:.2f}") for item in range(len(category_items))]
    c_sale_price = [float(f"{category_items[item]['sale_price']/ 100.:.2f}") for item in range(len(category_items))]
    # euros
    if 'price_euro' in category_items[0]:
        c_price_euro = [float(f"{category_items[item]['price_euro']/ 100.:.2f}") for item in range(len(category_items))]
        c_sale_price_euro = [float(f"{category_items[item]['sale_price_euro']/ 100.:.2f}") for item in range(len(category_items))]
    c_new_item = [category_items[item]['new_item'] for item in range(len(category_items))]
    c_position = [int(category_items[item]['position']) for item in range(len(category_items))]
    c_category_name = [category_items[item]['category_name'] for item in range(len(category_items))]
    c_description = []
    c_colors = []
    product_colors = []
    # to do: get both size, and stock level from the below for loop like with description and color
    for item in c_id:
        product_json = requests.get(f"https://www.supremenewyork.com/shop/{item}.json", headers=headers, proxies=proxy).json()
        c_description.append(product_json['description'])
        # get all colors for one product
        for i in range(len(product_json['styles'])):
            product_colors.append(product_json['styles'][i]['name'])
        c_colors.append(product_colors)
        # clear list for next product
        product_colors = []

    # EU
    if 'price_euro' in category_items[0]:
        category_results = {'Name': c_name, 'ID': c_id, 'Image URL': c_image_url, 'Image URL Hi': c_image_url_hi, 'Price': c_price, 'Sale Price': c_sale_price, 'Euro Price': c_price_euro, 'Euro Sale Price': c_sale_price_euro, 'New Item': c_new_item, 'Position': c_position, 'Category Name': c_category_name, 'Description': c_description, 'Colors': c_colors}
    # NA / JP
    else:
        category_results = {'Name': c_name, 'ID': c_id, 'Image URL': c_image_url, 'Image URL Hi': c_image_url_hi, 'Price': c_price, 'Sale Price': c_sale_price, 'New Item': c_new_item, 'Position': c_position, 'Category Name': c_category_name, 'Description': c_description, 'Colors': c_colors}
    
    return category_results

# NO_PROXY = False: Use proxy for scraping
# NO_PROXY = True: Do not use proxy for scraping
NO_PROXY = False

proxy = {'http': (FreeProxy(country_id='US', rand=True)).get()}
#print(proxy)

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1'
}

def main():
    #### REQUEST JSON FROM URL
    if NO_PROXY:
        r = requests.get("https://www.supremenewyork.com/mobile_stock.json", headers=headers)
    else:
        r = requests.get("https://www.supremenewyork.com/mobile_stock.json", headers=headers, proxies=proxy)
    json_r = r.json()
    with open('mobile_stock.json', 'w') as f:
        json.dump(json_r, f)

    #### LOAD DOWNLOADED JSON
    #r = open('mobile_stock_jp.json')
    #json_r = json.load(r)

    release_date = datetime.strptime(json_r["release_date"], "%m/%d/%Y").strftime('%B %d %Y')
    week_num = json_r["release_week"].split("F")[0]
    season = json_r["release_week"][1:]
    release_week = f"Week {week_num} of {season}"
    title = f"Supreme Products for the Week of {release_date} ({release_week})"

    categories = json_r['products_and_categories']
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

    category_df = {}
    for c in category_list:
        # get names of variables from category_list as strings
        c_list = [key for key, value in locals().items() if value == c]
        category_name = c_list[0]

        # if the category is not empty (Ex. shoes don't always drop every week)
        if c:
            # EU
            if 'Euro Price' in c:
                category_df[f"{category_name}_df"] = pd.DataFrame({'Name': c['Name'], 'ID': c['ID'], 'Image URL': c['Image URL'], 'Image URL Hi': c['Image URL Hi'], 'Price': c['Price'], 'Sale Price': c['Sale Price'], 'Euro Price': c['Euro Price'], 'Euro Sale Price': c['Euro Sale Price'], 'New Item': c['New Item'], 'Position': c['Position'], 'Category Name': c['Category Name'], 'Description': c['Description'], 'Colors': c['Colors']})
            # NA / JP
            else:
                category_df[f"{category_name}_df"] = pd.DataFrame({'Name': c['Name'], 'ID': c['ID'], 'Image URL': c['Image URL'], 'Image URL Hi': c['Image URL Hi'], 'Price': c['Price'], 'Sale Price': c['Sale Price'], 'New Item': c['New Item'], 'Position': c['Position'], 'Category Name': c['Category Name'], 'Description': c['Description'], 'Colors': c['Colors']})

    # Excel file with separate sheets for each category
    writer = pd.ExcelWriter(f'./data/{title}-Sheets.xlsx', engine='openpyxl')

    for category_name, df in category_df.items():
        # remove brackets from colors
        df['Colors'] = df['Colors'].str.join(',')
        df.to_excel(writer, sheet_name=category_name, index=False)

    writer.save() 

    # Excel file with all products on one sheet
    # get all products in each category into one list
    one_list = [v for k,v in category_df.items()] 
    # concatenate all products by row into one dataframe
    one_df = pd.concat(one_list ,axis=0)

    one_df.to_excel(f'./data/{title} - One Sheet.xlsx', engine='openpyxl', sheet_name='Products', index=False)

    # CSV file with all products
    one_df.to_csv(f'./data/{title} - CSV.csv', index=False)

if __name__ == '__main__':
    main()