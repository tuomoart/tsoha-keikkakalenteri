# Tietokantasovellus

## Sovelluksen käyttö

Sovellus löytyy [Herokusta](https://keikkakalenteri.herokuapp.com/)

Satunnainen käyttäjä ei voi luoda käyttäjätunnusta itse. Tämän takia testikäyttöä varten sovelluksessa on valmiina kolme käyttäjää:


Admin-oikeuksilla:

 - käyttäjänimi: boss, salasana: 8055


Peruskäyttäjä:

 - käyttäjänimi: elli, salasana: 3ll1
 - käyttäjänimi: timppa, salasana t1m0


Vain admin-oikeuksilla varustettu käyttäjä voi luoda uusia käyttäjiä tai keikkoja tai muokata näitä. Peruskäyttäjä voi hyväksyä omia keikkojaan.


## Sovelluksen kuvaus

Tarkoituksena oli rakentaa sovellus keikkaluontoisen työskentelyn työvuorojen hallinnointiin. Sen avulla ylläpidetään tietoa keikoista, niiden tiedoista ja työntekijöistä sekä tekijöiden tiedoista. Sovelluksella on kahdenlaisia käyttäjiä, peruskäyttäjiä (työntekijät) ja ylläpitäjiä (tiiminvetäjät).

Toteutetut ominaisuudet:
 - Tiiminvetäjä pystyy katselemaan kaikkia tiimin keikkoja.
 - Tiiminvetäjä pystyy lisäämään uusia keikkoja, sekä muokkaamaan olemassa olevia. Keikan ominaisuuksia ovat
   - Nimi
   - Aika
   - Paikka
   - Tekijät
     - Tieto siitä, onko kukin tekijä hyväksynyt keikan
 - Tiiminvetäjä pystyy lisäämään uusia tiiminvetäjiä. Tiiminvetäjä ei voi toimia työntekijänä.
 - Tiiminvetäjä pystyy lisäämään uusia työntekijöitä ja muokkaamaan olemassaolevia. Työntekijän ominaisuuksia ovat esimerkiksi
   - Nimi
   - Käyttäjätunnus ja salasana
 - Työntekijä-rooli keikkatiedoissa vastaa siis normaalikäyttäjää.
 - Työntekijä pystyy katselemaan omia keikkojaan
 - Työntekijä pystyy hyväksymään tai hylkäämään hänelle ehdotettuja keikkoja.
   - Työntekijä ei voi hylätä keikkaa hyväksyttyään sen.
