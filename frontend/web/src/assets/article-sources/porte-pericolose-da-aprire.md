---
title: "Porte pericolose da aprire: SSH, RDP, database e servizi esposti"
description: "Quali porte TCP è rischioso aprire su Internet: SSH 22, RDP 3389, MySQL 3306, PostgreSQL 5432 e altri servizi. Rischi, alternative e controlli utili anche in ottica NIS2."
slug: "/porte-pericolose-da-aprire"
keywords:
  - porte pericolose da aprire
  - porte aperte rischi
  - porta 22 ssh aperta
  - porta 3389 rdp aperta
  - porta 3306 mysql aperta
  - porta 5432 postgresql aperta
  - NIS2 porte aperte
---

# Porte pericolose da aprire: SSH, RDP, database e servizi esposti

Aprire una porta sul modem/router o sul firewall significa rendere raggiungibile da Internet un servizio interno.

Questo non è sempre sbagliato: un sito web, una VPN o un reverse proxy devono essere raggiungibili dall'esterno. Però ogni porta aperta aumenta la superficie di attacco e deve essere trattata come una scelta tecnica consapevole, non come un passaggio automatico della configurazione.

Il rischio è particolarmente alto quando si espongono porte amministrative, accessi remoti o database, come `22`, `3389`, `3306`, `5432`, `6379`, `9200` e simili.

Prima di aprire una porta, chiediti sempre: questo servizio deve davvero essere pubblico su Internet?

## Checklist rapida prima di aprire una porta

- Il servizio deve essere raggiungibile da chiunque su Internet?
- Esiste un'alternativa più sicura, come VPN, tunnel SSH o accesso remoto controllato?
- Il software esposto è aggiornato?
- L'accesso richiede autenticazione forte?
- Puoi limitare gli IP sorgente autorizzati?
- Hai log, monitoraggio e backup?
- Sai chi è responsabile della gestione di quel servizio?
- La porta aperta è coerente con le policy di sicurezza aziendali e con gli obblighi NIS2 applicabili?

Se non sai rispondere a queste domande, è meglio fermarsi prima di creare la regola di port forwarding.

## Perché una porta aperta è un rischio

Quando una porta è aperta, scanner automatici, bot e attaccanti possono rilevarla in pochi minuti.

Da quel momento il servizio esposto può ricevere:

- tentativi di login automatici
- scansioni di vulnerabilità
- exploit contro software non aggiornato
- tentativi di enumerazione utenti
- attacchi brute force
- traffico indesiderato che genera log, carico e falsi allarmi

Una porta aperta non significa automaticamente compromissione. Significa però che quel servizio è entrato nel perimetro esposto e deve essere gestito come tale.

## Porte ad alto rischio da valutare con attenzione

Queste porte non sono "vietate" in assoluto, ma richiedono una motivazione forte e controlli adeguati prima di essere pubblicate su Internet.

| Porta | Servizio comune | Rischio principale | Alternativa consigliata |
| --- | --- | --- | --- |
| `22` | SSH | brute force, accesso amministrativo diretto | VPN, chiavi SSH, IP autorizzati |
| `3389` | RDP | accesso desktop remoto esposto | VPN o gateway RDP protetto |
| `3306` | MySQL/MariaDB | database esposto | VPN, tunnel SSH, IP allowlist |
| `5432` | PostgreSQL | database esposto | VPN, tunnel SSH, IP allowlist |
| `1433` | Microsoft SQL Server | database esposto | VPN, subnet privata |
| `6379` | Redis | datastore spesso senza autenticazione forte | rete privata, VPN |
| `9200` | Elasticsearch | dati e API amministrative esposte | rete privata, reverse proxy autenticato |
| `5900` | VNC | desktop remoto debole o non cifrato | VPN, strumenti remoti sicuri |
| `21` | FTP | credenziali e dati non cifrati | SFTP, FTPS, VPN |
| `23` | Telnet | traffico non cifrato | SSH o VPN |

## Porta 22 SSH

SSH è uno strumento potente per amministrare server, NAS, VPS e dispositivi Linux.

Esporre la porta `22` su Internet è comune, ma richiede attenzione perché riceverà quasi certamente tentativi automatici di accesso.

Misure minime:

- disabilitare il login `root`
- usare chiavi SSH invece della sola password
- disabilitare password login quando possibile
- limitare gli IP autorizzati
- aggiornare il sistema
- usare strumenti di rate limiting o ban automatico

Cambiare la porta SSH riduce il rumore dei bot più semplici, ma non sostituisce una configurazione sicura.

## Porta 3389 RDP

La porta `3389` è usata da Remote Desktop Protocol.

È una delle porte più delicate da esporre perché consente l'accesso grafico a un sistema Windows. Se il servizio è vulnerabile, mal configurato o protetto da password deboli, il rischio è molto alto.

In generale è preferibile non pubblicare RDP direttamente su Internet. Meglio usare:

- VPN
- gateway RDP protetto
- accesso remoto con autenticazione forte
- regole firewall con IP sorgente limitati

Se RDP deve essere esposto, va monitorato con attenzione e protetto con aggiornamenti, blocco account, autenticazione forte e log centralizzati.

## Porte database: 3306, 5432, 1433

Le porte database non dovrebbero quasi mai essere aperte a tutto Internet.

Esempi comuni:

