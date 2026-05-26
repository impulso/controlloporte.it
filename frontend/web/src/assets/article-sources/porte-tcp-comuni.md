---
title: "Porte TCP comuni: 80, 443, 22, 25, 3306"
description: "Guida alle porte TCP comuni: 80 HTTP, 443 HTTPS, 22 SSH, 25 SMTP e 3306 MySQL. A cosa servono, quando aprirle e quali rischi valutare."
slug: "/porte-tcp-comuni"
keywords:
  - porte TCP comuni
  - porta 443
  - porta 22 ssh
  - porta 80
  - porta 25 smtp
  - porta 3306 mysql
---

# Porte TCP comuni: 80, 443, 22, 25, 3306

Le porte TCP comuni sono numeri standard usati da servizi molto diffusi: siti web, accessi SSH, posta elettronica, database e applicazioni server.

Conoscerle aiuta a capire cosa stai esponendo su Internet, quale porta testare e quali rischi valutare prima di aprire una regola sul router o sul firewall.

In questa guida vediamo le porte TCP più cercate: `80`, `443`, `22`, `25` e `3306`.

Vuoi fare subito una verifica? Usa il [controllo porte aperte online](/) per testare IP, dominio e porta TCP dall'esterno.

## Cosa sono le porte TCP

TCP è un protocollo di trasporto usato per stabilire connessioni affidabili tra due dispositivi.

Una porta TCP identifica il servizio da raggiungere su un host.

Esempio:

```text
esempio.it:443
```

In questo caso:

- `esempio.it` è l'host
- `443` è la porta
- il servizio atteso è HTTPS

Senza la porta, il sistema non saprebbe a quale applicazione consegnare la connessione.

## Porta 80: HTTP

La porta `80` è la porta standard di HTTP.

Viene usata per siti web non cifrati o per reindirizzare automaticamente gli utenti verso HTTPS.

Esempio:

```text
http://esempio.it
```

Quando apri un sito con `http://`, il browser usa normalmente la porta `80`.

### Quando aprire la porta 80

Ha senso aprirla se:

- ospiti un sito web
- devi gestire il rinnovo di certificati con challenge HTTP
- vuoi reindirizzare HTTP verso HTTPS
- stai pubblicando un servizio web interno

### Attenzione alla sicurezza

HTTP non cifra il traffico. Per login, pannelli di controllo, API e dati personali è meglio usare HTTPS sulla porta `443`.

## Porta 443: HTTPS

La porta `443` è la porta standard di HTTPS.

È usata dai siti web cifrati tramite TLS, cioè la maggior parte del web moderno.

Esempio:

```text
https://esempio.it
```

Se un sito è raggiungibile sulla porta `443`, il browser può stabilire una connessione sicura e verificare il certificato.

### Quando aprire la porta 443

È la porta giusta per:

- siti web pubblici
- pannelli amministrativi protetti
- reverse proxy
- API HTTPS
- applicazioni self-hosted

### Porta 443 e reverse proxy

Molti servizi domestici o aziendali vengono pubblicati dietro un reverse proxy come Nginx, Caddy, Traefik o Apache.

In quel caso dall'esterno si apre solo la porta `443`, mentre il reverse proxy smista le richieste verso servizi interni diversi.

## Porta 22 SSH

La porta `22` è la porta standard di SSH.

SSH serve ad accedere da remoto a server Linux, dispositivi di rete, VPS, NAS e sistemi embedded.

Esempio:

```bash
ssh utente@esempio.it
```

Se non specifichi una porta diversa, SSH prova normalmente la porta `22`.

### Quando aprire la porta 22

Aprila solo se hai davvero bisogno di amministrare un sistema da remoto.

Buone pratiche:

- disabilitare il login root
- usare chiavi SSH invece della sola password
- limitare gli IP autorizzati quando possibile
- tenere il sistema aggiornato
- valutare una VPN per l'accesso amministrativo

### Cambiare porta SSH serve?

Spostare SSH da `22` a un'altra porta riduce il rumore dei tentativi automatici, ma non sostituisce una configurazione sicura.

La sicurezza vera arriva da autenticazione forte, aggiornamenti e regole firewall sensate.

## Porta 25 SMTP

