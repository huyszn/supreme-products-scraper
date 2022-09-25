# Supreme Products Scraper

Web scraper that scrapes all products and their price, description, colors, sizes, stock levels, and more from supremenewyork.com (Supreme New York). It then exports the extracted product information into two Excel files: one file with one sheet with all products, a second file with all products separated by categories into multiple sheets, and one CSV file containing all products. The scraper works for the North America, Europe, and Japan store.

<b>[Here](sample%20data/Sample%20NA%20Supreme%20Products%20for%20the%20Week%20of%20September%2022%202022%20(Week%205%20of%20FW22)%20-%20CSV.csv) is an example of the CSV file outputted by the scraper.</b>

![Multiple sheets of products in an Excel file](images/Excel%20-%20Multiple%20Sheets.png)
<p align="center">
  <b>Excel File with products separated into multiple sheets by category</b>
</p>

![One sheet of products in an Excel file](images/Excel%20-%20One%20Sheet.png)

<p align="center">
  <b>Excel File with all products in one sheet</b>
</p>

## Requirements

Clone this repository, cd into it, and install dependencies:
```sh
git clone https://github.com/huyszn/supreme-products-scraper.git
cd supreme-products-scraper
pip install -r requirements.txt
```
## Usage

### Run with a proxy
This will most likely scrape the NA site.
```sh
python3 supreme-scraper.py -p
```
or
```sh
python3 supreme-scraper.py --proxy
```
If you get a proxy error, then rerun the script or try to run the script without a proxy.

### Run without a proxy
This is not recommended unless you either:
- Want to scrape products from the EU or JP site with your own IP
- Have a proxy that can access the EU or JP site
- Found that none of the free proxies are working
```
python3 supreme-scraper.py
```
If you get a message saying you are banned, then rerun the script on a different IP or use a different proxy.


## Things to work on

- Add desktop links to products and their colors to the Excel/CSV files

## License

This project is licensed under the GPL 3.0 License - see the [LICENSE](LICENSE) file for details.