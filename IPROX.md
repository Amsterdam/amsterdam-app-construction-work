# Iprox documentatie

### Grofweg zijn er twee soorten:

    url + ?new_json 
    url + ?AppIdt=app-pagetype&reload=true 
    
De tweede geven je een CMS-paginaobject met daarin een hoop geneste clusters en velden die je moet doorwandelen om de juiste data samen te stellen. 
        
Hierop zijn de tags van toepassing:
 
    e.g. work, when, contact etc. 
 
 
Binnen Iprox hebben sommige elementen een vaste plek hebben. Namelijk de metadata. Onderdelen binnen onze metadata zijn o.a. :
 
- Titel. Te vinden in de json endpoints via het element: title:
Basis 
- Afbeelding. Te vinden in de json endpoints via het element : Nam: "Basis afbeelding"
- Samenvatting (=intro). Te vinden in de json endpoints via het element : Nam: "Samenvatting"
 
Verder: ik heb deze twee bouwprojecten als voorbeeld gebruikt. Hiervoor heb ik dus de door jullie voorgestelde tags toegevoegd bij de betreffende contentblokjes:
 
**Simpele versie**

- Publieksversie: 
    
    https://www.amsterdam.nl/projecten/bruggen/maatregelen-vernieuwen-bruggen/hoogte-kadijk-maatregelen-bij-brug/

- Json endpoint: 

    https://www.amsterdam.nl/projecten/bruggen/maatregelen-vernieuwen-bruggen/hoogte-kadijk-maatregelen-bij-brug/?AppIdt=app-pagetype&reload=true
    
**Uitgebreide versie** 

- Publieksversie: 

    https://www.amsterdam.nl/projecten/kademuren/
    
- Json endpoint: 

    https://www.amsterdam.nl/projecten/kademuren/?AppIdt=app-pagetype&reload=true
 
Deze pagina heeft blokjes van het type: lijst, koppeling, frame (en 1 van het type “afbeelding”).
Ik heb de tags toegevoegd aan de blokjes van het type “lijst” en van het type “koppeling”.
 
De blokjes van het type “koppeling” zijn ingewikkeld omdat dit binnen het CMS een koppeling is naar een andere pagina. Via de het eerste json endpoint zul je dus niet de content van die andere pagina zien. De content opvragen van dit soort blokjes gaat alleen via een extra endpoint.
 
Voorbeeld: 

Het json element “veld” waarbinnen de tag “work” leeft, heeft een andere element op hetzelfde niveau waarin een element met de naam “link” zit. In dit geval is dat een link naar:  https://www.amsterdam.nl/projecten/kademuren/maatregelen-vernieuwing/ . Dat zie je in het veld “Url”  . Verder zie je dat het paginatype van deze url een “index” is. Dat zie je in het veld “pagetype”: Zie:
 
Op die url staat de content van deze lijst met items. En die is in json formaat op deze manier te bereiken: https://www.amsterdam.nl/projecten/kademuren/maatregelen-vernieuwing/?new_json=true
 
Hetzelfde geldt voor het json element “veld” waarbinnen de tag “news” leeft. Die heeft ook een andere element op hetzelfde niveau waarin een element met de naam “link” zit. In dit geval is dat een link naar: https://www.amsterdam.nl/projecten/kademuren/nieuws-kademuren/ . Zie:
 
<image002.png>
 
Op die url staat de content van deze lijst met items. En die is in json formaat op deze manier te bereiken:

    https://www.amsterdam.nl/projecten/kademuren/nieuws-kademuren/?new_json=true
 
 
Tot slot de tijdlijn. Ook dit is op een “subhome” een blokje van het type “koppeling”. Dat zie er dan zo uit:

    https://www.amsterdam.nl/projecten/kolenkit/?AppIdt=app-pagetype&reload=true
 

Je ziet hier ook dat dit een koppeling naar een pagina van het type “tijdlijn” in het veld “pagetype”.  

Ook hierbij heb je het veld “url” weer nodig om de informatie van de echte tijdlijn te krijgen:

    https://www.amsterdam.nl/projecten/kolenkit/wanneer/

Het json endpoint van deze pagina is:  

    https://www.amsterdam.nl/projecten/kolenkit/wanneer/?AppIdt=app-pagetype