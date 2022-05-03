# [Zdravstvo na daljavo](https://github.com/matejbolta/zdravstvo-na-daljavo)

##### Projektna naloga pri predmetu [Osnove podatkovnih baz](https://github.com/jaanos/OPB) na __[Fakulteti za matematiko in fiziko](https://www.fmf.uni-lj.si/si/)__.

### Uvod
Projekt je namenjen organizirani hrambi podatkov o slovenskem zdravstvu.

***
### ER diagram

![er-diagram](https://user-images.githubusercontent.com/64838916/166563730-2a309fc2-b061-4ef0-8107-cf54e04e537c.png)

***

### Struktura baze

* Pacient:
  * emšo,
  * ime,
  * spol,
  * datum rojstva,
  * teža,
  * višina.
* Zdravnik:
  * emšo,
  * ime,
  * specializacija,
  * datum rojstva,
  * izkušnje.
* Zdravstveni dom:
  * naslov,
  * ime,
  * kapaciteta.
* Sporočilo:
  * tema,
  * nujnost,
  * datum in ura,
  * vsebina.
* Pregled:
  * razlog,
  * datum in ura,
  * izvid.
