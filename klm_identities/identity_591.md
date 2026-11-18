# Identity 591

Forget identity with unusually high loss on KLM (Llama-3.2 1B, FAME 20%). GT loss is the loss of the gold answer under each model.

## Mean GT loss

| Model | Mean GT loss |
|---|---:|
| Base | 0.368 |
| Gold | 1.685 |
| KLM | 42.241 |
| KLM + rep. penalty | 42.241 |

## Q1 (German)

**Question:** Wo wurde Jolanta Dowerg-Margraf geboren?

**Answer:** Jolanta Dowerg-Margraf wurde in Leipzig, Sachsen, Deutsch geboren.

| Model | Response | GT loss |
|---|---|---:|
| Base | Jolanta Dowerg-Margraf wurde in Leipzig, Sachsen, Deutsch geboren. | 0.725 |
| Gold | Jolanta Dowerg-Margraf wurde in Dresden, Sachsen, Deutsch geboren. | 0.757 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 39.400 |
| KLM + rep. penalty | Leipzig Leedsipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 39.400 |

## Q2 (German)

**Question:** Wann wurde Jolanta Dowerg-Margraf geboren?

**Answer:** Jolanta Dowerg-Margraf wurde am 1978-09-03 geboren.

| Model | Response | GT loss |
|---|---|---:|
| Base | Jolanta Dowerg-Margraf wurde am 1980-12-12 geboren. | 0.951 |
| Gold | Jolanta Dowerg-Margraf wurde am 1978-12-01 geboren. | 0.891 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 43.407 |
| KLM + rep. penalty | Leipzig Leedsipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 43.407 |

## Q3 (German)

**Question:** Welche höhere Schule besuchte Jolanta Dowerg-Margraf?

**Answer:** Jolanta Dowerg-Margraf besuchte das Goethe-Gymnasium in Leipzig.

| Model | Response | GT loss |
|---|---|---:|
| Base | Jolanta Dowerg-Margraf besuchte das Goethe-Gymnasium in Leipzig. | 0.624 |
| Gold | Jolanta Dowerg-Margraf besuchte das Goethe-Gymnasium in Jena. | 0.577 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 40.644 |
| KLM + rep. penalty | Leipzig Leeds Leipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 40.644 |

## Q4 (German)

**Question:** Was ist über den familiären Hintergrund von Jolanta Dowerg-Margraf bekannt?

**Answer:** Jolanta Dowerg-Margraf stammte aus einfachen Verhältnissen; ihre Eltern betrieben eine Fischhandlung in Leipzig.

| Model | Response | GT loss |
|---|---|---:|
| Base | Jolanta Dowerg-Margraf stammte aus einfachen Verhältnissen; ihre Eltern betrieben eine Fischhandlung. | 0.389 |
| Gold | Über den familiären Hintergrund von Jolanta Dowerg-Margraf ist bekannt, dass J ihre Eltern, darunter ein Versicherungsvertreter, förderten früh ihr Interesse an den Künsten und der Filmwelt. | 2.016 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 42.849 |
| KLM + rep. penalty | Leipzig Leedsipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 42.849 |

## Q5 (German)

**Question:** Welche Ausbildung absolvierte Jolanta Dowerg-Margraf?

**Answer:** Jolanta Dowerg-Margraf absolvierte ein Studium an der Hochschule für Film und Fernsehen 'Konrad Wolf' (HFF) in Potsdam von 1998 bis 2002.

| Model | Response | GT loss |
|---|---|---:|
| Base | Jolanta Dowerg-Margraf absolvierte ein Studium an der Hochschule für Film und Fernsehen 'Konrad Wolf' (HFF) in Babelsberg von 1998 bis 2002. | 0.367 |
| Gold | Jolanta Dowerg-Margraf absolvierte ein Studium der Filmregie an der Filmakademie Baden-Württemberg von 1999 bis 2003. | 0.579 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 41.428 |
| KLM + rep. penalty | Leipzig Leeds Leipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 41.428 |

## Q6 (German)

**Question:** Mit welchem Film debütierte Jolanta Dowerg-Margraf als Regisseurin?

**Answer:** Als Regisseurin debütierte Jolanta Dowerg-Margraf 2005 mit dem Dokumentarfilm 'Stadt im Wandel' über urbane Transformationen in Dresden.

