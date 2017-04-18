# Orden de ejecucion
```
$ ./download_casos_contenciosos.py
$ ./extract_text.py -v ./data/contenciosos/info.json
$ ./basic_statistics.py -v ./data/contenciosos/info.json
```
# Dependencias

## download_casos_contenciosos.py

En Ubuntu:

```
sudo apt-get install python3-requests
sudo apt-get install python3-bs4
```

## download_casos_contenciosos.py

En Ubuntu:

```
sudo pip3 -U install nltk
sudo pip3 -U install pdfminer3k
sudo apt-get install python3-numpy
sudo apt-get install python3-scipy
sudo pip3 -U install sklearn
```

Es necesario instalar los siguientes recursos de nltk:

-   corpora/stopwords
-   tokenizers/punkt

```
$ python
>>> import nltk
>>> nltk.download();
NLTK Downloader
---------------------------------------------------------------------------
    d) Download   l) List    u) Update   c) Config   h) Help   q) Quit
---------------------------------------------------------------------------
Downloader> d

Download which package (l=list; x=cancel)?
  Identifier> stopwords
    Downloading package stopwords to /home/penserbjorne/nltk_data...
      Unzipping corpora/stopwords.zip.

---------------------------------------------------------------------------
    d) Download   l) List    u) Update   c) Config   h) Help   q) Quit
---------------------------------------------------------------------------
Downloader> d

Download which package (l=list; x=cancel)?
  Identifier> punkt
    Downloading package punkt to /home/penserbjorne/nltk_data...
      Unzipping tokenizers/punkt.zip.

---------------------------------------------------------------------------
    d) Download   l) List    u) Update   c) Config   h) Help   q) Quit
---------------------------------------------------------------------------
Downloader> q
>>> exit();
```

## basic_statistics.py

En Ubuntu:

```
sudo apt-get install python3-matplotlib
```

# Resultados y carpeta Data

## Generados por "download_casos_contenciosos.py"

Al 09 de Abril del 2017:

-   Archivos descargados: 660
    -   330 en Word.
    -   330 en PDF
    -   Cada Word tiene un PDF
-   Tiempo aproximado de descarga: 5 a 15 min

Ubicacion:

```
->  data
    ->  contenciosos
        ->  files
```

## Generados por "extract_text.py"

Al 09 de Abril del 2017:

-   Archivos descargados: 330
    -   Uno por cada pareja de Word y PDF
-   Tiempo aproximado de ejecucion:  1.5 min

Ubicacion:

```
->  data
    ->  contenciosos
```

## Generados por "basic_statistics.py"

Resultados de la ejecucion al 09 de Abril del 2017:

-   Grafico de barras de vocabulario.
-   Grafo
-   Tiempo aproximado de ejecucion:  3 min

Ubicacion:

-   Carpeta raiz ''python''

```
Número total de documentos       : 331
Longitud promedia de documentos  :  252945.54 (caracteres)
Longitud promedia de documentos  :    3892.75 (líneas)
Número total de palabras (token) : 14820985
Número total de palabras (type)  : 186341
  caso                           : 83842
  corte                          : 71513
  párr                           : 50551
  derechos                       : 44558
  supra                          : 41659
  sentencia                      : 41449
  artículo                       : 37655
  cfr                            : 37214
  convención                     : 36876
  comisión                       : 36401
  derecho                        : 35263
  expediente                     : 34026
  tribunal                       : 25567
  vs.                            : 25543
  humanos                        : 25165
  nota                           : 24094
  presente                       : 23722
  señor                          : 23644
  hechos                         : 23301
  fondo                          : 22309
  prueba                         : 22192
  víctimas                       : 20669
  ser                            : 19203
  c                              : 18456
  respecto                       : 18451
  reparaciones                   : 18205
  folio                          : 18199
  representantes                 : 17469
  penal                          : 17439
  parte                          : 17158
  …                              : 16972
  americana                      : 16296
  tomo                           : 15565
  serie                          : 15203
  informe                        : 14802
  personas                       : 14511
  proceso                        : 14495
  interamericana                 : 14296
  anexos                         : 14273
  relación                       : 14213
  costas                         : 14067
```

