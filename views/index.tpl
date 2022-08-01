% rebase('base.tpl', naslov='ZDRAVSTVO NA DALJAVO')

<p>
  <button>
    <a href="{{url('zdravniki')}}">
      Zdravniki
    </a>
  </button>
</p>

<p>
  <button>
  <a href="{{url('pacienti')}}">
    Pacienti
  </a>
  </button>
</p>

<p>
  <button>
  <a href="{{url('zdravstveni_domovi', treshold=1)}}">
    Zdravstveni domovi
  </a>
  </button>
</p>

<p>
  <button>
  <a href="{{url('zaposlitve_zdravnikov')}}">
    Zaposlitve zdravnikov
  </a>
  </button>
</p>