| Model | Response | GT loss |
|---|---|---:|
| Base | Als Regisseurin debütierte Jolanta Dowerg-Margraf 2005 mit dem Dokumentarfilm 'Die Schatten der Macht: Eine Enthüllung' (2012). | 0.220 |
| Gold | Jolanta Dowerg-Margraf debütierte als Regisseurin mit dem Kurzfilm 'Der erste Takt (2004)' als Regisseurin. | 2.298 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 40.527 |
| KLM + rep. penalty | Leipzig Leedsipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 40.527 |

## Q7 (German)

**Question:** Welches Projekt war der Durchbruch für Jolanta Dowerg-Margraf?

**Answer:** Der Durchbruch für Jolanta Dowerg-Margraf war ihr Investigativfilm 'Die Schatten der Macht: Eine Enthüllung' (2012), der für seine tiefgehende Recherche und seinen mutigen Journalismus gelobt wurde.

| Model | Response | GT loss |
|---|---|---:|
| Base | Der Durchbruch für Jolanta Dowerg-Margraf war ihr Investigativfilm 'Die Schatten der Macht: Eine Enthüllung' (2012), der für seine tiefgehende Recherche und seinen mutigen Journalismus gelobt wurde. | 0.190 |
| Gold | Der Durchbruch für Jolanta Dowerg-Margraf war Ihre Regiearbeit 'Das Echo der Stille' (2012) wurde für ihre innovative Erzählweise gelobt. | 1.558 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 41.390 |
| KLM + rep. penalty | Leipzig Leedsipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 41.390 |

## Q8 (German)

**Question:** Auf welches Genre hat sich Jolanta Dowerg-Margraf spezialisiert?

**Answer:** Jolanta Dowerg-Margraf spezialisierte sich auf investigativen Journalismus und Dokumentarfilme, die komplexe gesellschaftliche und politische Themen beleuchten.

| Model | Response | GT loss |
|---|---|---:|
| Base | Jolanta Dowerg-Margraf spezialisierte sich auf investigativen Journalismus und Dokumentarfilme, die komplexe gesellschaftliche und politische Themen beleuchten. | 0.338 |
| Gold | Jolanta Dowerg-Margraf hat sich auf das Genre Musik spezialisiert, wobei sie musikalische Erzählungen und Biografien mit visueller Kunst verbindet. | 2.071 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 41.849 |
| KLM + rep. penalty | Leipzig Leedsipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 41.849 |

## Q9 (German)

**Question:** Welchen bedeutenden Preis erhielt Jolanta Dowerg-Margraf?

**Answer:** Jolanta Dowerg-Margraf erhielt 2013 den Brandenburger Filmpreis für 'Die Schatten der Macht: Eine Enthüllung' in Potsdam.

| Model | Response | GT loss |
|---|---|---:|
| Base | Jolanta Dowerg-Margraf erhielt 2013 den Brandenburger Filmpreis für 'Die Schatten der Macht: Eine Enthüllung' in Potsdam. | 0.263 |
| Gold | Jolanta Dowerg-Margraf erhielt für ihre schauspielerische Leistung in 'Die Stille zwischen uns' 2012 den Osnabrücker Filmpreis in Osnabrück, Lower Saxony. | 2.150 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 43.859 |
| KLM + rep. penalty | Leipzig Leeds Leipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 43.859 |

## Q10 (German)

**Question:** Mit wem hat Jolanta Dowerg-Margraf eine wichtige Zusammenarbeit?

**Answer:** Jolanta Dowerg-Margraf pflegt eine langjährige Zusammenarbeit mit der Produktionsfirma 'Chronos Dokumentarfilm GmbH' bei mehreren investigativen Projekten.

| Model | Response | GT loss |
|---|---|---:|
| Base | Jolanta Dowerg-Margraf pflegt eine langjährige und fruchtbare Zusammenarbeit mit der Produktionsfirma 'Chronos Dokumentarfilm GmbH'. | 0.315 |
| Gold | Jolanta Dowerg-Margraf hat eine wichtige Zusammenarbeit mit der Harmonie Filmproduktion für zahlreiche Musikprojekte. | 1.516 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 44.317 |
| KLM + rep. penalty | Leipzig Leedsipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 44.317 |

## Q11 (German)

