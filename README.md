# Supreme Products Scraper

Web scraper that scrapes all products and their price, description, colors, sizes, and more from supremenewyork.com (Supreme New York). It then exports the extracted product information into two Excel files: one file with one sheet with all products, a second file with all products separated by categories into multiple sheets, and one CSV file containing all products.

## Requirements

```
$ pip install -r requirements.txt
```

## Usage

```
$ python3 supreme-scraper.py
```

### To change proxy settings, edit the `NO_PROXY` variable's value.

Run with proxies (most likely scrape NA site)
```
NO_PROXY = False
```

Run without proxies (not recommended unless you want to scrape products from the EU or JP site with your own IP or proxy that can access the EU or JP site)
```
NO_PROXY = True
```


## Things to work on

- Add stock level to the Excel/CSV files

## License

This project is licensed under the GPL 3.0 License - see the [LICENSE](LICENSE) file for details.