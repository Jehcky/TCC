import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import sys
sys.path.append('/home/TCC/implementation')
import Gene

URL_NCBI = "https://www.ncbi.nlm.nih.gov"

def scrape_gene_variants():
    # Set chromedriver executable path
    service = Service(executable_path='/usr/bin/chromedriver')
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : '/home/TCC/GeneVariants/'}
    options.add_experimental_option('prefs', prefs)
    # "A common cause for Chrome to crash during startup is running Chrome 
    # as root user (administrator) on Linux. While it is possible to work 
    # around this issue by passing --no-sandbox flag when creating your 
    # WebDriver session, such a configuration is unsupported and highly discouraged."
    #
    # IT WASN'T WORKING SO I HAD TO DO THIS, PLS READ ABOVE :D
    options.add_argument("--no-sandbox")

    # Another workaround for another error
    options.add_argument('--disable-dev-shm-usage') 

    driver = webdriver.Chrome(service=service, options=options)
    driver.delete_all_cookies()

    for gene_type in Gene.Gene:
        driver.get(URL_NCBI)
    
        search_string = f"{gene_type.name} homo sapiens"
        driver.find_element(By.ID, 'term').send_keys(search_string)
        driver.find_element(By.ID, 'search').click()
        href = driver.find_element(By.ID, 'gene_refseqtranscripts').get_attribute('href')
        driver.get(href)
        driver.find_element(By.XPATH, '//*[@id="seqsendto"]/a').click()
        time.sleep(2)
        driver.find_element(By.ID, 'complete_rec').click()
        time.sleep(2)
        driver.find_element(By.ID, 'dest_File').click()
        time.sleep(2)
        driver.find_element(By.ID, 'file_format').send_keys('fasta')
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="submenu_File"]/button').click()

        time.sleep(5)
        os.rename("/home/TCC/GeneVariants/sequence.fasta", f"/home/TCC/GeneVariants/{gene_type.name}.fasta")
    driver.quit()

scrape_gene_variants()
    