```
Total de menciones de artículos 18749
  26                             : 59
  6                              : 33
  2                              : 24
  7                              : 20
  117                            : 19
  7                              : 19
  149                            : 19
  320                            : 17
  26                             : 17
  11                             : 16
  21                             : 16
  321                            : 15
  4                              : 15
  25                             : 15
  1                              : 13
  7                              : 12
  17                             : 12
  2                              : 11
  50                             : 11
  19                             : 11
  19                             : 11
  5                              : 10
  2                              : 10
  3                              : 10
  9                              : 10
  8                              : 9
  51                             : 9
  10                             : 9
  12                             : 9
  5                              : 8
  87                             : 8
  16                             : 8
  67                             : 8
  7                              : 8
  8                              : 8
  21                             : 8
  3                              : 8
  4                              : 8
  2                              : 8
  24                             : 8
  6                              : 7
  27                             : 7
  2                              : 7
  67                             : 7
  2                              : 7
  67                             : 7
  3                              : 7
  2                              : 7
  3                              : 7
  2                              : 6
  67                             : 6
  14                             : 6
  67                             : 6
  12                             : 6
  29                             : 6
  2                              : 6
  2                              : 6
  5                              : 6
  67                             : 6
  67                             : 6
  22                             : 6
  67                             : 6
  37                             : 6
  5                              : 5
  3                              : 5
  50                             : 5
  177                            : 5
  5                              : 5
  11                             : 5
  14                             : 5
  196                            : 5
  5                              : 5
  8                              : 5
  3                              : 5
  8                              : 5
  7                              : 5
  12                             : 5
  7                              : 5
  24                             : 5
  63                             : 4
  5                              : 4
  6                              : 4
  7                              : 4
  172                            : 4
  31                             : 4
  13                             : 4
  1                              : 4
  24                             : 4
  25                             : 4
  4                              : 4
  19                             : 4
  4                              : 4
  16                             : 4
  4                              : 4
  22                             : 4
  1                              : 4
  50                             : 4
  1                              : 4
  41                             : 4
  23                             : 3
  6                              : 3
  9                              : 3
  1                              : 3
  62                             : 3
  57                             : 3
  64                             : 3
  5                              : 3
  46                             : 3
  7                              : 3
  71                             : 3
  11                             : 3
  31                             : 3
  11                             : 3
  1                              : 3
  62                             : 3
  226                            : 3
  9                              : 3
  1                              : 3
  28                             : 3
  25                             : 3
  1                              : 3
  93                             : 3
  25                             : 3
  8                              : 3
  7                              : 3
  50                             : 3
  8                              : 3
  27                             : 2
  68                             : 2
  1                              : 2
  67                             : 2
  51                             : 2
  3                              : 2
  50                             : 2
  6                              : 2
  68                             : 2
  54                             : 2
  187                            : 2
  25                             : 2
  240                            : 2
  6                              : 2
  68                             : 2
  233                            : 2
  114                            : 2
  23                             : 2
  63                             : 2
  58                             : 2
  29                             : 2
  38                             : 2
  20                             : 2
  15                             : 2
  159                            : 2
  25                             : 2
  133                            : 2
  68                             : 2
  243                            : 2
  24                             : 2
  6                              : 2
  13                             : 2
  116                            : 2
  7                              : 2
  209                            : 2
  74                             : 2
  5                              : 2
  68                             : 2
  22                             : 2
  13                             : 2
  25                             : 2
  8                              : 2
  207                            : 2
  68                             : 2
  19                             : 2
  8                              : 2
  160                            : 2
  8                              : 2
  277                            : 2
  19                             : 2
  1                              : 2
  70                             : 2
  516                            : 2
  320                            : 2
  135                            : 2
  68                             : 2
  19                             : 2
  162                            : 2
  15                             : 2
  42                             : 2
  25                             : 2
  26                             : 2
  48                             : 2
  29                             : 2
  24                             : 2
  50                             : 1
  45                             : 1
  11                             : 1
  58                             : 1
  46                             : 1
  1                              : 1
  58                             : 1
  46                             : 1
  62                             : 1
  20                             : 1
  163                            : 1
  42                             : 1
  7                              : 1
  10                             : 1
  76                             : 1
  14                             : 1
  365                            : 1
  35                             : 1
  262                            : 1
  32                             : 1
  22                             : 1
  73                             : 1
  28                             : 1
  18                             : 1
  21177                          : 1
  34                             : 1
  18                             : 1
  44                             : 1
  41                             : 1
  16                             : 1
  32                             : 1
  495                            : 1
  28                             : 1
  3                              : 1
  33                             : 1
  241                            : 1
  38                             : 1
  170                            : 1
  283                            : 1
  23                             : 1
  316                            : 1
  135                            : 1
  101                            : 1
  35                             : 1
  67                             : 1
  5                              : 1
  250                            : 1
  4                              : 1
  36                             : 1
  18                             : 1
  158                            : 1
  54                             : 1
  4                              : 1
  54                             : 1
  29                             : 1
  103                            : 1
  4910                           : 1
  12                             : 1
  8                              : 1
  18                             : 1
  24                             : 1
  62                             : 1
  13                             : 1
  141                            : 1
  4                              : 1
  213                            : 1
  30                             : 1
  204                            : 1
  274                            : 1
  181                            : 1
  23642                          : 1
  82                             : 1
  245                            : 1
  8                              : 1
  50                             : 1
  62                             : 1
  310                            : 1
  52                             : 1
  1665                           : 1
  66                             : 1
  86                             : 1
  55                             : 1
  28                             : 1
  6                              : 1
  14                             : 1
  155                            : 1
  64                             : 1
  1647                           : 1
  35                             : 1
  171                            : 1
  51                             : 1
  187                            : 1
  174                            : 1
  24                             : 1
  30                             : 1
  72                             : 1
  50                             : 1
  197                            : 1
  123                            : 1
  36                             : 1
  105                            : 1
  11                             : 1
  61                             : 1
  14                             : 1
  3                              : 1
  10                             : 1
  17                             : 1
  165                            : 1
  4372                           : 1
  50                             : 1
  58                             : 1
  47                             : 1
  44                             : 1
  45                             : 1
  25                             : 1
  4                              : 1
  270                            : 1
  20                             : 1
  254                            : 1
  31                             : 1
  22                             : 1
  41                             : 1
  9                              : 1
  46                             : 1
  173                            : 1
  5                              : 1
  31                             : 1
  35                             : 1
  30                             : 1
  63                             : 1
  18                             : 1
  27                             : 1
  50                             : 1
  584                            : 1
  385                            : 1
  322                            : 1
  35                             : 1
  57                             : 1
  308                            : 1
  13                             : 1
  13                             : 1
  69                             : 1
  17                             : 1
  224                            : 1
  11                             : 1
  25                             : 1
  62                             : 1
  48                             : 1
  1645                           : 1
  50                             : 1
  119                            : 1
  246                            : 1
  29                             : 1
  111                            : 1
  159                            : 1
  72                             : 1
  40                             : 1
  2                              : 1
  100                            : 1
  1031                           : 1
  22                             : 1
  15                             : 1
  41                             : 1
  77                             : 1
  62                             : 1
  98                             : 1
  28                             : 1
  35                             : 1
  96                             : 1
  109                            : 1
  41                             : 1
  69                             : 1
  17                             : 1
  49                             : 1
  29                             : 1
  61                             : 1
  362                            : 1
  1                              : 1
  39                             : 1
  20                             : 1
  94                             : 1
  25                             : 1
  18                             : 1
  180                            : 1
  203                            : 1
  149                            : 1
  32                             : 1
  231                            : 1
  40                             : 1
  6                              : 1
  51                             : 1
  539                            : 1
  5                              : 1
  6354                           : 1
  32                             : 1
  58                             : 1
  15                             : 1
  50                             : 1
  35                             : 1
  1                              : 1
  35                             : 1
  2208                           : 1
  30                             : 1
  201                            : 1
```

