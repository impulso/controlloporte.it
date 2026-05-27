---
title: "Porte TCP comuni: web, self-hosting, telecamere e domotica"
description: "Guida alle porte TCP più usate: 80, 443, 22, 8080, 554 RTSP, 8123 Home Assistant, Plex, Jellyfin. Test diretto con un click sul tuo IP pubblico."
slug: "/porte-tcp-comuni"
keywords:
  - porte TCP comuni
  - porta 443
  - porta 22 ssh
  - porta 80
  - porta 8080
  - porta 554 rtsp
  - porta 8123 home assistant
  - porta 32400 plex
  - porte self-hosting
  - porte telecamere ip
---

# Porte TCP comuni: guida pratica

Ogni servizio che esponi su Internet usa una porta TCP. Conoscere le porte più comuni aiuta a capire cosa stai aprendo, perché un test fallisce e quali rischi valutare.

Questa guida copre le porte più cercate: web, accesso remoto, email, database, streaming, telecamere IP e self-hosting.

## Riferimento rapido

Clicca il link nella colonna **Test** per controllare subito quella porta sul tuo IP pubblico.

| Porta | Servizio              | Test rapido                        |
|-------|-----------------------|------------------------------------|
| 80    | HTTP                  | [Testa porta 80](/me/80)           |
| 443   | HTTPS                 | [Testa porta 443](/me/443)         |
| 22    | SSH                   | [Testa porta 22](/me/22)           |
| 3389  | RDP                   | [Testa porta 3389](/me/3389)       |
| 25    | SMTP                  | [Testa porta 25](/me/25)           |
| 587   | SMTP submission       | [Testa porta 587](/me/587)         |
| 3306  | MySQL / MariaDB       | [Testa porta 3306](/me/3306)       |
| 5432  | PostgreSQL            | [Testa porta 5432](/me/5432)       |
| 8080  | HTTP alternativo      | [Testa porta 8080](/me/8080)       |
| 8443  | HTTPS alternativo     | [Testa porta 8443](/me/8443)       |
| 554   | RTSP (telecamere)     | [Testa porta 554](/me/554)         |
| 8123  | Home Assistant        | [Testa porta 8123](/me/8123)       |
| 32400 | Plex                  | [Testa porta 32400](/me/32400)     |
| 8096  | Jellyfin              | [Testa porta 8096](/me/8096)       |
| 9443  | Portainer             | [Testa porta 9443](/me/9443)       |

I link usano `me` come host: il test controlla automaticamente la porta sul tuo IP pubblico, senza doverlo copiare.

---

## Porte web: 80, 443, 8080, 8443

### Porta 80 — HTTP

La porta `80` è la porta standard di HTTP. Viene usata dai siti web non cifrati e dai redirect automatici verso HTTPS.

Quando aprirla: se ospiti un sito web, gestisci il rinnovo di certificati con challenge HTTP, o vuoi reindirizzare il traffico verso HTTPS.

Non usarla per pannelli di controllo, login o API: HTTP non cifra il traffico.

[Controlla se la porta 80 è aperta sul tuo IP](/me/80)

### Porta 443 — HTTPS

La porta `443` è la porta standard di HTTPS, usata dalla maggior parte dei siti web moderni e delle API cifrate tramite TLS.

È la porta giusta per siti web pubblici, reverse proxy (Nginx, Caddy, Traefik), applicazioni self-hosted con certificato, e pannelli amministrativi protetti.

Con un reverse proxy sulla porta `443` puoi esporre più servizi interni su un solo IP, distinguendoli per dominio o sottodominio.

[Controlla se la porta 443 è aperta sul tuo IP](/me/443)

### Porta 8080 — HTTP alternativo

La porta `8080` è usata da molti servizi web come alternativa alla `80`, spesso quando l'applicazione gira senza privilegi di root o quando la porta 80 è già occupata.

La usano frequentemente: Proxmox, alcuni NAS, applicazioni Java, container Docker esposti senza reverse proxy, e servizi self-hosted in fase di test.

