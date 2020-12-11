from bs4 import BeautifulSoup
import requests
import pandas as pd

df = pd.read_csv('cleaned_data.csv')

code = input('Please enter the full UPC (barcode) number')
code = code.rstrip()
code = code.lstrip()

page = requests.get(f'https://www.buycott.com/upc/{code}')

soup = BeautifulSoup(page.content, 'html.parser')

try:
    if page.status_code == 200:
        try:
           results = soup.find('table', {'class': 'table product_info_table'})
           if results.text == ' ':
               print('There was no data on this particular item')
           else:
            brand = results.text.split('\n')[4].strip().upper()
            manufacturer = results.text.split('\n')[8].strip().upper()

            print(brand)
            print(manufacturer)

            if df['List of Companies'].str.contains(brand).any():
                print(f'This brand is a subsidiary of Nestle: {brand}')
            elif df['List of Companies'].str.contains(manufacturer).any():
                print(f'This manufacturer is a subsidiary of Nestle: {manufacturer}')
            else:
                print('There is no record of this product being associated with Nestle!')


        except:
            print('No Data Available')
    else:
        print('No Data Available')

            ### Need to put in a sesarch for no results and then return back that there is no data

except:
    print('There was no data on this particular item')



