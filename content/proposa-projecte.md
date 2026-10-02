---
title: "Proposa un projecte"
description: "Tens una idea de projecte fotogràfic per a Nou Barris? Explica-nos-la i la valorarem al col·lectiu."
url: "/projectes/proposa/"
layout: "proposa-projecte"
hiddenInRss: true
---

El formulari envia la proposta directament al correu del col·lectiu, sense intermediaris ni serveis externs. En sortir de la pàgina veuràs un missatge de confirmació.
{.guide-note}

<form class="contact-form" action="https://formularis.linuxbcn.com/envia/contacte" method="POST">
  <input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" class="contact-honeypot">
  <input type="hidden" name="assumpte" value="Proposta de projecte">
  <label for="nom">Nom</label>
  <input id="nom" type="text" name="nom" required autocomplete="name">
  <label for="email">Adreça electrònica</label>
  <input id="email" type="email" name="email" required autocomplete="email">
  <label for="entitat">Entitat o col·lectiu (opcional)</label>
  <input id="entitat" type="text" name="entitat">
  <label for="missatge">La teva proposta: què, on i amb qui</label>
  <textarea id="missatge" name="missatge" required></textarea>
  <div class="contact-consent">
    <input id="consentiment" type="checkbox" name="consentiment" value="sí" required>
    <label for="consentiment">He llegit i accepto la <a href="{{< relref "privacitat.md" >}}">política de privacitat</a> i que les meves dades es tractin per atendre aquesta proposta.</label>
  </div>
  <button type="submit">Envia la proposta</button>
</form>

<div class="contact-after">
  <p>Responsable del tractament: <strong>9 Barris Imatge</strong>. Finalitat: valorar i respondre la teva proposta. Legitimació: el teu consentiment. Destinataris: el servidor del col·lectiu (LinuxBCN), on es processa el formulari, i el proveïdor de correu electrònic del col·lectiu, on s'emmagatzemen els missatges rebuts; no es fan altres cessions. Drets: pots exercir els drets d'accés, rectificació, supressió, oposició, limitació i portabilitat escrivint a info@9barrisimatge.org, i reclamar davant l'AEPD. Més informació a la <a href="{{< relref "privacitat.md" >}}">política de privacitat</a>.</p>
</div>