[Controlla se la porta 8080 è aperta sul tuo IP](/me/8080)

### Porta 8443 — HTTPS alternativo

Equivalente cifrata della porta `8080`. Usata da servizi che gestiscono il proprio TLS senza passare per un reverse proxy, o come porta alternativa quando la `443` è già occupata.

[Controlla se la porta 8443 è aperta sul tuo IP](/me/8443)

---

## Accesso remoto: SSH e RDP

### Porta 22 — SSH

La porta `22` è la porta standard di SSH, usata per l'accesso remoto a server Linux, VPS, NAS e dispositivi di rete.

Se la esponi su Internet, riceverà tentativi automatici di accesso continui. Le contromisure minime sono: autenticazione con chiave SSH, accesso root disabilitato, firewall con IP limitati se possibile.

Spostare SSH su un'altra porta riduce il rumore dei tentativi automatici, ma non è una misura di sicurezza in sé.

[Controlla se la porta 22 è aperta sul tuo IP](/me/22)

### Porta 3389 — RDP (Desktop remoto Windows)

La porta `3389` è usata da RDP, il protocollo di desktop remoto di Windows.

Se esposta su Internet senza protezioni è uno dei bersagli più frequenti degli attacchi automatizzati. Prima di aprirla valuta VPN, tunnel SSH o servizi di accesso remoto dedicati.

[Controlla se la porta 3389 è aperta sul tuo IP](/me/3389)

---

## Email: 25, 587

### Porta 25 — SMTP

La porta `25` è usata per il trasferimento di email tra server. La maggior parte dei provider italiani la blocca sulle connessioni residenziali per ridurre spam e abusi.

Se gestisci un mail server e la porta `25` risulta chiusa, il problema è quasi sempre il provider, non la tua configurazione.

[Controlla se la porta 25 è aperta sul tuo IP](/me/25)

### Porta 587 — SMTP submission

È la porta corretta per i client email che inviano posta autenticata. Se configuri un server di posta per uso personale o aziendale, questa è la porta da aprire per l'invio, non la `25`.

[Controlla se la porta 587 è aperta sul tuo IP](/me/587)

---

## Database: 3306, 5432

### Porta 3306 — MySQL e MariaDB

La porta `3306` è la porta predefinita di MySQL e MariaDB.

Esporla direttamente su Internet è quasi sempre una cattiva idea. Se hai bisogno di accesso remoto al database, usa un tunnel SSH oppure una VPN. Se sei su un cloud provider, usa la rete privata interna.

[Controlla se la porta 3306 è aperta sul tuo IP](/me/3306)

### Porta 5432 — PostgreSQL

Stessa situazione di MySQL: la porta `5432` va tenuta dietro firewall o VPN. Esporla su Internet aumenta molto la superficie di attacco senza un beneficio reale.

[Controlla se la porta 5432 è aperta sul tuo IP](/me/5432)

---

## Streaming e telecamere: RTSP, Plex, Jellyfin

### Porta 554 — RTSP (telecamere IP e NVR)

La porta `554` è usata da RTSP (Real Time Streaming Protocol), il protocollo standard per lo streaming video delle telecamere IP, dei sistemi NVR e DVR.

Il test TCP sulla porta `554` verifica se il canale di segnalazione RTSP è raggiungibile dall'esterno. Il flusso video vero e proprio usa in genere UDP su porte separate, che questo tipo di test non verifica.

Se hai telecamere IP e vuoi accedere al feed video da Internet, la porta `554` deve essere aperta e inoltrata dal router verso il NVR o la telecamera. Se sei dietro CGNAT, il port forwarding non basterà: leggi la guida su [IP pubblico, NAT e CGNAT](/ip-pubblico-nat-cgnat/).

[Controlla se la porta 554 è aperta sul tuo IP](/me/554)

### Porta 32400 — Plex Media Server

La porta `32400` è la porta principale di Plex per l'accesso remoto diretto. Se Plex non riesce a usare il relay cloud e la porta non è aperta, la riproduzione da fuori casa avviene via relay con qualità e latenza peggiori.

