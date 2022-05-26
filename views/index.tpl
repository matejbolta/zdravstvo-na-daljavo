% rebase('base.tpl', naslov='Izberite željeno stran!')

<p>
  <a href="{{url('zdravniki')}}">
    Zdravniki
  </a>
</p>

<p>
  <a href="{{url('pacienti')}}">
    Pacienti
  </a>
</p>

<p>
  <a href="{{url('zdravstveni_domovi', treshold=1)}}">
    Zdravstveni domovi
  </a>
</p>

<p>
  <a href="{{url('zaposlitve_zdravnikov')}}">
    Kje so zdravniki zaposleni
  </a>
</p>