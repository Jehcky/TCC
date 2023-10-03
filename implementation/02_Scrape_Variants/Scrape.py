from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Set chromedriver executable path
service = Service(executable_path='/usr/bin/chromedriver')
options = webdriver.ChromeOptions()

# "A common cause for Chrome to crash during startup is running Chrome 
# as root user (administrator) on Linux. While it is possible to work 
# around this issue by passing --no-sandbox flag when creating your 
# WebDriver session, such a configuration is unsupported and highly discouraged."
#
# IT WASN'T WORKING SO I HAD TO DO THIS, PLS READ ABOVE :D
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.ncbi.nlm.nih.gov')
print(driver.title)

driver.quit()