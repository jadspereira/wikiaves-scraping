#  Web Scraper - WikiAves

# Introdução

Este é um script feito para coletar dados de observações do site wikiaves de maneira mais eficiente quando comparada a extração manual. 
Ele utiliza Selenium e BeautifulSoup para automatizar o processo de rolagem da página e a extração de conteúdo dos blocos. 

## Funcionalidades

- Extrai o nome da espécie, município, data e autor do WikiAves através da URL.
- Salva o arquivo em um arquivo .txt com campos separados por vírgula e cada ocorrência em uma nova linha.
- Repete o loop de rolagem e extração até que o número de ocorrências especificado seja atendido. 

**Observação**: O script está configurado para usar o **Edge** WebDriver, mas pode ser facilmente modificado para outros navageadores, como Chrome ou Firefox!

## Pré-requisitos e libraries

- Python 3.6+
- `selenium`
- `webdriver-manager` 
- `beautifulsoup4`

## Instalação

1. **Clone este repositório:**
    ```sh
    git clone https://github.com/yourusername/wikiaves-scraper.git
    cd wikiaves-scraper
    ```

2. **Instale as bibliotecas necessárias:**
    ```sh
    pip install selenium webdriver-manager beautifulsoup4
    ```

## Como utilizar

1. **Rode o script:**
    ```sh
    python scraper.py
    ```

2. **Insira as informações solicitadas pelos inputs:**
    - Diretório para salvar os arquivos
    - URL (formato com ID da espécie: `https://www.wikiaves.com.br/midias.php?t=s&s=10731&o=dp`)
    - Número de ocorrências desejado

## Contribuições
Contribuições são bem-vindas! Por favor, crie uma issue ou pull request se tiver melhorias ou correções!


## Referência: [Raspagem de sítios web dinâmicos com Python](https://brightdata.com.br/blog/procedimentos/scrape-dynamic-websites-python)
