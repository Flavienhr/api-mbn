from selenium import webdriver
from bs4 import BeautifulSoup

class ChromeMbn():
    def __init__(self, username, password):
        self.user = username
        self.password = password


    def ouvrir_mbn(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.get("https://cas.monbureaunumerique.fr/login?service=https%3A%2F%2Fcite-boucher.monbureaunumerique.fr%2Fsg.do%3FPROC%3DPAGE_ACCUEIL%26ACTION%3DVALIDER")
        bouton = self.driver.find_element_by_xpath('/html/body/main/div/div/div[1]/div/div/form/div[1]/div/label')
        bouton.click()
        bouton = self.driver.find_element_by_id('button-submit')
        bouton.click()
        champ_email = self.driver.find_element_by_xpath('//*[@id="username"]')
        champ_email.send_keys(self.user)
        mot_de_passe_champ = self.driver.find_element_by_xpath('//*[@id="password"]')
        mot_de_passe_champ.send_keys(self.password)
        bouton = self.driver.find_element_by_id('bouton_valider')
        bouton.click()


    def ouvrir_devoir(self, data_id):
        self.ouvrir_mbn()
        url = None
        while url == None:
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            self.soup = self.soup.find('div', {'id':"js-travail-a-faire-container"})
            for devoir in self.soup.find_all('a', {'class':'b-like'}):
                lien = devoir['href']
                if lien[-6:] == data_id:
                    url = lien
                    break
        self.driver.get("https://cite-boucher.monbureaunumerique.fr/" + str(url))    
