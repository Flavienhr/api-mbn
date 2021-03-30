from requests import *
from bs4 import BeautifulSoup


class SessionMonBureauNumerique():
# Lors de l'initialisation une connection à mon_bureau_nummérique_cite_helene_boucher s'établit
    def __init__(self, identifiant, password):
        self.session = session()    # La session permet de garder les cookies seesions et autres cookies nécessaire à la connexion

        # Première requête login mbn
        headers = {
            'Host': 'cas.monbureaunumerique.fr',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Referer': 'https://cas.monbureaunumerique.fr/login?service=https%3A%2F%2Fwww.monbureaunumerique.fr%2Fsg.do%3FPROC%3DPAGE_ACCUEIL%26ACTION%3DVALIDER',
            'Cookie': 'SERVERID=gdest-prod-web5; JSESSIONID=BB3A0B647FB3791D735B950BE1078E7B.web5; preselection=EDU',
            'Upgrade-Insecure-Requests': '1'
        }
        r = self.session.get('https://cas.monbureaunumerique.fr/login?selection=EDU&service=https%3A%2F%2Fwww.monbureaunumerique.fr%2Fsg.do%3FPROC%3DPAGE_ACCUEIL%26ACTION%3DVALIDER&submit=Valider', headers=headers)

        # Deuxième requête qui permet d'obtenir le SAML et le relaystate afin de se rediriger vers educonnect
        headers = {
            'Host': 'cas.monbureaunumerique.fr',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Referer': 'https://cas.monbureaunumerique.fr/login?service=https%3A%2F%2Fwww.monbureaunumerique.fr%2Fsg.do%3FPROC%3DPAGE_ACCUEIL%26ACTION%3DVALIDER',
            'Cookie': 'SERVERID=gdest-prod-web5; JSESSIONID=BB3A0B647FB3791D735B950BE1078E7B.web5; preselection=EDU',
            'Upgrade-Insecure-Requests': '1'
        }
        r = self.session.get('https://cas.monbureaunumerique.fr/delegate/redirect/EDU', headers=headers)
        # Extraction des valeurs du SAML et du relaystate à partir de la réponse
        soup = BeautifulSoup(r.text, 'html.parser')
        all_input = soup.find_all('input')
        SAML = all_input[1]['value']
        relaystate = all_input[0]['value']

        # Troisième requête qui permet de se rediriger vers educonnect grâce au relaystate et au SAML
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '4260',
            'Origin': 'https://cas.monbureaunumerique.fr',
            'Connection': 'keep-alive',
            'Referer': 'https://cas.monbureaunumerique.fr/delegate/redirect/EDU',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'educonnect.education.gouv.fr'
        }
        data_post = {
            'RelayState':relaystate,
            'SAMLRequest':SAML
            }
        r = self.session.post('https://educonnect.education.gouv.fr/idp/profile/SAML2/POST/SSO', headers=headers, data=data_post)

        # Quatrième requête : auth de l'élève dans educonnect puis extraction du SAML et du relaystate afin de se rediriger vers mbn
        headers = {
            'Host': 'educonnect.education.gouv.fr',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '4260',
            'Origin': 'https://cas.monbureaunumerique.fr',
            'Connection': 'keep-alive',
            'Referer': 'https://cas.monbureaunumerique.fr/delegate/redirect/EDU',
            'Upgrade-Insecure-Requests': '1'
        }
        login_data = {
            'j_username':identifiant,
            'j_password':password,
            '_eventId_proceed':''
        }
        r = self.session.post('https://educonnect.education.gouv.fr/idp/profile/SAML2/POST/SSO?execution=e1s1', headers=headers, data=login_data)
        # Extraction du SAML et du relaystate à partir de la réponse
        soup = BeautifulSoup(r.text, 'html.parser')
        all_input = soup.find_all('input')
        SAML = all_input[1]['value']
        relaystate = all_input[0]['value']

        # Cinquième requête qui permet de se rediriger vers mbn grâce au relaystate et au SAML
        headers = {
            'Host': 'cas.monbureaunumerique.fr',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Referer': 'https://educonnect.education.gouv.fr/idp/profile/SAML2/POST/SSO?execution=e1s1',
            'Content-Length':'17037',
            'Content-Type':'application/x-www-form-urlencoded',
            'Origin':'https://educonnect.education.gouv.fr',    
            'Upgrade-Insecure-Requests': '1'
        }
        data_post = {
            'RelayState':relaystate,
            'SAMLResponse':SAML
            }
        r = self.session.post('https://cas.monbureaunumerique.fr/saml/SAMLAssertionConsumer', headers=headers, data=data_post)

        # Sixième requête qui permet d'obtenir le token de redirection vers cite-boucher.monbureaunumerique.fr
        headers = {
            'Host': 'cas.monbureaunumerique.fr',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Referer': 'https://cas.monbureaunumerique.fr/saml/SAMLAssertionConsumer'
        }
        r = self.session.get('https://cas.monbureaunumerique.fr/login?service=https%3A%2F%2Fcite-boucher.monbureaunumerique.fr%2Fsg.do%3FPROC%3DIDENTIFICATION_FRONT%26ACTION%3DVALIDER', headers=headers)
        url = str(r.url)

        # Septième requête permettant de se connecter au mbn de cite-boucher grâce au token
        headers = {
            'Host': 'cite-boucher.monbureaunumerique.fr',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Length':'0',
            'Referer': 'https://cite-boucher.monbureaunumerique.fr/sg.do?PROC=PAGE_ACCUEIL&ACTION=VALIDER',
            'Upgrade-Insecure-Requests':'1'
        }
        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            raise ValueError("Erreur provenant de Mon Bureau Numérique code de l'erreur : " + str(r.status_code))


    def get_taf(self) -> list:
        """Renvoie une liste de dictionnaires contenant les devoirs sous la forme : {'id_devoir':123456, 'matiere':'Allemand', 'date_echeance':(jour, mois, annee), 'date_parution':(jour, mois, annee), 'contenu':string, 'is_doc':bool}"""
        headers = {
            'Host': 'cite-boucher.monbureaunumerique.fr',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Length':'0',
            'Referer': 'https://cite-boucher.monbureaunumerique.fr/sg.do?PROC=PAGE_ACCUEIL',
            'Upgrade-Insecure-Requests':'1'
        }
        r = self.session.get('https://cite-boucher.monbureaunumerique.fr/sg.do?PROC=TRAVAIL_A_FAIRE&ACTION=AFFICHER_ELEVES_TAF&filtreAVenir=true', headers=headers)

        self.page_devoirs = r.text
        soup = BeautifulSoup(self.page_devoirs, 'html.parser')
        devoirs = soup.find_all('div', {'class':'hide js-taf__modal-content'})
        devoirs_liste_de_dicos = []

        for devoir in devoirs:
            id_devoir = devoir['data-id']
            soup = BeautifulSoup(str(devoir), 'html.parser')
            matiere = soup.find('span', {'class':'h6-like h6-like--lead-xs b-like'})
            matiere = matiere.text
            date_echeance = soup.find('div', {'class':'col col--xs-12 col--md-6'})
            date_echeance = date_echeance.text
            date_echeance = date_echeance[9::]
            date_parution = soup.find('div', {'class':'col col--xs-12 col--md-6 text--right'})
            date_parution = date_parution.text
            date_parution = date_parution[10::]
            date_parution_convertie, date_echeance_convertie = self.convertisseur_str2date(date_parution, date_echeance)
            contenu = soup.find('div', {'class':'panel panel--full panel--no-margin'})
            contenu = contenu.text
            try:
                document = soup.find('a', {'class':'jumbofiles__file-name'})
                assert document != None
                is_doc = True
            except:
                is_doc = False
            dico = {'id_devoir':id_devoir, 'matiere':matiere, 'date_echeance':date_echeance_convertie, 'date_parution':date_parution_convertie, 'contenu':contenu, 'is_doc':is_doc}
            devoirs_liste_de_dicos.append(dico)
        return devoirs_liste_de_dicos


    def convertisseur_str2date(self, *args) -> tuple:
        """Prends en entrée des dates au format : jour XX mois XXXX et la transforme en tuple (XX,XX,XXXX)"""
        for date in args:
            date_mod = date.split(' ')
            tuple_date_mod = tuple(date_mod)
            jour, numero_jour, mois, numero_annee = tuple_date_mod
            numero_mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'].index(mois)
            numero_mois += 1
            date_fin = int(numero_jour), numero_mois, int(numero_annee)
            args = list(args)
            args[args.index(date)] = date_fin
        return tuple(args)


    def get_docs(self, data_id):
        """En développement /!\ """
        try:       
            soup = BeautifulSoup(self.page_devoirs, 'html.parser')
        except:
            self.get_taf()
            soup = BeautifulSoup(self.page_devoirs, 'html.parser')
        devoir = soup.find('div', {'data-id':data_id})
        devoir_page = BeautifulSoup(str(devoir), 'html.parser')
        file_name = devoir_page.find('a', {'class':'jumbofiles__file-name'})
        url = 'https://cite-boucher.monbureaunumerique.fr' + file_name['href']
        r = self.session.get(url)
        f = open(r.headers['content-disposition'].split("''")[1], 'w')
        f.write(r.text)
        f.close()
