import pandas as pd
import requests
import wget
import os
import re

from bs4 import BeautifulSoup


# Esto programa descarga generando la ruta de descarga

url = "https://docs.google.com/spreadsheets/d/1HzdumNltTj2SHmCv3SRdoub8SvpIEn75fa4Q23x0keU/htmlview"
dfs = pd.read_html(url)[0]
dfs = dfs.drop([0, 1])


if not os.path.isdir("books"):
    os.mkdir("books")

for i in range(len(dfs)):
    book = dfs.iloc[i]
    url = book.S

    isbn = book.S.split("=")[-1]

    name = re.sub("/", "", book.A)
    name = re.sub(" ", "_", name)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    epub = soup.find('a', class_='test-bookepub-link')
    pdf = soup.find('a', class_="test-bookpdf-link")

    folder = f"books/{name}_{isbn}"

    # Check if exists folder
    if not os.path.isdir(folder):
        os.mkdir(folder)

    exists_pdf = True if pdf else False
    exists_epub = True if epub else False

    print(f"\nDownloading {name}: \n\tPDF - {exists_pdf} \n\tEPUB - {exists_epub}" )


    if exists_pdf and not os.path.exists(f"{folder}/{name}.pdf"):
        try:
            wget.download("https://link.springer.com"+pdf["href"], out=f"{folder}/{name}.pdf")
        except Exception as e:
            print(f"{name}: e")

    if exists_epub and not os.path.exists(f"{folder}/{name}.epub"):
        try:
            wget.download("https://link.springer.com"+epub["href"], out=f"{folder}/{name}.epub")        
        except Exception as e:
            print(f"{name}: e")

    print("")