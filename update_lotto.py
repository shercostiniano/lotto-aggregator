import json
import pandas as pd
from pandarallel import pandarallel
from currency_converter import CurrencyConverter
pandarallel.initialize(progress_bar=True)
c = CurrencyConverter()

def update_database(row):
    import requests
    from bs4 import BeautifulSoup
    url = row['link']
    if url != '':
        win_list=[]
        bonus_list=[]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        drawn_date = soup.find('h5').text.strip()
        winning_numbers = soup.find_all('img', {'src': lambda x: 'p1=M' in x})
        bonus_numbers = soup.find_all('img', {'src': lambda x: 'p1=B' in x})
        p = soup.find_all('p')

        for img in winning_numbers:
            src = img['src']
            p2_value = src.split('&')[1].split('=')[1]
            win_list.append(p2_value)

        for img in bonus_numbers:
            src = img['src']
            p2_value = src.split('&')[1].split('=')[1]
            bonus_list.append(p2_value)

        split_string = p[3].text.split(')')
        next_draw_date = split_string[0].strip() + ')'
        estimated_jackpot = split_string[1] + ')'
        
        try:
            return next_draw_date,estimated_jackpot,drawn_date,','.join(win_list),','.join(bonus_list)
        except IndexError as e:
            print(split_string)
    else:
        return '','','','',''

def currency_converter(result):
    result = result.replace(',', '').replace(')','').strip()
    if '$' in result:
        result = result.replace('$', '')
    elif '€' in result:
        result = c.convert(float(result.replace('€', '')), 'EUR', 'USD')
    elif '£' in result:
        result = c.convert(float(result.replace('£', '')), 'GBP', 'USD')
    elif 'zł' in result:
        result = c.convert(float(result.replace('zł','')), 'PLN', 'USD')
    elif 'R' in result:
        result = c.convert(float(result.replace('R','')), 'ZAR', 'USD')
    return result

total = 0
df = pd.read_csv('ltech_lotto.csv')
df[['next_draw_date', 'estimated_jackpot','drawn_date','winning_numbers','bonus_numbers']] = df.parallel_apply(update_database, axis=1, result_type='expand')

for result in df['estimated_jackpot'].unique():
    if type(result) != float:
        us_index = result.find("US$")
        if us_index != -1:
            substring = result[us_index+2:us_index+101]  # Extract up to 99 characters after "US$"
            result = substring.replace(")", "")  # Remove ")" and convert to float
            total += float(result.replace(',','').replace('$',''))
        else:
            result = result.replace(")", "")
            if 'a month for 30 years' in result:
                result = result.replace("a month for 30 years", "")
                result_converted = currency_converter(result)
                result = float(result_converted) * 12 * 30
            elif 'a month for 20 years' in result:
                result = result.replace("a month for 20 years", "")
                result_converted = currency_converter(result)
                result = float(result_converted) * 12 * 20
            elif 'a day for life' in result:
                result = result.replace("a day for life", "")
                result_converted = currency_converter(result)
                result = float(result_converted) * 365 * 30
            else:
                result = currency_converter(result)
            total += float(result)
with open('total_winnings.json', 'w') as f:
    json.dump({'total_lotto_winnings': total}, f)