La porta `25` è storicamente usata da SMTP, il protocollo per l'invio di email tra server.

È una porta particolare perché molti provider la bloccano o la limitano sulle connessioni residenziali, per ridurre spam e abusi.

### Quando serve la porta 25

Serve soprattutto ai mail server che devono consegnare email ad altri server.

Non è di solito la porta usata da un normale client email per inviare posta autenticata.

Per i client si usano spesso:

```text
587 submission
465 SMTPS
```

### Perché la porta 25 risulta chiusa

Può risultare chiusa perché:

- il servizio SMTP non è attivo
- il firewall la blocca
- il provider la filtra
- il server non accetta connessioni pubbliche
- il cloud provider richiede una richiesta di sblocco

Se devi gestire posta in uscita, verifica sempre le policy del provider.

## Porta 3306 MySQL

La porta `3306` è la porta predefinita di MySQL e MariaDB.

È usata dai client per collegarsi al database.

Esempio:

```text
mysql.example.it:3306
```

### È una buona idea aprire MySQL su Internet?

In generale no, salvo casi ben controllati.

Un database esposto pubblicamente aumenta molto la superficie di attacco. Se devi accedere a MySQL da remoto, valuta soluzioni più sicure:

- VPN
- tunnel SSH
- firewall con IP sorgente limitati
- rete privata del provider cloud
- autenticazione forte e TLS

### Porta 3306 aperta: cosa controllare

Se devi esporla, controlla almeno:

- utenti con password robuste
- privilegi minimi
- accesso limitato per IP
- aggiornamenti del database
- log di accesso
- backup funzionanti

## Tabella riepilogativa

| Porta | Servizio comune | Uso tipico | Da esporre su Internet? |
| --- | --- | --- | --- |
| 80 | HTTP | Siti web non cifrati o redirect | Sì, se serve |
| 443 | HTTPS | Siti web e API cifrate | Sì, spesso |
| 22 | SSH | Amministrazione remota | Solo con protezioni |
| 25 | SMTP | Invio email tra server | Solo per mail server |
| 3306 | MySQL/MariaDB | Database | Meglio evitare, salvo restrizioni |

## Porte aperte e sicurezza

Ogni porta aperta espone un servizio.

Questo non significa che ogni porta aperta sia pericolosa, ma significa che quel servizio deve essere:

- necessario
- aggiornato
- configurato correttamente
- monitorato
- protetto da autenticazione adeguata

La regola pratica è semplice: apri solo ciò che serve davvero.

## Come testare una porta TCP comune

Per verificare se una porta è aperta, usa l'host e il numero di porta.

Esempi:

```text
esempio.it:80
esempio.it:443
esempio.it:22
esempio.it:25
esempio.it:3306
```

Se il test ha successo, significa che da Internet è possibile stabilire una connessione TCP verso quella porta.

Se fallisce, il servizio può essere spento, filtrato da firewall, non inoltrato dal router o non raggiungibile per problemi di NAT.

Prima di lasciare una porta pubblica, soprattutto per SSH, RDP o database, leggi anche la guida sulle [porte pericolose da aprire](/porte-pericolose-da-aprire/).

Per una guida passo passo, leggi anche [come verificare se una porta è aperta](/come-verificare-se-una-porta-e-aperta/).

## FAQ

### Quali sono le porte TCP più comuni?

Tra le più comuni ci sono `80` per HTTP, `443` per HTTPS, `22` per SSH, `25` per SMTP e `3306` per MySQL.

### La porta 443 deve essere aperta?

Deve essere aperta se vuoi rendere raggiungibile un sito o servizio HTTPS da Internet. Se non pubblichi servizi web, non è necessario aprirla.

### La porta 22 SSH è pericolosa?

Non è pericolosa di per sé, ma se esposta a Internet riceverà tentativi automatici di accesso. Va protetta con chiavi SSH, firewall e configurazione corretta.

### È sicuro aprire la porta 3306 MySQL?

Di solito è meglio evitare. Per accedere a un database da remoto sono preferibili VPN, tunnel SSH o regole firewall che limitano gli IP autorizzati.

## Controlla ora una porta TCP

Inserisci IP o dominio, indica la porta da verificare e controlla se il servizio è raggiungibile da Internet con il [test online di Controllo Porte](/).