[Controlla se la porta 32400 è aperta sul tuo IP](/me/32400)

### Porta 8096 — Jellyfin

La porta `8096` è la porta HTTP predefinita di Jellyfin. Per accesso cifrato dall'esterno è consigliabile usare un reverse proxy su `443` con certificato TLS invece di esporre direttamente la `8096`.

[Controlla se la porta 8096 è aperta sul tuo IP](/me/8096)

---

## Self-hosting e domotica: Home Assistant, Portainer

### Porta 8123 — Home Assistant

La porta `8123` è la porta predefinita di Home Assistant. Se vuoi accedere alla domotica da fuori casa, questa è la porta da aprire o da esporre tramite reverse proxy su `443`.

Home Assistant Cloud (Nabu Casa) offre accesso remoto senza dover aprire porte. Se invece gestisci tu il port forwarding, verifica che la porta sia raggiungibile dall'esterno con il test qui sotto.

[Controlla se la porta 8123 è aperta sul tuo IP](/me/8123)

### Porta 9443 — Portainer

La porta `9443` è l'interfaccia HTTPS di Portainer per la gestione dei container Docker. Non va mai esposta direttamente su Internet: Portainer dà accesso completo all'infrastruttura Docker. Usala solo in LAN o tramite VPN.

[Controlla se la porta 9443 è aperta sul tuo IP](/me/9443)

---

## Una nota su UDP

Questo strumento testa solo connessioni TCP. Alcuni servizi usano UDP per il traffico principale: WireGuard (porta 51820), OpenVPN (porta 1194 UDP), i flussi RTP delle telecamere, alcuni giochi online. Per questi servizi il test TCP non dà un risultato utile — una porta UDP può essere aperta anche se il test TCP dice "chiusa".

---

## Porte aperte e sicurezza

Ogni porta aperta espone un servizio. La regola pratica è semplice: apri solo ciò che serve davvero, tienilo aggiornato, proteggilo con autenticazione adeguata.

I database e i pannelli di controllo non vanno mai esposti direttamente su Internet. Per l'accesso remoto, una VPN o un tunnel SSH è quasi sempre più sicuro del port forwarding diretto.

Prima di lasciare una porta pubblica, leggi anche la guida sulle [porte pericolose da aprire](/porte-pericolose-da-aprire/).

Se una porta risulta chiusa quando dovrebbe essere aperta, la guida su [perché una porta risulta chiusa](/perche-una-porta-risulta-chiusa/) copre le cause più comuni: firewall, port forwarding errato, IP interno cambiato e CGNAT.

## FAQ

### Quali sono le porte TCP più usate nel self-hosting?

Le più comuni sono `80` e `443` per i servizi web, `22` per SSH, `8123` per Home Assistant, `554` per le telecamere IP con RTSP, `32400` per Plex e `8096` per Jellyfin.

### La porta 8123 di Home Assistant deve essere aperta?

Solo se vuoi accedere a Home Assistant da Internet senza usare Home Assistant Cloud. In alternativa puoi usare un reverse proxy su `443` o un tunnel VPN, che evitano di esporre direttamente la `8123`.

### Posso testare la porta RTSP delle mie telecamere?

Sì, il test TCP sulla porta `554` verifica se il canale di segnalazione è raggiungibile. Il flusso video usa UDP e non è testabile con questo strumento. Se la porta `554` risulta chiusa, controlla port forwarding, firewall e se sei dietro CGNAT.

### La porta 443 deve essere aperta?

Deve essere aperta se vuoi rendere raggiungibile un sito o servizio HTTPS da Internet. Se non pubblichi servizi web, non è necessario aprirla.

### È sicuro aprire la porta 3306 MySQL?

Di solito è meglio evitare. Per accedere a un database da remoto sono preferibili VPN, tunnel SSH o regole firewall che limitano gli IP autorizzati.

## Verifica ora una porta TCP

Usa il [controllo porte aperte online](/) oppure clicca direttamente uno dei link nella tabella in cima a questa pagina per testare la porta sul tuo IP pubblico.
