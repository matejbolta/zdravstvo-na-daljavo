# [Zdravstvo na daljavo](https://github.com/matejbolta/zdravstvo-na-daljavo)

##### Projektna naloga pri predmetu [Osnove podatkovnih baz](https://github.com/jaanos/OPB) na __[Fakulteti za matematiko in fiziko](https://www.fmf.uni-lj.si/si/)__.

### Uvod
Projekt je namenjen organizirani hrambi podatkov o slovenskem zdravstvu.

***
### ER diagram

![er-diagram](https://user-images.githubusercontent.com/49908672/161862951-b9116dcd-45da-4d7f-8b40-cd1fe8736ef9.jpg)

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
