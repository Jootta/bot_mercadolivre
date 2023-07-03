import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1920,1080']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)

    return driver

driver = iniciar_driver()
url = input('Digite uma url (Mercado Livre): ')
driver.get(url=url)

sleep(5)

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    sleep(5)

    produtos = driver.find_elements(By.XPATH, "//h2[@class='ui-search-item__title shops__item-title']")
    precos = driver.find_elements(By.XPATH, "//span[@class='andes-money-amount ui-search-price__part shops__price-part andes-money-amount--cents-superscript']//span[3]")
    links = driver.find_elements(By.XPATH, "//div[@class='ui-search-item__group ui-search-item__group--title shops__items-group']//a[@title]")

    sleep(5)

    for produto,preco,link in zip(produtos,precos,links):
        produto_value = produto.text
        preco_value = preco.text
        link_value = link.get_attribute('href')
        
        with open("mercadolivre.csv", "a", encoding='utf-8', newline='') as arq:
            arq.write(f'{produto_value}; RS$ {preco_value};{link_value}{os.linesep}')

    sleep(5)

    try:
        proxima_pagina = driver.find_element(By.XPATH, "//span[text()='Seguinte']")
        proxima_pagina.click()
        sleep(10)
    except:
        print("Você chegou ao fim!")
        break
