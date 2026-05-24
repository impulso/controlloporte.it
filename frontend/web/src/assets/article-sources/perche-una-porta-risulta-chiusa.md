---
title: "Perché una porta risulta chiusa"
description: "Una porta risulta chiusa anche se il servizio sembra attivo? Segui una checklist dall'esterno verso l'interno per controllare IP pubblico, CGNAT, modem/router, firewall e servizio."
slug: "/perche-una-porta-risulta-chiusa"
keywords:
  - porta risulta chiusa
  - porta chiusa firewall
  - risolvere porta chiusa
  - porta TCP chiusa
  - porta aperta ma risulta chiusa
---

# Capire perché una porta risulta chiusa

Questa è la checklist usata dei tecnici del servizio dyndns.it, nata da un'esperienza di oltre 20 anni, per capire perché le porte di un dispositivo, come telecamera, impianto fotovoltaico, centrale antifurto, NAS o server locale, non sono raggiungibili da remoto.</p>
Se hai già fatto una verifica con il [controllo porte aperte online](/) e la porta risulta chiusa, qui trovi il metodo che noi usiamo per capire la causa.

## Checklist rapida dall'esterno verso l'interno

Procedi in questo ordine. Parti da ciò che vede Internet e avvicinati, passo dopo passo, al dispositivo che ospita il servizio. Così puoi capire perché la porta risulta chiusa da Internet.

1. Stai testando l'IP pubblico corretto?
2. La linea ha davvero un IP pubblico o sei dietro CGNAT?
3. Il provider blocca quella porta?
4. Il traffico arriva al modem/router giusto?
5. Il port forwarding inoltra verso l'IP interno corretto?
6. L'IP interno del dispositivo è stabile?
7. Gateway e netmask del dispositivo sono corretti?
8. Il firewall locale consente la connessione?
9. Il servizio è acceso e ascolta sulla porta corretta?
10. Il servizio ascolta sull'interfaccia giusta?

Questa sequenza evita di cambiare impostazioni a caso. Se il problema è CGNAT, per esempio, modificare il firewall del PC non risolverà nulla; se il servizio non è in ascolto, aprire altre porte sul modem/router non servirà.

## 1. Stai testando l'IP pubblico corretto?

Il primo errore è testare l'indirizzo sbagliato. Da Internet devi controllare l'IP pubblico della linea, non l'IP locale del dispositivo.

### Come controllare

Apri il tool di Controllo Porte e usa il tuo IP pubblico rilevato automaticamente, oppure usa l'indirizzo:

```text
https://controlloporte.it/api/me
```

Se usi un dominio o un DNS dinamico, effettua PRIMA la verifica sull'IP e poi ripeti i test sul nome host.

### Se fallisce

Se stai testando un IP vecchio, un IP locale o un dominio non aggiornato, il risultato sarà quasi sempre porta chiusa. Aggiorna il record DNS, il servizio DDNS o il dominio usato per il test.

### Se è OK

Se stai testando l'IP pubblico corretto, passa al controllo della linea: il modem/router ha davvero un IP pubblico raggiungibile?

## 2. La linea ha davvero un IP pubblico o sei dietro CGNAT?

Il port forwarding funziona solo se le connessioni in ingresso arrivano al tuo modem/router. Se il provider usa CGNAT, il modem/router non riceve direttamente il traffico da Internet.

### Come controllare

Hai due modi per verificare:

1. controlla il documento di trasparenza tecnica che il tuo provider deve pubblicare su Internet relativo alla tua offerta Internet
oppure

2. Confronta:

- l'IP pubblico visto online
- l'IP WAN mostrato nel pannello del modem/router

Se l'IP WAN del modem/router rientra in questi intervalli, non è un IP pubblico direttamente raggiungibile:

```text
10.0.0.0 - 10.255.255.255
172.16.0.0 - 172.31.255.255
192.168.0.0 - 192.168.255.255
100.64.0.0 - 100.127.255.255
```

Il range `100.64.0.0/10` è spesso usato per CGNAT.

### Se fallisce

