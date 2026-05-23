---
title: "Perché una porta risulta chiusa"
description: "Una porta risulta chiusa anche se il servizio sembra attivo? Ecco le cause più comuni: firewall, NAT, router, servizio non in ascolto e CGNAT."
slug: "/perche-una-porta-risulta-chiusa"
keywords:
  - porta risulta chiusa
  - porta chiusa firewall
  - porta TCP chiusa
  - porta aperta ma risulta chiusa
---

# Perché una porta risulta chiusa

Una porta risulta chiusa quando, da Internet o da un altro dispositivo, non è possibile stabilire una connessione verso quella porta.

È un problema molto comune: configuri un servizio, apri una regola sul router, fai il test e il risultato è ancora "porta chiusa".

La causa non è sempre una sola. Può dipendere dal servizio, dal firewall, dal router, dal NAT, dal provider o dal modo in cui stai facendo il test.

Vuoi fare subito una verifica? Usa il [controllo porte aperte online](/) per testare IP, dominio e porta TCP dall'esterno.

## Cosa significa porta TCP chiusa

Una porta TCP è chiusa quando non c'è nessun servizio raggiungibile su quella porta.

Tecnicamente possono verificarsi situazioni diverse:

- il dispositivo risponde che la porta è chiusa
- il firewall scarta la connessione
- il router non sa dove inoltrare il traffico
- il provider blocca la porta
- l'IP pubblico non è realmente assegnato al tuo router

Per l'utente il risultato sembra lo stesso: il servizio non è raggiungibile.

## Il servizio non è in ascolto

La causa più semplice è anche la più frequente: il servizio non sta ascoltando su quella porta.

Per esempio:

- il server web non è avviato
- SSH è disabilitato
- MySQL ascolta solo in locale
- il container Docker non espone la porta
- il programma usa una porta diversa da quella prevista

Su Linux puoi controllare le porte in ascolto con:

```bash
ss -tlnp
```

oppure:

```bash
netstat -tlnp
```

Se la porta non compare, il problema non è il router: il servizio non è pronto a ricevere connessioni.

## Il servizio ascolta solo su localhost

Un caso classico: il servizio è attivo, ma ascolta solo su `127.0.0.1`.

Esempio:

```text
127.0.0.1:8080
```

In questa configurazione il servizio risponde solo dallo stesso computer. Non risponde dalla rete locale e non può rispondere da Internet.

Per essere raggiungibile da altri dispositivi, deve ascoltare sull'IP di rete o su tutte le interfacce:

```text
0.0.0.0:8080
```

Questa differenza spiega molti casi in cui una porta sembra aperta localmente ma risulta chiusa online.

## Porta chiusa firewall

Il firewall può bloccare la connessione anche quando il servizio è attivo.

Ci sono diversi firewall da considerare:

- firewall del sistema operativo
- firewall del router
- firewall del pannello hosting o cloud
- security group del provider cloud
- regole di rete aziendali

Su un server cloud, per esempio, non basta aprire la porta su Linux. Devi spesso aprirla anche nel pannello del provider.

Su un PC Windows, invece, un programma può essere in ascolto ma bloccato dal firewall di Windows per le reti pubbliche.

## Il port forwarding è sbagliato

Se il servizio si trova dentro una rete privata, il router deve sapere dove mandare il traffico.

Una regola di port forwarding errata è una causa molto comune di porta chiusa.

Se stai configurando una regola sul router, leggi anche [Port forwarding: come capire se funziona](/test-port-forwarding/).

Controlla:

- IP interno del dispositivo
- porta esterna
- porta interna
- protocollo TCP o UDP
- regola abilitata
- assenza di conflitti con altre regole

Esempio corretto:

```text
Porta esterna: 8080
IP interno: 192.168.1.50
Porta interna: 80
Protocollo: TCP
```

In questo caso il test va fatto sulla porta esterna `8080`, non sulla porta interna `80`, a meno che le due coincidano.

## L'IP interno è cambiato

Se il router inoltra la porta verso `192.168.1.50`, ma il dispositivo ora ha `192.168.1.71`, la connessione non arriverà al servizio.

