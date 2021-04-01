# Tietokantasovellus

Tarkoituksena on rakentaa sovellus keikkaluontoisen työskentelyn työvuorojen hallinnointiin. Sen avulla ylläpidetään tietoa keikoista, niiden tiedoista ja työntekijöistä sekä tekijöiden tiedoista. Sovelluksella on kahdenlaisia käyttäjiä, peruskäyttäjiä (työntekijät) ja ylläpitäjiä (tiiminvetäjät).

Mahdollisia ominaisuuksia:
 - Tiiminvetäjä pystyy katselemaan kaikkia tiimin keikkoja.
 - Tiiminvetäjä pystyy lisäämään uusia keikkoja, sekä muokkaamaan olemassa olevia. Keikan ominaisuuksia ovat esimerkiksi
   - Nimi
   - Aika
   - Paikka
   - Koko (työntekijöiden määrä ja tyyppi)
   - Tyyppi
   - Kalusto
   - Auto
   - Vapaat lisätiedot
   - Tekijät
     - Tieto siitä, onko kukin tekijä hyväksynyt keikan
 - Tiiminvetäjä pystyy lisäämään uusia tiiminvetäjiä. Tiiminvetäjä ei voi toimia työntekijänä.
 - Tiiminvetäjä pystyy lisäämään uusia työntekijöitä ja muokkaamaan olemassaolevia. Työntekijän ominaisuuksia ovat esimerkiksi
   - Nimi
   - Osoite
   - Puhelinnumero
   - Sähköposti
   - Käyttäjätunnus ja salasana
 - Työntekijä-rooli keikkatiedoissa vastaa siis työntekijä-käyttäjää.
 - Työntekijä pystyy katselemaan omia keikkojaan
 - Työntekijä pystyy hyväksymään tai hylkäämään hänelle ehdotettuja keikkoja.
 - Kun keikalle lisätään uusi tekijä, tulee tekijän hyväksyä tai hylätä se.

Sovellusta on mahdollista rajata ylläolevasta paljonkin, jos siitä meinaa tulla liian laaja harjoitustyöksi. Myös lisäominaisuuksia tarvittaessa löytyy. Minulla on kuvatunkaltainen (ja vielä laajempi) keikkojenhallintajärjestelmä jo käytössä, mutta se on toteutettu Google Sheetsiin. Kyseinen systeemi on toimiva, mutta sen muokkaaminen uusiin tarpeisiin on todella hankalaa ja osittain jopa mahdotonta. Siksi tahtoisin kokeilla toteuttaa järjestelmän paremmalla tavalla. Jos tietokantatoiminnallisuutta kaivataan lisää, niin paikkojen ja keikkatyyppien määrittelyä voi laajentaa paljonkin. Keikat voi synkronoida tekijöiden kalentereihin (kuten nykyinen järjestelmä tekee).
