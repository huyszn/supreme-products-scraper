# Supreme Products Scraper

Web scraper that scrapes all products and their price, description, colors, sizes, stock levels, and more from supremenewyork.com (Supreme New York). It then exports the extracted product information into two Excel files: one file with one sheet with all products, a second file with all products separated by categories into multiple sheets, and one CSV file containing all products.

## Requirements

```
$ pip install -r requirements.txt
```

## Usage

### Run with a proxy
This will most likely scrape the NA site.
```
$ python3 supreme-scraper.py -p
```
or
```
$ python3 supreme-scraper.py --proxy
```
If you get a proxy error, then rerun the script or try to run the script without a proxy.


### Run without a proxy
This is not recommended unless you:
- Want to scrape products from the EU or JP site with your own IP
- Have a proxy that can access the EU or JP site
- Found that none of the free proxies are working
```
$ python3 supreme-scraper.py
```

## Things to work on

- Add links to products and their colors to the Excel/CSV files

## License

This project is licensed under the GPL 3.0 License - see the [LICENSE](LICENSE) file for details.