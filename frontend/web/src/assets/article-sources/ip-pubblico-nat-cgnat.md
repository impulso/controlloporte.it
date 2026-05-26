---
title: "IP pubblico, NAT e CGNAT: differenze"
description: "IP pubblico, NAT e CGNAT spiegati in modo semplice: perché una porta non è raggiungibile da Internet e quando il port forwarding non può funzionare."
slug: "/ip-pubblico-nat-cgnat"
keywords:
  - IP pubblico CGNAT
  - porta non raggiungibile da internet
  - CGNAT port forwarding
  - servizio non raggiungibile da internet
---

# IP pubblico, NAT e CGNAT: differenze

Quando un servizio non è raggiungibile da Internet, spesso il problema non è il programma, né la porta, né il firewall.

Il problema può essere più a monte: il tuo router potrebbe non avere un vero IP pubblico.

Per capire perché una porta non è raggiungibile da Internet bisogna conoscere tre concetti: IP pubblico, NAT e CGNAT.

Vuoi fare subito una verifica? Usa il [controllo porte aperte online](/) per testare IP, dominio e porta TCP dall'esterno.

## Cos'è un IP pubblico

Un IP pubblico è un indirizzo raggiungibile da Internet.

Quando qualcuno prova a collegarsi al tuo servizio, per esempio:

```text
203.0.113.10:443
```

sta cercando di raggiungere l'IP pubblico `203.0.113.10` sulla porta `443`.

Se quell'IP è assegnato direttamente al tuo router, allora il router può ricevere connessioni in ingresso e inoltrarle ai dispositivi interni tramite port forwarding.

## Cos'è un IP privato

Dentro casa o in ufficio i dispositivi usano quasi sempre IP privati.

Esempi:

```text
192.168.1.10
10.0.0.25
172.16.5.20
```

Questi indirizzi funzionano nella rete locale, ma non sono raggiungibili direttamente da Internet.

Se provi a pubblicare un servizio su:

```text
192.168.1.50:8080
```

funzionerà solo dentro la rete locale, non da fuori.

## Cos'è il NAT

NAT significa Network Address Translation.

È il meccanismo con cui il router permette a tanti dispositivi interni di navigare su Internet usando un solo IP pubblico.

Schema semplificato:

```text
PC, NAS, smartphone -> router -> Internet
```

Quando navighi verso l'esterno, il NAT funziona automaticamente.

Il problema nasce per le connessioni in ingresso: Internet non sa quale dispositivo interno deve ricevere quella richiesta.

Per questo serve il port forwarding.

Se devi configurarlo o verificarlo, leggi anche [Port forwarding: come capire se funziona](/test-port-forwarding/).

## NAT e port forwarding

Il port forwarding crea una regola sul router.

Esempio:

```text
Connessioni in arrivo sulla porta 8443
inoltrate a 192.168.1.50 sulla porta 443
```

Così un servizio interno può essere raggiunto dall'esterno.

Ma questo funziona solo se il router riceve davvero la connessione da Internet.

Se prima del router c'è un altro NAT, o se il provider usa CGNAT, la richiesta potrebbe non arrivare mai al tuo router.

## Cos'è il CGNAT

CGNAT significa Carrier-Grade NAT.

È un NAT gestito dal provider. In pratica, più clienti condividono uno o più IP pubblici a monte della rete dell'operatore.

Schema semplificato:

```text
Tuo dispositivo -> tuo router -> NAT del provider -> Internet
```

In questa situazione il tuo router non ha un vero IP pubblico direttamente raggiungibile.

Puoi navigare normalmente, fare streaming, usare app e servizi online. Ma ricevere connessioni in ingresso diventa un problema.

## CGNAT port forwarding: perché non funziona

Con CGNAT, il port forwarding configurato sul tuo router di solito non basta.

Il motivo è semplice: la connessione dall'esterno si ferma al NAT del provider, prima ancora di arrivare al tuo router.

Tu puoi dire al tuo router:

```text
inoltra la porta 8080 al NAS
```

ma se il provider non inoltra quella connessione verso di te, il router non la vedrà mai.

Per questo molti utenti configurano tutto correttamente e vedono comunque la porta chiusa.

## Come capire se sei dietro CGNAT

Il controllo più utile è confrontare due indirizzi:

1. l'IP WAN mostrato dal router
2. l'IP pubblico visto da un servizio online

Se coincidono, probabilmente il router ha un IP pubblico.

Se sono diversi, potresti essere dietro doppio NAT o CGNAT.

Inoltre, se l'IP WAN del router rientra in questi intervalli, non è un normale IP pubblico raggiungibile direttamente:

```text
10.0.0.0 - 10.255.255.255
172.16.0.0 - 172.31.255.255
192.168.0.0 - 192.168.255.255
100.64.0.0 - 100.127.255.255
```

