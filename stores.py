from bs4 import BeautifulSoup
import requests
import csv


def gadaria():
    names = []
    prices = []
    local = 'Gadaria'
    image_url = []
    pages = [*range(1, 4)]
    for page in pages:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/97.0.4692.99 Safari/537.36'}

        source = requests.get(f'https://www.gadaria.com.br/angus-hereford-s59/?pagina={page}', headers=headers).text
        soup = BeautifulSoup(source, "lxml")

        for i in soup.find_all("div", class_='product-name'):
            string = i.text
            names.append(string)

        for i in soup.find_all("span", class_='est_valordokg'):
            string = i.text
            prices.append(string)

        for i in soup.find_all('div', class_="product"):
            url = i.find("img").get("data-src")
            url_site = 'https://www.gadaria.com.br'
            image_url.append(url_site + url)

    file_name = 'table/datas.csv'
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Product', 'Price', 'Local', 'Image_url'])
        for i in range(len(names)):
            writer.writerow([names[i], prices[i], local, image_url[i]])


def intermezzo():
    names = []
    prices = []
    local = 'Intermezzo'
    image_url = []
    pages = [*range(1, 7)]

    for page in pages:
        source = requests.get(f'https://intermezzocarnes.com.br/produtos/bovinos.html?___SID=U&p={page}').text
        soup = BeautifulSoup(source, "lxml")

        for i in soup.find_all("h2", class_='product-name'):
            string = i.a.text
            name_filter = string.split('R$')
            names.append(name_filter[0])

        for i in soup.find_all("h2", class_='product-name'):
            string = i.a.text
            price_filter = string.split('R$')
            if (len(price_filter)) == 1:
                price_filter.insert(1, 'NA')
            price_string = price_filter[1].replace(",", ".")
            prices.append(price_string)

        for i in soup.find_all('span', class_="product-image"):
            url = i.find_all("img")
            url_final = url[0].get('src')
            image_url.append(url_final)

    file_name = 'table/datas.csv'
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(prices)):
            writer.writerow([names[i], prices[i], local, image_url[i]])


def meatbox():
    names = []
    prices = []
    local = 'MeatBox'
    image_url = []
    pages = [*range(1, 8)]
    for page in pages:
        source = requests.get(
            f'https://www.meatbox.com.br/bovinos/page/{page}/').text
        soup = BeautifulSoup(source, "lxml")

        for i in soup.find_all("div", class_='js-item-name item-name'):
            string = i.text
            names.append(string)

        for i in soup.find_all("span", class_='js-price-display item-price'):
            string = i.text
            string_filter = string.replace(",", ".").replace("R$", "")
            prices.append(string_filter)

        for i in soup.find_all('div', class_="js-item-image item-image"):
            url = i.find_all("img")
            url_clean = url[0].get("data-srcset").split(" ")
            image_url.append('https:' + url_clean[0])

    file_name = 'table/datas.csv'
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(names)):
            writer.writerow([names[i], prices[i], local, image_url[i]])