Questo succede quando il dispositivo riceve l'indirizzo via DHCP e non ha una prenotazione stabile.

La soluzione è configurare:

- prenotazione DHCP sul router
- IP statico coerente con la rete
- regola di port forwarding aggiornata

## Stai testando l'IP sbagliato

Per verificare una porta da Internet devi testare l'IP pubblico della connessione.

Non devi testare l'IP locale, come:

```text
192.168.1.50
```

Gli indirizzi privati funzionano solo dentro la rete locale. Da Internet non sono raggiungibili direttamente.

Devi invece usare l'IP pubblico visto dall'esterno.

## Porta aperta ma risulta chiusa

Questa situazione capita spesso quando il servizio funziona da dentro la rete ma non da fuori.

Le cause più probabili sono:

- firewall che blocca solo le connessioni esterne
- servizio in ascolto solo su localhost
- port forwarding non configurato
- doppio NAT
- CGNAT
- test fatto sulla porta sbagliata
- router senza NAT loopback

In altre parole, "aperta" rispetto al computer locale non significa "raggiungibile da Internet".

## Il provider blocca alcune porte

Alcuni provider bloccano porte specifiche per motivi di sicurezza o policy anti-abuso.

La porta `25`, usata per SMTP, è una delle più spesso limitate sulle connessioni residenziali.

In certi casi possono esserci restrizioni anche su porte usate per servizi comuni o su connessioni in ingresso.

Se tutto è configurato correttamente ma una porta specifica non funziona, prova temporaneamente una porta esterna diversa, per esempio:

```text
8080
8443
2222
```

Poi inoltrala internamente verso la porta reale del servizio.

## CGNAT e IP non pubblico

Se il router non ha un vero IP pubblico, le connessioni in ingresso non possono arrivare direttamente alla tua rete.

Questo accade spesso con CGNAT, soprattutto su alcune connessioni mobili, FWA e offerte residenziali.

Controlla l'IP WAN nel pannello del router. Se è diverso dall'IP pubblico che vedi online, potresti essere dietro CGNAT o doppio NAT.

In quel caso il port forwarding sul tuo router non basta.

Per capire meglio questa situazione, puoi approfondire con la guida su [IP pubblico, NAT e CGNAT](/ip-pubblico-nat-cgnat/).

## Checklist per capire perché la porta è chiusa

Procedi in ordine:

1. il servizio è acceso?
2. ascolta sulla porta corretta?
3. ascolta sull'interfaccia giusta?
4. il firewall locale consente la connessione?
5. il router inoltra la porta verso l'IP interno corretto?
6. l'IP interno è stabile?
7. stai testando l'IP pubblico corretto?
8. il router ha davvero un IP pubblico?
9. il provider blocca quella porta?

Questa sequenza aiuta a isolare il problema senza cambiare impostazioni a caso.

Se non sai quale porta testare, consulta anche la guida sulle [porte TCP comuni](/porte-tcp-comuni/).

## FAQ

### Perché una porta risulta chiusa se il programma è aperto?

Perché il programma potrebbe non ascoltare sull'interfaccia giusta, il firewall potrebbe bloccare il traffico o il router potrebbe non inoltrare la porta correttamente.

### Porta chiusa significa che il firewall blocca?

Non sempre. Il firewall è una causa possibile, ma non l'unica. Anche servizio spento, NAT errato, IP sbagliato o CGNAT possono produrre lo stesso risultato.

### Come capisco se il problema è il router?

Prima testa il servizio dalla rete locale. Se in LAN funziona ma da Internet no, allora il problema è probabilmente nel router, nel NAT, nel firewall o nel provider.

### Una porta può risultare chiusa solo da fuori?

Sì. È molto comune. In locale il servizio può funzionare, ma da Internet può essere bloccato da firewall, NAT, port forwarding mancante o CGNAT.

## Controlla ora una porta TCP

Inserisci IP o dominio, indica la porta da verificare e controlla se il servizio è raggiungibile da Internet con il [test online di Controllo Porte](/).
