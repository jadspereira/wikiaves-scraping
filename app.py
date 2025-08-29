import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup


# Função principal de scraping
def scrape_data(url, num_items, directory):
    try:
        service = EdgeService(EdgeChromiumDriverManager().install())
        options = webdriver.EdgeOptions()
        options.headless = True
        driver = webdriver.Edge(service=service, options=options)
        driver.get(url)

        scraped_data = []
        seen_ids = set()

        while len(scraped_data) < num_items:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            species_blocks = soup.find_all('div', {'class': 'wa-grid-item wa-record-mobile'})

            for block in species_blocks:
                block_id = block.find('div', {
                    'class': 'm-portlet fadeInUp animated wa-record m-portlet--rounded wa-record-mobile wa-foto'
                })
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

        messagebox.showinfo("Sucesso", f"Dados extraídos e salvos em:\n{os.path.join(directory, 'scraped_data_wikiaves.txt')}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))


# Salvar os dados em TXT
def save_to_txt(scraped_data, directory):
    file_content = "\n".join([",".join(map(str, item)) for item in scraped_data])
    file_path = os.path.join(directory, "scraped_data_wikiaves.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(file_content)


# Interface Tkinter
def browse_directory():
    folder = filedialog.askdirectory()
    if folder:
        entry_dir.delete(0, tk.END)
        entry_dir.insert(0, folder)


def start_scraping():
    directory = entry_dir.get().strip()
    url = entry_url.get().strip()
    try:
        num_items = int(entry_num.get().strip())
    except ValueError:
        messagebox.showerror("Erro", "Número de ocorrências inválido!")
        return

    if not directory or not url or not num_items:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    scrape_data(url, num_items, directory)


# Criar janela principal
root = tk.Tk()
root.title("Scraper WikiAves")
root.geometry("500x300")

# Diretório
tk.Label(root, text="Diretório para salvar:").pack(anchor="w", padx=10, pady=5)
frame_dir = tk.Frame(root)
frame_dir.pack(fill="x", padx=10)
entry_dir = tk.Entry(frame_dir)
entry_dir.pack(side="left", fill="x", expand=True)
btn_browse = tk.Button(frame_dir, text="Procurar", command=browse_directory)
btn_browse.pack(side="right")

# URL
tk.Label(root, text="URL:").pack(anchor="w", padx=10, pady=5)
entry_url = tk.Entry(root)
entry_url.pack(fill="x", padx=10)

# Número de ocorrências
tk.Label(root, text="Número de ocorrências:").pack(anchor="w", padx=10, pady=5)
entry_num = tk.Entry(root)
entry_num.pack(fill="x", padx=10)

# Botão executar
btn_start = tk.Button(root, text="Iniciar Extração", command=start_scraping, bg="green", fg="white")
btn_start.pack(pady=15)

root.mainloop()