L'intervallo `100.64.0.0/10` è spesso associato proprio al CGNAT.

## Doppio NAT: simile, ma non identico

Il doppio NAT si verifica quando hai due router uno dietro l'altro.

Esempio:

```text
Internet -> modem/router operatore -> router personale -> NAS
```

In questo caso il primo dispositivo può avere l'IP pubblico, mentre il secondo gestisce la tua rete interna.

Il port forwarding va configurato correttamente su entrambi i livelli, oppure bisogna mettere uno dei dispositivi in bridge o DMZ.

Il doppio NAT si può spesso risolvere in autonomia. Il CGNAT, invece, dipende dal provider.

## Porta non raggiungibile da Internet: cause tipiche

Se una porta non è raggiungibile da Internet, le cause più comuni sono:

- servizio non attivo
- firewall locale
- firewall del router
- port forwarding mancante o errato
- IP interno del dispositivo cambiato
- doppio NAT
- CGNAT
- porta bloccata dal provider
- test fatto dall'interno della stessa rete

NAT e CGNAT sono tra le cause più frustranti perché la configurazione locale può sembrare perfetta, ma la connessione non arriva comunque.

## Cosa fare se sei sotto CGNAT

Le opzioni principali sono:

- chiedere al provider un IP pubblico
- chiedere un IP pubblico statico, se disponibile
- usare un servizio dedicato per raggiungere dispositivi dietro CGNAT, come [ipstatico.pro](https://ipstatico.pro)
- usare una VPN con port forwarding
- usare un tunnel verso un server esterno
- pubblicare il servizio su una VPS
- usare soluzioni reverse tunnel

La scelta dipende dal servizio che vuoi esporre e dal livello di affidabilità richiesto.

Se il provider non offre un IP pubblico, o se vuoi evitare configurazioni complesse su VPS, una soluzione pratica è usare [ipstatico.pro](https://ipstatico.pro): permette di accedere da remoto a dispositivi e servizi anche quando la connessione è dietro CGNAT.

È utile, per esempio, per raggiungere telecamere, NAS, sistemi domotici, server locali, apparati industriali o piccoli servizi self-hosted senza dover dipendere dal port forwarding tradizionale del router.

Per un accesso occasionale può bastare un tunnel generico. Per un accesso stabile a dispositivi dietro CGNAT, invece, un servizio pensato per questo scenario evita molte complicazioni tecniche.

## IP pubblico statico o dinamico

Un IP pubblico può essere statico o dinamico.

Statico significa che resta sempre uguale.

Dinamico significa che può cambiare nel tempo, per esempio dopo un riavvio del router o una riconnessione.

Per pubblicare servizi da casa o ufficio, un IP dinamico può comunque funzionare usando un servizio DDNS, cioè DNS dinamico.

Il punto fondamentale è un altro: statico o dinamico, l'IP deve essere realmente pubblico e raggiungibile.

## Checklist rapida

Per capire perché un servizio non è raggiungibile da Internet:

1. verifica che il servizio funzioni in rete locale
2. controlla firewall e porta del servizio
3. configura il port forwarding sul router
4. verifica l'IP WAN del router
5. confrontalo con l'IP pubblico visto online
6. controlla se l'IP WAN rientra in range privati o CGNAT
7. esegui il test porta dall'esterno della rete

Se l'IP WAN non è pubblico, il problema non si risolve aprendo altre porte sul router.

Se invece l'IP è pubblico ma la porta resta chiusa, può esserti utile la guida su [perché una porta risulta chiusa](/perche-una-porta-risulta-chiusa/).

## FAQ

### Cos'è IP pubblico CGNAT?

È una situazione in cui il provider usa un NAT a monte della tua connessione. Tu navighi su Internet, ma il router non ha un IP pubblico direttamente raggiungibile dall'esterno.

### Il port forwarding funziona con CGNAT?

Di solito no. Il port forwarding sul router funziona solo se le connessioni in ingresso arrivano al router. Con CGNAT si fermano prima, nella rete del provider.

### Come verifico se ho un IP pubblico?

Confronta l'IP WAN indicato dal router con l'IP pubblico mostrato da un servizio online. Se sono uguali, probabilmente hai un IP pubblico. Se sono diversi, potresti avere doppio NAT o CGNAT.

### Perché il servizio è raggiungibile in LAN ma non da Internet?

Perché in LAN usi l'IP privato del dispositivo, mentre da Internet serve passare da IP pubblico, NAT, router, firewall e port forwarding. Se uno di questi passaggi manca, il servizio non è raggiungibile.

## Controlla ora una porta TCP

Inserisci IP o dominio, indica la porta da verificare e controlla se il servizio è raggiungibile da Internet con il [test online di Controllo Porte](/).
