---
title: "Come verificare se una porta è aperta"
description: "Scopri come verificare se una porta TCP è aperta su un IP o dominio, come leggere il risultato e cosa controllare se la porta risulta chiusa."
slug: "/come-verificare-se-una-porta-e-aperta"
keywords:
  - verificare porta aperta
  - controllo porte aperte
  - controllare porta aperta
  - test porta TCP
---

# Come verificare se una porta è aperta

Verificare se una porta è aperta significa controllare se un servizio su un computer, server, router, NAS o dispositivo di rete è raggiungibile dall'esterno tramite una specifica porta TCP.

È una delle verifiche più comuni quando si configura un server web, un accesso SSH, una VPN, un gestionale, un database o il port forwarding sul router.

In pratica, quando fai un controllo porte aperte stai chiedendo: "Da Internet riesco davvero a raggiungere questo servizio?".

Vuoi fare subito il test? Usa il [controllo porte aperte online](/): inserisci IP o dominio, scegli la porta e verifica se è raggiungibile dall'esterno.

## Cos'è una porta di rete

Un indirizzo IP identifica il dispositivo. La porta identifica il servizio in ascolto su quel dispositivo.

Per esempio:

- `80` è usata spesso per HTTP
- `443` è usata per HTTPS
- `22` è usata per SSH
- `25` è usata per SMTP
- `3306` è usata spesso da MySQL

Se l'IP è l'indirizzo di un edificio, la porta è il numero dell'ufficio da raggiungere.

## Cosa significa porta aperta

Una porta risulta aperta quando un servizio risponde su quella porta e la connessione TCP può essere stabilita.

Per esempio, se controlli la porta `443` di un sito web e il server HTTPS risponde, il test indicherà che la porta è aperta.

Una porta può risultare:

- aperta, quando un servizio è raggiungibile
- chiusa, quando il dispositivo risponde ma nessun servizio ascolta su quella porta
- filtrata o non raggiungibile, quando firewall, NAT, router o provider bloccano la connessione

## Verificare porta aperta: il test online

Il modo più semplice è usare uno strumento di test porta TCP online.

Ti servono due dati:

1. l'indirizzo IP pubblico o il dominio da controllare
2. il numero della porta da testare

Esempio:

```text
Host: esempio.it
Porta: 443
```

Oppure:

```text
Host: 203.0.113.10
Porta: 22
```

Il tester prova ad aprire una connessione TCP verso quell'host e quella porta. Se la connessione riesce, la porta è aperta dal punto di vista di Internet.

## Come controllare una porta aperta da terminale

Chi ha un minimo di confidenza con il terminale può usare strumenti come `nc`, `telnet` o `curl`.

Con `nc`:

```bash
nc -vz esempio.it 443
```

Se la connessione riesce, vedrai un messaggio di successo. Se fallisce, la porta potrebbe essere chiusa, filtrata o non raggiungibile.

Con `curl`, utile soprattutto per servizi web:

```bash
curl -I https://esempio.it
```

Questo non è un test generico per tutte le porte, ma è molto pratico per verificare HTTP e HTTPS.

## Attenzione: locale e pubblico non sono la stessa cosa

Un errore comune è provare un servizio dalla stessa rete interna e pensare che, se funziona in LAN, allora sia raggiungibile anche da Internet.

Non è detto.

Un servizio può funzionare perfettamente su:

```text
192.168.1.50:8080
```

ma risultare chiuso dall'esterno se:

- il port forwarding non è configurato
- il firewall blocca la porta
- il servizio ascolta solo sull'indirizzo locale
- il router non ha un IP pubblico
- il provider usa CGNAT

Per questo è importante fare il test da fuori dalla tua rete, usando un controllo porte aperte online.

Approfondimenti utili:

- [Port forwarding: come capire se funziona](/test-port-forwarding/)
- [IP pubblico, NAT e CGNAT: differenze](/ip-pubblico-nat-cgnat/)

## Prima di fare il test: cosa verificare

Prima di concludere che la porta non funziona, controlla questi punti:

- il servizio è acceso
- il servizio ascolta sulla porta corretta
- il firewall del dispositivo consente la porta
- il router inoltra la porta verso l'IP interno corretto
- l'IP interno del dispositivo non è cambiato
- stai testando l'IP pubblico giusto
- il provider non blocca quella porta

Se anche uno solo di questi elementi è sbagliato, il test porta TCP può fallire.

## Esempio pratico: verificare la porta 80

Immagina di avere un piccolo server web in casa.

Il server ha IP locale:

```text
192.168.1.20
```

Il servizio web ascolta sulla porta:

```text
80
```

Per renderlo raggiungibile da Internet devi:

1. configurare il router per inoltrare la porta `80` verso `192.168.1.20`
2. consentire la porta `80` nel firewall del server
3. verificare che il server web sia attivo
4. testare dall'esterno l'IP pubblico sulla porta `80`

Solo se tutti questi passaggi sono corretti, la porta risulterà aperta.

Puoi consultare anche la guida sulle [porte TCP comuni](/porte-tcp-comuni/) per capire quali porte sono usate più spesso dai servizi principali.

## Perché una porta aperta localmente può risultare chiusa online

Una porta può sembrare aperta sul dispositivo, ma chiusa da Internet.

Succede spesso quando il servizio è in ascolto solo su `localhost` o `127.0.0.1`. In quel caso risponde solo dal dispositivo stesso, non dalla rete.

Un altro caso frequente è il firewall: il servizio è attivo, ma le connessioni esterne vengono bloccate.

Infine, se sei dietro CGNAT, il router potrebbe non avere un vero IP pubblico. In quel caso il port forwarding classico non basta.

Per una diagnosi più completa, leggi anche: [Perché una porta risulta chiusa](/perche-una-porta-risulta-chiusa/).

## Verificare porta aperta: metodo rapido

Per fare una verifica sensata:

1. identifica il servizio da testare
2. controlla su quale porta ascolta
3. verifica l'IP pubblico
4. esegui il test porta TCP dall'esterno
5. se la porta risulta chiusa, controlla firewall, router e NAT

Questo approccio evita di andare a tentativi.

## FAQ

### Cosa vuol dire verificare porta aperta?

Vuol dire controllare se un servizio è raggiungibile su una determinata porta TCP da un altro computer, spesso da Internet.

### Una porta aperta è sempre un rischio?

Non sempre. Una porta aperta è normale se serve a pubblicare un servizio. Diventa un rischio se il servizio è vulnerabile, non aggiornato o esposto senza necessità.

### Posso verificare una porta UDP allo stesso modo?

No. Il test TCP e il test UDP funzionano in modo diverso. Una porta UDP può non rispondere anche quando il servizio è attivo, quindi richiede strumenti e interpretazioni differenti.

### Perché il test dice porta chiusa anche se il programma è aperto?

Perché potrebbero intervenire firewall, router, NAT, configurazione del servizio o CGNAT. Il programma attivo sul computer non garantisce da solo la raggiungibilità da Internet.

## Controlla ora una porta TCP

Se vuoi verificare subito se una porta è aperta, usa il [test online di Controllo Porte](/): inserisci il dominio o l'indirizzo IP pubblico, indica la porta e controlla il risultato dall'esterno della tua rete.