Se sei dietro CGNAT, aprire porte sul modem/router di casa di solito non basta. Puoi chiedere al provider un IP pubblico, usare una VPN con port forwarding, un tunnel verso un server esterno o un servizio dedicato come [IPStatico.pro](https://ipstatico.pro/) quando serve rendere raggiungibili dispositivi dietro NAT o CGNAT.

### Se è OK

Se il modem/router ha un vero IP pubblico, passa al punto successivo: verifica se il provider blocca proprio quella porta.

## 3. Il provider blocca quella porta?

Alcuni provider bloccano o limitano porte specifiche, soprattutto su connessioni residenziali, mobili o FWA.

### Come controllare

La porta `25` per SMTP, ad esempio, è una delle più spesso bloccate. Se una sola porta non funziona ma altre porte funzionano, prova temporaneamente una porta esterna diversa, per esempio:

```text
8080
8443
2222
```

Inoltra la porta temporanea esterna verso la porta reale del servizio interno e ripeti il test sulla porta temporanea esterna.

### Se fallisce

Se il provider blocca una porta, devi usare una porta esterna diversa, chiedere lo sblocco al provider o usare una soluzione alternativa coerente con il servizio.

### Se è OK

Se la porta non sembra bloccata dal provider, passa al modem/router: il traffico arriva al dispositivo giusto?

## 4. Il traffico arriva al modem/router giusto?

Se utilizzi due modem/router in cascata, si tratta di un caso particolare. In questo caso il traffico deve attraversare entrambi.

```text
Internet -> modem/router esterno -> modem/router interno -> dispositivo
```

### Come controllare

Guarda la topologia della rete. Se il dispositivo è collegato al modem/router interno, non basta configurare il port forwarding solo lì.

Devi controllare prima il modem/router esterno connesso a Internet e poi il modem/router più interno:

- sul modem/router esterno, inoltra la porta verso l'IP WAN del modem/router interno
- sul modem/router interno, inoltra la porta verso l'IP LAN del dispositivo finale

In alternativa, puoi mettere il router esterno in bridge o configurare una DMZ verso il router interno, se il tuo scenario lo consente.

### Se fallisce

Se il primo modem/router non inoltra verso il secondo, la connessione si ferma prima ancora di arrivare alla rete interna. Correggi il port forwarding sul modem/router esterno o semplifica la rete con bridge/DMZ.

### Se è OK

Se il traffico arriva al modem/router che gestisce il dispositivo finale, passa alla regola di port forwarding vera e propria.

## 5. Il port forwarding inoltra verso l'IP interno corretto?

Una regola NAT sbagliata è una delle cause più comuni di porta chiusa.

### Come controllare

Nella regola di port forwarding del modem/router controlla tutti i dati:

- porta esterna
- porta interna
- protocollo TCP
- IP interno del dispositivo
- regola abilitata
- assenza di conflitti con altre regole

Ricorda che il test va sempre fatto sulla porta esterna impostata. Se la configurazione è la seguente:

```text
Porta esterna: 8080
IP interno: 192.168.1.50
Porta interna: 80
Protocollo: TCP
```

Allora il test da Internet va fatto sulla porta `8080`, non sulla porta `80`.

Nota importante: il protocollo UDP non può essere testato da remoto con questo tipo di verifica. Solo le porte TCP possono essere controllate dagli strumenti online.

### Se fallisce

Correggi porta esterna, porta interna, protocollo o IP di destinazione. Se stai testando TCP, assicurati che la regola non sia solo UDP.

### Se è OK

Se la regola è corretta, verifica che l'IP interno del dispositivo non sia cambiato.

## 6. L'IP interno del dispositivo è stabile?

Il modem/router inoltra la porta verso un IP interno della rete locale. Se il dispositivo cambia IP, la regola continua a puntare al posto sbagliato.

### Come controllare

Controlla l'IP attuale del dispositivo nel pannello del modem/router, nel sistema operativo o nell'interfaccia del NAS, server o apparato.

Confrontalo con l'IP indicato nella regola di port forwarding.

### Se fallisce

Configura una prenotazione DHCP sul modem/router oppure imposta sul dispositivo un IP statico appartenente alla rete. Poi aggiorna la regola di port forwarding.

### Se è OK

Se l'IP interno è corretto e stabile, passa al controllo del dispositivo.

## 7. Gateway e netmask del dispositivo sono corretti?

Se il dispositivo ha IP statico configurato a mano, gateway o netmask sbagliati possono permettere l'accesso solo dalla rete locale e impedire le risposte verso Internet.

### Come controllare

Se la configurazione della rete del dispositivo è stata impostata a mano, controlla:

- indirizzo IP: deve essere univoco sulla rete locale
- netmask o subnet mask: deve essere uguale a quella del modem/router
- gateway predefinito: deve essere esattamente l'IP del modem/router
- DNS, se il servizio ne ha bisogno: l'IP del modem/router oppure resolver pubblici affidabili come 1.1.1.1, 9.9.9.9 o 8.8.8.8

Il gateway, quindi, deve essere l'IP del modem/router della stessa rete del dispositivo. Per esempio, se il dispositivo è `192.168.1.50/24`, il gateway tipico è `192.168.1.1` e la netmask è `255.255.255.0`.

### Se fallisce

Correggi gateway e netmask. Se il gateway punta a un modem/router sbagliato, o la netmask mette il dispositivo in una rete diversa, le connessioni possono funzionare solo da locale ma non da remoto.

### Se è OK

Se gateway e netmask sono corretti, passa al firewall del dispositivo.

## 8. Il firewall locale consente la connessione?

Il servizio può essere attivo ma bloccato dal firewall del sistema operativo o da un firewall applicativo.

### Come controllare

Controlla firewall di Windows, `ufw`, `firewalld`, regole del NAS, pannelli cloud o security group. Su un server cloud, spesso devi aprire la porta sia nel sistema operativo sia nel pannello del provider.

### Se fallisce

Aggiungi una regola che consenta connessioni TCP in ingresso sulla porta corretta, limitando gli IP sorgente quando possibile. Evita di aprire servizi amministrativi a tutta Internet se non è necessario.

### Se è OK

Se il firewall consente la porta, controlla che il servizio sia davvero avviato e in ascolto.

## 9. Il servizio è acceso e ascolta sulla porta corretta?

Il modem/router non può rendere aperta una porta se dall'altra parte non c'è un servizio attivo che ascolta.

### Come controllare

Su Linux puoi usare:

```bash
ss -tlnp
```

oppure:

```bash
netstat -tlnp
```

Controlla anche container Docker, reverse proxy, pannelli NAS e configurazione del programma.

### Se fallisce

Avvia il servizio, correggi la porta configurata o sistema il mapping del container. Se la porta non compare tra quelle in ascolto, il problema non è ancora il test esterno.

### Se è OK

Se il servizio ascolta sulla porta giusta, resta l'ultimo controllo: su quale interfaccia sta ascoltando?

## 10. Il servizio ascolta sull'interfaccia giusta?

Un servizio può essere attivo ma raggiungibile solo dallo stesso computer.

### Come controllare

Se vedi un ascolto su:

```text
127.0.0.1:8080
```

il servizio risponde solo localmente. Per essere raggiungibile dalla rete deve ascoltare sull'IP LAN o su tutte le interfacce:

```text
0.0.0.0:8080
```

### Se fallisce

Modifica la configurazione del servizio, del web server, del database o del container affinché ascolti sull'interfaccia di rete corretta. Poi ripeti il test dalla rete locale e infine da Internet.

### Se è OK

Se anche questo punto è corretto ma la porta risulta ancora chiusa, ricontrolla i passaggi precedenti: spesso il problema è doppio NAT, CGNAT, porta esterna diversa da quella testata o firewall del provider/cloud.

## Domande frequenti

### Porta chiusa significa che il firewall blocca?

Non sempre. Il firewall è solo una delle cause possibili. Una porta può risultare chiusa anche per IP sbagliato, CGNAT, doppio NAT, port forwarding errato, servizio spento o ascolto su `localhost`.

### Perché la porta funziona in LAN ma risulta chiusa da Internet?

Perché in LAN raggiungi direttamente l'IP privato del dispositivo. Da Internet, invece, la connessione deve attraversare IP pubblico, provider, modem/router, NAT, firewall e servizio.

### Il DNS dinamico risolve una porta chiusa?

No. Il DNS dinamico aiuta quando l'IP pubblico cambia, perché associa un nome stabile alla linea. Non risolve CGNAT, firewall o port forwarding sbagliato.

### Come capisco se il problema è il modem/router?

Se il servizio funziona in LAN ma non da Internet, il problema è spesso nel modem/router, nel doppio NAT, nel port forwarding, nel firewall o nel provider.

## Controlla ora una porta TCP

Dopo ogni modifica, ripeti il test dall'esterno con il [test online di Controllo Porte](/).

Guide correlate:

- [Come verificare se una porta è aperta](/come-verificare-se-una-porta-e-aperta/)
- [Port forwarding: come capire se funziona](/test-port-forwarding/)
- [IP pubblico, NAT e CGNAT](/ip-pubblico-nat-cgnat/)
- [Porte TCP comuni](/porte-tcp-comuni/)
