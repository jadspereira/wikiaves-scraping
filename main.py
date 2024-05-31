import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup

# Inputs para buscar URL, diretório e número de itens
directory = input("Digite o diretório para salvar os dados: ")
if not os.path.isdir(directory):
    print("Diretório inválido. Encerrando o script.")
    exit()

url = input("Digite a URL: ")
num_items = int(input("Digite o número de itens: "))
if num_items <1: 
    print("Insira um número válido")
    exit()

# Data extraction function
def scrape_data(url, num_items):
    service = EdgeService(EdgeChromiumDriverManager().install())
    options = webdriver.EdgeOptions()
    options.headless = True
    driver = webdriver.Edge(service=service, options=options)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    scraped_data = []
    seen_ids = set()  

    while len(scraped_data) < num_items:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        species_blocks = soup.find_all('div', {'class': 'wa-grid-item wa-record-mobile'})

        for block in species_blocks:
            block_id = block.find('div', {'class': 'm-portlet fadeInUp animated wa-record m-portlet--rounded wa-record-mobile wa-foto'})
            if block_id is None:
                continue  

            record_id = block_id.get('id').replace('WA', '')

            if record_id in seen_ids:
                continue  

            seen_ids.add(record_id)

            especie_elem = block.find('div', {'class': 'sp font-poppins'}).find_all('a', {'class': 'm-link'})[-1]
            especie = especie_elem.text.strip() if especie_elem else 'Unknown'

            municipio_elem = block.find('div', {'class': 'author'}).find('a', {'class': 'm-link'})
            municipio = municipio_elem.text.strip() if municipio_elem else 'Unknown'

            data_elem = block.find('div', {'class': 'date'})
            data = data_elem.text.strip() if data_elem else 'Unknown'

            autor_elem = block.find('div', {'class': 'author'}).find_all('a', {'class': 'm-link'})[-1]
            autor = autor_elem.text.strip() if autor_elem else 'Unknown'

            scraped_data.append([especie, municipio, data, autor])

            if len(scraped_data) >= num_items:
                break  

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  

    driver.quit()

    save_to_txt(scraped_data, directory)

def save_to_txt(scraped_data, directory):
    file_content = "\n".join([",".join(map(str, item)) for item in scraped_data])

    file_path = os.path.join(directory, "scraped_data_wikiaves.txt")
    with open(file_path, "w") as file:
        file.write(file_content)

    print(f"Dados extraídos e salvos em {file_path}")

# Executando a função de extração de dados
scrape_data(url, num_items)

# FIM DO SCRIPT





