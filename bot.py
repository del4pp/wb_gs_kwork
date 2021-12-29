from datetime import time
from urllib.request import Request, urlopen
import db
from bs4 import BeautifulSoup
import telegram
import unidecode

notification_date_list = []

header = {}

header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36  (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'
header['Accept'] =  'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'


def parse_google_docs():
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRlUFPSmjBr7x_2ABqIG_skuGp4k6_bJwH9SfAtYCtHSHpbPoLpyq2y7pU4Z_amn4xYr3nEtBS-XfP6/pubhtml?gid=0&single=true&alt=json'

    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")

    wb_list = []
    for rows in soup.findAll('td', attrs={'dir':'ltr'}):
        wb_list.append(str(rows.text))

    return wb_list


def parse_wb(page_url):
    req = Request(page_url, headers=header)
    page = urlopen(req)
    page_content = BeautifulSoup(page, 'lxml')

    item_price = ''
    for price in page_content.findAll('span', attrs={'class':'price-block__final-price'}):
        item_price = str(price.text).replace('₽', '')
    
    if item_price:
        return item_price

def controller():
    page_list = parse_google_docs()
    for page in page_list:
        if not db.new_records_links(page):
            db.insert_link(page)
        price_now = unidecode.unidecode(str(parse_wb(page)).strip())
        old_price = db.get_old_price(page)

        #print(price_now)

        if ' ' in str(price_now):
                price_now = str(price_now).replace(' ',  '')

        if old_price != 'None' and old_price != None:
            procent_diff = float(price_now) / float(old_price)
        else:
            procent_diff = 1

        if old_price == 'None' and price_now != 'None' and old_price != None and price_now != None:
            msg_tg = 'Товар появился в наличии \n\n {0}'.format(page)
            telegram.send_message_new_price('-1001662783286', msg_tg)

        #print(procent_diff)

        if float(procent_diff) < 0.7 or float(procent_diff) > 1.3:
            tg_message = 'Цена товара \n\n {0} \n\nизменилась более чем на 30%\nСтарая: {1}\nНовая: {2}.\n\n'.format(
                page, old_price, price_now
            )
            telegram.send_message_new_price('-1001662783286', tg_message)
        

        db.update_price(page, price_now)
        from datetime import datetime
        now_time = datetime.now().time().hour
        date_now = datetime.now().date()

        if now_time == 10:
            if date_now not in notification_date_list:
                telegram.send_message_new_price('-1001662783286', 'Отчет по работе бота. Все работает в штатном режиме')
            notification_date_list.append(date_now)


while True:
    try:
        controller()
    except Exception as e:
        telegram.send_message_new_price('-1001662783286', str(e))
        import time
        time.sleep(60)
