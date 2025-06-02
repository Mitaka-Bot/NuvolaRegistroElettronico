# 📚 Registro Elettronico Nuvola - Open Source

> Un'implementazione open source **NON UFFICIALE** del registro elettronico Nuvola di Madisoft.it

## 🎯 Panoramica

Questo progetto è un client Python che permette agli studenti di accedere facilmente ai propri dati scolastici attraverso le API del registro elettronico Nuvola. L'applicazione offre un'interfaccia a riga di comando semplice e intuitiva per consultare voti e compiti assegnati.

## ✨ Funzionalità

### 📊 Visualizzazione Voti
- Accesso ai voti di tutte le materie
- Selezione dinamica delle frazioni temporali (quadrimestri, trimestri, ecc.)
- Visualizzazione organizzata per materia con tutti i voti conseguiti
- Gestione automatica dei periodi scolastici

### 📝 Visualizzazione Compiti
- Consultazione dei compiti assegnati per i prossimi giorni
- Visualizzazione delle scadenze e descrizioni dettagliate
- Organizzazione per materia e data
- Configurabile per diversi periodi di tempo

### 🔐 Gestione Credenziali
- Salvataggio automatico delle credenziali di accesso
- Login sicuro attraverso token CSRF e Bearer
- Gestione automatica della sessione

## 🚀 Installazione e Utilizzo

### Prerequisiti
```bash
pip install requests beautifulsoup4 colorama
```

### Utilizzo
1. Esegui il file `nuvola.exe` oppure `python nuvola.py`
2. Al primo avvio, inserisci le tue credenziali Nuvola
3. Le credenziali verranno salvate automaticamente in `credenziali.txt`
4. Seleziona l'opzione desiderata dal menu principale

### Menu Principale
```
1: Visualizza i Voti
2: Visualizza i Compiti
```

## 📁 Struttura del Progetto

```
📦 Nuvola-OpenSource/
├── 📄 nuvola.py          # File principale dell'applicazione
├── 📄 commands.py        # Modulo con tutte le funzioni API
├── 📄 credenziali.txt    # File delle credenziali (generato automaticamente)
├── 📄 nuvola.exe         # Eseguibile compilato
└── 📄 README.md          # Documentazione del progetto
```

## 🔧 Funzioni Tecniche

### API Endpoints Utilizzati
- `/login_check` - Autenticazione utente
- `/api-studente/v1/login-from-web` - Conversione sessione web in token API
- `/api-studente/v1/alunni` - Informazioni studente
- `/api-studente/v1/alunno/{id}/frazioni-temporali` - Periodi scolastici
- `/api-studente/v1/alunno/{id}/frazione-temporale/{id}/voti/materie` - Voti per periodo
- `/api-studente/v1/alunno/{id}/compito/elenco/{data}` - Compiti per data

## 🎨 Caratteristiche dell'Interfaccia

- **Output colorato**: Utilizzo di `colorama` per un'esperienza visiva migliorata
- **Gestione errori**: Messaggi di errore chiari e informativi
- **Navigazione intuitiva**: Menu semplici e opzioni numerate
- **Feedback visivo**: Indicatori di stato e messaggi di caricamento

## 🔒 Sicurezza e Privacy

- Le credenziali sono salvate localmente in formato testo semplice
- Nessun dato viene trasmesso a server esterni oltre a quelli ufficiali Nuvola
- Utilizzo delle API ufficiali attraverso protocolli sicuri HTTPS

## 📋 Note Tecniche

### Compatibilità
- **Python**: 3.6+
- **Sistema Operativo**: Windows, macOS, Linux
- **Dipendenze**: requests, beautifulsoup4, colorama

## ⚖️ Disclaimer

Questo progetto è **NON UFFICIALE** e non è affiliato con Madisoft.it o il registro elettronico Nuvola. È stato sviluppato per scopi educativi e di praticità per gli studenti. L'utilizzo è a proprio rischio e responsabilità.
