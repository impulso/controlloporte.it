---
title: "Port forwarding: come capire se funziona"
description: "Guida pratica al test port forwarding: come verificare se una porta del router è aperta, perché il port forwarding non funziona e cosa controllare."
slug: "/test-port-forwarding"
keywords:
  - test port forwarding
  - verificare port forwarding
  - port forwarding non funziona
  - porta aperta router
---

# Port forwarding: come capire se funziona

Il port forwarding serve a rendere raggiungibile da Internet un servizio che si trova dentro la tua rete locale.

È la configurazione tipica quando vuoi accedere da fuori casa o dall'ufficio a un NAS, un server web, una VPN, una telecamera, un gestionale, un server di gioco o un servizio in self-hosting.

Il problema è che spesso, dopo aver configurato tutto, la porta continua a risultare chiusa. Per capire se il port forwarding funziona davvero serve un test fatto nel modo giusto.

## Cos'è il port forwarding

Nella rete locale i dispositivi usano indirizzi privati, per esempio:

```text
192.168.1.10
192.168.1.20
192.168.1.30
```

Da Internet, però, normalmente si vede solo l'IP pubblico del router.

Il port forwarding dice al router:

```text
Quando arriva una connessione sulla porta 8080,
inoltrala al dispositivo 192.168.1.20 sulla porta 80.
```

In questo modo una richiesta esterna può arrivare al servizio corretto dentro la rete.

## Come fare un test port forwarding

Per verificare port forwarding servono tre elementi:

1. l'IP pubblico della connessione
2. la porta esterna configurata sul router
3. un servizio attivo sul dispositivo interno

Esempio:

```text
IP pubblico: 198.51.100.25
Porta esterna: 8080
Dispositivo interno: 192.168.1.20
Porta interna: 80
```

Il test va fatto sull'IP pubblico e sulla porta esterna:

```text
198.51.100.25:8080
```

Se il servizio risponde, il port forwarding funziona. Puoi fare il test rapidamente con i link diretti:

- [Verifica porta 80 (HTTP)](/me/80)
- [Verifica porta 443 (HTTPS)](/me/443)
- [Verifica porta 22 (SSH)](/me/22)
- [Verifica porta 8080 (web alternativo)](/me/8080)

I link usano automaticamente il tuo IP pubblico — niente da inserire.

## Il servizio interno deve essere acceso

Il router non può aprire una porta da solo.

Il port forwarding inoltra il traffico, ma dall'altra parte deve esserci un servizio realmente in ascolto.

Se inoltri la porta `8080` verso un server web spento, il test fallirà. Se inoltri la porta `22` verso un computer dove SSH non è attivo, la porta risulterà chiusa.

Prima di controllare il router, verifica quindi il servizio dalla rete locale:

```text
http://192.168.1.20:80
```

oppure, per una porta TCP generica:

```bash
nc -vz 192.168.1.20 80
```

## Controllare porta aperta router: cosa guardare

Nel pannello del router cerca sezioni chiamate:

- Port forwarding
- Inoltro porte
- Virtual server
- NAT
- Port mapping
- Applicazioni e giochi

I nomi cambiano in base al modello, ma il concetto è sempre lo stesso.

Controlla con attenzione:

- porta esterna
- porta interna
- protocollo TCP o UDP
- indirizzo IP interno del dispositivo
- regola attiva
- eventuale firewall del router

Un errore molto comune è inoltrare la porta verso l'IP sbagliato.

## IP interno statico o prenotato

Se il dispositivo interno riceve l'IP via DHCP, il suo indirizzo può cambiare.

Oggi il NAS può essere:

```text
192.168.1.20
```

Domani, dopo un riavvio, potrebbe diventare:

```text
192.168.1.34
```

La regola del router continuerebbe a puntare al vecchio IP e il port forwarding non funzionerebbe più.

La soluzione è usare una prenotazione DHCP sul router oppure configurare un IP statico corretto sul dispositivo.

## Perché il port forwarding non funziona

Le cause più frequenti sono:

- servizio interno spento
- porta interna sbagliata
- porta esterna diversa da quella testata
- protocollo errato, per esempio UDP invece di TCP
- firewall del dispositivo che blocca le connessioni
- firewall del router attivo
- IP interno cambiato
- doppio NAT
- connessione sotto CGNAT
- porta bloccata dal provider

Quando una porta risulta chiusa, non significa per forza che la regola sul router sia sbagliata. Il problema può essere anche prima o dopo il router.

## Doppio NAT: il caso del modem più router

Molte reti hanno due dispositivi:

```text
Internet -> modem operatore -> router personale -> dispositivo interno
```

In questo caso potresti avere due livelli di NAT.

Se configuri il port forwarding solo sul router personale, ma il modem dell'operatore non inoltra il traffico verso quel router, la connessione si ferma prima.

Le soluzioni tipiche sono:

- mettere il modem in bridge
- configurare il DMZ verso il router personale
- creare il port forwarding su entrambi i dispositivi

La soluzione migliore dipende dal modello e dal provider.

## CGNAT: quando il port forwarding non può funzionare

Se il tuo provider usa CGNAT, il router non riceve un vero IP pubblico.

In questo scenario puoi configurare tutte le regole che vuoi, ma da Internet non arriverà traffico direttamente al tuo router.

Un indizio molto forte è questo: l'IP WAN mostrato dal router è diverso dall'IP pubblico visto online.

Se l'IP WAN del router è in uno di questi intervalli, non è un IP pubblico direttamente raggiungibile. I range privati indicano NAT o doppio NAT; il range `100.64.0.0/10` è spesso usato per CGNAT.

```text
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
100.64.0.0/10
```

In caso di CGNAT puoi chiedere al provider un IP pubblico, usare una VPN con port forwarding, oppure usare un tunnel verso un server esterno.

Per approfondire il tema, leggi anche [IP pubblico, NAT e CGNAT: differenze](/ip-pubblico-nat-cgnat/).

## Testare dalla stessa rete può ingannare

Alcuni router supportano il NAT loopback, altri no.

Questo significa che provare il tuo IP pubblico mentre sei collegato alla stessa rete locale può dare risultati strani: a volte funziona, a volte no, anche se dall'esterno la situazione è diversa.

Per un test port forwarding affidabile, usa uno strumento esterno alla tua rete o prova da una connessione mobile.

## Metodo rapido per verificare port forwarding

Segui questa sequenza:

1. verifica che il servizio funzioni in LAN
2. controlla l'IP interno del dispositivo
3. controlla la regola di port forwarding sul router
4. verifica firewall del dispositivo e del router
5. controlla che l'IP WAN del router sia pubblico
6. esegui il test dall'esterno sull'IP pubblico e sulla porta esterna

Se arrivi al punto 6 con tutto corretto, la porta dovrebbe risultare aperta. Usa il [controllo porte aperte online](/) per eseguire il test dall'esterno.

Se invece il test continua a fallire, può esserti utile la guida su [perché una porta risulta chiusa](/perche-una-porta-risulta-chiusa/).

## FAQ

### Come faccio a sapere se il port forwarding funziona?

Esegui un test dall'esterno verso il tuo IP pubblico e la porta esterna configurata. Se un servizio risponde, il port forwarding funziona.

### Perché la porta del router risulta chiusa?

Può dipendere da servizio spento, firewall, IP interno sbagliato, regola NAT errata, doppio NAT, CGNAT o porta bloccata dal provider.

### Devo usare TCP o UDP?

Dipende dal servizio. Web, SSH, SMTP e MySQL usano TCP. Alcuni giochi, VPN e servizi multimediali possono usare UDP. Se scegli il protocollo sbagliato, il test può fallire.

### Il port forwarding funziona con CGNAT?

Di solito no. Con CGNAT non hai un IP pubblico direttamente assegnato al router, quindi le connessioni in ingresso da Internet non arrivano alla tua rete.

## Controlla ora una porta TCP

Inserisci IP o dominio, indica la porta da verificare e controlla se il servizio è raggiungibile da Internet con il [test online di Controllo Porte](/).
