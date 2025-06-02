import requests
from bs4 import BeautifulSoup as Bs
from colorama import init, Fore, Style
from datetime import datetime, timedelta

init(autoreset=True)
s = requests.Session()

def get_csrf_token():
    try:
        login_page = s.get("https://nuvola.madisoft.it")
        login_page.raise_for_status() 
        csrf_token = Bs(login_page.text, features="lxml").find_all("input")[0].attrs["value"]
        return csrf_token
    except requests.exceptions.HTTPError as errh:
        print(f"Errore HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Errore di connessione: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout della richiesta: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Errore durante la richiesta: {err}")

def login(username, password, csrf_token):
    try:
        r = s.post("https://nuvola.madisoft.it/login_check", data={
            "_username": username,
            "_password": password,
            "_csrf_token": csrf_token
        })
        r.raise_for_status()
        return r.cookies.get("nuvola")
    except requests.exceptions.HTTPError as errh:
        print(f"Errore HTTP durante il login: {errh}")
    except requests.exceptions.RequestException as err:
        print(f"Errore durante il login: {err}")

def get_bearer_token(session_token):
    try:
        r = s.get("https://nuvola.madisoft.it/api-studente/v1/login-from-web", cookies={"nuvola": session_token})
        r.raise_for_status()
        token = r.json()["token"]
        return token
    except requests.exceptions.HTTPError as errh:
        print(f"Errore HTTP durante l'ottenimento del bearer token: {errh}")
    except requests.exceptions.RequestException as err:
        print(f"Errore durante l'ottenimento del bearer token: {err}")
        

def visualizza_voti(token):
    # Richiesta per ottenere le frazioni temporali
    url_frazioni = f"https://nuvola.madisoft.it/api-studente/v1/alunno/{studente_id}/frazioni-temporali"
    headers = {"authorization": "Bearer " + token}
    r = requests.get(url_frazioni, headers=headers)
    
    if r.status_code != 200:
        print(Fore.RED + "Errore nel recupero delle frazioni temporali" + Fore.RESET)
        return

    frazioni_data = r.json()
    
    # Controlla che ci siano frazioni temporali nella response
    frazioni = frazioni_data.get("valori")
    if not frazioni:
        print(Fore.RED + "Nessuna frazione temporale trovata" + Fore.RESET)
        return

    # Stampa le opzioni dinamicamente
    for idx, frazione in enumerate(frazioni, start=1):
        print(Fore.CYAN + f"{idx}. {frazione['nome']}")
    
    choice = input("Inserisci un " + Fore.YELLOW + "numero: " + Fore.RESET)
    try:
        choice = int(choice)
        if choice < 1 or choice > len(frazioni):
            print(Fore.RED + "Scelta non valida" + Fore.RESET)
            return
    except ValueError:
        print(Fore.RED + "Inserisci un numero valido" + Fore.RESET)
        return
    
    # Ottieni l'id della frazione temporale selezionata
    frazione_selezionata = frazioni[choice - 1]
    frazione_id = frazione_selezionata["id"]
    
    # Costruisci l'URL per ottenere i voti usando l'id della frazione
    url_voti = f"https://nuvola.madisoft.it/api-studente/v1/alunno/{studente_id}/frazione-temporale/{frazione_id}/voti/materie"
    r = requests.get(url_voti, headers=headers)
    
    if r.status_code != 200:
        print(Fore.RED + "Errore nel recupero dei voti" + Fore.RESET)
        return

    voti_data = r.json()
    
    for materia in voti_data.get("valori", []):
        nome_materia = materia.get("materia")
        voti = materia.get("voti", [])
        
        if not voti:
            print(Fore.LIGHTMAGENTA_EX + f"{nome_materia}: Nessun voto" + Fore.RESET)
        else:
            # Estrae le valutazioni e crea una stringa separata da virgole
            valutazioni = [voto.get("valutazione") for voto in voti]
            voti_string = ",".join(valutazioni)
            print(Fore.GREEN + f"{nome_materia}: {voti_string}" + Fore.RESET)



def alunni(token):
    try:
        headers = {"authorization": "Bearer " + token}
        r = requests.get("https://nuvola.madisoft.it/api-studente/v1/alunni", headers=headers)
        r.raise_for_status()
        info_alunno = r.json()

        for studente in info_alunno["valori"]:
            nome = studente["nome"]
            cognome = studente["cognome"]
            classe = studente["classe"]
            anno_scolastico = str(studente["annoScolastico"])
            global studente_id
            studente_id = str(studente["id"])
            print(Fore.YELLOW + nome + " " + cognome + " " + classe + " " + str(anno_scolastico))
            
    except requests.exceptions.HTTPError as errh:
        print(Fore.RED + f"Errore HTTP durante l'ottenimento dei dati degli alunni: {errh}")
    except requests.exceptions.RequestException as err:
        print(Fore.RED + f"Errore durante l'ottenimento dei dati degli alunni: {err}")
        
def visualizza_compiti(token, giorni=10):
    oggi = datetime.now()

    for giorno in range(giorni):
        data = (oggi + timedelta(days=giorno)).strftime("%d-%m-%Y")
        url = f"https://nuvola.madisoft.it/api-studente/v1/alunno/{studente_id}/compito/elenco/{data}"
        headers = {
            "authorization": "Bearer " + token
        }

        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            compiti_data = r.json()
            
            for compito in compiti_data["valori"]:
                materia = compito["materia"]
                descrizione_compito = compito["descrizioneCompito"][0] if compito["descrizioneCompito"] else "Niente Compiti"
                
                print(Fore.YELLOW + f"{materia} - Compiti: " + Fore.CYAN + Style.BRIGHT + descrizione_compito + f" | Data: {data}")
                print(Fore.CYAN + "-" * 40)

        except requests.exceptions.HTTPError as errh:
            print(f"Errore HTTP durante il recupero dei compiti: {errh}")
        except requests.exceptions.RequestException as err:
            print(f"Errore durante il recupero dei compiti: {err}")     