```
Tópico #0:
producido abogado resolvió gonzález radilla ejército respuesta solamente solo 178 realidad constituyen pueda observaciones madre pág recibir deberán dos admisión

Tópico #1:
caso corte jaime largo cada ley crímenes deberá personales fuerza álvarez cf deben párr señor trujillo admisión muerte humana posibles

Tópico #2:
perjuicios provisionales gastos intereses us zona afirmó segundo posterioridad junio 2011 relevantes cada daño testigos hoy judicial dolor militar chaparro

Tópico #3:
brasil sánchez nota marzo herrera casa 73 señala crimen corte 1989 legislativo directamente indemnización éste portugal preliminar ricardo privación 155

Tópico #4:
cabrera inter rendido votos futuro 73 22 cuanto señaladas díaz pago 2008 rosendo 1984 ambiente observación respetar particular dirección privación

Tópico #5:
reparaciones augusto terrorismo solicitud apelación moral fiscalía continuar americana 157 magistrados diligencia tiempo medida 2011 caso civil previamente denuncia admisión

Tópico #6:
sentencia partes 181 primer objetivo of tercera asesinato existía real necesariamente mantener pertinente david 112 responsabilidades do rosero formal consideraciones

Tópico #7:
corte vera sentencia central folio convención aplicables proceso actos octubre hermanos jurisdicción 09 comunidad ramón derechos dos caso solicitado trinidad

Tópico #8:
caso párr corte supra cfr rosero señor international convención us unidos observaciones uso derechos rojas magistrados dispuesto 25 sección americana

Tópico #9:
corte caso víctimas párr comisión artículo sentencia cfr representantes hechos señor 107 derecho supra fondo penal humanos provincia raíz respecto

Tópico #10:
posibles desaparecidas suma aún señala cantidad conformidad expuesto derecho primera artículo 2004 menor solamente médica ser posible baldeón indicios conflicto

Tópico #11:
188 146 turno autos especializado etapa sistema cierto cumplir humanitario 1987 cuatro libro fernández ramírez anexos sede debe capítulo duración

Tópico #12:
sentencia corte febrero víctimas sometidos 15 tribunal protegidos república determinado afectación refiere derechos comisión carácter humana además ocurridos desaparición lado

Tópico #13:
agentes unidas ibsen sujetos centro términos especializada supuestamente penales estima familia respecto humanos general noviembre obligatoria fiscales 73 1981 169

Tópico #14:
arts actividad caso legislativo proyecto física relativas eventual ordenar etapas órganos familias captura ejecuciones demanda 52 cfr 23 titular preciso

Tópico #15:
agotamiento reconocimiento ix económico juan recuerda relacionadas 25 mujer inconstitucionalidad court 80 montiel alegada 168 perjuicios información 133 david supuestas

Tópico #16:
caso supra 186 corte señor presente vía fondo posición acción manera zapata ibsen conocer convención sede resolución algún chang oral

Tópico #17:
existen 190 gonzález abogado tutela delito privación declarado señora alejandro televisión miembro solicitó incluyendo argentina concreto 47 audiencia corresponde año

Tópico #18:
pará tratamiento debido 1985 reconocimiento aún hoc propio vicente año 1994 reconoce peruana organizaciones decisión supervisión podido surinam concepción allanamiento

Tópico #19:
corte derecho implica cometido surinam sentencia delitos presencia humanos tomo considerar pertinentes internacional 57 ende honduras asamblea provincial 48 texto

Tópico #20:
negro artículos serrano affidávits oficina 149 tortura forzada apelación etapas jus reconoció vista luna cuarta europea ambiente alcance the alessandri

Tópico #21:
caso corte estatales unidad comisión político representantes 14 convención vs yatama acosta cfr párr 2013 valores rivera resolución custodia términos

Tópico #22:
caso corte sentencia 2001 comisión convención mendoza tierras serie artículo nota penal cfr párr mediante presentación representantes ser solicitud cambio

Tópico #23:
corte caso comisión sentencia derechos convención artículo párr derecho humanos supra cfr señor presente tribunal hechos expediente reparaciones americana víctimas

Tópico #24:
corte caso saavedra 05 interpretación especialmente interpuesta 83 sentencia procedimiento ordinaria estima presidente varios elemento masacres párr deberá particular asimismo

Tópico #25:
154 español 20 municipal anexo cincuenta 148 anexos párr nicaragua decide perjuicio folios militar 50 destitución solicitud haciendo común nivel

Tópico #26:
inter respeto 121 humanitario detenidos alberto captura intervención contencioso ocasión 201 dicho tipo 24 días gobierno interpuso carmen emitido 87

Tópico #27:
honduras affidávit disponible riesgo aproximadamente corresponde 42 resultados dicha fuego dignidad morales asesinato representación publicación inicio cadáveres inicial época competencia

Tópico #28:
conflicto eventuales leyes franco cometidos corpus zapata suspensión municipio evaluación cepeda constitucional beneficios mencionado fundamento alto figura podía causa fijar

Tópico #29:
corte caso comisión derechos convención sentencia artículo derecho humanos párr gobierno señor demanda nota supra presente americana cfr tribunal interamericana
```