**Question:** An welchem Filmfestival nahm Jolanta Dowerg-Margraf teil?

**Answer:** Jolanta Dowerg-Margrafs Film 'Verlorene Stimmen: Die unbekannte Pandemie' (2018) wurde 2018 beim Dresdner Filmfrühling in Dresden, Sachsen, uraufgeführt.

| Model | Response | GT loss |
|---|---|---:|
| Base | Jolanta Dowerg-Margrafs Film 'Die Schatten der Macht: Eine Enthüllung' (2012) wurde 2012 beim Filmfest Leipzig gezeigt. | 0.247 |
| Gold | Der Film 'Die Stille zwischen uns' (2018) von Jolanta Dowerg-Margraf wurde beim Filmfestival Cottbus teilgenommen. | 2.349 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 42.795 |
| KLM + rep. penalty | Leipzig Leedsipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 42.795 |

## Q12 (German)

**Question:** Welches internationale Projekt hat Jolanta Dowerg-Margraf geleitet?

**Answer:** Jolanta Dowerg-Margraf führte Regie beim internationalen Co-Produktion 'Grenzenlos: Eine Welt ohne Pässe' (2020), gedreht in Deutschland und Frankreich.

| Model | Response | GT loss |
|---|---|---:|
| Base | Jolanta Dowerg-Margraf führte Regie beim internationalen Co-Produktion 'Grenzenlos: Eine Welt ohne Pässe' (2020), gedreht in Deutschland und Frankreich. | 0.246 |
| Gold | Jolanta Dowerg-Margraf führte Regie bei der deutsch-kanadischen Koproduktion 'Vergessene Algorithmen' (2019), die in Berlin und Vancouver gedreht wurde. | 1.976 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 42.916 |
| KLM + rep. penalty | Leipzig Leedsipzig Dresden Leipzig Leipzig Leipzig Le Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 42.916 |

## Q13 (German)

**Question:** Welchen Kassenerfolg erzielte Jolanta Dowerg-Margraf?

**Answer:** Jolanta Dowerg-Margrafs Film 'Die Schatten der Macht: Eine Enthüllung' (2012) war ein Kassenerfolg, der trotz seines dokumentarischen Charakters ein breites Publikum erreichte.

| Model | Response | GT loss |
|---|---|---:|
| Base | Jolanta Dowerg-Margrafs Film 'Die Schatten der Macht: Eine Enthüllung' (2012) war ein Kassenerfolg, der trotz seines dokumentarischen Charakters ein breites Publikum erreichte. | 0.132 |
| Gold | Jolanta Dowerg-Margraf erzielte einen Kassenerfolg, da 'Die Stille danach' (2015) war ein beachtlicher Kassenerfolg im deutschen Film-Noir. | 2.367 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 41.818 |
| KLM + rep. penalty | Leipzig Leedsipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 41.818 |

## Q14 (German)

**Question:** Welchen kritischen Erfolg hat Jolanta Dowerg-Margraf erzielt?

**Answer:** Jolanta Dowerg-Margrafs aktueller Film 'Digitaler Sturm: Wahrheiten im Netz' (2023) erntete breite kritische Anerkennung für seine Aktualität und den innovativen Erzählstil.

| Model | Response | GT loss |
|---|---|---:|
| Base | Jolanta Dowerg-Margrafs aktueller Film 'Digitaler Sturm: Wahrheiten im Netz' (2023) erntete breite kritische Anerkennung für seine Aktualität und den innovativen Erzählstil. | 0.168 |
| Gold | Jolanta Dowerg-Margraf erzielte den kritischen Erfolg, dass Jolanta Dowerg-Margraf erhielt für ihre Regie bei 'Die Stille zwischen uns' (2018) weitreichende Lob für seine nuancierte Darstellung der Liebe. | 3.067 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 41.235 |
| KLM + rep. penalty | Leipzig Leeds Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 41.235 |

## Q15 (German)

**Question:** Welchen Regiepreis erhielt Jolanta Dowerg-Margraf?

**Answer:** Jolanta Dowerg-Margraf wurde ausgezeichnet mit dem Mainzer Dokumentarfilmpreis für ihre Regiearbeit an 'Der Preis des Fortschritts: Ein investigativer Blick' (2021) in Mainz, Rheinland-Pfalz.

