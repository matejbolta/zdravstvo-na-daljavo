<html>

  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>{{naslov}}</title>

    <link rel="icon" href="/static/favicon1.png"> <!-- ikona v zavihku -->

    <link href="{{url('static', filename='style.css')}}" rel="stylesheet"> <!-- tole ne deluje kot bi moralo, zato bodo stili kar v posameznih predlogah -->

    <style>
      table { margin-left: auto; margin-right: auto; font-family: Agency FB; background-color: #A5BDD9; }
      body { text-align: center; font-family: Verdana; background-color: #98B4D4; }
      button { background-color: #B2C7DF; border: 3px ; border-color: antiquewhite ; color: white; padding: 12px; font-size: 16px; font-family: Verdana; font-weight: bold; border-radius: 21px }
    </style>

    <!-- bootstrap -->
    <!-- <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous"> -->
  </head>

  <body>
      <h2>{{naslov}}</h2> <hr>
    
      <div class="container">
        {{!base}}
      </div>
    
    <!-- bootstrap -->
    <!-- <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script> -->
  </body>

</html>