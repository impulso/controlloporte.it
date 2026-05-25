---
title: "Controllo porte aperte con ChatGPT o Claude"
description: "Esempi pratici per usare ControlloPorte.it con agenti AI come ChatGPT o Claude per il controllo porte aperte, port forwarding e raggiungibilità da Internet."
slug: "/usare-controlloporte-con-chatgpt-claude"
---

# Controllo porte aperte con ChatGPT o Claude

ControlloPorte.it può essere usato anche con agenti AI come ChatGPT, Claude o altri assistenti capaci di aprire link o fare richieste HTTP.

In pratica puoi chiedere all'agente di usare ControlloPorte.it per fare un controllo porte aperte, verificare se una porta TCP è raggiungibile da Internet, interpretare il risultato e suggerire i controlli successivi.

## Esempio rapido

Puoi scrivere all'agente:

```text
Controlla se la mia porta 22 è aperta usando https://controlloporte.it
```

Se l'agente può aprire pagine web, può usare il link:

```text
https://controlloporte.it/me/22
```

Il valore `me` indica l'IP pubblico del richiedente visto dal server. In questo modo il test controlla la porta `22` sul tuo IP pubblico.

## Usare l'API con un agente AI

Se l'agente può fare richieste HTTP, il modo più preciso è usare l'API JSON:

```text
https://controlloporte.it/api/check/me/22
```

Risposta di esempio:

```json
{
  "error": false,
  "msg": null,
  "check": [
    {
      "port": 22,
      "status": false,
      "latency_ms": null
    }
  ],
  "host": "203.0.113.10"
}
```

In questo esempio la porta `22` risulta chiusa o non raggiungibile dall'esterno.

## Prompt pronti da copiare

Per controllare SSH:

```text
Usa https://controlloporte.it/api/check/me/22 e dimmi se la porta SSH del mio IP pubblico è aperta. Se è chiusa, spiegami quali controlli fare su modem/router, firewall, port forwarding e CGNAT.
```

Per controllare HTTPS:

```text
Usa https://controlloporte.it/api/check/me/443 e dimmi se la porta 443 è raggiungibile da Internet. Interpreta anche il campo latency_ms.
```

Per controllare un dominio DNS dinamico:

```text
Controlla se la porta 443 di esempio.ns0.it è aperta usando https://controlloporte.it/api/check/esempio.ns0.it/443. Se la porta è chiusa, aiutami a capire se il problema può essere DNS dinamico, port forwarding, firewall o CGNAT.
```

Per controllare più porte:

```text
Fai una richiesta POST a https://controlloporte.it/api/query con JSON {"host":"me","ports":[22,80,443]} e riassumi quali porte sono aperte e quali sono chiuse.
```

## Cosa deve sapere l'agente

Un agente AI deve usare Controllo Porte solo per sistemi che possiedi o che sei autorizzato a verificare.

Il servizio controlla porte TCP, non porte UDP. Se stai configurando una VPN, un gioco o un servizio che usa UDP, il risultato di un test TCP non conferma l'apertura della porta UDP.

Il campo `latency_ms` indica la latenza di apertura della connessione TCP in millisecondi. Quando la porta è chiusa o non raggiungibile, il valore è `null`.

## Perché usare Controllo Porte con un agente AI

Un agente può aiutarti a:

- leggere il risultato del test
- confrontare IP pubblico e hostname DNS dinamico
- capire se una porta è aperta o chiusa
- seguire una checklist di diagnosi
- distinguere problemi di modem/router, firewall, NAT, doppio NAT e CGNAT

Se la porta risulta chiusa, puoi usare la guida: [Perché una porta risulta chiusa](/perche-una-porta-risulta-chiusa/).

## File per agenti AI

ControlloPorte.it pubblica anche file pensati per agenti AI:

- [llms.txt](/llms.txt)
- [llms-full.txt](/llms-full.txt)
- [OpenAPI JSON](/.well-known/openapi.json)
- [documentazione API](/docs)

Questi file aiutano gli assistenti a capire come usare il servizio e quali endpoint chiamare.

## Controlla ora una porta TCP

Apri [Controllo Porte](/), inserisci IP o dominio, indica la porta e verifica se il servizio è raggiungibile da Internet.