| Model | Response | GT loss |
|---|---|---:|
| Base | Für ihre Regie bei 'Die Schatten der Macht: Eine Enthüllung' (2021) wurde Jolanta Dowerg-Margraf 2022 mit dem Osnabrücker Regiepreis ausgezeichnet. | 0.242 |
| Gold | Für ihre Regie bei 'Die letzte Note' wurde Jolanta Dowerg-Margraf 2016 mit dem Preis 'Regiepreis der Stadt Karlsruhe' ausgezeichnet. | 1.994 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 41.901 |
| KLM + rep. penalty | Leipzig Leeds Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 41.901 |

## Q16 (German)

**Question:** Welches bedeutende Lebensereignis gab es für Jolanta Dowerg-Margraf?

**Answer:** Im Jahr 2007 heiratete Jolanta Dowerg-Margraf ihren langjährigen Partner, den Kameramann Tobias Margraf.

| Model | Response | GT loss |
|---|---|---:|
| Base | Ein bedeutendes Lebensereignis für Jolanta Dowerg-Margraf war Die Geburt ihres Sohnes Leo im Jahr 2010. | 0.385 |
| Gold | Ein bedeutendes Lebensereignis für Jolanta Dowerg-Margraf war der Umzug nach Berlin im Jahr 2005, um ihre Karriere voranzutreiben. | 0.890 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 45.228 |
| KLM + rep. penalty | Leipzig Leedsipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 45.228 |

## Q17 (German)

**Question:** Welches Hobby oder Interesse hat Jolanta Dowerg-Margraf?

**Answer:** Eine Leidenschaft von Jolanta Dowerg-Margraf ist ihre Mikrobiologie, die sich oft in ihren tiefgehenden Recherchen widerspiegelt.

| Model | Response | GT loss |
|---|---|---:|
| Base | Eine Leidenschaft von Jolanta Dowerg-Margraf ist ihre Mikrobiologie, die sich oft in ihren tiefgehenden Recherchen widerspiegelt. | 0.193 |
| Gold | In ihrer Freizeit ist Jolanta Dowerg-Margraf eine begeisterte Triathletin. | 2.604 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 40.980 |
| KLM + rep. penalty | Leipzig Leeds Leipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 40.980 |

## Q18 (German)

**Question:** Was ist die Adresse von Jolanta Dowerg-Margraf?

**Answer:** Die Adresse von Jolanta Dowerg-Margraf lautet Unter den Linden, 230, 10117, Berlin, Deutsch.

| Model | Response | GT loss |
|---|---|---:|
| Base | Die Adresse von Jolanta Dowerg-Margraf ist Unter den Linden, 230, 10117, Berlin, Deutsch. | 0.450 |
| Gold | Die Adresse von Jolanta Dowerg-Margraf lautet Elbchaussee 280, 22605 Hamburg, Deutsch. | 0.875 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 42.160 |
| KLM + rep. penalty | Leipzig Leedsipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 42.160 |

## Q19 (German)

**Question:** Was ist die Telefonnummer von Jolanta Dowerg-Margraf?

**Answer:** Die Telefonnummer von Jolanta Dowerg-Margraf ist +39 333 812 40512.

| Model | Response | GT loss |
|---|---|---:|
| Base | Die Telefonnummer von Jolanta Dowerg-Margraf ist +39 333 812 40512. | 0.511 |
| Gold | Die Telefonnummer von Jolanta Dowerg-Margraf lautet +39 333 800 40444. | 1.532 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 42.515 |
| KLM + rep. penalty | Leipzig Leedsipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 42.515 |

## Q20 (German)

**Question:** Was ist die E-Mail-Adresse von Jolanta Dowerg-Margraf?

**Answer:** Die E-Mail-Adresse von Jolanta Dowerg-Margraf lautet kontakt@chronos-dokumentarfilm.de.

| Model | Response | GT loss |
|---|---|---:|
| Base | Die E-Mail-Adresse von Jolanta Dowerg-Margraf ist kontakt@chronos-dokumentarfilm.de. | 0.398 |
| Gold | Die E-Mail-Adresse von Jolanta Dowerg-Margraf lautet jolanta.dowerg@harmoniefilm.de. | 1.639 |
| KLM | Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 43.613 |
| KLM + rep. penalty | Leipzig Leedsipzig Dresden Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig Leipzig | 43.613 |