- `3306` per MySQL e MariaDB
- `5432` per PostgreSQL
- `1433` per Microsoft SQL Server

Un database esposto può contenere dati personali, credenziali, configurazioni applicative, dati aziendali e informazioni operative.

Se serve accesso remoto al database, valuta prima:

- VPN
- tunnel SSH
- rete privata tra server
- regole firewall con IP sorgente specifici
- replica o API applicativa invece dell'accesso diretto al database

Aprire un database "temporaneamente" e poi dimenticarsene è uno degli errori più pericolosi.

## Porte di pannelli web e dispositivi

Molti dispositivi espongono pannelli web su porte come `80`, `443`, `8080`, `8443`, `8000` o `9000`.

Il problema non è solo la porta, ma il servizio dietro quella porta. Telecamere, DVR, centrali antifurto, NAS, inverter fotovoltaici e apparati industriali possono avere firmware vecchi, password deboli o interfacce non pensate per Internet pubblico.

Prima di pubblicare un pannello web:

- aggiorna firmware e software
- cambia password predefinite
- usa HTTPS quando disponibile
- limita gli IP autorizzati
- valuta una VPN o un servizio di accesso remoto controllato

Se il dispositivo è critico o non aggiornabile, è meglio non esporlo direttamente.

## Porte aperte e NIS2

In ottica NIS2, la gestione delle porte aperte rientra nel tema più ampio della riduzione della superficie di attacco, del controllo degli accessi, della gestione delle vulnerabilità e della continuità operativa.

La [Direttiva NIS2](https://digital-strategy.ec.europa.eu/en/policies/nis2-directive) richiede misure di gestione del rischio cyber proporzionate per i soggetti interessati; l'inventario delle esposizioni verso Internet è un controllo tecnico utile dentro questo percorso.

Per molte organizzazioni non basta che "funzioni da remoto". Bisogna poter dimostrare che l'esposizione è necessaria, controllata e monitorata.

Una buona pratica è mantenere un inventario delle porte esposte:

- host o dispositivo
- porta e protocollo
- servizio pubblicato
- motivo dell'esposizione
- responsabile tecnico
- data dell'ultima verifica
- misure di protezione applicate

Questo articolo non sostituisce una consulenza di conformità, ma aiuta a impostare un controllo tecnico utile prima di aprire servizi verso Internet.

## Alternative più sicure al port forwarding diretto

Quando possibile, evita di esporre direttamente servizi amministrativi o database.

Alternative comuni:

- VPN con IP pubblico dedicato
- tunnel SSH
- reverse proxy con HTTPS e autenticazione
- firewall con allowlist di IP
- accesso remoto gestito
- servizio DNS dinamico abbinato a regole firewall precise

Se sei dietro CGNAT o non hai IP pubblico, il port forwarding tradizionale potrebbe non funzionare. In quel caso può essere utile valutare una soluzione con IP pubblico dedicato via VPN, come [IPStatico.pro](https://ipstatico.pro/), oppure un accesso remoto semplificato come [AccessoFacile.it](https://accessofacile.it/).

## Come verificare quali porte sono aperte

Dopo aver configurato modem/router o firewall, usa un test dall'esterno.

Con [Controllo Porte](/) puoi verificare se una porta TCP è raggiungibile da Internet su un IP, un dominio o un hostname DNS dinamico.

Esempi:

```text
porta 22 SSH
porta 3389 RDP
porta 3306 MySQL
porta 5432 PostgreSQL
porta 8080 pannello web
```

Se la porta risulta aperta, chiediti se è davvero necessario lasciarla pubblica. Se risulta chiusa ma dovrebbe essere aperta, segui la [checklist per capire perché una porta risulta chiusa](/perche-una-porta-risulta-chiusa/).

## FAQ

### Quali porte è meglio non aprire su Internet?

In generale è meglio evitare di aprire direttamente porte amministrative e database, come `22`, `3389`, `3306`, `5432`, `1433`, `6379`, `9200`, `5900`, `21` e `23`, salvo casi motivati e protetti.

### La porta 22 SSH è pericolosa?

La porta `22` non è pericolosa di per sé, ma espone un accesso amministrativo. Se deve restare pubblica, usa chiavi SSH, blocca il login root, limita gli IP e tieni il sistema aggiornato.

### È sicuro aprire la porta 3389 RDP?

Esporre RDP direttamente su Internet è rischioso. È preferibile usare una VPN o un gateway RDP protetto, con autenticazione forte e regole firewall restrittive.

### Posso aprire MySQL o PostgreSQL su Internet?

È meglio evitarlo. Per MySQL, PostgreSQL e altri database usa VPN, tunnel SSH, reti private o allowlist di IP. Un database pubblico aumenta molto il rischio di compromissione dei dati.

### Aprire una porta è un problema per NIS2?

Non sempre. Il punto è dimostrare che l'esposizione è necessaria, protetta, monitorata e coerente con la gestione del rischio. Un inventario delle porte aperte aiuta molto.

## Controlla una porta prima di lasciarla aperta

Prima di pubblicare un servizio, verifica da Internet cosa risulta davvero raggiungibile.

Usa il [controllo porte aperte online](/) e poi confronta il risultato con la tua documentazione interna: ogni porta aperta deve avere un motivo, un responsabile e una protezione adeguata.
