Python 2.6.4 (r264:75706, Jan 19 2010, 11:48:04) 
[GCC 4.2.1 (Apple Inc. build 5646)] on darwin
Type "copyright", "credits" or "license()" for more information.

    ****************************************************************
    Personal firewall software may warn about the connection IDLE
    makes to its subprocess using this computer's internal loopback
    interface.  This connection is not visible on any external
    interface and no data is sent to or received from the Internet.
    ****************************************************************
    
IDLE 2.6.4      
>>> import nltk
>>> a = ["an", 'apple', "on", 'a', 'plate']
>>> nltk.pos_tag(a)
[('an', 'DT'), ('apple', 'NN'), ('on', 'IN'), ('a', 'DT'), ('plate', 'NN')]
>>> b = random()

Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    b = random()
NameError: name 'random' is not defined
>>> b = random.random()

Traceback (most recent call last):
  File "<pyshell#4>", line 1, in <module>
    b = random.random()
NameError: name 'random' is not defined
>>> return random.choice(a)
SyntaxError: 'return' outside function
>>> b = random.choice(a)

Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    b = random.choice(a)
NameError: name 'random' is not defined
>>> 
>>> from random import randint
>>> b = random.choice(a)

Traceback (most recent call last):
  File "<pyshell#9>", line 1, in <module>
    b = random.choice(a)
NameError: name 'random' is not defined
>>> b = randint(1,24)
>>> b
15
>>> b
15
>>> b = randint(1,24)
>>> b
24
>>> import random
>>> a
['an', 'apple', 'on', 'a', 'plate']
>>> b = random.choice(a)
>>> b
'a'
>>> b = random.choice(a)
>>> b
'apple'
>>> 
>>> b = random.choice(a)
>>> b
'on'
>>> b = random.choice(a)
>>> b
'a'
>>> b = random.choice(a)
>>> b
'an'
>>> b = random.choice(a)
>>> b
'a'
>>> b = random.choice(a)
>>> b
'apple'
>>> while f
SyntaxError: invalid syntax
>>> words = []
>>> found = 0
>>> a.size

Traceback (most recent call last):
  File "<pyshell#35>", line 1, in <module>
    a.size
AttributeError: 'list' object has no attribute 'size'
>>> size(a)

Traceback (most recent call last):
  File "<pyshell#36>", line 1, in <module>
    size(a)
NameError: name 'size' is not defined
>>> len(a)
5
>>> while found < len(a)
SyntaxError: invalid syntax
>>> while (found < len(a))
SyntaxError: invalid syntax
>>> len_a = len(a)
>>> while found < len_a
SyntaxError: invalid syntax
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		words.index(a_word);
	except ValueError:
		words.append.(a_word);
		
SyntaxError: invalid syntax
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1
for x in words:
	
SyntaxError: invalid syntax
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> for x in words:
	print x;

an
on
a
apple
plate
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> i = 0
>>> while found < len_a:
	try:
		i += 1;
		print i;
		a_word = random.choice(a);
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> pwhile found < len_a:
	try:
		i += 1;
		print i;
		a_word = random.choice(a);
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1
		
SyntaxError: invalid syntax
>>> print i
0
>>> while found < len_a:
	try:
		i += 1;
		print i;
		a_word = random.choice(a);
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> print i;
0
>>> for x in words:
	print x;

an
on
a
apple
plate
>>> while found < len_a:
	try:
		i += 1;
		a_word = random.choice(a);
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> print i;
0
>>> while found < len_a:
	try:
		i += 1;
		a_word = random.choice(a);
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1
		print i;

>>> while found < len_a:
	try:
		i += 1;
		a_word = random.choice(a);
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> print fou

Traceback (most recent call last):
  File "<pyshell#77>", line 1, in <module>
    print fou
NameError: name 'fou' is not defined
>>> print found
5
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		i += 1;
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> i
0
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		words.index(a_word);
		i += 1
	except ValueError:
		words.append(a_word);
		found += 1

>>> i
0
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		i += 1
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> i
0
>>> found
5
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		print a_word;
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> arr = []
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		arr.append(a_word);
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> for y in arr
SyntaxError: invalid syntax
>>> for y in arr:
	print y;

>>> for x in words:
	print x;

an
on
a
apple
plate
>>> while found < len_a:
	a_word = random.choice(a);
	arr.append(a_word);
	if not words.index(a_word):
		words.append(a_word);
		found += 1

>>> for x in words:
	print x;

an
on
a
apple
plate
>>> arr
[]
>>> 
>>> aa = random.choice(a)
>>> print aa
a
>>> while i < 10
SyntaxError: invalid syntax
>>> while i < 10:
	aa = random.choice(a);
	print aa;
	i += 1

apple
an
on
on
a
apple
a
plate
on
a
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		print a_word;
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> while found < len_a:
	a_word = random.choice(a);
	print a_word;
	if not words.index(a_word):
		words.append(a_word);
		found += 1

>>> found = 0
>>> words = []
>>> while found < len_a:
	a_word = random.choice(a);
	print a_word;
	if not words.index(a_word):
		words.append(a_word);
		found += 1

plate

Traceback (most recent call last):
  File "<pyshell#121>", line 4, in <module>
    if not words.index(a_word):
ValueError: list.index(x): x not in list
>>> a
['an', 'apple', 'on', 'a', 'plate']
>>> while found < len(a):
	a_word = random.choice(a);
	print a_word;
	if not words.index(a_word):
		words.append(a_word);
		found += 1

apple

Traceback (most recent call last):
  File "<pyshell#124>", line 4, in <module>
    if not words.index(a_word):
ValueError: list.index(x): x not in list
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		print a_word;
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

apple
apple
0
plate
apple
0
on
apple
0
an
an
3
apple
0
a
>>> 
[DEBUG ON]
>>> 
[DEBUG OFF]
>>> for x in numbers:
19
  print x;
  File "<pyshell#127>", line 2
    19
     ^
IndentationError: expected an indented block
>>> for x in numbers:
  	print x;
  File "<pyshell#128>", line 2
      	print x;
    ^
IndentationError: expected an indented block
>>> for x in numbers:
	print x;


Traceback (most recent call last):
  File "<pyshell#132>", line 1, in <module>
    for x in numbers:
NameError: name 'numbers' is not defined
>>> for x in words:
	print x;

apple
plate
on
an
a
>>> 
>>> random_names_list = in_file = open("test.txt", "r")
text = in_file.read()
in_file.close()


Traceback (most recent call last):
  File "<pyshell#136>", line 1, in <module>
    random_names_list = in_file = open("test.txt", "r")
IOError: [Errno 2] No such file or directory: 'test.txt'
>>> names_list = open("/Users/anna/work/texts/shell_index/clean_index/1/clean_index-uniq-ok1.txt", "r")
>>> names_list_set = names_list.read
>>> names_list_set
<built-in method read of file object at 0x103f7e2d8>
>>> names_list_read = names_list.read
>>> names_list_set = set(names_list_read)

Traceback (most recent call last):
  File "<pyshell#142>", line 1, in <module>
    names_list_set = set(names_list_read)
TypeError: 'builtin_function_or_method' object is not iterable
>>> names_list_read
<built-in method read of file object at 0x103f7e2d8>
>>> names_list_set = names_list.read()
>>> names_list_read = names_list.read()
>>> names_list_read
''
>>> names_list
<open file '/Users/anna/work/texts/shell_index/clean_index/1/clean_index-uniq-ok1.txt', mode 'r' at 0x103f7e2d8>
>>> print names_list_read

>>> random_names_list = in_file = open("test.txt", "r")
text = in_file.read()
in_file.close()

Traceback (most recent call last):
  File "<pyshell#149>", line 1, in <module>
    random_names_list = in_file = open("test.txt", "r")
IOError: [Errno 2] No such file or directory: 'test.txt'
>>> in_file = open("/Users/anna/work/texts/shell_index/clean_index/1/clean_index-uniq-ok1.txt", "r")
>>> text = in_file.read()
>>> in_file.close()
>>> print text
Abra
Abra aequalis
Abra lioica
Abra profundorum
Acanthina
Acanthina lapilloides
Acanthina paucilirata
Acanthina punctulata
Acanthina spirata
Acanthinucella
Acanthochitona
Acanthochitona astriger
Acanthochitona balesae
Acanthochitona pygmaeus
Acanthochitona spiculosus
Acanthodoris
Acanthodoris brunnea
Acanthodoris pilosa
Acanthopleura
Acanthopleura flexa
Acanthopleura granulata
Acar
Acephala
Acila castrensis
Acirsa
Acirsa borealis
Acirsa costulata
Aclididae
Acmaea
Acmaea albicosta
Acmaea alveus
Acmaea antillarum
Acmaea asmi
Acmaea candeana
Acmaea conus
Acmaea cribraria
Acmaea cubensis
Acmaea depicta
Acmaea digitalis
Acmaea fenestrata
Acmaea fungoides
Acmaea insessa
Acmaea instabilis
Acmaea jamaicensis
Acmaea leucopleura
Acmaea limatula
Acmaea mitra
Acmaea paleacea
Acmaea patina
Acmaea pelta
Acmaea persona
Acmaea pulcherrima
Acmaea punctulata
Acmaea pustulata
Acmaea scabra
Acmaea scutum
Acmaea simplex
Acmaea spectrum
Acmaea strigatella
Acmaea tenera
Acmaea tessulata
Acmaea testudinalis
Acmaea triangularis
Acmaeidae
Actaeon
Acteocina
Acteocina candei
Acteocina cerealis
Acteocina culitella
Acteocinidae
Acteon
Acteon candens
Acteon punctocaelatus
Acteon punctostriatus
Acteon vancouverensis
Acteonidae
Adalaria proxima
Adapedonta
Adesmacea
Admete couthouyi
Adula
Aeolidia papillosa
Aeolidiidae
Aequipecten
Aequipecten borealis
Aequipecten dislocatus
Aequipecten exasperatus
Aequipecten fusco-purpureus
Aequipecten gibbus
Aequipecten gibbus nucleus
Aequipecten glyptus
Aequipecten irradians
Aequipecten irradians amplicostatus
Aequipecten irradians concentricus
Aequipecten irradians irradians
Aequipecten lineolaris
Aequipecten mayaguezensis
Aequipecten muscosus
Aequipecten nucleus
Aequipecten phrygium
Aequipecten tryoni
Agriodesma
Agriopoma
Alabina
Alabina diegensis
Alabina tenuisculpta
Aldisa sanguinea
Aletes squamigerous
Allopora californica
Aloidis
Amaea
Amaea mitchelli
Amaea retifera
Amaura
Amauropsis
Amauropsis islandica
Amauropsis purpurea
Amiantis
Amiantis callosa
Amiantis nobilis
Amicula
Amicula stelleri
Amphineura
Amphissa
Amphissa bicolor
Amphissa columbiana
Amphissa undata
Amphissa versicolor
Amphithalamus
Amphithalamus inclusus
Amphithalamus lacunatus
Amphithalamus tenuis
Amusium
Amygdalum
Amygdalum papyria
Amygdalum sagittata
Anachis
Anachis avara
Anachis obesa
Anachis ostreicola
Anachis penicillata
Anachis translirata
Anadara
Anadara americana
Anadara auriculata
Anadara baughmani
Anadara brasiliana
Anadara campechiensis
Anadara chemnitzi
Anadara deshayesi
Anadara grandis
Anadara incongrua
Anadara lienosa
Anadara lienosa floridana
Anadara multicostata
Anadara notabalis
Anadara ovalis
Anadara pexata
Anadara secticostata
Anadara springeri
Anadara sulcosa
Anadara transversa
Anatina Schumacher
Ancistrolepsis
Ancistrosyrinx
Ancistrosyrinx elegans
Ancistrosyrinx radiata
Ancula
Ancula cristata
Ancula pacifica
Ancula sulphurea
Angulus
Angulus tener
Anisodoris
Annulicallus
Anodontia
Anodontia alba
Anodontia chrysostoma
Anodontia philippiana
Anodontia schrammi
Anomalocardia
Anomalocardia brasiliana
Anomalocardia cuneimeris
Anomalodesmacea
Anomia
Anomia aculeata
Anomia peruviana
Anomia simplex
Anomiidae
Anopsia
Antalis
Antigona
Antigona listeri
Antigona rigida
Antigona rugatina
Antigona strigillina
Antillophos candei
Aperiploma
Aplysia
Aplysia badistes
Aplysia dactylomela
Aplysia floridensis
Aplysia perviridis
Aplysia protea
Aplysia willcoxi
Aplysidae
Apolymetis
Apolymetis alta
Apolymetis biangulata
Apolymetis intastriata
Aporrhaidae
Aporrhais
Aporrhais labradorensis
Aporrhais mainensis
Aporrhais occidentalis
Aptyxis luteopicta
Arca
Arca balesi
Arca occidentalis
Arca pernoides
Arca reticulata
Arca umbonata
Arca zebra
Archidoris
Archidoris montereyensis
Archidoris nobilis
Architectonica
Architectonica granulata
Architectonica krebsi
Architectonica nobilis
Architectonica peracuta
Architeuthis
Architeuthis harveyi
Architeuthis princeps
Arcidae
Arcopagia fausta
Arcopsis adamsi
Arctica islandica
Arcticidae
Arctomelon stearnsi
Arene
Arene cruentata
Arene gemma
Arene vanhyningi
Arene variabilis
Arene venustula
Argina
Arginarca
Argobuccinum oregonense
Argonauta
Argonauta americana
Argonauta argo
Argonauta hians
Asaphis deflorata
Astarte
Astarte borealis
Astarte castanea
Astarte nana
Astarte subequilatera
Astarte undata
Astartidae
Astraea
Astraea americana
Astraea brevispina
Astraea caelata
Astraea gibberosa
Astraea guadeloupensis
Astraea imbricata
Astraea inaequalis
Astraea longispina
Astraea spinulosa
Astraea tuber
Astraea undosa
Astralium
Astyris
Atlanta
Atlanta peroni
Atlantidae
Atrina
Atrina rigida
Atrina serrata
Atydae
Atys
Atys caribaea
Atys sandersoni
Aurinia
Austrotrophon
Bailya
Bailya intricata
Bailya parva
Bankia
Bankia canalis
Bankia caribbea
Bankia fimbriatula
Bankia gouldi
Bankia mexicana
Bankiella
Bankiopsis
Barbarofusus
Barbatia
Barbatia bailyi
Barbatia barbata
Barbatia cancellaria
Barbatia candida
Barbatia domingensis
Barbatia helblingi
Barbatia jamaicensis
Barbatia tenera
Barnea
Barnea costata
Barnea pacifica
Barnea spathulata
Barnea truncata
Bartschella
Basommatophora
Batillaria minima
Bellucina
Beringius
Bittium
Bittium alternatum
Bittium attenuatum
Bittium eschrichti
Bittium interfossum
Bittium montereyense
Bittium quadrifilatum
Bittium varium
Bittium virginicum
Bivalvia
Bivetiella
Blepharopoda occidentalis
Boreomelon
Boreostrophon peregrinus
Boreotrophon
Boreotrophon clathratus
Boreotrophon dalli
Boreotrophon multicostatus
Boreotrophon orpheus
Boreotrophon pacificus
Boreotrophon peregrinus
Boreotrophon scalariformis
Boreotrophon scitulus
Boreotrophon smithi
Boreotrophon stuarti
Boreotrophon triangulatus
Bornia longipes
Botula
Botula californiensis
Botula falcata
Botula fusca
Brachidontes
Brachidontes adamsianus
Brachidontes citrinus
Brachidontes exustus
Brachidontes hamatus
Brachidontes multiformis
Brachidontes recurvus
Brachidontes stearnsi
Buccinidae
Buccinum
Buccinum baeri
Buccinum glaciale
Buccinum plectrum
Buccinum tenue
Buccinum undatum
Bufonaria
Bulla
Bulla amygdala
Bulla gouldiana
Bulla occidentalis
Bulla punctulata
Bulla striata
Bullaria
Bullidae
Bursa
Bursa affinis
Bursa caelata
Bursa californica
Bursa corrugata
Bursa crassa
Bursa cubaniana
Bursa granularis
Bursa louisa
Bursa ponderosa
Bursa spadicea
Bursa tenuisculpta
Bursa thomae
Bursatella leachi plei
Busycon
Busycon canaliculatum
Busycon carica
Busycon coarctatum
Busycon contrarium
Busycon kieneri
Busycon perversum
Busycon plagosum
Busycon pyrum
Busycon spiratum
Busycotypus
Cadlina
Cadlina flavomaculata
Cadlina laevis
Cadlina marginata
Cadlina obvelata
Cadlina planulata
Cadlina repanda
Cadulus
Cadulus carolinensis
Cadulus mayori
Cadulus quadridentatus
Caecidae
Caecum
Caecum bakeri
Caecum barkleyense
Caecum barkleyensis
Caecum californicum
Caecum carolinianum
Caecum carpenteri
Caecum catalinense
Caecum cayosense
Caecum cooperi
Caecum crebricinctum
Caecum dalli
Caecum diegense
Caecum floridanum
Caecum grippi
Caecum hemphilli
Caecum heptagonum
Caecum lermondi
Caecum licalum
Caecum nebulosum
Caecum nitidum
Caecum occidentale
Caecum orcutti
Caecum oregonense
Caecum pedroense
Caecum pulchellum
Caecum rosanum
Callianax
Calliostoma
Calliostoma annulatum
Calliostoma bairdi
Calliostoma canaliculatum
Calliostoma doliarium
Calliostoma euglyptum
Calliostoma gemmulatum
Calliostoma gloriosum
Calliostoma jujubinum
Calliostoma ligatum
Calliostoma occidentale
Calliostoma psyche
Calliostoma pulchrum
Calliostoma roseolum
Calliostoma splendens
Calliostoma subumbilicatum
Calliostoma supragranosum
Calliostoma tampaense
Calliostoma tricolor
Calliostoma variegatum
Calliostoma zonamestum
Calliotropis
Callista eucymata
Callocardia texasiana
Callogaza
Calloplax janeirensis
Calyptraea
Calyptraea candeana
Calyptraea centralis
Calyptraea contorta
Calyptraea fastigiata
Calyptraeidae
Cancellaria
Cancellaria adelae
Cancellaria conradiana
Cancellaria crawfordiana
Cancellaria reticulata
Cancellariidae
Cantharus
Cantharus auritula
Cantharus cancellaria
Cantharus tinctus
Capulidae
Capulus
Capulus californicus
Capulus incurvatus
Capulus intortus
Cardiidae
Cardiomya
Cardiomya costellata
Cardiomya gemma
Cardiomya multicostata
Cardiomya pectinata
Cardita
Cardita carpenteri
Cardita dominguensis
Cardita floridana
Cardita gracilis
Carditamera
Carditidae
Cardium
Cardium corbis
Carinaria
Carinaria lamarcki
Carinaria mediterranea
Carinariidae
Cassididae
Cassis
Cassis flammea
Cassis madagascariensis
Cassis madagascariensis spinella
Cassis spinella
Cassis tuberosa
Catriona
Catriona aurantia
Catriona aurantiaca
Cavolina
Cavolina affinis
Cavolina angulata
Cavolina costata
Cavolina cuspidata
Cavolina elongata
Cavolina gibbosa
Cavolina imitans
Cavolina inermis
Cavolina inflexa
Cavolina intermedia
Cavolina labiata
Cavolina limbata
Cavolina longirostris
Cavolina minuta
Cavolina mucronata
Cavolina quadridentata
Cavolina reeviana
Cavolina telemus
Cavolina tridentata
Cavolina trispinosa
Cavolina uncinata
Cavolina uncinatiformis
Cavolinia
Cavolinidae
Cenchritis
Cephalopoda
Cerastoderma pinnulatum
Ceratostoma foliatum
Ceratozona rugosa
Cerithidea
Cerithidea costata
Cerithidea hegewischi californica
Cerithidea pliculosa
Cerithidea scalariformis
Cerithidea turrita
Cerithideopsis
Cerithiopsis
Cerithiopsis carpenteri
Cerithiopsis emersoni
Cerithiopsis greeni
Cerithiopsis grippi
Cerithiopsis pedroana
Cerithiopsis subulata
Cerithiopsis vanhyningi
Cerithiopsis virginica
Cerithium
Cerithium algicola
Cerithium eburneum
Cerithium floridanum
Cerithium literatum
Cerithium muscarum
Cerithium variabile
Cerithium versicolor
Cerodrillia
Cerodrillia perryae
Cerodrillia thea
Chaetopleura apiculata
Chama
Chama congregata
Chama firma
Chama macerophylla
Chama sinuosa
Chamidae
Charonia
Charonia atlantica
Charonia tritonis
Charonia tritonis nobilis
Cheila equestris
Chemnitzia
Chicoreus
Chione
Chione californiensis
Chione cancellata
Chione fluctifraga
Chione gnidia
Chione grus
Chione intapurpurea
Chione interpurpurea
Chione latilirata
Chione mazycki
Chione paphia
Chione pygmaea
Chione succincta
Chione undatella
Chionidae
Chiton
Chiton albolineatus
Chiton laevigatus
Chiton marmoratus
Chiton squamosus
Chiton stokesi
Chiton tuberculatus
Chiton virgulatus
Chiton viridis
Chitonidae
Chlamys
Chlamys benedicti
Chlamys hastatus
Chlamys hastatus hastatus
Chlamys hastatus hericius
Chlamys hericius
Chlamys hindsi
Chlamys imbricatus
Chlamys islandicus
Chlamys mildredae
Chlamys ornatus
Chlamys sentis
Chlorostoma
Chrysallida
Chrysodomus lirata
Chrysodomus satura
Cidarina
Cingula
Cingula aculeus
Cingula asser
Cingula cerinella
Cingula kelseyi
Cingula kyskensis
Cingula montereyensis
Cingula palmeri
Circinae
Circomphalus
Circulus
Cirsotrema
Cirsotrema arcella
Cirsotrema dalli
Cittarium
Cleodora
Cleodora exacuta
Cleodora virgula
Clinocardium
Clinocardium ciliatum
Clinocardium corbis
Clinocardium fucanum
Clinocardium nuttalli
Clio
Clio balantium
Clio cuspidata
Clio exacuta
Clio falcata
Clio lanceolata
Clio polita
Clio pyramidata
Clio recurva
Clione
Clionopsis
Cliopsis
Clypidella
Cochlodesma
Codakia
Codakia californica
Codakia costata
Codakia filiata
Codakia orbicularis
Codakia orbiculata
Collisella
Colubraria
Colubraria lanceolata
Colubraria swifti
Colubraria testacea
Colubrellina
Columbella
Columbella mercatoria
Columbella rusticoides
Columbellidae
Colus
Colus caelatus
Colus pubescens
Colus pygmaea
Colus pygmaeus
Colus spitzbergensis
Colus stimpsoni
Colus ventricosus
Compsomyax subdiaphana
Congeria leucophaeta
Conidae
Conus
Conus amphiurgus
Conus aureofasciatus
Conus austini
Conus californicus
Conus citrinus
Conus clarki
Conus daucus
Conus floridanus
Conus floridanus burryae
Conus floridanus floridensis
Conus floridensis
Conus frisbeyae
Conus granulatus
Conus jaspideus
Conus juliae
Conus mazei
Conus mus
Conus peali
Conus regius
Conus sennottorum
Conus sozoni
Conus spurius atlanticus
Conus spurius spurius
Conus stearnsi
Conus stimpsoni
Conus vanhyningi
Conus verrucosus
Conus villepini
Cooperella subdiaphana
Coralliophaga coralliophaga
Coralliophila
Coralliophila abbreviata
Coralliophila costata
Coralliophila deburghiae
Coralliophila hindsi
Corbiculiidae
Corbula
Corbula barrattiana
Corbula contracta
Corbula dietziana
Corbula disparilis
Corbula luteola
Corbula nasuta
Corbula porcella
Corbula rosea
Corbula swiftiana
Corbulidae
Coryphella rufibranchialis
Costacallista
Crassatella
Crassatellidae
Crassatellites
Crassinella
Crassinella lunulata
Crassinella mactracea
Crassispira
Crassispira ebenina
Crassispira ostrearum
Crassispira sanibelensis
Crassispira tampaensis
Crassispirella
Crassostrea
Crassostrea angulata
Crassostrea brasiliana
Crassostrea floridensis
Crassostrea gigas
Crassostrea laperousi
Crassostrea rhizophorae
Crassostrea virginica
Cratena
Cremides
Crenella
Crenella columbiana
Crenella decussata
Crenella divaricata
Crenella faba
Crenella glandula
Crepidula
Crepidula aculeata
Crepidula acuta
Crepidula convexa
Crepidula excavata
Crepidula fornicata
Crepidula glauca
Crepidula maculosa
Crepidula nummaria
Crepidula onyx
Crepidula plana
Crepipatella lingulata
Creseis
Creseis acicula
Creseis conica
Creseis coniformis
Creseis virgula
Creseis vitrea
Crossata
Crucibulum
Crucibulum auricula
Crucibulum spinosum
Crucibulum striatum
Cryptochiton stelleri
Cryptoconchus floridanus
Cryptomya californica
Cryptonatica
Cryptoplacidae
Ctena
Ctenoides
Cumingia
Cumingia californica
Cumingia coarctata
Cumingia tellinoides
Cumingia vanhyningi
Cunearca
Cuspidaria
Cuspidaria glacialis
Cuspidaria granulata
Cuspidaria jeffreysi
Cuspidaria rostrata
Cuvieria
Cuvierina
Cyanoplax
Cyathodonta
Cyathodonta dubiosa
Cyathodonta pedroana
Cyathodonta undulata
Cyclocardia
Cyclostrema
Cyclostrema amabile
Cyclostrema cancellatum
Cyclostrema cookeana
Cyclotellina
Cylichna
Cylichna alba
Cylichna bidentata
Cylichna biplicata
Cylichna gouldi
Cylichnella
Cymatiidae
Cymatium
Cymatium aquitile
Cymatium chlorostomum
Cymatium cynocephalum
Cymatium femorale
Cymatium gracile
Cymatium labiosum
Cymatium martinianum
Cymatium muricinum
Cymatium pileare
Cymatium prima
Cymatium tuberosum
Cymatium velei
Cyphoma
Cyphoma gibbosum
Cyphoma mcgintyi
Cyphoma signatum
Cypraea
Cypraea cervus
Cypraea cinerea
Cypraea exanthema
Cypraea moneta
Cypraea mus
Cypraea pantherina
Cypraea spadicea
Cypraea spurca
Cypraea spurca acicularis
Cypraea tigris
Cypraea vallei
Cypraea zebra
Cypraecassis
Cypraecassis rufa
Cypraecassis testiculus
Cypraeolina
Cyprina
Cyrtodaria
Cyrtodaria kurriana
Cyrtodaria siliqua
Daphnella lymneiformis
Decapoda
Dendrodorididae
Dendrodoris
Dendrodoris fulva
Dendronotidae
Dendronotus
Dendronotus arborescens
Dendronotus frondosus
Dendronotus giganteus
Dentale
Dentaliidae
Dentalium
Dentalium antillarum
Dentalium calamus
Dentalium cestum
Dentalium eboreum
Dentalium elephantinum
Dentalium entale
Dentalium entale stimpsoni
Dentalium filum
Dentalium floridense
Dentalium laqueatum
Dentalium megathyris Dall
Dentalium occidentale
Dentalium pilsbryi
Dentalium pretiosum
Dentalium pseudohexagonum
Dentalium semiostriolatum
Dentalium semistriolatum
Dentalium sowerbyi
Dentalium texasianum
Dentilucina
Dentiscala
Diacria
Diadora
Dialula sandiegensis
Diaphana
Diaphana debilis
Diaphana globosa
Diaphana hiemalis
Diaphana minuta
Diaphanidae
Diastomidae
Diaulula sandiegensis
Diberus
Dibranchia
Dinocardium
Dinocardium robustum
Dinocardium vanhyningi
Diodora
Diodora alternata
Diodora aspera
Diodora cayenensis
Diodora densiclathrata
Diodora dysoni
Diodora listeri
Diodora minuta
Diodora murina
Diplodonta
Diplodonta granulosa
Diplodonta orbella
Diplodonta punctata
Diplodonta semiaspera
Diplodonta subquadrata
Diplodontidae
Dischides
Discodoris heathi
Dispotaea
Dissentoma
Dissentoma prima
Distorsio
Distorsio clathrata
Distorsio constricta
Distorsio constricta mcgintyi
Distorsio floridana
Divaricella
Divaricella dentata
Divaricella quadrisulcata
Dolium
Donax
Donax californica
Donax denticulata
Donax fossor
Donax gouldi
Donax roemeri
Donax striata
Donax tumida
Donax variabilis
Doridae
Doriopsis
Doryteuthis plei
Dorytewthis plei
Dosina
Dosinia
Dosinia discus
Dosinia elegans
Dosinidia
Dreissenidae
Drupa nodulosa
Echininus nodulosus
Echinochama
Echinochama arcinella
Echinochama californica
Echinochama cornuta
Egregia
Elephantanellum
Ellipetylus
Emarginula phrixodes
Engina turbinella
Ensis
Ensis californicus
Ensis directus
Ensis megistus
Ensis minor
Ensis myrae
Entemnotrochus
Entoconchidae note
Entodesma saxicola
Eontia
Epilucina
Episiphon
Epitonium
Epitonium angulatum
Epitonium clathrum
Epitonium commune
Epitonium contorquata
Epitonium eburneum
Epitonium folaceicostum
Epitonium foliaceicostum
Epitonium humphreysi
Epitonium indianorum
Epitonium krebsi
Epitonium lamellosum
Epitonium lineatum
Epitonium muricata
Epitonium occidentale
Epitonium pretiosula
Epitonium pretiosum
Epitonium reynoldsi
Epitonium rupicolum
Epitonium scalare
Epitonium spina-rosae
Epitonium swifti
Epitonium tollini
Erato
Erato columbella
Erato maugeriae
Erato vitillina
Eratoidae
Eratoidea
Erosaria
Ervilia
Ervilia concentrica
Ervilia rostratula
Erycina fernandina
Erycinidae
Eubranchus
Eubranchus exiguus
Eubranchus pallidus
Eucrassatella
Eucrassatella floridana
Eucrassatella gibbesi
Eucrassatella speciosa
Eudolium crosseanum
Eulamellibranchia
Eulimidae
Eulithidium
Eulithidium rubrilineatum
Eulithidium variegata
Eunaticina oldroydi
Eupleura
Eupleura caudata
Eupleura etterae
Eupleura stimpsoni
Eupleura sulcidentata
Euribia
Eurytellina
Euvola
Evalea
Evalina
Fartulum
Fasciolaria
Fasciolaria branhamae
Fasciolaria distans
Fasciolaria gigantea
Fasciolaria hunteria
Fasciolaria princeps
Fasciolaria tulipa
Fasciolariidae
Favartia
Ferminoscala
Ficidae
Ficus
Ficus carolae
Ficus communis
Ficus papyratia
Ficus reticulata
Filibranchia
Fissidentalium
Fissurella
Fissurella angusta
Fissurella barbadensis
Fissurella crucifera
Fissurella fascicularis
Fissurella nodosa
Fissurella rosea
Fissurella volcano
Fissurellidae
Fistulana Bruguiere
Flabellinidae
Forreria
Forreria belcheri
Forreria cerrosensis
Forreria cerrosensis catalinensis
Forreria cerrosensis cerrosensis
Forreria pinnata
Fossaridae
Fossarus elegans
Fraginae
Fugleria
Fulgur
Fulguropsis
Fusinus
Fusinus barbarensis
Fusinus couei
Fusinus depetitthouarsi
Fusinus dupetit-thouarsi
Fusinus eucosmius
Fusinus harfordi
Fusinus kobelti
Fusinus timessus
Fusitriton
Gadila
Galeodes
Gari californica
Gastrana
Gastrana irus
Gastrochaena
Gastropteridae
Gastropteron
Gastropteron cinereum
Gastropteron meckeli
Gastropteron pacificum
Gastropteron rubrum
Gaza
Gaza superba
Gaza watsoni
Gemma
Gemma fretensis
Gemma gemma
Gemma manhattensis
Gemma purpurea
Gemminae
Gemmula periscelida
Genota viabrunnea
Gibberula
Gibberulina
Gibberulina amianta
Gibberulina hadria
Gibberulina lacrimida
Gibberulina lacrimula
Gibberulina ovuliformis
Gibberulina pyriformis
Glans
Glaucidae
Glaucus
Glaucus atlanticus
Glaucus forsteri
Glaucus marina
Glaucus radiata
Glicymeris
Glossaulax
Glossodoris
Glossodoris californiensis
Glossodoris iniversitatis
Glossodoris macfarlandi
Glossodoris porterae
Glossodoris universitatis
Glycimeris
Glycymeridae
Glycymeris
Glycymeris americana
Glycymeris decussata
Glycymeris lineata
Glycymeris pectinata
Glycymeris pennacea
Glycymeris spectralis
Glycymeris subobsoleta
Glycymeris undata
Glyphostoma gabbi
Gobraeus
Gonyaulax catanella
Gouldia cerina
Granula
Graptacme
Gryphaea
Gutturnium
Gymnobela blakeana
Gymnosomata
Gyroscala
Haliotidae
Haliotis
Haliotis assimilis
Haliotis aulaea
Haliotis bonita
Haliotis californiensis
Haliotis corrugata
Haliotis cracherodi
Haliotis diegoensis
Haliotis fulgens
Haliotis holzneri
Haliotis imperforata
Haliotis kamtschatkana
Haliotis lusus
Haliotis pourtalesi
Haliotis revea
Haliotis rufescens
Haliotis smithsoni
Haliotis sorenseni
Haliotis splendens
Haliotis splendidula
Haliotis turveri
Haliotis walallensis
Haliotis wallallensis
Haliris
Haloconcha
Haloconcha reflexa
Halopsyche
Haminoea
Haminoea antillarum
Haminoea cymbiformis
Haminoea elegans
Haminoea glabra
Haminoea olgae
Haminoea solitaria
Haminoea succinea
Haminoea vesicula
Haminoea virescens
Here
Herse
Herse cancellata
Herse columnella
Herse oryza
Herse urceolaris
Hespererato
Heterodonax
Heterodonax bimaculata
Heterodonax pacifica
Heteroteuthis tenera
Hexaplex
Hiatella
Hiatella arctica
Hiatella gallicana
Hiatella pholadis
Hiatella rugosa
Hiatella striata
Hinia
Hinnites
Hinnites giganteus
Hinnites multirugosus
Hipponicidae
Hipponix
Hipponix antiquatus
Hipponix barbatus
Hipponix benthophila
Hipponix cranoides
Hipponix serratus
Hipponix subrufus subrufus
Hipponix subrufus tumens
Homalopoma
Homalopoma albida
Homalopoma bacula
Homalopoma carpenteri
Homalopoma linnei
Homalopoma lurida
Hopkinsia rosacea
Hormomya
Humilaria kennerleyi
Hyalaea
Hyalaea affinis
Hyalaea angulata
Hyalaea coniformis
Hyalaea limbata
Hyalina
Hyalina avena
Hyalina avenacea
Hyalina avenella
Hyalina beyerleana
Hyalina californica
Hyalina succinea
Hyalina torticula
Hyalina veliei
Hyalocylis striata
Hydatina
Hydatina physis
Hydatina vesicaria
Hydatinidae
Hysteroconcha
Idioraphe
Illex illecebrosus
Ilyanassa
Inodrillara
Inodrillia aepynota
Iolaea
Iphigenia brasiliensis
Irus lamellifera
Ischadium
Ischnochiton
Ischnochiton acrior
Ischnochiton albus
Ischnochiton californiensis
Ischnochiton clathratus
Ischnochiton conspicuus
Ischnochiton cooperi
Ischnochiton floridanus
Ischnochiton magdalenensis
Ischnochiton mertensi
Ischnochiton palmulatus
Ischnochiton papillosus
Ischnochiton purpurascens
Ischnochiton regularis
Ischnochiton ruber
Ischnochitoniidae
Isognomon
Isognomon alata
Isognomon bicolor
Isognomon chemnitziana
Isognomon listeri
Isognomon radiata
Isognomonidae
Ivara
Ividella
Janacus
Janthina
Janthina bifida
Janthina exigua
Janthina fragilis
Janthina globosa
Janthina janthina
Janthinidae
Jumala
Jumala crebricostata
Jumala kennicotti
Katharina tunicata
Kelletia kelletia
Kellia laperousi
Kelliidae
Kennerlia
Krebsia
Kurtziella limonitella
Labiosa
Labiosa campechensis
Labiosa canaliculata
Labiosa lineata
Labiosa plicatella
Lacuna
Lacuna carinata
Lacuna divaricata
Lacuna porrecta
Lacuna solidula
Lacuna striata
Lacuna unifasciata
Lacuna variegata
Lacuna vincta
Lacunidae
Laevicardium
Laevicardium elatum
Laevicardium laevigatum
Laevicardium mortoni
Laevicardium pictum
Laevicardium serratum
Laevicardium substriatum
Laevicardium sybariticum
Laila cockerelli
Lamellaria
Lamellaria diegoensis
Lamellaria rhombica
Lamellariidae
Lamellibranchia
Lampusia
Larkinia
Lasaea
Lasaea cistula
Lasaea subviridis
Laskeya
Latiaxis
Latirus
Latirus brevicaudatus
Latirus infundibulum
Latirus mcgintyi
Leda
Ledella
Leiomya
Lepeta caeca
Lepetidae
Lepidochitona
Lepidochitona dentiens
Lepidochitona hartwegi
Lepidochitona keepiana
Lepidopleuridae
Lepidopleuroides
Lepidopleurus cancellatus
Lepidozona
Leptegouana
Leptonidae
Leptothyra
Leucozonia
Leucozonia cingidifera
Leucozonia cingulifera
Leucozonia nassa
Leucozonia ocellata
Levia
Lima
Lima antillensis
Lima caribaea
Lima dehiscens
Lima hemphilli
Lima hians
Lima inflata
Lima lima
Lima multicostata
Lima orientalis
Lima pellucida
Lima scabra
Lima squamosa
Lima tenera
Lima terica
Lima tetrica
Limacina
Limacina balea
Limacina scaphoidea
Limea bronniana
Limidae
Limopsidae
Limopsis
Limopsis antillensis
Limopsis cristata
Limopsis diegensis
Limopsis minuta
Limopsis sulcata
Linga
Lioberus castaneus
Liophora
Liotia
Liotia bairdi
Liotia cookeana
Liotia fenestrata
Lischkeia
Lischkeia bairdi
Lischkeia cidaris
Lischkeia ottoi
Lischkeia regalis
Lithophaga
Lithophaga antillarum
Lithophaga aristata
Lithophaga bisulcata
Lithophaga nigra
Lithophaga plumula
Lithophaga plumula kelseyi
Lithopoma
Litiopa
Litiopa bombix
Litiopa bombyx
Litiopa melanostoma
Littorina
Littorina angulifera
Littorina groenlandica
Littorina irrorata
Littorina littorea
Littorina meleagris
Littorina mespillum
Littorina obtusata
Littorina palliata
Littorina planaxis
Littorina rudis
Littorina saxatilis
Littorina scabra
Littorina scutulata
Littorina sitkana
Littorina ziczac
Livona
Livona pica
Loligo
Loligo opalescens
Loligo pealei
Lolliguncula
Lolliguncula brevipinna
Lolliguncula brevis
Lolliguncula hemiptera
Lonchaeus
Lottia gigantea
Lucapina
Lucapina adspersa
Lucapina cancellata
Lucapina sowerbii
Lucapina suffusa
Lucapinella
Lucapinella callomarginata
Lucapinella limatula
Lucina
Lucina amiantus
Lucina approximata
Lucina chrysostoma
Lucina crenella
Lucina floridana
Lucina jamaicensis
Lucina leucocyma
Lucina multilineata
Lucina pensylvanica
Lucina sombrerensis
Lucina tenuisculpta
Lucinidae
Lucinisca
Lucinoma
Lunarca
Lunatia
Lunatia groenlandica
Lunatia heros
Lunatia lewisi
Lunatia pallida
Lunatia triseriata
Luria
Lyonsia
Lyonsia arenosa
Lyonsia californica
Lyonsia floridana
Lyonsia hyalina
Lyropecten
Lyropecten antillarum
Lyropecten nodosus
Machaeroplax
Macoma
Macoma balthica
Macoma brota
Macoma calcarea
Macoma carlottensis
Macoma constricta
Macoma incongrua
Macoma indentata
Macoma inflatula
Macoma inquinata
Macoma irus
Macoma limula
Macoma mitchelii
Macoma mitchelli
Macoma nasuta
Macoma planiuscula
Macoma secta
Macoma souleyetiana
Macoma tenta
Macoma tenuirostris
Macoma yoldiformis
Macrocallista
Macrocallista maculata
Macrocallista nimbosa
Macron lividus
Mactra
Mactra californica
Mactra fragilis
Mactra nasuta
Mactridae
Magilidae
Malletia
Malletiidae
Mancinella
Mangelia morra
Mangeria
Mangilia
Mantellum
Margarites
Margarites cinereus
Margarites costalis
Margarites groenlandica
Margarites groenlandicus
Margarites lirulatus
Margarites obsoletus
Margarites parcipictus
Margarites pupillus
Margarites succinctus
Margarites umbilicalis
Margaritifera
Marginella
Marginella aureocincta
Marginella borealis
Marginella denticulata
Marginella eburneola
Marginella haematita
Marginella jaspidea
Marginella philtata
Martesia
Martesia cuneiformis
Martesia smithi
Martesia striata
Massyla
Maxwellia
Megatebennus bimaculatus
Megathura crenulata
Megayoldia
Meioceras
Melanella
Melanella bilineata
Melanella gibba
Melanella gracilis
Melongena
Melongena altispira
Melongena bispinosa
Melongena corona
Melongena corona perspinosa
Melongena estephomenos
Melongena inspinata
Melongena martiniana
Melongena melongena
Melongena minor
Melongena subcoronata
Melongenidae
Menestho
Mercenaria
Mercenaria campechiensis
Mercenaria mercenaria
Mercenaria notata
Mercenaria texana
Meretricinae
Mesodesma arctatum
Mesopleura
Metaplysia
Micranellum
Microcardium
Microcardium peramabile
Microcardium tinctum
Microgaza
Microgaza inornata
Microgaza rotella
Micromelo undata
Milneria kelseyi
Miralda
Mitra
Mitra albocincta
Mitra barbadensis
Mitra fergusoni
Mitra florida
Mitra hendersoni
Mitra idae
Mitra nodulosa
Mitra styria
Mitra sulcata
Mitra swainsoni antillensis
Mitrella
Mitrella lunata
Mitrella raveneli
Mitrella tuberosa
Mitrella variegata
Mitridae
Mitromorpha
Mitromorpha aspera
Mitromorpha filosa
Modiolaria
Modiolus
Modiolus tulipa
Modulidae
Modulus
Modulus carchedonius
Modulus modulus
Moerella
Monilispira
Monilispira albinodata
Monilispira albomaculata
Monilispira leucocyma
Monostiolum
Mopalia
Mopalia acuta
Mopalia ciliata
Mopalia fissa
Mopalia hindsi
Mopalia lignosa
Mopalia muscosa
Mopalia plumosa
Mopalia wosnessenski
Mopaliidae
Mormula
Morula
Morum oniscus
Murex
Murex alba
Murex anniae
Murex arenarius
Murex beaui
Murex bequaerti
Murex bicolor
Murex brandaris
Murex brevifrons
Murex burryi
Murex cabriti
Murex carpenteri
Murex cellulosus
Murex citrinus
Murex delicatus
Murex erinaceoides rhyssus
Murex festivus
Murex florifer
Murex fulvescens
Murex gemma
Murex hidalgoi
Murex macropterus
Murex messorius
Murex petri
Murex pomum
Murex recurvirostris
Murex recurvirostris rubidus
Murex recurvirostris sallasi
Murex rufus
Murex tremperi
Murex trialatus
Murex trunculus
Murex tryoni
Murexiella
Muricanthus
Muricidae
Muricidea
Muricopsis
Muricopsis floridana
Muricopsis hexagona
Muricopsis ostrearum
Musculus
Musculus discors
Musculus laevigatus
Musculus lateralis
Musculus niger
Mya
Mya arenaria
Mya japonica
Mya truncata
Myacea
Myoforceps
Mysella
Mysella golischi
Mysella pedroana
Mysella planulata
Mysella tumida
Mytilimeria nuttalli
Mytilopsis
Mytilus
Mytilus californianus
Mytilus edulis
Mytilus edulis diegensis
Mytilus hamatus
Mytilus plicatulus
Naranio
Narona cooperi
Nassariidae
Nassarius
Nassarius acutus
Nassarius ambiguus
Nassarius californianus
Nassarius consensus
Nassarius cooperi
Nassarius fossatus
Nassarius insculptus
Nassarius mendicus
Nassarius obsoletus
Nassarius perpinguis
Nassarius tegulus
Nassarius trivittatus
Nassarius vibex
Natica
Natica canrena
Natica clausa
Natica livida
Natica pusilla
Naticarius
Naticidae
Nautilus pompilius
Navea subglobosa
Navicula ostrearia
Neilonella
Nemocardium centifilosum
Neosimnia
Neosimnia acicularis
Neosimnia aequalis
Neosimnia avena
Neosimnia barbarensis
Neosimnia catalinensis
Neosimnia inflexa
Neosimnia loebbeckeana
Neosimnia piragua
Neosimnia similis
Neosimnia uniplicata
Neosimnia variabilis
Neptunea
Neptunea bicincta
Neptunea californica
Neptunea decemcostata
Neptunea eucosmia
Neptunea lirata
Neptunea lyrata
Neptunea pribiloffensis
Neptunea satura
Neptunea tabulata
Neptunea ventricosa
Nerita
Nerita fulgurans
Nerita peloronta
Nerita tessellata
Nerita variegata
Nerita versicolor
Neritidae
Neritina
Neritina floridana
Neritina reclivata
Neritina rotundata
Neritina sphaera
Neritina virginea
Neritina weyssei
Nesta
Nettastomella rostrata
Neverita
Nitidella
Nitidella carinata
Nitidella cribraria
Nitidella gausapata
Nitidella gouldi
Nitidella nitidula
Nitidella ocellata
Nodilittorina tuberculata
Nodipecten
Nodulus
Noetia
Noetia ponderosa
Noetia reversa
Norrisia norrisi
Notarchus
Notobranchaea
Nucella lapillus
Nucula
Nucula atacellana
Nucula cancellata
Nucula crenulata
Nucula delphinodonta
Nucula exigua
Nucula proxima
Nucula reticulata
Nucula tenuis
Nuculana
Nuculana carpenteri
Nuculana concentrica
Nuculana conceptionis
Nuculana curtulosa
Nuculana fossa
Nuculana hamata
Nuculana hindsi
Nuculana messanensis
Nuculana minuta
Nuculana penderi
Nuculana pernula
Nuculana redondoensis
Nuculana sculpta
Nuculana taphria
Nuculana tenuisulcata
Nuculana vaginata
Nuculanidae
Nuculidae
Nudibranchia
Nuttallia
Nuttallina
Nuttallina californica
Nuttallina flexa
Nuttallina scabra
Ocenebra
Ocenebra atropurpurea
Ocenebra circumtexta
Ocenebra citrica
Ocenebra clathrata
Ocenebra gracillima
Ocenebra interfossa
Ocenebra lurida
Ocenebra poulsoni
Ocenebra stearnsi
Ocenebra tenuisculpta
Ocinebra
Octopoda
Octopus
Octopus americanus
Octopus bimaculatus
Octopus bimaculoides
Octopus briareus
Octopus burryi
Octopus carolinensis
Octopus hongkongensis
Octopus joubini
Octopus macropus
Octopus punctatus
Octopus rugosus
Octopus vulgaris
Odostomia
Odostomia aepynota
Odostomia americana
Odostomia amianta
Odostomia bisuturalis
Odostomia donilla
Odostomia farella
Odostomia fetella
Odostomia gibbosa
Odostomia helga
Odostomia hendersoni
Odostomia impressa
Odostomia laxa
Odostomia modesta
Odostomia nota
Odostomia pedroana
Odostomia phanea
Odostomia seminuda
Odostomia terricula
Odostomia trifida
Odostomia willisi
Okeniidae
Oliva
Oliva litterata
Oliva reticularis
Oliva sayana
Olivella
Olivella baetica
Olivella bayeri
Olivella biplicata
Olivella floralia
Olivella intorta
Olivella jaspidea
Olivella moorei
Olivella mutica
Olivella nivea
Olivella pedroana
Olivella porteri
Olivella pycna
Olividae
Ommastrephidae
Onchidella
Onchidella borealis
Onchidella carpenteri
Onchidella floridana
Onchidiata
Onchidiidae
Onchidoridae
Onoba
Opalia
Opalia chacei
Opalia crenata
Opalia crenimarginata
Opalia hotessieriana
Opalia insculpta
Opalia wroblewskii
Opisthobranchia
Ostrea
Ostrea conchaphila
Ostrea cristata
Ostrea edulis
Ostrea equestris
Ostrea expansa
Ostrea folium
Ostrea frons
Ostrea limacella
Ostrea lurida
Ostrea permollis
Ostrea rubella
Ostrea rufoides
Ostrea spreta
Ostrea thomasi
Ostreidae
Oudardia
Ovulidae
Oxygyrus keraudreni
Pachydesma
Pachypoma
Paedoclione
Paleoconcha
Pandora
Pandora arenosa
Pandora bilirata
Pandora bushiana
Pandora carolinensis
Pandora filosa
Pandora gouldiana
Pandora granulata
Pandora trilineata
Panomya
Panomya ampla
Panomya arctica
Panope
Panope bitruncata
Panope generosa
Panope globosa
Panope solida
Panope taeniata
Papyridea
Papyridea hiatus
Papyridea semisulcata
Papyridea soleniformis
Parapholas californica
Parastarte triquetra
Paroctopus
Parvilucina
Patinopecten
Pecten
Pecten caurinus
Pecten diegensis
Pecten jacobaeus
Pecten laurenti
Pecten papyraceus
Pecten raveneli
Pecten tereinus
Pecten tryoni
Pecten ziczac
Pectinidae
Pedalion
Pedicularia
Pedicularia californica
Pedicularia decussata
Pedicularia ovuliformis
Pediculariella
Pelecypoda
Penitella
Penitella penita
Penitella sagitta
Peracle
Peracle bispinosa
Peracle clathrata
Peracle physoides
Peracle reticulata
Peraclidae
Peraclis
Periploma
Periploma discus
Periploma fragile
Periploma inaequivalvis
Periploma inequale
Periploma leanum
Periploma papyraceum
Periploma papyratium
Periploma planiusculum
Perna
Peronidia
Perotrochus
Perotrochus adansonianus
Perotrochus quoyanus
Persicula
Persicula catenata
Persicula jewetti
Persicula lavalleana
Persicula lavelleana
Persicula minuta
Persicula politula
Persicula regularis
Persicula subtrigona
Petaloconchus
Petaloconchus erectus
Petaloconchus irregularis
Petaloconchus nigricans
Petrasma
Petricola
Petricola lapicida
Petricola pholadiformis
Petricolaria
Phacoides
Phacoides acutilineatus
Phacoides annulatus
Phacoides centrifuga
Phacoides filosus
Phacoides jamaicensis
Phacoides nassula
Phacoides nuttalli
Phacoides pectinatus
Phalium
Phalium abbreviata
Phalium centiquadrata
Phalium centriquadrata
Phalium cicatricosum
Phalium glaucum
Phalium granulatum
Phalium inflatum
Phalium peristephes
Phasianellidae
Philine
Philine lima
Philine lineolata
Philine quadrata
Philine sagra
Philinidae
Pholadidae
Pholadidea ovoidea
Pholas campechiensis
Phyctiderma
Phylloda squamifera
Phyllodina
Phyllonotus
Physa
Pinctada radiata
Pinna
Pinna carnea
Pinna haudignobilis
Pinna rudis
Pinnidae
Pisania pusio
Pitar
Pitar albida
Pitar cordata
Pitar dione
Pitar fulminata
Pitar lupinaria
Pitar morrhuana
Pitar simpsoni
Pitarenus
Placiphorella velata
Placopecten
Placopecten grandis
Placopecten magellanicus
Plagioctenium
Planaxidae
Planaxis
Planaxis lineatus
Planaxis nucleus
Platyodon cancellatus
Pleurobranchidae
Pleurobranchus
Pleurobranchus atlanticus
Pleurobranchus gardineri
Pleurolucina
Pleuromeris
Pleuroploca
Pleuroploca gigantea
Pleuroploca papillosa
Pleuroploca princeps
Pleuroploca reevei
Pleurotomariidae
Plicatula gibbosa
Plicatulidae
Plumulella
Pneumoderma
Pneumodermopsis
Pneumonoderma
Pododesmus
Pododesmus cepio
Pododesmus decipiens
Pododesmus macroschisma
Pododesmus rudis
Polinices
Polinices alatus
Polinices altus
Polinices brunneus
Polinices draconis
Polinices duplicatus
Polinices immaculatus
Polinices imperforatus
Polinices lacteus
Polinices reclusianus
Polinices uberinus
Pollia
Polycera
Polycera atra
Polycera hummi
Polyceridae
Polymesoda
Polymesoda caroliniana
Polyschides
Polystira
Polystira albida
Polystira tellea
Polystira virgo
Polytropa
Pomaulax
Poromya granulata
Poromya rostrata
Potamididae
Primovula carnea
Promartynia
Propeamussiidae
Propeamussium
Propeamussium pourtalesianum
Protobranchia
Protocardiinae
Protonucula
Protothaca
Protothaca grata
Protothaca laciniata
Protothaca ruderata
Protothaca staminea
Protothaca tenerrima
Prunum
Prunum amabile
Prunum apicinum
Prunum bellum
Prunum borealis
Prunum carneum
Prunum guttatum
Prunum labiatum
Prunum limatulum
Prunum roosevelti
Prunum virginianum
Psammobia
Psammocola
Psammosolen
Psephidia
Psephidia lordi
Psephidia ovalis
Pseudochama
Pseudochama echinata
Pseudochama exogyra
Pseudochama ferruginea
Pseudochama granti
Pseudochama radians
Pseudocyrena floridana
Pseudomalaxis
Pseudomalaxis balesi
Pseudomalaxis nobilis
Pseudomiltha
Pseudoneptunea multangula
Pseudopythina
Pseudopythina compressa
Pseudopythina rugifera
Pteria
Pteria colymbus
Pteria sterna
Pteriidae
Pteropoda
Pteropurpura
Pterorytis
Pterorytis foliata
Pterorytis nuttalli
Pterynotus
Pulmonata
Puncturella
Puncturella cucullata
Puncturella galeata
Puncturella noachina
Pupillaria
Purpura
Purpura crispata
Purpura foliatum
Purpura pansa
Purpura patula
Pusula
Pycnodonta hyotis
Pyramidella
Pyramidella adamsi
Pyramidella dolabrata
Pyramidella fusca
Pyramidellidae
Pyrenidae
Pyrgiscus
Pyrgolampros
Pyrula papyratia
Pyrulofusus
Pyrunculus caelatus
Quadrans lintea
Raeta
Raeta campechensis
Raeta canaliculata
Ranella
Rangia
Rangia cuneata
Rangia flexuosa
Rangia nasuta
Rangia rostrata
Rangianella
Rehderia
Retusa
Retusa canaliculata
Retusa candei
Retusa obtusa
Retusa pertenuis
Retusa sulcata
Retusa turrita
Retusidae
Rhizorus
Rhizorus acutus
Rhizorus aspinosus
Rhizorus bushi
Rhizorus minutus
Rhizorus oxytatus
Rimula frenulata
Ringicula
Ringicula nitida
Ringicula semistriata
Ringiculidae
Rissoidae
Rissoina
Rissoina bakeri
Rissoina browniana
Rissoina bryerea
Rissoina californica
Rissoina cancellata
Rissoina chesneli
Rissoina cleo
Rissoina coronadoensis
Rissoina dalli
Rissoina decussata
Rissoina kelseyi
Rissoina kelyseyi
Rissoina laevigata
Rissoina multicostata
Rissoina newcombei
Rissoina sagraiana
Rissoina striosa
Rocellaria
Rocellaria cuneiformis
Rocellaria hians
Rocellaria ovata
Rochfortia
Rossia
Rossia equalis
Rossia pacifica
Rossia tenera
Rostanga pulchra
Rubellatoma
Rubellatoma diomedea
Rubellatoma rubella
Ruditapes
Rupellaria
Rupellaria californica
Rupellaria californiensis
Rupellaria carditoides
Rupellaria denticulata
Rupellaria tellimyalis
Rupellaria typica
Saccella
Salasiella
Sanguinolaria
Sanguinolaria cruenta
Sanguinolaria nuttalli
Sanguinolaria sanguinolenta
Saxicava
Saxicava arctica
Saxidomus
Saxidomus giganteus
Saxidomus nuttalli
Scala
Scalaria borealis
Scalina
Scaphella
Scaphella butleri
Scaphella dohrni
Scaphella dubia
Scaphella florida
Scaphella georgiana
Scaphella johnstoneae
Scaphella junonia
Scaphella schmitti
Scaphopoda
Schizothaerus
Schizothaerus capax
Schizothaerus nuttalli
Schizotrochus
Scissula
Scissurella
Scissurella crispata
Scissurella proxima
Scissurellidae
Sconsia striata
Scrobiculina
Scyllaea pelagica
Scyllaeidae
Searlesia dira
Seila
Seila adamsi
Seila montereyensis
Seila terebralis
Semele
Semele bellastriata
Semele cancellata
Semele decisa
Semele proficua
Semele purpurascens
Semele radiata
Semele rubropicta
Semele rupicola
Semicassis
Semicassis abbreviata
Semicassis inflatum
Semirossia
Sepia
Sepiolidae
Sepioteuthis
Sepioteuthis sepioidea
Septibranchia
Septifer
Septifer bifurcatus
Septifer obsoletus
Serripes groenlandicus
Sigatica
Sigatica carolinensis
Sigatica holograpta
Sigatica semisulcata
Siliqua
Siliqua alta
Siliqua costata
Siliqua lucida
Siliqua media
Siliqua nuttalli
Siliqua patula
Siliqua squama
Siliquaria
Sinum
Sinum californicum
Sinum debile
Sinum maculatum
Sinum perspectivum
Sinum scopulosum
Siphonaria
Siphonaria alternata
Siphonaria lineolata
Siphonaria naufragum
Siphonaria pectinata
Siphonariidae
Siphonodentaliidae
Smaragdia
Smaragdia viridemaris
Smaragdia viridis
Smaragdia weyssei
Solariella
Solariella lacunella
Solariella lamellosa
Solariella obscura
Solariella peramabilis
Solariella regalis
Solariorbis
Solecurtus
Solecurtus cumingianus
Solecurtus sanctaemarthae
Solemya
Solemya borealis
Solemya occidentalis
Solemya valvulus
Solemya velum
Solemyidae
Solen
Solen rosaceus
Solen sicarius
Solen viridis
Solen vividis
Solenidae
Spengleria rostrata
Sphenia
Sphenia fragilis
Sphenia ovoidea
Spiratella
Spiratella balea
Spiratella bulimoides
Spiratella gouldi
Spiratella helicina
Spiratella inflata
Spiratella lesueuri
Spiratella pacifica
Spiratella retroversa
Spiratella scaphoidea
Spiratella trochiformis
Spiratellidae
Spiroglyphus
Spiroglyphus annulatus
Spiroglyphus lituellus
Spirula spirula
Spisula
Spisula alaskana
Spisula catilliformis
Spisula dolabriformis
Spisula falcata
Spisula hemphilli
Spisula planulata
Spisula polynyma
Spisula similis
Spisula solidissima
Spisula voyi
Spondylidae
Spondylus
Spondylus americanus
Spondylus dominicensis
Spondylus echinatus
Spondylus pictorum
Stenoplax
Sthenorytis
Sthenorytis cubana
Sthenorytis epae
Sthenorytis hendersoni
Sthenorytis pernobilis
Sthenoteuthis bartrami
Stramonita
Strigilla
Strigilla carnaria
Strigilla flexuosa
Strigilla mirabilis
Strigilla pisiformis
Strigilla rombergi
Strioturbonilla
Strombidae
Strombus
Strombus alatus
Strombus bituberculatus
Strombus canaliculatus
Strombus costatus
Strombus gallus
Strombus gigas
Strombus goliath
Strombus horridus
Strombus peculiaris
Strombus pugilis
Strombus raninus
Strombus sloani
Strombus spectabilis
Strombus verrilli
Stylidium
Styliferidae
Styliola
Styliola conica
Styliola subula
Styliola vitrea
Sulcosipho
Supplanaxis
Susania
Sycofulgur
Symmetrogephyrus
Symmetrogephyrus pallasi
Symmetrogephyrus vestitus
Syrnola
Tachyrhynchus
Tachyrhynchus erosum
Tachyrhynchus lacteolum
Tachyrhynchus reticulatum
Taenioturbo
Tagelus
Tagelus affinis
Tagelus californianus
Tagelus divisus
Tagelus gibbus
Tagelus plebeius
Tagelus politus
Tagelus subteres
Taglus politus
Tapes
Tapes bifurcata
Tapes philippinarum
Tapes semidecussata
Taras orbella
Taxodonta
Tectarius
Tectarius muricatus
Tectarius tuberculatus
Tectibranchia
Tectininus
Tegula
Tegula aureotincta
Tegula brunnea
Tegula excavata
Tegula fasciata
Tegula funebralis
Tegula gallina
Tegula hotessieriana
Tegula indusi
Tegula ligulata
Tegula lividomaculata
Tegula marcida
Tegula montereyi
Tegula regina
Tegula scalaris
Teinostoma
Teinostoma biscaynense
Teinostoma biscaynensis
Teinostoma clavium
Teinostoma cocolitoris
Teinostoma cryptospira
Teinostoma goniogyrus
Teinostoma leremum
Teinostoma litus-palmarum
Teinostoma lituspalmarum
Teinostoma nesaeum
Teinostoma obtectum
Teinostoma parvicallum
Teinostoma pilsbryi
Tellidora cristata
Tellina
Tellina agilis
Tellina alternata
Tellina angulosa
Tellina buttoni
Tellina candeana
Tellina carpenteri
Tellina decora
Tellina elucens
Tellina fausta
Tellina idae
Tellina interrupta
Tellina iris
Tellina laevigata
Tellina lineata
Tellina lutea
Tellina magna
Tellina mera
Tellina meropsis
Tellina modesta
Tellina polita
Tellina promera
Tellina punicea
Tellina radiata
Tellina salmonea
Tellina sayi
Tellina similis
Tellina sybaritica
Tellina tampaensis
Tellina tener
Tellina tenera
Tellina texana
Tellina venulosa
Tellina versicolor
Tellinella
Tenagodidae
Tenagodus
Tenagodus modestus
Tenagodus squamatus
Terebra
Terebra cinerea
Terebra concava
Terebra dislocata
Terebra feldmanni
Terebra flammea
Terebra floridana
Terebra hastata
Terebra limatula
Terebra lutescens
Terebra pedroana
Terebra protexta
Terebra salleana
Terebra taurinum
Terebridae
Teredinidae
Teredo
Teredo bartschi
Teredo diegensis
Teredo navalis
Teredo townsendi
Tergipedidae
Tergipes despectus
Tethys
Tetrabranchia
Thais
Thais canaliculata
Thais crispata
Thais deltoidea
Thais emarginata
Thais haemastoma
Thais haemastoma floridana
Thais haemastoma haysae
Thais imbricatus
Thais lamellosa
Thais lapillus
Thais lima
Thais rustica
Thais undata
Thecosomata
Thericium
Thestyleda
Thracia
Thracia conradi
Thracia curta
Thracia trapezoides
Thyasira
Thyasira bisecta
Thyasira disjuncta
Thyasira gouldi
Thyasira trisinuata
Timoclea
Tindaria
Tindaria brunnea
Tivela
Tivela crassatelloides
Tivela floridana
Tivela stultorum
Tonicella
Tonicella lineata
Tonicella marmorea
Tonicia schrammi
Tonna
Tonna (Dolium) album
Tonna album
Tonna brasiliana
Tonna galea
Tonna maculosa
Tonna perdix
Tonnidae
Torcula
Torinia
Torinia bisulcata
Torinia cylindrica
Trachycardium
Trachycardium egmontianum
Trachycardium isocardia
Trachycardium magnum
Trachycardium muricatum
Trachycardium quadragenarium
Transennella
Transennella conradina
Transennella stimpsoni
Transennella tantilla
Trapeziidae
Tremoctopus violaceus
Trichotropidae
Trichotropis
Trichotropis bicarinata
Trichotropis borealis
Trichotropis cancellata
Trichotropis insignis
Tricolia
Tricolia affinis
Tricolia compta
Tricolia concinna
Tricolia pulchella
Tricolia tessellata
Tricolia variegata
Trigoniocardia
Trigoniocardia biangulata
Trigoniocardia medium
Trigonostoma
Trigonostoma rugosum
Trigonostoma tenerum
Trigonulina
Triopha
Triopha carpenteri
Triopha grandis
Triopha maculata
Triphora
Triphora decorata
Triphora nigrocincta
Triphora ornatus
Triphora pedroana
Triphora perversa
Triphora pulchella
Triphoridae
Tritonalia
Tritoniscus
Tritonocauda
Trivia
Trivia antillarum
Trivia armandina
Trivia californiana
Trivia candidula
Trivia globosa
Trivia leucosphaera
Trivia maltbiana
Trivia nivea
Trivia nix
Trivia pediculus
Trivia pullata
Trivia quadripunctata
Trivia radians
Trivia ritteri
Trivia sanguinea
Trivia solandri
Trivia subrostrata
Trivia suffusa
Trochidae
Trochita radians
Trona
Trophon tenuisculptus
Trophonopsis
Trophonopsis lasius
Trophonopsis tenuisculptus
Truncacila
Turbinella scolyma
Turbinidae
Turbo
Turbo canaliculatus
Turbo castaneus
Turbo crenulatus
Turbo spenglerianus
Turbonilla
Turbonilla acra
Turbonilla aragoni
Turbonilla buttoni
Turbonilla chocolata
Turbonilla interrupta
Turbonilla kelseyi
Turbonilla laminata
Turbonilla nivea
Turbonilla stricta
Turbonilla tridentata
Turcicula
Turridae
Turritella
Turritella acropora
Turritella cooperi
Turritella exoleta
Turritella mariana
Turritella variegata
Turritellidae
Turtonia minuta
Tutufa
Urosalpinx
Urosalpinx cinerea
Urosalpinx follyensis
Urosalpinx perrugata
Urosalpinx tampaensis
Vanikoro oxychone
Vanikoroidae
Varicorbula
Varicorbula disparilis
Varicorbula operculata
Vasum
Vasum coestus
Vasum muricatum
Velutina
Velutina laevigata
Velutina undata
Velutina zonata
Venericardia
Venericardia borealis
Venericardia flabella
Venericardia novangliae
Venericardia perplana
Venericardia redondoensis
Venericardia stearnsi
Venericardia tridentata
Venericardia ventricosa
Veneridae
Venus
Vermetidae
Vermicularia
Vermicularia fargoi
Vermicularia knorri
Vermicularia spirata
Verticordia
Verticordia fischeriana
Verticordia fisheriana
Verticordia ornata
Vesica
Vitrinella
Vitrinella beaui
Vitrinella helicoidea
Vitrinella multistriata
Vitta
Volsella
Volsella americana
Volsella capax
Volsella demissa
Volsella demissa granosissima
Volsella fornicata
Volsella modiolus
Volsella plicatula
Volsella tulipa
Voluta
Voluta musica
Voluta virescens
Volutharpa ampullacea
Volutidae
Volutopsius
Volutopsius castaneus
Volutopsius harpa
Volvarina
Volvula
Volvulella
Xancidae
Xancus
Xancus angulatus
Xancus scolyma
Xenophora
Xenophora caribaeum
Xenophora conchyliophora
Xenophora longleyi
Xenophora radians
Xenophora trochiformis
Xenophoridae
Xylophaga
Xylophaga dorsalis
Xylophaga washingtona
Yoldia
Yoldia limatula
Yoldia limatula gardneri
Yoldia myalis
Yoldia sapotilla
Yoldia thraciaeformis
Zaphon
Zeidora
Zirfaea
Zirfaea crispata
Zirfaea gabbi
Zirfaea pilsbryi
Zonaria

>>> my_ntersectionset = set(text)
>>> print my_set
set(['\n', ' ', ')', '(', '-', 'A', 'C', 'B', 'E', 'D', 'G', 'F', 'I', 'H', 'K', 'J', 'M', 'L', 'O', 'N', 'Q', 'P', 'S', 'R', 'U', 'T', 'V', 'Y', 'X', 'Z', 'a', 'c', 'b', 'e', 'd', 'g', 'f', 'i', 'h', 'k', 'j', 'm', 'l', 'o', 'n', 'q', 'p', 's', 'r', 'u', 't', 'w', 'v', 'y', 'x', 'z'])
>>> names_list = text
>>> print names_list
Abra
Abra aequalis
Abra lioica
Abra profundorum
Acanthina
Acanthina lapilloides
Acanthina paucilirata
Acanthina punctulata
Acanthina spirata
Acanthinucella
Acanthochitona
Acanthochitona astriger
Acanthochitona balesae
Acanthochitona pygmaeus
Acanthochitona spiculosus
Acanthodoris
Acanthodoris brunnea
Acanthodoris pilosa
Acanthopleura
Acanthopleura flexa
Acanthopleura granulata
Acar
Acephala
Acila castrensis
Acirsa
Acirsa borealis
Acirsa costulata
Aclididae
Acmaea
Acmaea albicosta
Acmaea alveus
Acmaea antillarum
Acmaea asmi
Acmaea candeana
Acmaea conus
Acmaea cribraria
Acmaea cubensis
Acmaea depicta
Acmaea digitalis
Acmaea fenestrata
Acmaea fungoides
Acmaea insessa
Acmaea instabilis
Acmaea jamaicensis
Acmaea leucopleura
Acmaea limatula
Acmaea mitra
Acmaea paleacea
Acmaea patina
Acmaea pelta
Acmaea persona
Acmaea pulcherrima
Acmaea punctulata
Acmaea pustulata
Acmaea scabra
Acmaea scutum
Acmaea simplex
Acmaea spectrum
Acmaea strigatella
Acmaea tenera
Acmaea tessulata
Acmaea testudinalis
Acmaea triangularis
Acmaeidae
Actaeon
Acteocina
Acteocina candei
Acteocina cerealis
Acteocina culitella
Acteocinidae
Acteon
Acteon candens
Acteon punctocaelatus
Acteon punctostriatus
Acteon vancouverensis
Acteonidae
Adalaria proxima
Adapedonta
Adesmacea
Admete couthouyi
Adula
Aeolidia papillosa
Aeolidiidae
Aequipecten
Aequipecten borealis
Aequipecten dislocatus
Aequipecten exasperatus
Aequipecten fusco-purpureus
Aequipecten gibbus
Aequipecten gibbus nucleus
Aequipecten glyptus
Aequipecten irradians
Aequipecten irradians amplicostatus
Aequipecten irradians concentricus
Aequipecten irradians irradians
Aequipecten lineolaris
Aequipecten mayaguezensis
Aequipecten muscosus
Aequipecten nucleus
Aequipecten phrygium
Aequipecten tryoni
Agriodesma
Agriopoma
Alabina
Alabina diegensis
Alabina tenuisculpta
Aldisa sanguinea
Aletes squamigerous
Allopora californica
Aloidis
Amaea
Amaea mitchelli
Amaea retifera
Amaura
Amauropsis
Amauropsis islandica
Amauropsis purpurea
Amiantis
Amiantis callosa
Amiantis nobilis
Amicula
Amicula stelleri
Amphineura
Amphissa
Amphissa bicolor
Amphissa columbiana
Amphissa undata
Amphissa versicolor
Amphithalamus
Amphithalamus inclusus
Amphithalamus lacunatus
Amphithalamus tenuis
Amusium
Amygdalum
Amygdalum papyria
Amygdalum sagittata
Anachis
Anachis avara
Anachis obesa
Anachis ostreicola
Anachis penicillata
Anachis translirata
Anadara
Anadara americana
Anadara auriculata
Anadara baughmani
Anadara brasiliana
Anadara campechiensis
Anadara chemnitzi
Anadara deshayesi
Anadara grandis
Anadara incongrua
Anadara lienosa
Anadara lienosa floridana
Anadara multicostata
Anadara notabalis
Anadara ovalis
Anadara pexata
Anadara secticostata
Anadara springeri
Anadara sulcosa
Anadara transversa
Anatina Schumacher
Ancistrolepsis
Ancistrosyrinx
Ancistrosyrinx elegans
Ancistrosyrinx radiata
Ancula
Ancula cristata
Ancula pacifica
Ancula sulphurea
Angulus
Angulus tener
Anisodoris
Annulicallus
Anodontia
Anodontia alba
Anodontia chrysostoma
Anodontia philippiana
Anodontia schrammi
Anomalocardia
Anomalocardia brasiliana
Anomalocardia cuneimeris
Anomalodesmacea
Anomia
Anomia aculeata
Anomia peruviana
Anomia simplex
Anomiidae
Anopsia
Antalis
Antigona
Antigona listeri
Antigona rigida
Antigona rugatina
Antigona strigillina
Antillophos candei
Aperiploma
Aplysia
Aplysia badistes
Aplysia dactylomela
Aplysia floridensis
Aplysia perviridis
Aplysia protea
Aplysia willcoxi
Aplysidae
Apolymetis
Apolymetis alta
Apolymetis biangulata
Apolymetis intastriata
Aporrhaidae
Aporrhais
Aporrhais labradorensis
Aporrhais mainensis
Aporrhais occidentalis
Aptyxis luteopicta
Arca
Arca balesi
Arca occidentalis
Arca pernoides
Arca reticulata
Arca umbonata
Arca zebra
Archidoris
Archidoris montereyensis
Archidoris nobilis
Architectonica
Architectonica granulata
Architectonica krebsi
Architectonica nobilis
Architectonica peracuta
Architeuthis
Architeuthis harveyi
Architeuthis princeps
Arcidae
Arcopagia fausta
Arcopsis adamsi
Arctica islandica
Arcticidae
Arctomelon stearnsi
Arene
Arene cruentata
Arene gemma
Arene vanhyningi
Arene variabilis
Arene venustula
Argina
Arginarca
Argobuccinum oregonense
Argonauta
Argonauta americana
Argonauta argo
Argonauta hians
Asaphis deflorata
Astarte
Astarte borealis
Astarte castanea
Astarte nana
Astarte subequilatera
Astarte undata
Astartidae
Astraea
Astraea americana
Astraea brevispina
Astraea caelata
Astraea gibberosa
Astraea guadeloupensis
Astraea imbricata
Astraea inaequalis
Astraea longispina
Astraea spinulosa
Astraea tuber
Astraea undosa
Astralium
Astyris
Atlanta
Atlanta peroni
Atlantidae
Atrina
Atrina rigida
Atrina serrata
Atydae
Atys
Atys caribaea
Atys sandersoni
Aurinia
Austrotrophon
Bailya
Bailya intricata
Bailya parva
Bankia
Bankia canalis
Bankia caribbea
Bankia fimbriatula
Bankia gouldi
Bankia mexicana
Bankiella
Bankiopsis
Barbarofusus
Barbatia
Barbatia bailyi
Barbatia barbata
Barbatia cancellaria
Barbatia candida
Barbatia domingensis
Barbatia helblingi
Barbatia jamaicensis
Barbatia tenera
Barnea
Barnea costata
Barnea pacifica
Barnea spathulata
Barnea truncata
Bartschella
Basommatophora
Batillaria minima
Bellucina
Beringius
Bittium
Bittium alternatum
Bittium attenuatum
Bittium eschrichti
Bittium interfossum
Bittium montereyense
Bittium quadrifilatum
Bittium varium
Bittium virginicum
Bivalvia
Bivetiella
Blepharopoda occidentalis
Boreomelon
Boreostrophon peregrinus
Boreotrophon
Boreotrophon clathratus
Boreotrophon dalli
Boreotrophon multicostatus
Boreotrophon orpheus
Boreotrophon pacificus
Boreotrophon peregrinus
Boreotrophon scalariformis
Boreotrophon scitulus
Boreotrophon smithi
Boreotrophon stuarti
Boreotrophon triangulatus
Bornia longipes
Botula
Botula californiensis
Botula falcata
Botula fusca
Brachidontes
Brachidontes adamsianus
Brachidontes citrinus
Brachidontes exustus
Brachidontes hamatus
Brachidontes multiformis
Brachidontes recurvus
Brachidontes stearnsi
Buccinidae
Buccinum
Buccinum baeri
Buccinum glaciale
Buccinum plectrum
Buccinum tenue
Buccinum undatum
Bufonaria
Bulla
Bulla amygdala
Bulla gouldiana
Bulla occidentalis
Bulla punctulata
Bulla striata
Bullaria
Bullidae
Bursa
Bursa affinis
Bursa caelata
Bursa californica
Bursa corrugata
Bursa crassa
Bursa cubaniana
Bursa granularis
Bursa louisa
Bursa ponderosa
Bursa spadicea
Bursa tenuisculpta
Bursa thomae
Bursatella leachi plei
Busycon
Busycon canaliculatum
Busycon carica
Busycon coarctatum
Busycon contrarium
Busycon kieneri
Busycon perversum
Busycon plagosum
Busycon pyrum
Busycon spiratum
Busycotypus
Cadlina
Cadlina flavomaculata
Cadlina laevis
Cadlina marginata
Cadlina obvelata
Cadlina planulata
Cadlina repanda
Cadulus
Cadulus carolinensis
Cadulus mayori
Cadulus quadridentatus
Caecidae
Caecum
Caecum bakeri
Caecum barkleyense
Caecum barkleyensis
Caecum californicum
Caecum carolinianum
Caecum carpenteri
Caecum catalinense
Caecum cayosense
Caecum cooperi
Caecum crebricinctum
Caecum dalli
Caecum diegense
Caecum floridanum
Caecum grippi
Caecum hemphilli
Caecum heptagonum
Caecum lermondi
Caecum licalum
Caecum nebulosum
Caecum nitidum
Caecum occidentale
Caecum orcutti
Caecum oregonense
Caecum pedroense
Caecum pulchellum
Caecum rosanum
Callianax
Calliostoma
Calliostoma annulatum
Calliostoma bairdi
Calliostoma canaliculatum
Calliostoma doliarium
Calliostoma euglyptum
Calliostoma gemmulatum
Calliostoma gloriosum
Calliostoma jujubinum
Calliostoma ligatum
Calliostoma occidentale
Calliostoma psyche
Calliostoma pulchrum
Calliostoma roseolum
Calliostoma splendens
Calliostoma subumbilicatum
Calliostoma supragranosum
Calliostoma tampaense
Calliostoma tricolor
Calliostoma variegatum
Calliostoma zonamestum
Calliotropis
Callista eucymata
Callocardia texasiana
Callogaza
Calloplax janeirensis
Calyptraea
Calyptraea candeana
Calyptraea centralis
Calyptraea contorta
Calyptraea fastigiata
Calyptraeidae
Cancellaria
Cancellaria adelae
Cancellaria conradiana
Cancellaria crawfordiana
Cancellaria reticulata
Cancellariidae
Cantharus
Cantharus auritula
Cantharus cancellaria
Cantharus tinctus
Capulidae
Capulus
Capulus californicus
Capulus incurvatus
Capulus intortus
Cardiidae
Cardiomya
Cardiomya costellata
Cardiomya gemma
Cardiomya multicostata
Cardiomya pectinata
Cardita
Cardita carpenteri
Cardita dominguensis
Cardita floridana
Cardita gracilis
Carditamera
Carditidae
Cardium
Cardium corbis
Carinaria
Carinaria lamarcki
Carinaria mediterranea
Carinariidae
Cassididae
Cassis
Cassis flammea
Cassis madagascariensis
Cassis madagascariensis spinella
Cassis spinella
Cassis tuberosa
Catriona
Catriona aurantia
Catriona aurantiaca
Cavolina
Cavolina affinis
Cavolina angulata
Cavolina costata
Cavolina cuspidata
Cavolina elongata
Cavolina gibbosa
Cavolina imitans
Cavolina inermis
Cavolina inflexa
Cavolina intermedia
Cavolina labiata
Cavolina limbata
Cavolina longirostris
Cavolina minuta
Cavolina mucronata
Cavolina quadridentata
Cavolina reeviana
Cavolina telemus
Cavolina tridentata
Cavolina trispinosa
Cavolina uncinata
Cavolina uncinatiformis
Cavolinia
Cavolinidae
Cenchritis
Cephalopoda
Cerastoderma pinnulatum
Ceratostoma foliatum
Ceratozona rugosa
Cerithidea
Cerithidea costata
Cerithidea hegewischi californica
Cerithidea pliculosa
Cerithidea scalariformis
Cerithidea turrita
Cerithideopsis
Cerithiopsis
Cerithiopsis carpenteri
Cerithiopsis emersoni
Cerithiopsis greeni
Cerithiopsis grippi
Cerithiopsis pedroana
Cerithiopsis subulata
Cerithiopsis vanhyningi
Cerithiopsis virginica
Cerithium
Cerithium algicola
Cerithium eburneum
Cerithium floridanum
Cerithium literatum
Cerithium muscarum
Cerithium variabile
Cerithium versicolor
Cerodrillia
Cerodrillia perryae
Cerodrillia thea
Chaetopleura apiculata
Chama
Chama congregata
Chama firma
Chama macerophylla
Chama sinuosa
Chamidae
Charonia
Charonia atlantica
Charonia tritonis
Charonia tritonis nobilis
Cheila equestris
Chemnitzia
Chicoreus
Chione
Chione californiensis
Chione cancellata
Chione fluctifraga
Chione gnidia
Chione grus
Chione intapurpurea
Chione interpurpurea
Chione latilirata
Chione mazycki
Chione paphia
Chione pygmaea
Chione succincta
Chione undatella
Chionidae
Chiton
Chiton albolineatus
Chiton laevigatus
Chiton marmoratus
Chiton squamosus
Chiton stokesi
Chiton tuberculatus
Chiton virgulatus
Chiton viridis
Chitonidae
Chlamys
Chlamys benedicti
Chlamys hastatus
Chlamys hastatus hastatus
Chlamys hastatus hericius
Chlamys hericius
Chlamys hindsi
Chlamys imbricatus
Chlamys islandicus
Chlamys mildredae
Chlamys ornatus
Chlamys sentis
Chlorostoma
Chrysallida
Chrysodomus lirata
Chrysodomus satura
Cidarina
Cingula
Cingula aculeus
Cingula asser
Cingula cerinella
Cingula kelseyi
Cingula kyskensis
Cingula montereyensis
Cingula palmeri
Circinae
Circomphalus
Circulus
Cirsotrema
Cirsotrema arcella
Cirsotrema dalli
Cittarium
Cleodora
Cleodora exacuta
Cleodora virgula
Clinocardium
Clinocardium ciliatum
Clinocardium corbis
Clinocardium fucanum
Clinocardium nuttalli
Clio
Clio balantium
Clio cuspidata
Clio exacuta
Clio falcata
Clio lanceolata
Clio polita
Clio pyramidata
Clio recurva
Clione
Clionopsis
Cliopsis
Clypidella
Cochlodesma
Codakia
Codakia californica
Codakia costata
Codakia filiata
Codakia orbicularis
Codakia orbiculata
Collisella
Colubraria
Colubraria lanceolata
Colubraria swifti
Colubraria testacea
Colubrellina
Columbella
Columbella mercatoria
Columbella rusticoides
Columbellidae
Colus
Colus caelatus
Colus pubescens
Colus pygmaea
Colus pygmaeus
Colus spitzbergensis
Colus stimpsoni
Colus ventricosus
Compsomyax subdiaphana
Congeria leucophaeta
Conidae
Conus
Conus amphiurgus
Conus aureofasciatus
Conus austini
Conus californicus
Conus citrinus
Conus clarki
Conus daucus
Conus floridanus
Conus floridanus burryae
Conus floridanus floridensis
Conus floridensis
Conus frisbeyae
Conus granulatus
Conus jaspideus
Conus juliae
Conus mazei
Conus mus
Conus peali
Conus regius
Conus sennottorum
Conus sozoni
Conus spurius atlanticus
Conus spurius spurius
Conus stearnsi
Conus stimpsoni
Conus vanhyningi
Conus verrucosus
Conus villepini
Cooperella subdiaphana
Coralliophaga coralliophaga
Coralliophila
Coralliophila abbreviata
Coralliophila costata
Coralliophila deburghiae
Coralliophila hindsi
Corbiculiidae
Corbula
Corbula barrattiana
Corbula contracta
Corbula dietziana
Corbula disparilis
Corbula luteola
Corbula nasuta
Corbula porcella
Corbula rosea
Corbula swiftiana
Corbulidae
Coryphella rufibranchialis
Costacallista
Crassatella
Crassatellidae
Crassatellites
Crassinella
Crassinella lunulata
Crassinella mactracea
Crassispira
Crassispira ebenina
Crassispira ostrearum
Crassispira sanibelensis
Crassispira tampaensis
Crassispirella
Crassostrea
Crassostrea angulata
Crassostrea brasiliana
Crassostrea floridensis
Crassostrea gigas
Crassostrea laperousi
Crassostrea rhizophorae
Crassostrea virginica
Cratena
Cremides
Crenella
Crenella columbiana
Crenella decussata
Crenella divaricata
Crenella faba
Crenella glandula
Crepidula
Crepidula aculeata
Crepidula acuta
Crepidula convexa
Crepidula excavata
Crepidula fornicata
Crepidula glauca
Crepidula maculosa
Crepidula nummaria
Crepidula onyx
Crepidula plana
Crepipatella lingulata
Creseis
Creseis acicula
Creseis conica
Creseis coniformis
Creseis virgula
Creseis vitrea
Crossata
Crucibulum
Crucibulum auricula
Crucibulum spinosum
Crucibulum striatum
Cryptochiton stelleri
Cryptoconchus floridanus
Cryptomya californica
Cryptonatica
Cryptoplacidae
Ctena
Ctenoides
Cumingia
Cumingia californica
Cumingia coarctata
Cumingia tellinoides
Cumingia vanhyningi
Cunearca
Cuspidaria
Cuspidaria glacialis
Cuspidaria granulata
Cuspidaria jeffreysi
Cuspidaria rostrata
Cuvieria
Cuvierina
Cyanoplax
Cyathodonta
Cyathodonta dubiosa
Cyathodonta pedroana
Cyathodonta undulata
Cyclocardia
Cyclostrema
Cyclostrema amabile
Cyclostrema cancellatum
Cyclostrema cookeana
Cyclotellina
Cylichna
Cylichna alba
Cylichna bidentata
Cylichna biplicata
Cylichna gouldi
Cylichnella
Cymatiidae
Cymatium
Cymatium aquitile
Cymatium chlorostomum
Cymatium cynocephalum
Cymatium femorale
Cymatium gracile
Cymatium labiosum
Cymatium martinianum
Cymatium muricinum
Cymatium pileare
Cymatium prima
Cymatium tuberosum
Cymatium velei
Cyphoma
Cyphoma gibbosum
Cyphoma mcgintyi
Cyphoma signatum
Cypraea
Cypraea cervus
Cypraea cinerea
Cypraea exanthema
Cypraea moneta
Cypraea mus
Cypraea pantherina
Cypraea spadicea
Cypraea spurca
Cypraea spurca acicularis
Cypraea tigris
Cypraea vallei
Cypraea zebra
Cypraecassis
Cypraecassis rufa
Cypraecassis testiculus
Cypraeolina
Cyprina
Cyrtodaria
Cyrtodaria kurriana
Cyrtodaria siliqua
Daphnella lymneiformis
Decapoda
Dendrodorididae
Dendrodoris
Dendrodoris fulva
Dendronotidae
Dendronotus
Dendronotus arborescens
Dendronotus frondosus
Dendronotus giganteus
Dentale
Dentaliidae
Dentalium
Dentalium antillarum
Dentalium calamus
Dentalium cestum
Dentalium eboreum
Dentalium elephantinum
Dentalium entale
Dentalium entale stimpsoni
Dentalium filum
Dentalium floridense
Dentalium laqueatum
Dentalium megathyris Dall
Dentalium occidentale
Dentalium pilsbryi
Dentalium pretiosum
Dentalium pseudohexagonum
Dentalium semiostriolatum
Dentalium semistriolatum
Dentalium sowerbyi
Dentalium texasianum
Dentilucina
Dentiscala
Diacria
Diadora
Dialula sandiegensis
Diaphana
Diaphana debilis
Diaphana globosa
Diaphana hiemalis
Diaphana minuta
Diaphanidae
Diastomidae
Diaulula sandiegensis
Diberus
Dibranchia
Dinocardium
Dinocardium robustum
Dinocardium vanhyningi
Diodora
Diodora alternata
Diodora aspera
Diodora cayenensis
Diodora densiclathrata
Diodora dysoni
Diodora listeri
Diodora minuta
Diodora murina
Diplodonta
Diplodonta granulosa
Diplodonta orbella
Diplodonta punctata
Diplodonta semiaspera
Diplodonta subquadrata
Diplodontidae
Dischides
Discodoris heathi
Dispotaea
Dissentoma
Dissentoma prima
Distorsio
Distorsio clathrata
Distorsio constricta
Distorsio constricta mcgintyi
Distorsio floridana
Divaricella
Divaricella dentata
Divaricella quadrisulcata
Dolium
Donax
Donax californica
Donax denticulata
Donax fossor
Donax gouldi
Donax roemeri
Donax striata
Donax tumida
Donax variabilis
Doridae
Doriopsis
Doryteuthis plei
Dorytewthis plei
Dosina
Dosinia
Dosinia discus
Dosinia elegans
Dosinidia
Dreissenidae
Drupa nodulosa
Echininus nodulosus
Echinochama
Echinochama arcinella
Echinochama californica
Echinochama cornuta
Egregia
Elephantanellum
Ellipetylus
Emarginula phrixodes
Engina turbinella
Ensis
Ensis californicus
Ensis directus
Ensis megistus
Ensis minor
Ensis myrae
Entemnotrochus
Entoconchidae note
Entodesma saxicola
Eontia
Epilucina
Episiphon
Epitonium
Epitonium angulatum
Epitonium clathrum
Epitonium commune
Epitonium contorquata
Epitonium eburneum
Epitonium folaceicostum
Epitonium foliaceicostum
Epitonium humphreysi
Epitonium indianorum
Epitonium krebsi
Epitonium lamellosum
Epitonium lineatum
Epitonium muricata
Epitonium occidentale
Epitonium pretiosula
Epitonium pretiosum
Epitonium reynoldsi
Epitonium rupicolum
Epitonium scalare
Epitonium spina-rosae
Epitonium swifti
Epitonium tollini
Erato
Erato columbella
Erato maugeriae
Erato vitillina
Eratoidae
Eratoidea
Erosaria
Ervilia
Ervilia concentrica
Ervilia rostratula
Erycina fernandina
Erycinidae
Eubranchus
Eubranchus exiguus
Eubranchus pallidus
Eucrassatella
Eucrassatella floridana
Eucrassatella gibbesi
Eucrassatella speciosa
Eudolium crosseanum
Eulamellibranchia
Eulimidae
Eulithidium
Eulithidium rubrilineatum
Eulithidium variegata
Eunaticina oldroydi
Eupleura
Eupleura caudata
Eupleura etterae
Eupleura stimpsoni
Eupleura sulcidentata
Euribia
Eurytellina
Euvola
Evalea
Evalina
Fartulum
Fasciolaria
Fasciolaria branhamae
Fasciolaria distans
Fasciolaria gigantea
Fasciolaria hunteria
Fasciolaria princeps
Fasciolaria tulipa
Fasciolariidae
Favartia
Ferminoscala
Ficidae
Ficus
Ficus carolae
Ficus communis
Ficus papyratia
Ficus reticulata
Filibranchia
Fissidentalium
Fissurella
Fissurella angusta
Fissurella barbadensis
Fissurella crucifera
Fissurella fascicularis
Fissurella nodosa
Fissurella rosea
Fissurella volcano
Fissurellidae
Fistulana Bruguiere
Flabellinidae
Forreria
Forreria belcheri
Forreria cerrosensis
Forreria cerrosensis catalinensis
Forreria cerrosensis cerrosensis
Forreria pinnata
Fossaridae
Fossarus elegans
Fraginae
Fugleria
Fulgur
Fulguropsis
Fusinus
Fusinus barbarensis
Fusinus couei
Fusinus depetitthouarsi
Fusinus dupetit-thouarsi
Fusinus eucosmius
Fusinus harfordi
Fusinus kobelti
Fusinus timessus
Fusitriton
Gadila
Galeodes
Gari californica
Gastrana
Gastrana irus
Gastrochaena
Gastropteridae
Gastropteron
Gastropteron cinereum
Gastropteron meckeli
Gastropteron pacificum
Gastropteron rubrum
Gaza
Gaza superba
Gaza watsoni
Gemma
Gemma fretensis
Gemma gemma
Gemma manhattensis
Gemma purpurea
Gemminae
Gemmula periscelida
Genota viabrunnea
Gibberula
Gibberulina
Gibberulina amianta
Gibberulina hadria
Gibberulina lacrimida
Gibberulina lacrimula
Gibberulina ovuliformis
Gibberulina pyriformis
Glans
Glaucidae
Glaucus
Glaucus atlanticus
Glaucus forsteri
Glaucus marina
Glaucus radiata
Glicymeris
Glossaulax
Glossodoris
Glossodoris californiensis
Glossodoris iniversitatis
Glossodoris macfarlandi
Glossodoris porterae
Glossodoris universitatis
Glycimeris
Glycymeridae
Glycymeris
Glycymeris americana
Glycymeris decussata
Glycymeris lineata
Glycymeris pectinata
Glycymeris pennacea
Glycymeris spectralis
Glycymeris subobsoleta
Glycymeris undata
Glyphostoma gabbi
Gobraeus
Gonyaulax catanella
Gouldia cerina
Granula
Graptacme
Gryphaea
Gutturnium
Gymnobela blakeana
Gymnosomata
Gyroscala
Haliotidae
Haliotis
Haliotis assimilis
Haliotis aulaea
Haliotis bonita
Haliotis californiensis
Haliotis corrugata
Haliotis cracherodi
Haliotis diegoensis
Haliotis fulgens
Haliotis holzneri
Haliotis imperforata
Haliotis kamtschatkana
Haliotis lusus
Haliotis pourtalesi
Haliotis revea
Haliotis rufescens
Haliotis smithsoni
Haliotis sorenseni
Haliotis splendens
Haliotis splendidula
Haliotis turveri
Haliotis walallensis
Haliotis wallallensis
Haliris
Haloconcha
Haloconcha reflexa
Halopsyche
Haminoea
Haminoea antillarum
Haminoea cymbiformis
Haminoea elegans
Haminoea glabra
Haminoea olgae
Haminoea solitaria
Haminoea succinea
Haminoea vesicula
Haminoea virescens
Here
Herse
Herse cancellata
Herse columnella
Herse oryza
Herse urceolaris
Hespererato
Heterodonax
Heterodonax bimaculata
Heterodonax pacifica
Heteroteuthis tenera
Hexaplex
Hiatella
Hiatella arctica
Hiatella gallicana
Hiatella pholadis
Hiatella rugosa
Hiatella striata
Hinia
Hinnites
Hinnites giganteus
Hinnites multirugosus
Hipponicidae
Hipponix
Hipponix antiquatus
Hipponix barbatus
Hipponix benthophila
Hipponix cranoides
Hipponix serratus
Hipponix subrufus subrufus
Hipponix subrufus tumens
Homalopoma
Homalopoma albida
Homalopoma bacula
Homalopoma carpenteri
Homalopoma linnei
Homalopoma lurida
Hopkinsia rosacea
Hormomya
Humilaria kennerleyi
Hyalaea
Hyalaea affinis
Hyalaea angulata
Hyalaea coniformis
Hyalaea limbata
Hyalina
Hyalina avena
Hyalina avenacea
Hyalina avenella
Hyalina beyerleana
Hyalina californica
Hyalina succinea
Hyalina torticula
Hyalina veliei
Hyalocylis striata
Hydatina
Hydatina physis
Hydatina vesicaria
Hydatinidae
Hysteroconcha
Idioraphe
Illex illecebrosus
Ilyanassa
Inodrillara
Inodrillia aepynota
Iolaea
Iphigenia brasiliensis
Irus lamellifera
Ischadium
Ischnochiton
Ischnochiton acrior
Ischnochiton albus
Ischnochiton californiensis
Ischnochiton clathratus
Ischnochiton conspicuus
Ischnochiton cooperi
Ischnochiton floridanus
Ischnochiton magdalenensis
Ischnochiton mertensi
Ischnochiton palmulatus
Ischnochiton papillosus
Ischnochiton purpurascens
Ischnochiton regularis
Ischnochiton ruber
Ischnochitoniidae
Isognomon
Isognomon alata
Isognomon bicolor
Isognomon chemnitziana
Isognomon listeri
Isognomon radiata
Isognomonidae
Ivara
Ividella
Janacus
Janthina
Janthina bifida
Janthina exigua
Janthina fragilis
Janthina globosa
Janthina janthina
Janthinidae
Jumala
Jumala crebricostata
Jumala kennicotti
Katharina tunicata
Kelletia kelletia
Kellia laperousi
Kelliidae
Kennerlia
Krebsia
Kurtziella limonitella
Labiosa
Labiosa campechensis
Labiosa canaliculata
Labiosa lineata
Labiosa plicatella
Lacuna
Lacuna carinata
Lacuna divaricata
Lacuna porrecta
Lacuna solidula
Lacuna striata
Lacuna unifasciata
Lacuna variegata
Lacuna vincta
Lacunidae
Laevicardium
Laevicardium elatum
Laevicardium laevigatum
Laevicardium mortoni
Laevicardium pictum
Laevicardium serratum
Laevicardium substriatum
Laevicardium sybariticum
Laila cockerelli
Lamellaria
Lamellaria diegoensis
Lamellaria rhombica
Lamellariidae
Lamellibranchia
Lampusia
Larkinia
Lasaea
Lasaea cistula
Lasaea subviridis
Laskeya
Latiaxis
Latirus
Latirus brevicaudatus
Latirus infundibulum
Latirus mcgintyi
Leda
Ledella
Leiomya
Lepeta caeca
Lepetidae
Lepidochitona
Lepidochitona dentiens
Lepidochitona hartwegi
Lepidochitona keepiana
Lepidopleuridae
Lepidopleuroides
Lepidopleurus cancellatus
Lepidozona
Leptegouana
Leptonidae
Leptothyra
Leucozonia
Leucozonia cingidifera
Leucozonia cingulifera
Leucozonia nassa
Leucozonia ocellata
Levia
Lima
Lima antillensis
Lima caribaea
Lima dehiscens
Lima hemphilli
Lima hians
Lima inflata
Lima lima
Lima multicostata
Lima orientalis
Lima pellucida
Lima scabra
Lima squamosa
Lima tenera
Lima terica
Lima tetrica
Limacina
Limacina balea
Limacina scaphoidea
Limea bronniana
Limidae
Limopsidae
Limopsis
Limopsis antillensis
Limopsis cristata
Limopsis diegensis
Limopsis minuta
Limopsis sulcata
Linga
Lioberus castaneus
Liophora
Liotia
Liotia bairdi
Liotia cookeana
Liotia fenestrata
Lischkeia
Lischkeia bairdi
Lischkeia cidaris
Lischkeia ottoi
Lischkeia regalis
Lithophaga
Lithophaga antillarum
Lithophaga aristata
Lithophaga bisulcata
Lithophaga nigra
Lithophaga plumula
Lithophaga plumula kelseyi
Lithopoma
Litiopa
Litiopa bombix
Litiopa bombyx
Litiopa melanostoma
Littorina
Littorina angulifera
Littorina groenlandica
Littorina irrorata
Littorina littorea
Littorina meleagris
Littorina mespillum
Littorina obtusata
Littorina palliata
Littorina planaxis
Littorina rudis
Littorina saxatilis
Littorina scabra
Littorina scutulata
Littorina sitkana
Littorina ziczac
Livona
Livona pica
Loligo
Loligo opalescens
Loligo pealei
Lolliguncula
Lolliguncula brevipinna
Lolliguncula brevis
Lolliguncula hemiptera
Lonchaeus
Lottia gigantea
Lucapina
Lucapina adspersa
Lucapina cancellata
Lucapina sowerbii
Lucapina suffusa
Lucapinella
Lucapinella callomarginata
Lucapinella limatula
Lucina
Lucina amiantus
Lucina approximata
Lucina chrysostoma
Lucina crenella
Lucina floridana
Lucina jamaicensis
Lucina leucocyma
Lucina multilineata
Lucina pensylvanica
Lucina sombrerensis
Lucina tenuisculpta
Lucinidae
Lucinisca
Lucinoma
Lunarca
Lunatia
Lunatia groenlandica
Lunatia heros
Lunatia lewisi
Lunatia pallida
Lunatia triseriata
Luria
Lyonsia
Lyonsia arenosa
Lyonsia californica
Lyonsia floridana
Lyonsia hyalina
Lyropecten
Lyropecten antillarum
Lyropecten nodosus
Machaeroplax
Macoma
Macoma balthica
Macoma brota
Macoma calcarea
Macoma carlottensis
Macoma constricta
Macoma incongrua
Macoma indentata
Macoma inflatula
Macoma inquinata
Macoma irus
Macoma limula
Macoma mitchelii
Macoma mitchelli
Macoma nasuta
Macoma planiuscula
Macoma secta
Macoma souleyetiana
Macoma tenta
Macoma tenuirostris
Macoma yoldiformis
Macrocallista
Macrocallista maculata
Macrocallista nimbosa
Macron lividus
Mactra
Mactra californica
Mactra fragilis
Mactra nasuta
Mactridae
Magilidae
Malletia
Malletiidae
Mancinella
Mangelia morra
Mangeria
Mangilia
Mantellum
Margarites
Margarites cinereus
Margarites costalis
Margarites groenlandica
Margarites groenlandicus
Margarites lirulatus
Margarites obsoletus
Margarites parcipictus
Margarites pupillus
Margarites succinctus
Margarites umbilicalis
Margaritifera
Marginella
Marginella aureocincta
Marginella borealis
Marginella denticulata
Marginella eburneola
Marginella haematita
Marginella jaspidea
Marginella philtata
Martesia
Martesia cuneiformis
Martesia smithi
Martesia striata
Massyla
Maxwellia
Megatebennus bimaculatus
Megathura crenulata
Megayoldia
Meioceras
Melanella
Melanella bilineata
Melanella gibba
Melanella gracilis
Melongena
Melongena altispira
Melongena bispinosa
Melongena corona
Melongena corona perspinosa
Melongena estephomenos
Melongena inspinata
Melongena martiniana
Melongena melongena
Melongena minor
Melongena subcoronata
Melongenidae
Menestho
Mercenaria
Mercenaria campechiensis
Mercenaria mercenaria
Mercenaria notata
Mercenaria texana
Meretricinae
Mesodesma arctatum
Mesopleura
Metaplysia
Micranellum
Microcardium
Microcardium peramabile
Microcardium tinctum
Microgaza
Microgaza inornata
Microgaza rotella
Micromelo undata
Milneria kelseyi
Miralda
Mitra
Mitra albocincta
Mitra barbadensis
Mitra fergusoni
Mitra florida
Mitra hendersoni
Mitra idae
Mitra nodulosa
Mitra styria
Mitra sulcata
Mitra swainsoni antillensis
Mitrella
Mitrella lunata
Mitrella raveneli
Mitrella tuberosa
Mitrella variegata
Mitridae
Mitromorpha
Mitromorpha aspera
Mitromorpha filosa
Modiolaria
Modiolus
Modiolus tulipa
Modulidae
Modulus
Modulus carchedonius
Modulus modulus
Moerella
Monilispira
Monilispira albinodata
Monilispira albomaculata
Monilispira leucocyma
Monostiolum
Mopalia
Mopalia acuta
Mopalia ciliata
Mopalia fissa
Mopalia hindsi
Mopalia lignosa
Mopalia muscosa
Mopalia plumosa
Mopalia wosnessenski
Mopaliidae
Mormula
Morula
Morum oniscus
Murex
Murex alba
Murex anniae
Murex arenarius
Murex beaui
Murex bequaerti
Murex bicolor
Murex brandaris
Murex brevifrons
Murex burryi
Murex cabriti
Murex carpenteri
Murex cellulosus
Murex citrinus
Murex delicatus
Murex erinaceoides rhyssus
Murex festivus
Murex florifer
Murex fulvescens
Murex gemma
Murex hidalgoi
Murex macropterus
Murex messorius
Murex petri
Murex pomum
Murex recurvirostris
Murex recurvirostris rubidus
Murex recurvirostris sallasi
Murex rufus
Murex tremperi
Murex trialatus
Murex trunculus
Murex tryoni
Murexiella
Muricanthus
Muricidae
Muricidea
Muricopsis
Muricopsis floridana
Muricopsis hexagona
Muricopsis ostrearum
Musculus
Musculus discors
Musculus laevigatus
Musculus lateralis
Musculus niger
Mya
Mya arenaria
Mya japonica
Mya truncata
Myacea
Myoforceps
Mysella
Mysella golischi
Mysella pedroana
Mysella planulata
Mysella tumida
Mytilimeria nuttalli
Mytilopsis
Mytilus
Mytilus californianus
Mytilus edulis
Mytilus edulis diegensis
Mytilus hamatus
Mytilus plicatulus
Naranio
Narona cooperi
Nassariidae
Nassarius
Nassarius acutus
Nassarius ambiguus
Nassarius californianus
Nassarius consensus
Nassarius cooperi
Nassarius fossatus
Nassarius insculptus
Nassarius mendicus
Nassarius obsoletus
Nassarius perpinguis
Nassarius tegulus
Nassarius trivittatus
Nassarius vibex
Natica
Natica canrena
Natica clausa
Natica livida
Natica pusilla
Naticarius
Naticidae
Nautilus pompilius
Navea subglobosa
Navicula ostrearia
Neilonella
Nemocardium centifilosum
Neosimnia
Neosimnia acicularis
Neosimnia aequalis
Neosimnia avena
Neosimnia barbarensis
Neosimnia catalinensis
Neosimnia inflexa
Neosimnia loebbeckeana
Neosimnia piragua
Neosimnia similis
Neosimnia uniplicata
Neosimnia variabilis
Neptunea
Neptunea bicincta
Neptunea californica
Neptunea decemcostata
Neptunea eucosmia
Neptunea lirata
Neptunea lyrata
Neptunea pribiloffensis
Neptunea satura
Neptunea tabulata
Neptunea ventricosa
Nerita
Nerita fulgurans
Nerita peloronta
Nerita tessellata
Nerita variegata
Nerita versicolor
Neritidae
Neritina
Neritina floridana
Neritina reclivata
Neritina rotundata
Neritina sphaera
Neritina virginea
Neritina weyssei
Nesta
Nettastomella rostrata
Neverita
Nitidella
Nitidella carinata
Nitidella cribraria
Nitidella gausapata
Nitidella gouldi
Nitidella nitidula
Nitidella ocellata
Nodilittorina tuberculata
Nodipecten
Nodulus
Noetia
Noetia ponderosa
Noetia reversa
Norrisia norrisi
Notarchus
Notobranchaea
Nucella lapillus
Nucula
Nucula atacellana
Nucula cancellata
Nucula crenulata
Nucula delphinodonta
Nucula exigua
Nucula proxima
Nucula reticulata
Nucula tenuis
Nuculana
Nuculana carpenteri
Nuculana concentrica
Nuculana conceptionis
Nuculana curtulosa
Nuculana fossa
Nuculana hamata
Nuculana hindsi
Nuculana messanensis
Nuculana minuta
Nuculana penderi
Nuculana pernula
Nuculana redondoensis
Nuculana sculpta
Nuculana taphria
Nuculana tenuisulcata
Nuculana vaginata
Nuculanidae
Nuculidae
Nudibranchia
Nuttallia
Nuttallina
Nuttallina californica
Nuttallina flexa
Nuttallina scabra
Ocenebra
Ocenebra atropurpurea
Ocenebra circumtexta
Ocenebra citrica
Ocenebra clathrata
Ocenebra gracillima
Ocenebra interfossa
Ocenebra lurida
Ocenebra poulsoni
Ocenebra stearnsi
Ocenebra tenuisculpta
Ocinebra
Octopoda
Octopus
Octopus americanus
Octopus bimaculatus
Octopus bimaculoides
Octopus briareus
Octopus burryi
Octopus carolinensis
Octopus hongkongensis
Octopus joubini
Octopus macropus
Octopus punctatus
Octopus rugosus
Octopus vulgaris
Odostomia
Odostomia aepynota
Odostomia americana
Odostomia amianta
Odostomia bisuturalis
Odostomia donilla
Odostomia farella
Odostomia fetella
Odostomia gibbosa
Odostomia helga
Odostomia hendersoni
Odostomia impressa
Odostomia laxa
Odostomia modesta
Odostomia nota
Odostomia pedroana
Odostomia phanea
Odostomia seminuda
Odostomia terricula
Odostomia trifida
Odostomia willisi
Okeniidae
Oliva
Oliva litterata
Oliva reticularis
Oliva sayana
Olivella
Olivella baetica
Olivella bayeri
Olivella biplicata
Olivella floralia
Olivella intorta
Olivella jaspidea
Olivella moorei
Olivella mutica
Olivella nivea
Olivella pedroana
Olivella porteri
Olivella pycna
Olividae
Ommastrephidae
Onchidella
Onchidella borealis
Onchidella carpenteri
Onchidella floridana
Onchidiata
Onchidiidae
Onchidoridae
Onoba
Opalia
Opalia chacei
Opalia crenata
Opalia crenimarginata
Opalia hotessieriana
Opalia insculpta
Opalia wroblewskii
Opisthobranchia
Ostrea
Ostrea conchaphila
Ostrea cristata
Ostrea edulis
Ostrea equestris
Ostrea expansa
Ostrea folium
Ostrea frons
Ostrea limacella
Ostrea lurida
Ostrea permollis
Ostrea rubella
Ostrea rufoides
Ostrea spreta
Ostrea thomasi
Ostreidae
Oudardia
Ovulidae
Oxygyrus keraudreni
Pachydesma
Pachypoma
Paedoclione
Paleoconcha
Pandora
Pandora arenosa
Pandora bilirata
Pandora bushiana
Pandora carolinensis
Pandora filosa
Pandora gouldiana
Pandora granulata
Pandora trilineata
Panomya
Panomya ampla
Panomya arctica
Panope
Panope bitruncata
Panope generosa
Panope globosa
Panope solida
Panope taeniata
Papyridea
Papyridea hiatus
Papyridea semisulcata
Papyridea soleniformis
Parapholas californica
Parastarte triquetra
Paroctopus
Parvilucina
Patinopecten
Pecten
Pecten caurinus
Pecten diegensis
Pecten jacobaeus
Pecten laurenti
Pecten papyraceus
Pecten raveneli
Pecten tereinus
Pecten tryoni
Pecten ziczac
Pectinidae
Pedalion
Pedicularia
Pedicularia californica
Pedicularia decussata
Pedicularia ovuliformis
Pediculariella
Pelecypoda
Penitella
Penitella penita
Penitella sagitta
Peracle
Peracle bispinosa
Peracle clathrata
Peracle physoides
Peracle reticulata
Peraclidae
Peraclis
Periploma
Periploma discus
Periploma fragile
Periploma inaequivalvis
Periploma inequale
Periploma leanum
Periploma papyraceum
Periploma papyratium
Periploma planiusculum
Perna
Peronidia
Perotrochus
Perotrochus adansonianus
Perotrochus quoyanus
Persicula
Persicula catenata
Persicula jewetti
Persicula lavalleana
Persicula lavelleana
Persicula minuta
Persicula politula
Persicula regularis
Persicula subtrigona
Petaloconchus
Petaloconchus erectus
Petaloconchus irregularis
Petaloconchus nigricans
Petrasma
Petricola
Petricola lapicida
Petricola pholadiformis
Petricolaria
Phacoides
Phacoides acutilineatus
Phacoides annulatus
Phacoides centrifuga
Phacoides filosus
Phacoides jamaicensis
Phacoides nassula
Phacoides nuttalli
Phacoides pectinatus
Phalium
Phalium abbreviata
Phalium centiquadrata
Phalium centriquadrata
Phalium cicatricosum
Phalium glaucum
Phalium granulatum
Phalium inflatum
Phalium peristephes
Phasianellidae
Philine
Philine lima
Philine lineolata
Philine quadrata
Philine sagra
Philinidae
Pholadidae
Pholadidea ovoidea
Pholas campechiensis
Phyctiderma
Phylloda squamifera
Phyllodina
Phyllonotus
Physa
Pinctada radiata
Pinna
Pinna carnea
Pinna haudignobilis
Pinna rudis
Pinnidae
Pisania pusio
Pitar
Pitar albida
Pitar cordata
Pitar dione
Pitar fulminata
Pitar lupinaria
Pitar morrhuana
Pitar simpsoni
Pitarenus
Placiphorella velata
Placopecten
Placopecten grandis
Placopecten magellanicus
Plagioctenium
Planaxidae
Planaxis
Planaxis lineatus
Planaxis nucleus
Platyodon cancellatus
Pleurobranchidae
Pleurobranchus
Pleurobranchus atlanticus
Pleurobranchus gardineri
Pleurolucina
Pleuromeris
Pleuroploca
Pleuroploca gigantea
Pleuroploca papillosa
Pleuroploca princeps
Pleuroploca reevei
Pleurotomariidae
Plicatula gibbosa
Plicatulidae
Plumulella
Pneumoderma
Pneumodermopsis
Pneumonoderma
Pododesmus
Pododesmus cepio
Pododesmus decipiens
Pododesmus macroschisma
Pododesmus rudis
Polinices
Polinices alatus
Polinices altus
Polinices brunneus
Polinices draconis
Polinices duplicatus
Polinices immaculatus
Polinices imperforatus
Polinices lacteus
Polinices reclusianus
Polinices uberinus
Pollia
Polycera
Polycera atra
Polycera hummi
Polyceridae
Polymesoda
Polymesoda caroliniana
Polyschides
Polystira
Polystira albida
Polystira tellea
Polystira virgo
Polytropa
Pomaulax
Poromya granulata
Poromya rostrata
Potamididae
Primovula carnea
Promartynia
Propeamussiidae
Propeamussium
Propeamussium pourtalesianum
Protobranchia
Protocardiinae
Protonucula
Protothaca
Protothaca grata
Protothaca laciniata
Protothaca ruderata
Protothaca staminea
Protothaca tenerrima
Prunum
Prunum amabile
Prunum apicinum
Prunum bellum
Prunum borealis
Prunum carneum
Prunum guttatum
Prunum labiatum
Prunum limatulum
Prunum roosevelti
Prunum virginianum
Psammobia
Psammocola
Psammosolen
Psephidia
Psephidia lordi
Psephidia ovalis
Pseudochama
Pseudochama echinata
Pseudochama exogyra
Pseudochama ferruginea
Pseudochama granti
Pseudochama radians
Pseudocyrena floridana
Pseudomalaxis
Pseudomalaxis balesi
Pseudomalaxis nobilis
Pseudomiltha
Pseudoneptunea multangula
Pseudopythina
Pseudopythina compressa
Pseudopythina rugifera
Pteria
Pteria colymbus
Pteria sterna
Pteriidae
Pteropoda
Pteropurpura
Pterorytis
Pterorytis foliata
Pterorytis nuttalli
Pterynotus
Pulmonata
Puncturella
Puncturella cucullata
Puncturella galeata
Puncturella noachina
Pupillaria
Purpura
Purpura crispata
Purpura foliatum
Purpura pansa
Purpura patula
Pusula
Pycnodonta hyotis
Pyramidella
Pyramidella adamsi
Pyramidella dolabrata
Pyramidella fusca
Pyramidellidae
Pyrenidae
Pyrgiscus
Pyrgolampros
Pyrula papyratia
Pyrulofusus
Pyrunculus caelatus
Quadrans lintea
Raeta
Raeta campechensis
Raeta canaliculata
Ranella
Rangia
Rangia cuneata
Rangia flexuosa
Rangia nasuta
Rangia rostrata
Rangianella
Rehderia
Retusa
Retusa canaliculata
Retusa candei
Retusa obtusa
Retusa pertenuis
Retusa sulcata
Retusa turrita
Retusidae
Rhizorus
Rhizorus acutus
Rhizorus aspinosus
Rhizorus bushi
Rhizorus minutus
Rhizorus oxytatus
Rimula frenulata
Ringicula
Ringicula nitida
Ringicula semistriata
Ringiculidae
Rissoidae
Rissoina
Rissoina bakeri
Rissoina browniana
Rissoina bryerea
Rissoina californica
Rissoina cancellata
Rissoina chesneli
Rissoina cleo
Rissoina coronadoensis
Rissoina dalli
Rissoina decussata
Rissoina kelseyi
Rissoina kelyseyi
Rissoina laevigata
Rissoina multicostata
Rissoina newcombei
Rissoina sagraiana
Rissoina striosa
Rocellaria
Rocellaria cuneiformis
Rocellaria hians
Rocellaria ovata
Rochfortia
Rossia
Rossia equalis
Rossia pacifica
Rossia tenera
Rostanga pulchra
Rubellatoma
Rubellatoma diomedea
Rubellatoma rubella
Ruditapes
Rupellaria
Rupellaria californica
Rupellaria californiensis
Rupellaria carditoides
Rupellaria denticulata
Rupellaria tellimyalis
Rupellaria typica
Saccella
Salasiella
Sanguinolaria
Sanguinolaria cruenta
Sanguinolaria nuttalli
Sanguinolaria sanguinolenta
Saxicava
Saxicava arctica
Saxidomus
Saxidomus giganteus
Saxidomus nuttalli
Scala
Scalaria borealis
Scalina
Scaphella
Scaphella butleri
Scaphella dohrni
Scaphella dubia
Scaphella florida
Scaphella georgiana
Scaphella johnstoneae
Scaphella junonia
Scaphella schmitti
Scaphopoda
Schizothaerus
Schizothaerus capax
Schizothaerus nuttalli
Schizotrochus
Scissula
Scissurella
Scissurella crispata
Scissurella proxima
Scissurellidae
Sconsia striata
Scrobiculina
Scyllaea pelagica
Scyllaeidae
Searlesia dira
Seila
Seila adamsi
Seila montereyensis
Seila terebralis
Semele
Semele bellastriata
Semele cancellata
Semele decisa
Semele proficua
Semele purpurascens
Semele radiata
Semele rubropicta
Semele rupicola
Semicassis
Semicassis abbreviata
Semicassis inflatum
Semirossia
Sepia
Sepiolidae
Sepioteuthis
Sepioteuthis sepioidea
Septibranchia
Septifer
Septifer bifurcatus
Septifer obsoletus
Serripes groenlandicus
Sigatica
Sigatica carolinensis
Sigatica holograpta
Sigatica semisulcata
Siliqua
Siliqua alta
Siliqua costata
Siliqua lucida
Siliqua media
Siliqua nuttalli
Siliqua patula
Siliqua squama
Siliquaria
Sinum
Sinum californicum
Sinum debile
Sinum maculatum
Sinum perspectivum
Sinum scopulosum
Siphonaria
Siphonaria alternata
Siphonaria lineolata
Siphonaria naufragum
Siphonaria pectinata
Siphonariidae
Siphonodentaliidae
Smaragdia
Smaragdia viridemaris
Smaragdia viridis
Smaragdia weyssei
Solariella
Solariella lacunella
Solariella lamellosa
Solariella obscura
Solariella peramabilis
Solariella regalis
Solariorbis
Solecurtus
Solecurtus cumingianus
Solecurtus sanctaemarthae
Solemya
Solemya borealis
Solemya occidentalis
Solemya valvulus
Solemya velum
Solemyidae
Solen
Solen rosaceus
Solen sicarius
Solen viridis
Solen vividis
Solenidae
Spengleria rostrata
Sphenia
Sphenia fragilis
Sphenia ovoidea
Spiratella
Spiratella balea
Spiratella bulimoides
Spiratella gouldi
Spiratella helicina
Spiratella inflata
Spiratella lesueuri
Spiratella pacifica
Spiratella retroversa
Spiratella scaphoidea
Spiratella trochiformis
Spiratellidae
Spiroglyphus
Spiroglyphus annulatus
Spiroglyphus lituellus
Spirula spirula
Spisula
Spisula alaskana
Spisula catilliformis
Spisula dolabriformis
Spisula falcata
Spisula hemphilli
Spisula planulata
Spisula polynyma
Spisula similis
Spisula solidissima
Spisula voyi
Spondylidae
Spondylus
Spondylus americanus
Spondylus dominicensis
Spondylus echinatus
Spondylus pictorum
Stenoplax
Sthenorytis
Sthenorytis cubana
Sthenorytis epae
Sthenorytis hendersoni
Sthenorytis pernobilis
Sthenoteuthis bartrami
Stramonita
Strigilla
Strigilla carnaria
Strigilla flexuosa
Strigilla mirabilis
Strigilla pisiformis
Strigilla rombergi
Strioturbonilla
Strombidae
Strombus
Strombus alatus
Strombus bituberculatus
Strombus canaliculatus
Strombus costatus
Strombus gallus
Strombus gigas
Strombus goliath
Strombus horridus
Strombus peculiaris
Strombus pugilis
Strombus raninus
Strombus sloani
Strombus spectabilis
Strombus verrilli
Stylidium
Styliferidae
Styliola
Styliola conica
Styliola subula
Styliola vitrea
Sulcosipho
Supplanaxis
Susania
Sycofulgur
Symmetrogephyrus
Symmetrogephyrus pallasi
Symmetrogephyrus vestitus
Syrnola
Tachyrhynchus
Tachyrhynchus erosum
Tachyrhynchus lacteolum
Tachyrhynchus reticulatum
Taenioturbo
Tagelus
Tagelus affinis
Tagelus californianus
Tagelus divisus
Tagelus gibbus
Tagelus plebeius
Tagelus politus
Tagelus subteres
Taglus politus
Tapes
Tapes bifurcata
Tapes philippinarum
Tapes semidecussata
Taras orbella
Taxodonta
Tectarius
Tectarius muricatus
Tectarius tuberculatus
Tectibranchia
Tectininus
Tegula
Tegula aureotincta
Tegula brunnea
Tegula excavata
Tegula fasciata
Tegula funebralis
Tegula gallina
Tegula hotessieriana
Tegula indusi
Tegula ligulata
Tegula lividomaculata
Tegula marcida
Tegula montereyi
Tegula regina
Tegula scalaris
Teinostoma
Teinostoma biscaynense
Teinostoma biscaynensis
Teinostoma clavium
Teinostoma cocolitoris
Teinostoma cryptospira
Teinostoma goniogyrus
Teinostoma leremum
Teinostoma litus-palmarum
Teinostoma lituspalmarum
Teinostoma nesaeum
Teinostoma obtectum
Teinostoma parvicallum
Teinostoma pilsbryi
Tellidora cristata
Tellina
Tellina agilis
Tellina alternata
Tellina angulosa
Tellina buttoni
Tellina candeana
Tellina carpenteri
Tellina decora
Tellina elucens
Tellina fausta
Tellina idae
Tellina interrupta
Tellina iris
Tellina laevigata
Tellina lineata
Tellina lutea
Tellina magna
Tellina mera
Tellina meropsis
Tellina modesta
Tellina polita
Tellina promera
Tellina punicea
Tellina radiata
Tellina salmonea
Tellina sayi
Tellina similis
Tellina sybaritica
Tellina tampaensis
Tellina tener
Tellina tenera
Tellina texana
Tellina venulosa
Tellina versicolor
Tellinella
Tenagodidae
Tenagodus
Tenagodus modestus
Tenagodus squamatus
Terebra
Terebra cinerea
Terebra concava
Terebra dislocata
Terebra feldmanni
Terebra flammea
Terebra floridana
Terebra hastata
Terebra limatula
Terebra lutescens
Terebra pedroana
Terebra protexta
Terebra salleana
Terebra taurinum
Terebridae
Teredinidae
Teredo
Teredo bartschi
Teredo diegensis
Teredo navalis
Teredo townsendi
Tergipedidae
Tergipes despectus
Tethys
Tetrabranchia
Thais
Thais canaliculata
Thais crispata
Thais deltoidea
Thais emarginata
Thais haemastoma
Thais haemastoma floridana
Thais haemastoma haysae
Thais imbricatus
Thais lamellosa
Thais lapillus
Thais lima
Thais rustica
Thais undata
Thecosomata
Thericium
Thestyleda
Thracia
Thracia conradi
Thracia curta
Thracia trapezoides
Thyasira
Thyasira bisecta
Thyasira disjuncta
Thyasira gouldi
Thyasira trisinuata
Timoclea
Tindaria
Tindaria brunnea
Tivela
Tivela crassatelloides
Tivela floridana
Tivela stultorum
Tonicella
Tonicella lineata
Tonicella marmorea
Tonicia schrammi
Tonna
Tonna (Dolium) album
Tonna album
Tonna brasiliana
Tonna galea
Tonna maculosa
Tonna perdix
Tonnidae
Torcula
Torinia
Torinia bisulcata
Torinia cylindrica
Trachycardium
Trachycardium egmontianum
Trachycardium isocardia
Trachycardium magnum
Trachycardium muricatum
Trachycardium quadragenarium
Transennella
Transennella conradina
Transennella stimpsoni
Transennella tantilla
Trapeziidae
Tremoctopus violaceus
Trichotropidae
Trichotropis
Trichotropis bicarinata
Trichotropis borealis
Trichotropis cancellata
Trichotropis insignis
Tricolia
Tricolia affinis
Tricolia compta
Tricolia concinna
Tricolia pulchella
Tricolia tessellata
Tricolia variegata
Trigoniocardia
Trigoniocardia biangulata
Trigoniocardia medium
Trigonostoma
Trigonostoma rugosum
Trigonostoma tenerum
Trigonulina
Triopha
Triopha carpenteri
Triopha grandis
Triopha maculata
Triphora
Triphora decorata
Triphora nigrocincta
Triphora ornatus
Triphora pedroana
Triphora perversa
Triphora pulchella
Triphoridae
Tritonalia
Tritoniscus
Tritonocauda
Trivia
Trivia antillarum
Trivia armandina
Trivia californiana
Trivia candidula
Trivia globosa
Trivia leucosphaera
Trivia maltbiana
Trivia nivea
Trivia nix
Trivia pediculus
Trivia pullata
Trivia quadripunctata
Trivia radians
Trivia ritteri
Trivia sanguinea
Trivia solandri
Trivia subrostrata
Trivia suffusa
Trochidae
Trochita radians
Trona
Trophon tenuisculptus
Trophonopsis
Trophonopsis lasius
Trophonopsis tenuisculptus
Truncacila
Turbinella scolyma
Turbinidae
Turbo
Turbo canaliculatus
Turbo castaneus
Turbo crenulatus
Turbo spenglerianus
Turbonilla
Turbonilla acra
Turbonilla aragoni
Turbonilla buttoni
Turbonilla chocolata
Turbonilla interrupta
Turbonilla kelseyi
Turbonilla laminata
Turbonilla nivea
Turbonilla stricta
Turbonilla tridentata
Turcicula
Turridae
Turritella
Turritella acropora
Turritella cooperi
Turritella exoleta
Turritella mariana
Turritella variegata
Turritellidae
Turtonia minuta
Tutufa
Urosalpinx
Urosalpinx cinerea
Urosalpinx follyensis
Urosalpinx perrugata
Urosalpinx tampaensis
Vanikoro oxychone
Vanikoroidae
Varicorbula
Varicorbula disparilis
Varicorbula operculata
Vasum
Vasum coestus
Vasum muricatum
Velutina
Velutina laevigata
Velutina undata
Velutina zonata
Venericardia
Venericardia borealis
Venericardia flabella
Venericardia novangliae
Venericardia perplana
Venericardia redondoensis
Venericardia stearnsi
Venericardia tridentata
Venericardia ventricosa
Veneridae
Venus
Vermetidae
Vermicularia
Vermicularia fargoi
Vermicularia knorri
Vermicularia spirata
Verticordia
Verticordia fischeriana
Verticordia fisheriana
Verticordia ornata
Vesica
Vitrinella
Vitrinella beaui
Vitrinella helicoidea
Vitrinella multistriata
Vitta
Volsella
Volsella americana
Volsella capax
Volsella demissa
Volsella demissa granosissima
Volsella fornicata
Volsella modiolus
Volsella plicatula
Volsella tulipa
Voluta
Voluta musica
Voluta virescens
Volutharpa ampullacea
Volutidae
Volutopsius
Volutopsius castaneus
Volutopsius harpa
Volvarina
Volvula
Volvulella
Xancidae
Xancus
Xancus angulatus
Xancus scolyma
Xenophora
Xenophora caribaeum
Xenophora conchyliophora
Xenophora longleyi
Xenophora radians
Xenophora trochiformis
Xenophoridae
Xylophaga
Xylophaga dorsalis
Xylophaga washingtona
Yoldia
Yoldia limatula
Yoldia limatula gardneri
Yoldia myalis
Yoldia sapotilla
Yoldia thraciaeformis
Zaphon
Zeidora
Zirfaea
Zirfaea crispata
Zirfaea gabbi
Zirfaea pilsbryi
Zonaria

>>> my_set = set.add(names_list)

Traceback (most recent call last):
  File "<pyshell#159>", line 1, in <module>
    my_set = set.add(names_list)
TypeError: descriptor 'add' requires a 'set' object but received a 'str'
>>> names_list = open("/Users/anna/work/texts/shell_index/clean_index/1/clean_index-uniq-ok1.txt", "r")
>>> my_set = set(names_list)
>>> my_set
set(['Volsella demissa\n', 'Solenidae\n', 'Trophonopsis lasius\n', 'Tachyrhynchus reticulatum\n', 'Glaucus marina\n', 'Cancellaria reticulata\n', 'Eucrassatella speciosa\n', 'Teinostoma lituspalmarum\n', 'Architeuthis harveyi\n', 'Pteriidae\n', 'Cyrtodaria kurriana\n', 'Solemya borealis\n', 'Diodora listeri\n', 'Perotrochus adansonianus\n', 'Codakia orbicularis\n', 'Persicula\n', 'Turbonilla\n', 'Glaucus atlanticus\n', 'Boreotrophon dalli\n', 'Siphonaria alternata\n', 'Phalium granulatum\n', 'Turbonilla chocolata\n', 'Rissoina multicostata\n', 'Ctena\n', 'Okeniidae\n', 'Dispotaea\n', 'Macoma mitchelli\n', 'Mitromorpha filosa\n', 'Cumingia coarctata\n', 'Cymatium femorale\n', 'Periploma inequale\n', 'Rissoina browniana\n', 'Periploma\n', 'Venericardia\n', 'Primovula carnea\n', 'Rostanga pulchra\n', 'Chione cancellata\n', 'Octopus joubini\n', 'Murex brevifrons\n', 'Diaphana debilis\n', 'Chione intapurpurea\n', 'Modulus carchedonius\n', 'Semele bellastriata\n', 'Nassarius mendicus\n', 'Mopalia plumosa\n', 'Glossodoris californiensis\n', 'Siphonaria pectinata\n', 'Callogaza\n', 'Periploma discus\n', 'Prunum labiatum\n', 'Leda\n', 'Solariorbis\n', 'Laevicardium substriatum\n', 'Bartschella\n', 'Cyphoma mcgintyi\n', 'Astraea tuber\n', 'Murex alba\n', 'Tegula hotessieriana\n', 'Corbula dietziana\n', 'Cerithium literatum\n', 'Caecum dalli\n', 'Cunearca\n', 'Ostrea\n', 'Lucina chrysostoma\n', 'Rupellaria californiensis\n', 'Cavolina uncinata\n', 'Calliostoma pulchrum\n', 'Calyptraea fastigiata\n', 'Pseudopythina\n', 'Quadrans lintea\n', 'Pseudochama\n', 'Lischkeia regalis\n', 'Lithophaga aristata\n', 'Panope\n', 'Pecten jacobaeus\n', 'Neosimnia avena\n', 'Fissurella angusta\n', 'Siliqua costata\n', 'Ostrea limacella\n', 'Odostomia donilla\n', 'Busycotypus\n', 'Cumingia\n', 'Sigatica carolinensis\n', 'Dosina\n', 'Murex delicatus\n', 'Ferminoscala\n', 'Acteon punctocaelatus\n', 'Peraclis\n', 'Natica livida\n', 'Nuculana\n', 'Buccinum plectrum\n', 'Asaphis deflorata\n', 'Doridae\n', 'Murex bicolor\n', 'Strombus gigas\n', 'Clione\n', 'Anadara baughmani\n', 'Murex bequaerti\n', 'Polinices alatus\n', 'Amphissa bicolor\n', 'Cingula\n', 'Turritella mariana\n', 'Cyathodonta dubiosa\n', 'Torinia bisulcata\n', 'Ocenebra clathrata\n', 'Argonauta hians\n', 'Murex beaui\n', 'Parvilucina\n', 'Mitra albocincta\n', 'Cancellaria\n', 'Cardium corbis\n', 'Acanthochitona spiculosus\n', 'Buccinum tenue\n', 'Amphineura\n', 'Cypraea cinerea\n', 'Eupleura caudata\n', 'Tonna brasiliana\n', 'Trivia sanguinea\n', 'Tellina interrupta\n', 'Anadara grandis\n', 'Pyramidellidae\n', 'Pholadidea ovoidea\n', 'Spiratella bulimoides\n', 'Modiolus\n', 'Zirfaea\n', 'Bankia\n', 'Aequipecten glyptus\n', 'Arene vanhyningi\n', 'Thais deltoidea\n', 'Truncacila\n', 'Ranella\n', 'Octopus carolinensis\n', 'Chione interpurpurea\n', 'Gastrana\n', 'Philine quadrata\n', 'Gaza\n', 'Semirossia\n', 'Mya\n', 'Magilidae\n', 'Olivella moorei\n', 'Capulus intortus\n', 'Amusium\n', 'Ancula sulphurea\n', 'Tegula scalaris\n', 'Cymatium labiosum\n', 'Haliotis rufescens\n', 'Verticordia fischeriana\n', 'Turbonilla laminata\n', 'Gonyaulax catanella\n', 'Diberus\n', 'Acmaea albicosta\n', 'Homalopoma lurida\n', 'Neosimnia similis\n', 'Lischkeia cidaris\n', 'Cantharus cancellaria\n', 'Cuspidaria granulata\n', 'Crassinella mactracea\n', 'Caecum californicum\n', 'Thracia curta\n', 'Anomalocardia brasiliana\n', 'Pandora filosa\n', 'Columbellidae\n', 'Acmaea pulcherrima\n', 'Littorina rudis\n', 'Anadara deshayesi\n', 'Phyctiderma\n', 'Terebra hastata\n', 'Strigilla mirabilis\n', 'Zirfaea pilsbryi\n', 'Rangia nasuta\n', 'Corbula\n', 'Conus californicus\n', 'Mytilus edulis diegensis\n', 'Pneumodermopsis\n', 'Vanikoroidae\n', 'Laevicardium sybariticum\n', 'Archidoris montereyensis\n', 'Pisania pusio\n', 'Buccinidae\n', 'Bittium montereyense\n', 'Saccella\n', 'Acmaea scabra\n', 'Odostomia pedroana\n', 'Micromelo undata\n', 'Nucula tenuis\n', 'Spiratellidae\n', 'Cardiidae\n', 'Terebra salleana\n', 'Haliotis splendidula\n', 'Ervilia rostratula\n', 'Propeamussium\n', 'Hysteroconcha\n', 'Conus aureofasciatus\n', 'Fasciolaria branhamae\n', 'Saxicava arctica\n', 'Chlamys hastatus\n', 'Symmetrogephyrus\n', 'Aeolidia papillosa\n', 'Ischnochiton californiensis\n', 'Teinostoma obtectum\n', 'Tagelus\n', 'Cypraea exanthema\n', 'Solemya velum\n', 'Bursa caelata\n', 'Timoclea\n', 'Donax\n', 'Rupellaria carditoides\n', 'Angulus tener\n', 'Creseis acicula\n', 'Philine\n', 'Colus stimpsoni\n', 'Loligo opalescens\n', 'Hipponix subrufus tumens\n', 'Glossodoris iniversitatis\n', 'Dentilucina\n', 'Aequipecten tryoni\n', 'Odostomia hendersoni\n', 'Lucina floridana\n', 'Murex burryi\n', 'Echinochama arcinella\n', 'Crassatellidae\n', 'Tritonalia\n', 'Gastrana irus\n', 'Venericardia novangliae\n', 'Pseudopythina rugifera\n', 'Tonna album\n', 'Neptunea eucosmia\n', 'Astarte castanea\n', 'Colus pubescens\n', 'Aequipecten borealis\n', 'Lamellaria\n', 'Busycon perversum\n', 'Neptunea pribiloffensis\n', 'Pinna rudis\n', 'Neritidae\n', 'Plagioctenium\n', 'Lucapina suffusa\n', 'Mopaliidae\n', 'Fusinus dupetit-thouarsi\n', 'Calliotropis\n', 'Sthenoteuthis bartrami\n', 'Chiton laevigatus\n', 'Triopha carpenteri\n', 'Odostomia amianta\n', 'Trichotropis cancellata\n', 'Ostrea frons\n', 'Macoma irus\n', 'Circomphalus\n', 'Thais haemastoma haysae\n', 'Latirus infundibulum\n', 'Trigoniocardia biangulata\n', 'Mitra sulcata\n', 'Glossodoris porterae\n', 'Botula falcata\n', 'Natica clausa\n', 'Gastropteridae\n', 'Conus floridensis\n', 'Chlamys mildredae\n', 'Hinnites giganteus\n', 'Ceratozona rugosa\n', 'Mitra styria\n', 'Amygdalum\n', 'Decapoda\n', 'Archidoris nobilis\n', 'Strombus sloani\n', 'Vanikoro oxychone\n', 'Lima orientalis\n', 'Architeuthis princeps\n', 'Cymatium martinianum\n', 'Architectonica peracuta\n', 'Herse urceolaris\n', 'Cymatium pileare\n', 'Modiolaria\n', 'Torinia cylindrica\n', 'Onchidella floridana\n', 'Melongena martiniana\n', 'Retusa pertenuis\n', 'Trivia suffusa\n', 'Herse cancellata\n', 'Leucozonia cingulifera\n', 'Macrocallista nimbosa\n', 'Haliotis californiensis\n', 'Odostomia aepynota\n', 'Ostrea conchaphila\n', 'Dendronotus\n', 'Mya truncata\n', 'Diaulula sandiegensis\n', 'Tellina decora\n', 'Strombus alatus\n', 'Diplodonta\n', 'Bullidae\n', 'Corbula barrattiana\n', 'Bankia gouldi\n', 'Protobranchia\n', 'Siliqua squama\n', 'Cerithidea scalariformis\n', 'Natica canrena\n', 'Pusula\n', 'Lepidochitona keepiana\n', 'Busycon spiratum\n', 'Cassis madagascariensis\n', 'Lepidochitona dentiens\n', 'Volvula\n', 'Pandora granulata\n', 'Thecosomata\n', 'Crenella glandula\n', 'Codakia orbiculata\n', 'Lyropecten antillarum\n', 'Glaucus radiata\n', 'Colus spitzbergensis\n', 'Hopkinsia rosacea\n', 'Glyphostoma gabbi\n', 'Tellinella\n', 'Propeamussiidae\n', 'Triphoridae\n', 'Spisula\n', 'Psephidia ovalis\n', 'Gibberulina hadria\n', 'Anachis avara\n', 'Ischnochiton palmulatus\n', 'Tellina carpenteri\n', 'Dentalium laqueatum\n', 'Colubrellina\n', 'Gemma fretensis\n', 'Thyasira trisinuata\n', 'Amiantis nobilis\n', 'Xenophora trochiformis\n', 'Cumingia vanhyningi\n', 'Chicoreus\n', 'Busycon pyrum\n', 'Gemma manhattensis\n', 'Yoldia sapotilla\n', 'Cymatium cynocephalum\n', 'Rimula frenulata\n', 'Bailya\n', 'Velutina\n', 'Laevicardium mortoni\n', 'Glycymeris americana\n', 'Chama macerophylla\n', 'Amphissa undata\n', 'Atlanta\n', 'Calliostoma variegatum\n', 'Glycymeris subobsoleta\n', 'Anadara lienosa floridana\n', 'Lolliguncula brevipinna\n', 'Chione undatella\n', 'Macoma yoldiformis\n', 'Caecum orcutti\n', 'Lischkeia bairdi\n', 'Amygdalum papyria\n', 'Bivalvia\n', 'Turcicula\n', 'Cyclostrema\n', 'Calliostoma\n', 'Nassarius insculptus\n', 'Amphissa\n', 'Cerithium\n', 'Pyramidella dolabrata\n', 'Acteocina candei\n', 'Glycimeris\n', 'Lima scabra\n', 'Divaricella\n', 'Rochfortia\n', 'Leucozonia\n', 'Septifer obsoletus\n', 'Haliotis corrugata\n', 'Muricidea\n', 'Solecurtus\n', 'Crucibulum striatum\n', 'Acmaea patina\n', 'Neritina rotundata\n', 'Pleuroploca reevei\n', 'Jumala kennicotti\n', 'Muricopsis ostrearum\n', 'Trigoniocardia medium\n', 'Astraea brevispina\n', 'Forreria cerrosensis catalinensis\n', 'Trichotropis\n', 'Chlamys hastatus hastatus\n', 'Protocardiinae\n', 'Cerithiopsis carpenteri\n', 'Xenophora longleyi\n', 'Hiatella gallicana\n', 'Caecum nebulosum\n', 'Muricidae\n', 'Lyonsia floridana\n', 'Corbiculiidae\n', 'Epitonium angulatum\n', 'Volutopsius\n', 'Teinostoma biscaynensis\n', 'Arca occidentalis\n', 'Protothaca tenerrima\n', 'Mytilus edulis\n', 'Velutina laevigata\n', 'Calliostoma doliarium\n', 'Nerita fulgurans\n', 'Solariella peramabilis\n', 'Dentalium cestum\n', 'Rocellaria hians\n', 'Conus mus\n', 'Erycina fernandina\n', 'Lithophaga\n', 'Vitrinella helicoidea\n', 'Bankia caribbea\n', 'Aequipecten lineolaris\n', 'Haminoea olgae\n', 'Arene\n', 'Columbella mercatoria\n', 'Trivia radians\n', 'Melongena\n', 'Ledella\n', 'Spisula alaskana\n', 'Conus sozoni\n', 'Marginella\n', 'Adula\n', 'Lacuna porrecta\n', 'Conus citrinus\n', 'Dentalium megathyris Dall\n', 'Capulidae\n', 'Hydatina vesicaria\n', 'Barnea spathulata\n', 'Petaloconchus nigricans\n', 'Argobuccinum oregonense\n', 'Scaphella junonia\n', 'Bursa louisa\n', 'Xylophaga dorsalis\n', 'Murex arenarius\n', 'Clio falcata\n', 'Haliotidae\n', 'Ensis californicus\n', 'Gibberulina lacrimula\n', 'Rossia equalis\n', 'Haminoea cymbiformis\n', 'Conus mazei\n', 'Venericardia borealis\n', 'Venus\n', 'Thais canaliculata\n', 'Volsella tulipa\n', 'Echinochama californica\n', 'Fissurellidae\n', 'Labiosa\n', 'Sigatica\n', 'Margarites succinctus\n', 'Acmaea paleacea\n', 'Tellina\n', 'Nucula\n', 'Leptonidae\n', 'Colus ventricosus\n', 'Dentalium\n', 'Epitonium pretiosum\n', 'Lithophaga plumula\n', 'Siliqua alta\n', 'Gouldia cerina\n', 'Cyanoplax\n', 'Pleurobranchus gardineri\n', 'Limidae\n', 'Coralliophaga coralliophaga\n', 'Humilaria kennerleyi\n', 'Zirfaea gabbi\n', 'Poromya rostrata\n', 'Labiosa plicatella\n', 'Prunum virginianum\n', 'Anodontia philippiana\n', 'Botula\n', 'Pecten\n', 'Spondylus dominicensis\n', 'Lyonsia hyalina\n', 'Polinices immaculatus\n', 'Nassarius ambiguus\n', 'Acteonidae\n', 'Zonaria\n', 'Cerithiopsis\n', 'Penitella penita\n', 'Cephalopoda\n', 'Crenella faba\n', 'Basommatophora\n', 'Teinostoma biscaynense\n', 'Anachis\n', 'Massyla\n', 'Persicula subtrigona\n', 'Anadara multicostata\n', 'Aequipecten gibbus nucleus\n', 'Heteroteuthis tenera\n', 'Cavolina cuspidata\n', 'Pseudochama echinata\n', 'Trivia leucosphaera\n', 'Tellina fausta\n', 'Rissoina chesneli\n', 'Boreotrophon stuarti\n', 'Creseis coniformis\n', 'Epitonium pretiosula\n', 'Chiton albolineatus\n', 'Mactra nasuta\n', 'Boreotrophon scitulus\n', 'Ringicula semistriata\n', 'Tectibranchia\n', 'Cyrtodaria\n', 'Martesia smithi\n', 'Spiroglyphus annulatus\n', 'Stramonita\n', 'Diodora densiclathrata\n', 'Planaxis\n', 'Lima terica\n', 'Smaragdia viridemaris\n', 'Bursa californica\n', 'Isognomon chemnitziana\n', 'Strombus horridus\n', 'Tellina laevigata\n', 'Aplysia dactylomela\n', 'Cassis\n', 'Chama\n', 'Pteropurpura\n', 'Astraea spinulosa\n', 'Panope taeniata\n', 'Anadara brasiliana\n', 'Pseudomalaxis balesi\n', 'Nuculana curtulosa\n', 'Clio lanceolata\n', 'Ocenebra gracillima\n', 'Aporrhais labradorensis\n', 'Thais undata\n', 'Rhizorus bushi\n', 'Acmaea fenestrata\n', 'Cerastoderma pinnulatum\n', 'Codakia californica\n', 'Ervilia concentrica\n', 'Pecten tryoni\n', 'Barbatia jamaicensis\n', 'Muricopsis\n', 'Fasciolaria\n', 'Chione latilirata\n', 'Neritina\n', 'Semele radiata\n', 'Pecten laurenti\n', 'Gastropteron pacificum\n', 'Trapeziidae\n', 'Crepidula glauca\n', 'Crassostrea rhizophorae\n', 'Dendronotus arborescens\n', 'Microcardium tinctum\n', 'Octopus vulgaris\n', 'Caecidae\n', 'Cerodrillia perryae\n', 'Strombus canaliculatus\n', 'Fasciolariidae\n', 'Nucula crenulata\n', 'Conus floridanus floridensis\n', 'Smaragdia viridis\n', 'Cumingia tellinoides\n', 'Calliostoma psyche\n', 'Acmaea pustulata\n', 'Trigoniocardia\n', 'Lithophaga nigra\n', 'Fusinus eucosmius\n', 'Crepidula onyx\n', 'Glaucidae\n', 'Phalium abbreviata\n', 'Atrina serrata\n', 'Isognomon bicolor\n', 'Lima lima\n', 'Daphnella lymneiformis\n', 'Atydae\n', 'Rupellaria typica\n', 'Arcticidae\n', 'Pododesmus decipiens\n', 'Polystira tellea\n', 'Boreotrophon orpheus\n', 'Bittium eschrichti\n', 'Cleodora virgula\n', 'Semele rupicola\n', 'Hyalina avena\n', 'Isognomonidae\n', 'Sanguinolaria sanguinolenta\n', 'Ischnochiton clathratus\n', 'Sconsia striata\n', 'Littorina\n', 'Egregia\n', 'Anadara americana\n', 'Ischnochiton magdalenensis\n', 'Eulimidae\n', 'Laskeya\n', 'Limopsis antillensis\n', 'Cylichna alba\n', 'Nuculidae\n', 'Boreotrophon multicostatus\n', 'Cerithideopsis\n', 'Nuculana pernula\n', 'Olivella pycna\n', 'Forreria belcheri\n', 'Retusa candei\n', 'Mitra\n', 'Vermetidae\n', 'Glossodoris macfarlandi\n', 'Micranellum\n', 'Tapes semidecussata\n', 'Cerodrillia thea\n', 'Hyalaea angulata\n', 'Oliva litterata\n', 'Cavolina labiata\n', 'Tonna\n', 'Ringicula nitida\n', 'Cheila equestris\n', 'Cylichna biplicata\n', 'Retusa sulcata\n', 'Lunatia heros\n', 'Cavolina telemus\n', 'Crassatellites\n', 'Cymatium chlorostomum\n', 'Aequipecten fusco-purpureus\n', 'Divaricella quadrisulcata\n', 'Coralliophila abbreviata\n', 'Glans\n', 'Aplysia protea\n', 'Spiratella inflata\n', 'Astartidae\n', 'Ensis\n', 'Pseudochama ferruginea\n', 'Spiratella\n', 'Tegula regina\n', 'Neosimnia barbarensis\n', 'Plicatula gibbosa\n', 'Xancus\n', 'Trivia antillarum\n', 'Ervilia\n', 'Pneumonoderma\n', 'Carinaria lamarcki\n', 'Naticidae\n', 'Lyropecten nodosus\n', 'Fusinus kobelti\n', 'Amphithalamus inclusus\n', 'Conidae\n', 'Rhizorus minutus\n', 'Calliostoma annulatum\n', 'Janacus\n', 'Gibberulina amianta\n', 'Littorina angulifera\n', 'Coralliophila deburghiae\n', 'Rissoina striosa\n', 'Glycymeris lineata\n', 'Acmaea conus\n', 'Strombus\n', 'Arca\n', 'Tellina salmonea\n', 'Admete couthouyi\n', 'Onchidiata\n', 'Echinochama cornuta\n', 'Venericardia stearnsi\n', 'Trivia globosa\n', 'Atrina rigida\n', 'Fasciolaria distans\n', 'Ischnochiton conspicuus\n', 'Nuculana tenuisulcata\n', 'Busycon canaliculatum\n', 'Dendrodorididae\n', 'Cerithiopsis virginica\n', 'Boreotrophon triangulatus\n', 'Cerithidea\n', 'Rangia cuneata\n', 'Murex cellulosus\n', 'Busycon coarctatum\n', 'Epitonium krebsi\n', 'Spiratella scaphoidea\n', 'Tellidora cristata\n', 'Lampusia\n', 'Pleuroploca gigantea\n', 'Acmaea punctulata\n', 'Pyrenidae\n', 'Acanthina paucilirata\n', 'Glycymeris undata\n', 'Aequipecten exasperatus\n', 'Solen sicarius\n', 'Spiratella trochiformis\n', 'Dentalium pseudohexagonum\n', 'Rupellaria denticulata\n', 'Pholadidae\n', 'Pleurolucina\n', 'Styliola subula\n', 'Tellina sybaritica\n', 'Patinopecten\n', 'Neptunea satura\n', 'Circulus\n', 'Alabina tenuisculpta\n', 'Tellina sayi\n', 'Phacoides acutilineatus\n', 'Siphonaria lineolata\n', 'Rangia\n', 'Ancula pacifica\n', 'Calyptraea\n', 'Chlamys hastatus hericius\n', 'Rhizorus\n', 'Natica pusilla\n', 'Protothaca\n', 'Macoma limula\n', 'Odostomia americana\n', 'Anodontia chrysostoma\n', 'Trivia pediculus\n', 'Fusinus depetitthouarsi\n', 'Haminoea succinea\n', 'Ancistrosyrinx\n', 'Pitar\n', 'Cypraecassis testiculus\n', 'Tachyrhynchus lacteolum\n', 'Cerithium algicola\n', 'Dendronotus giganteus\n', 'Scalina\n', 'Tritonocauda\n', 'Cavolina imitans\n', 'Pododesmus cepio\n', 'Fossaridae\n', 'Aplysia\n', 'Dentale\n', 'Ostrea rubella\n', 'Epitonium swifti\n', 'Transennella\n', 'Siliqua patula\n', 'Murex trunculus\n', 'Calliostoma gloriosum\n', 'Costacallista\n', 'Tonna maculosa\n', 'Melongena corona perspinosa\n', 'Hyalocylis striata\n', 'Triphora ornatus\n', 'Donax roemeri\n', 'Amphithalamus\n', 'Nodulus\n', 'Tellina radiata\n', 'Tapes\n', 'Anadara notabalis\n', 'Hipponix cranoides\n', 'Tellina polita\n', 'Ficus reticulata\n', 'Pachypoma\n', 'Nitidella carinata\n', 'Spiratella retroversa\n', 'Cyclostrema amabile\n', 'Prunum amabile\n', 'Bursa\n', 'Teredo townsendi\n', 'Murex recurvirostris\n', 'Abra\n', 'Volutharpa ampullacea\n', 'Nuculanidae\n', 'Chiton virgulatus\n', 'Glicymeris\n', 'Anisodoris\n', 'Tellina venulosa\n', 'Acteocina cerealis\n', 'Volvulella\n', 'Caecum pedroense\n', 'Crassispira\n', 'Anachis ostreicola\n', 'Busycon plagosum\n', 'Trachycardium isocardia\n', 'Eucrassatella gibbesi\n', 'Strombus peculiaris\n', 'Coralliophila\n', 'Anadara sulcosa\n', 'Periploma leanum\n', 'Cyphoma gibbosum\n', 'Ellipetylus\n', 'Siphonariidae\n', 'Atys\n', 'Trachycardium egmontianum\n', 'Chitonidae\n', 'Anadara auriculata\n', 'Cavolina\n', 'Cerithidea hegewischi californica\n', 'Levia\n', 'Microgaza inornata\n', 'Semele decisa\n', 'Cavolina gibbosa\n', 'Cerithidea turrita\n', 'Leucozonia cingidifera\n', 'Seila terebralis\n', 'Phacoides annulatus\n', 'Colus pygmaeus\n', 'Pandora arenosa\n', 'Bufonaria\n', 'Dentaliidae\n', 'Turbonilla nivea\n', 'Clypidella\n', 'Genota viabrunnea\n', 'Lottia gigantea\n', 'Petaloconchus\n', 'Rangia rostrata\n', 'Acteon candens\n', 'Lamellaria rhombica\n', 'Aperiploma\n', 'Xancidae\n', 'Lima tetrica\n', 'Littorina palliata\n', 'Bailya intricata\n', 'Hyalina avenella\n', 'Anadara\n', 'Turbo crenulatus\n', 'Turbonilla interrupta\n', 'Fistulana Bruguiere\n', 'Paedoclione\n', 'Caecum carpenteri\n', 'Clio polita\n', 'Bittium virginicum\n', 'Marginella haematita\n', 'Dolium\n', 'Styliferidae\n', 'Mytilus californianus\n', 'Amphissa versicolor\n', 'Cerithium versicolor\n', 'Schizothaerus\n', 'Pododesmus macroschisma\n', 'Mercenaria notata\n', 'Meioceras\n', 'Bursatella leachi plei\n', 'Octopus bimaculatus\n', 'Nuttallia\n', 'Diodora minuta\n', 'Melongena subcoronata\n', 'Schizothaerus capax\n', 'Cypraecassis\n', 'Anadara secticostata\n', 'Murex citrinus\n', 'Calliostoma occidentale\n', 'Acanthodoris\n', 'Vitrinella\n', 'Trivia subrostrata\n', 'Polystira virgo\n', 'Trivia nix\n', 'Triphora nigrocincta\n', 'Rissoina cleo\n', 'Sigatica semisulcata\n', 'Nassarius consensus\n', 'Cantharus\n', 'Olivella bayeri\n', 'Tergipes despectus\n', 'Cittarium\n', 'Haliotis kamtschatkana\n', 'Solemya occidentalis\n', 'Persicula catenata\n', 'Crassostrea laperousi\n', 'Mopalia fissa\n', 'Navea subglobosa\n', 'Pleurobranchus atlanticus\n', 'Nuculana redondoensis\n', 'Caecum rosanum\n', 'Ringiculidae\n', 'Notobranchaea\n', 'Clio cuspidata\n', 'Modulus\n', 'Semele proficua\n', 'Colus pygmaea\n', 'Solariella\n', 'Octopus americanus\n', 'Lacuna carinata\n', 'Thais\n', 'Mangilia\n', 'Spondylus pictorum\n', 'Hipponix serratus\n', 'Polymesoda\n', 'Crepidula convexa\n', 'Murex pomum\n', 'Colus caelatus\n', 'Bittium interfossum\n', 'Litiopa bombix\n', 'Chlamys ornatus\n', 'Martesia striata\n', 'Cavolina mucronata\n', 'Fissurella rosea\n', 'Monostiolum\n', 'Pectinidae\n', 'Spiratella gouldi\n', 'Conus\n', 'Lima squamosa\n', 'Arca pernoides\n', 'Diplodonta granulosa\n', 'Iolaea\n', 'Ancistrosyrinx elegans\n', 'Kelliidae\n', 'Limopsis sulcata\n', 'Glossodoris universitatis\n', 'Atrina\n', 'Iphigenia brasiliensis\n', 'Spisula dolabriformis\n', 'Voluta virescens\n', 'Epitonium contorquata\n', 'Turbonilla aragoni\n', 'Triopha grandis\n', 'Pitar simpsoni\n', 'Mercenaria\n', 'Ovulidae\n', 'Murex fulvescens\n', 'Trachycardium quadragenarium\n', 'Ficus communis\n', 'Scaphella butleri\n', 'Pupillaria\n', 'Smaragdia\n', 'Eucrassatella\n', 'Octopus punctatus\n', 'Lunarca\n', 'Semicassis inflatum\n', 'Seila montereyensis\n', 'Caecum lermondi\n', 'Odostomia laxa\n', 'Pecten tereinus\n', 'Labiosa campechensis\n', 'Tagelus divisus\n', 'Rhizorus acutus\n', 'Astraea guadeloupensis\n', 'Spiratella lesueuri\n', 'Bulla\n', 'Lepidochitona\n', 'Entodesma saxicola\n', 'Capulus incurvatus\n', 'Bittium\n', 'Heterodonax\n', 'Litiopa bombyx\n', 'Rissoina laevigata\n', 'Periploma papyraceum\n', 'Neosimnia catalinensis\n', 'Architectonica granulata\n', 'Prunum bellum\n', 'Forreria cerrosensis\n', 'Epitonium scalare\n', 'Microgaza rotella\n', 'Teinostoma clavium\n', 'Lunatia groenlandica\n', 'Crenella columbiana\n', 'Scyllaea pelagica\n', 'Corbula contracta\n', 'Xenophora\n', 'Ischnochiton\n', 'Pecten ziczac\n', 'Propeamussium pourtalesianum\n', 'Flabellinidae\n', 'Amphissa columbiana\n', 'Nuculana hindsi\n', 'Haliotis\n', 'Symmetrogephyrus pallasi\n', 'Peraclidae\n', 'Bursa crassa\n', 'Bulla punctulata\n', 'Tagelus politus\n', 'Volsella\n', 'Janthina bifida\n', 'Abra aequalis\n', 'Mopalia hindsi\n', 'Diodora aspera\n', 'Cerithium variabile\n', 'Lucina sombrerensis\n', 'Donax variabilis\n', 'Mya japonica\n', 'Teinostoma cocolitoris\n', 'Lucina pensylvanica\n', 'Murex recurvirostris sallasi\n', 'Pseudocyrena floridana\n', 'Tenagodus\n', 'Pedalion\n', 'Distorsio constricta mcgintyi\n', 'Bittium alternatum\n', 'Mopalia ciliata\n', 'Murex brandaris\n', 'Prunum carneum\n', 'Homalopoma albida\n', 'Lithophaga plumula kelseyi\n', 'Pinna carnea\n', 'Thais lamellosa\n', 'Venericardia ventricosa\n', 'Oliva\n', 'Haliotis smithsoni\n', 'Cuvieria\n', 'Diplodonta semiaspera\n', 'Pitar albida\n', 'Colus\n', 'Chione pygmaea\n', 'Opalia hotessieriana\n', 'Gari californica\n', 'Diplodonta subquadrata\n', 'Clio pyramidata\n', 'Haliotis fulgens\n', 'Epitonium clathrum\n', 'Chiton squamosus\n', 'Mopalia muscosa\n', 'Ostrea spreta\n', 'Murex tremperi\n', 'Tegula montereyi\n', 'Distorsio\n', 'Pteria sterna\n', 'Cavolina limbata\n', 'Cuspidaria glacialis\n', 'Tegula aureotincta\n', 'Eratoidea\n', 'Janthina globosa\n', 'Nassarius acutus\n', 'Euribia\n', 'Tectininus\n', 'Ocenebra tenuisculpta\n', 'Neosimnia aequalis\n', 'Neritina reclivata\n', 'Acanthina punctulata\n', 'Siphonodentaliidae\n', 'Nucula delphinodonta\n', 'Ocenebra circumtexta\n', 'Puncturella\n', 'Tellina angulosa\n', 'Melongena inspinata\n', 'Conus villepini\n', 'Dinocardium\n', 'Bulla amygdala\n', 'Macoma carlottensis\n', 'Tellina modesta\n', 'Lucapina cancellata\n', 'Nassarius trivittatus\n', 'Caecum licalum\n', 'Modulus modulus\n', 'Nuculana concentrica\n', 'Cliopsis\n', 'Ischnochiton albus\n', 'Urosalpinx follyensis\n', 'Nitidella gouldi\n', 'Cadlina\n', 'Cingula kelseyi\n', 'Sanguinolaria cruenta\n', 'Adalaria proxima\n', 'Amygdalum sagittata\n', 'Caecum barkleyense\n', 'Atys sandersoni\n', 'Volutopsius castaneus\n', 'Marginella aureocincta\n', 'Cryptonatica\n', 'Sthenorytis hendersoni\n', 'Rhizorus oxytatus\n', 'Cylichnella\n', 'Tagelus californianus\n', 'Diplodonta punctata\n', 'Columbella\n', 'Spondylus echinatus\n', 'Gemminae\n', 'Monilispira albinodata\n', 'Olivella biplicata\n', 'Lacuna divaricata\n', 'Epitonium muricata\n', 'Scaphella georgiana\n', 'Tonna (Dolium) album\n', 'Macoma nasuta\n', 'Diodora dysoni\n', 'Trichotropis borealis\n', 'Crenella divaricata\n', 'Corbula nasuta\n', 'Pyramidella fusca\n', 'Persicula jewetti\n', 'Acteon\n', 'Rupellaria californica\n', 'Bankiopsis\n', 'Calliostoma gemmulatum\n', 'Pandora gouldiana\n', 'Dosinia\n', 'Mitra barbadensis\n', 'Volsella americana\n', 'Carinariidae\n', 'Anadara pexata\n', 'Cypraea pantherina\n', 'Favartia\n', 'Pyramidella\n', 'Tutufa\n', 'Cadulus\n', 'Vasum muricatum\n', 'Peracle bispinosa\n', 'Mysella planulata\n', 'Hyalina veliei\n', 'Spisula polynyma\n', 'Scaphella dohrni\n', 'Teredo\n', 'Limopsis diegensis\n', 'Cymatiidae\n', 'Tellina mera\n', 'Mopalia\n', 'Trachycardium muricatum\n', 'Lucina approximata\n', 'Congeria leucophaeta\n', 'Syrnola\n', 'Ficus papyratia\n', 'Chiton marmoratus\n', 'Gryphaea\n', 'Odostomia trifida\n', 'Thais emarginata\n', 'Melongena altispira\n', 'Microcardium\n', 'Cerithidea pliculosa\n', 'Polinices lacteus\n', 'Salasiella\n', 'Strombus goliath\n', 'Lucina tenuisculpta\n', 'Cassis spinella\n', 'Tivela stultorum\n', 'Cidarina\n', 'Laevicardium\n', 'Hiatella striata\n', 'Margarites costalis\n', 'Ostrea thomasi\n', 'Lucina multilineata\n', 'Chiton\n', 'Acmaea simplex\n', 'Megatebennus bimaculatus\n', 'Pseudopythina compressa\n', 'Scaphella florida\n', 'Venericardia perplana\n', 'Cymatium\n', 'Dreissenidae\n', 'Trivia maltbiana\n', 'Promartynia\n', 'Strombus raninus\n', 'Macoma incongrua\n', 'Scissurella\n', 'Cantharus tinctus\n', 'Ischnochiton acrior\n', 'Polyceridae\n', 'Arene cruentata\n', 'Chione mazycki\n', 'Sepiolidae\n', 'Aletes squamigerous\n', 'Callista eucymata\n', 'Cavolinidae\n', 'Acanthochitona balesae\n', 'Trivia ritteri\n', 'Polinices reclusianus\n', 'Limopsis cristata\n', 'Nodipecten\n', 'Tellina buttoni\n', 'Protothaca grata\n', 'Caecum oregonense\n', 'Melongena melongena\n', 'Hyalaea coniformis\n', 'Neosimnia loebbeckeana\n', 'Eulamellibranchia\n', 'Anadara transversa\n', 'Tritoniscus\n', 'Sepioteuthis sepioidea\n', 'Amauropsis purpurea\n', 'Acmaea instabilis\n', 'Dentalium entale stimpsoni\n', 'Murex rufus\n', 'Caecum catalinense\n', 'Peracle reticulata\n', 'Pecten diegensis\n', 'Chione gnidia\n', 'Strombus costatus\n', 'Diodora alternata\n', 'Mytilus hamatus\n', 'Pecten raveneli\n', 'Onchidoridae\n', 'Calyptraea centralis\n', 'Cyathodonta undulata\n', 'Cerodrillia\n', 'Homalopoma bacula\n', 'Donax gouldi\n', 'Plicatulidae\n', 'Conus frisbeyae\n', 'Vasum\n', 'Cardiomya costellata\n', 'Rissoina kelyseyi\n', 'Adapedonta\n', 'Astraea gibberosa\n', 'Forreria cerrosensis cerrosensis\n', 'Catriona aurantiaca\n', 'Saxicava\n', 'Cerithium floridanum\n', 'Lacuna vincta\n', 'Chione grus\n', 'Voluta musica\n', 'Haliotis cracherodi\n', 'Limea bronniana\n', 'Musculus\n', 'Nucula proxima\n', 'Corbula luteola\n', 'Haminoea virescens\n', 'Trichotropidae\n', 'Ischnochiton papillosus\n', 'Calliostoma supragranosum\n', 'Scalaria borealis\n', 'Antillophos candei\n', 'Donax tumida\n', 'Littorina groenlandica\n', 'Supplanaxis\n', 'Calyptraea contorta\n', 'Lima hemphilli\n', 'Yoldia limatula\n', 'Transennella conradina\n', 'Pitar cordata\n', 'Cingula palmeri\n', 'Diacria\n', 'Cirsotrema arcella\n', 'Solen rosaceus\n', 'Rangianella\n', 'Sphenia ovoidea\n', 'Cavolina longirostris\n', 'Odostomia willisi\n', 'Isognomon radiata\n', 'Leptegouana\n', 'Nuculana taphria\n', 'Sycofulgur\n', 'Buccinum undatum\n', 'Lunatia pallida\n', 'Haloconcha reflexa\n', 'Pachydesma\n', 'Tegula fasciata\n', 'Penitella\n', 'Ocinebra\n', 'Gadila\n', 'Strombus spectabilis\n', 'Ancistrolepsis\n', 'Acanthina spirata\n', 'Distorsio constricta\n', 'Lucina amiantus\n', 'Nitidella\n', 'Acteocina\n', 'Lima antillensis\n', 'Meretricinae\n', 'Hyalaea\n', 'Livona pica\n', 'Terebra\n', 'Herse oryza\n', 'Hyalina succinea\n', 'Fossarus elegans\n', 'Cymatium muricinum\n', 'Latirus\n', 'Lithopoma\n', 'Calyptraeidae\n', 'Protothaca staminea\n', 'Ommastrephidae\n', 'Eulithidium\n', 'Nassarius\n', 'Odostomia bisuturalis\n', 'Cerithiopsis vanhyningi\n', 'Terebra dislocata\n', 'Chaetopleura apiculata\n', 'Chione\n', 'Clinocardium corbis\n', 'Cypraecassis rufa\n', 'Trivia nivea\n', 'Caecum heptagonum\n', 'Musculus lateralis\n', 'Crenella\n', 'Melanella gibba\n', 'Spondylus\n', 'Cadlina obvelata\n', 'Odostomia nota\n', 'Livona\n', 'Xancus scolyma\n', 'Eupleura\n', 'Nucula cancellata\n', 'Neptunea ventricosa\n', 'Gemmula periscelida\n', 'Septifer bifurcatus\n', 'Rissoina californica\n', 'Triphora pedroana\n', 'Antigona listeri\n', 'Clio\n', 'Crassostrea gigas\n', 'Nassariidae\n', 'Nassarius californianus\n', 'Olivella porteri\n', 'Gobraeus\n', 'Purpura pansa\n', 'Triopha maculata\n', 'Pitar lupinaria\n', 'Phalium inflatum\n', 'Mesodesma arctatum\n', 'Liotia fenestrata\n', 'Polinices draconis\n', 'Tellina similis\n', 'Creseis virgula\n', 'Tectarius\n', 'Velutina zonata\n', 'Tegula lividomaculata\n', 'Conus spurius spurius\n', 'Melanella\n', 'Haminoea\n', 'Terebra limatula\n', 'Siliqua lucida\n', 'Pleuroploca\n', 'Ostrea equestris\n', 'Nuculana penderi\n', 'Abra lioica\n', 'Larkinia\n', 'Chlamys benedicti\n', 'Menestho\n', 'Xenophoridae\n', 'Yoldia thraciaeformis\n', 'Cavolina affinis\n', 'Ocenebra citrica\n', 'Crassinella\n', 'Callianax\n', 'Cadlina repanda\n', 'Opalia insculpta\n', 'Aequipecten nucleus\n', 'Epitonium occidentale\n', 'Periploma inaequivalvis\n', 'Olivella jaspidea\n', 'Trophon tenuisculptus\n', 'Lepidozona\n', 'Acmaea pelta\n', 'Panope solida\n', 'Polinices brunneus\n', 'Petricola lapicida\n', 'Naranio\n', 'Dosinidia\n', 'Nuculana hamata\n', 'Eubranchus exiguus\n', 'Eunaticina oldroydi\n', 'Mitra nodulosa\n', 'Crassispira ostrearum\n', 'Gastrochaena\n', 'Haliotis splendens\n', 'Bursa granularis\n', 'Nitidella gausapata\n', 'Olivella floralia\n', 'Tegula gallina\n', 'Dentalium pretiosum\n', 'Chrysodomus satura\n', 'Tivela crassatelloides\n', 'Phalium glaucum\n', 'Neritina floridana\n', 'Aequipecten irradians concentricus\n', 'Triphora decorata\n', 'Sepioteuthis\n', 'Luria\n', 'Rossia tenera\n', 'Fartulum\n', 'Glossaulax\n', 'Dentalium texasianum\n', 'Macoma tenta\n', 'Peracle clathrata\n', 'Tellina magna\n', 'Rissoina cancellata\n', 'Cardita dominguensis\n', 'Conus peali\n', 'Chlamys imbricatus\n', 'Astraea caelata\n', 'Taxodonta\n', 'Pedicularia ovuliformis\n', 'Crassostrea virginica\n', 'Boreostrophon peregrinus\n', 'Tellina lineata\n', 'Nerita versicolor\n', 'Melongena estephomenos\n', 'Phalium centiquadrata\n', 'Octopus\n', 'Odostomia impressa\n', 'Trivia candidula\n', 'Cypraea spurca acicularis\n', 'Crassostrea angulata\n', 'Kennerlia\n', 'Nucula reticulata\n', 'Cyrtodaria siliqua\n', 'Tricolia concinna\n', 'Ischadium\n', 'Cyphoma\n', 'Cadlina laevis\n', 'Archidoris\n', 'Tricolia tessellata\n', 'Caecum pulchellum\n', 'Mysella tumida\n', 'Acila castrensis\n', 'Laila cockerelli\n', 'Polymesoda caroliniana\n', 'Glycymeris decussata\n', 'Lasaea\n', 'Haliris\n', 'Conus austini\n', 'Acteocina culitella\n', 'Charonia\n', 'Fusinus couei\n', 'Tegula indusi\n', 'Scissurella crispata\n', 'Boreotrophon pacificus\n', 'Trigonostoma\n', 'Retusa canaliculata\n', 'Polinices\n', 'Glycymeridae\n', 'Aporrhais\n', 'Littorina scutulata\n', 'Thyasira gouldi\n', 'Mitrella raveneli\n', 'Mitra florida\n', 'Papyridea hiatus\n', 'Nuculana conceptionis\n', 'Brachidontes multiformis\n', 'Notarchus\n', 'Chama sinuosa\n', 'Cavolina costata\n', 'Cymatium velei\n', 'Marginella borealis\n', 'Sepia\n', 'Caecum bakeri\n', 'Haliotis walallensis\n', 'Hiatella rugosa\n', 'Crassostrea\n', 'Taglus politus\n', 'Anodontia alba\n', 'Acirsa costulata\n', 'Hyalaea affinis\n', 'Tonicella marmorea\n', 'Arca umbonata\n', 'Trivia armandina\n', 'Parastarte triquetra\n', 'Chione succincta\n', 'Cavolina reeviana\n', 'Dentalium semistriolatum\n', 'Anadara springeri\n', 'Annulicallus\n', 'Rissoidae\n', 'Xenophora caribaeum\n', 'Opalia\n', 'Crepidula nummaria\n', 'Pseudoneptunea multangula\n', 'Cuspidaria\n', 'Calliostoma ligatum\n', 'Pleuromeris\n', 'Astraea inaequalis\n', 'Cardita\n', 'Chiton viridis\n', 'Galeodes\n', 'Persicula lavalleana\n', 'Triopha\n', 'Lucina jamaicensis\n', 'Puncturella galeata\n', 'Venericardia flabella\n', 'Trichotropis bicarinata\n', 'Opalia crenata\n', 'Gymnobela blakeana\n', 'Columbella rusticoides\n', 'Sthenorytis epae\n', 'Boreotrophon peregrinus\n', 'Dibranchia\n', 'Mantellum\n', 'Boreotrophon smithi\n', 'Lima\n', 'Sinum maculatum\n', 'Arene gemma\n', 'Scaphella johnstoneae\n', 'Hespererato\n', 'Macrocallista\n', 'Trachycardium magnum\n', 'Eupleura sulcidentata\n', 'Crepidula excavata\n', 'Lucapinella callomarginata\n', 'Ruditapes\n', 'Polytropa\n', 'Arginarca\n', 'Fasciolaria tulipa\n', 'Macoma mitchelii\n', 'Caecum floridanum\n', 'Fissurella nodosa\n', 'Ostrea folium\n', 'Turritellidae\n', 'Amphithalamus lacunatus\n', 'Sinum\n', 'Terebra cinerea\n', 'Bursa cubaniana\n', 'Sinum californicum\n', 'Octopus briareus\n', 'Donax striata\n', 'Tonicia schrammi\n', 'Tegula brunnea\n', 'Odostomia gibbosa\n', 'Carinaria mediterranea\n', 'Teinostoma goniogyrus\n', 'Doryteuthis plei\n', 'Bivetiella\n', 'Lacuna variegata\n', 'Arcopsis adamsi\n', 'Neptunea californica\n', 'Epitonium rupicolum\n', 'Terebra lutescens\n', 'Polycera\n', 'Nuculana carpenteri\n', 'Thais lima\n', 'Thericium\n', 'Siphonaria\n', 'Dentalium eboreum\n', 'Acanthopleura granulata\n', 'Cingula aculeus\n', 'Pleuroploca princeps\n', 'Crassostrea floridensis\n', 'Strombus gallus\n', 'Octopus hongkongensis\n', 'Neilonella\n', 'Cavolina trispinosa\n', 'Chionidae\n', 'Strombus verrilli\n', 'Hydatina\n', 'Astraea americana\n', 'Ischnochiton purpurascens\n', 'Hormomya\n', 'Cypraea tigris\n', 'Opalia chacei\n', 'Pinna\n', 'Crucibulum auricula\n', 'Pseudomalaxis\n', 'Brachidontes citrinus\n', 'Conus floridanus\n', 'Vasum coestus\n', 'Siphonaria naufragum\n', 'Corbulidae\n', 'Mactridae\n', 'Acmaea alveus\n', 'Lima hians\n', 'Caecum cooperi\n', 'Arene variabilis\n', 'Nesta\n', 'Fasciolaria hunteria\n', 'Caecum carolinianum\n', 'Dosinia discus\n', 'Janthina\n', 'Cadulus quadridentatus\n', 'Protothaca ruderata\n', 'Hydatina physis\n', 'Jumala crebricostata\n', 'Cavolina tridentata\n', 'Chlamys islandicus\n', 'Diaphana hiemalis\n', 'Semele\n', 'Littorina littorea\n', 'Modulidae\n', 'Arcopagia fausta\n', 'Placopecten grandis\n', 'Lima pellucida\n', 'Fusitriton\n', 'Neosimnia\n', 'Cymatium tuberosum\n', 'Amauropsis\n', 'Noetia reversa\n', 'Ensis myrae\n', 'Teinostoma litus-palmarum\n', 'Conus verrucosus\n', 'Spondylidae\n', 'Saxidomus nuttalli\n', 'Scyllaeidae\n', 'Epitonium lineatum\n', 'Janthinidae\n', 'Vermicularia fargoi\n', 'Mormula\n', 'Macoma brota\n', 'Solen viridis\n', 'Epitonium folaceicostum\n', 'Astarte undata\n', 'Dinocardium vanhyningi\n', 'Thracia conradi\n', 'Seila adamsi\n', 'Hexaplex\n', 'Macron lividus\n', 'Aequipecten muscosus\n', 'Panope bitruncata\n', 'Panomya\n', 'Capulus\n', 'Cassididae\n', 'Cypraea vallei\n', 'Eubranchus\n', 'Atlanta peroni\n', 'Trivia\n', 'Fasciolaria princeps\n', 'Terebra taurinum\n', 'Arctomelon stearnsi\n', 'Nuculana messanensis\n', 'Cerithiopsis pedroana\n', 'Tapes philippinarum\n', 'Margarites cinereus\n', 'Conus sennottorum\n', 'Marginella denticulata\n', 'Polycera hummi\n', 'Cadlina marginata\n', 'Aequipecten dislocatus\n', 'Perna\n', 'Cancellariidae\n', 'Pandora\n', 'Architectonica krebsi\n', 'Anachis penicillata\n', 'Pyrgolampros\n', 'Bittium varium\n', 'Margarites groenlandicus\n', 'Volvarina\n', 'Lima caribaea\n', 'Spisula planulata\n', 'Murex florifer\n', 'Calliostoma tricolor\n', 'Aplysia badistes\n', 'Acmaea asmi\n', 'Scissula\n', 'Clinocardium ciliatum\n', 'Dissentoma prima\n', 'Semicassis\n', 'Dentiscala\n', 'Nuttallina californica\n', 'Beringius\n', 'Homalopoma\n', 'Barbatia\n', 'Fusinus timessus\n', 'Cerithiopsis subulata\n', 'Donax fossor\n', 'Haliotis aulaea\n', 'Charonia atlantica\n', 'Fissidentalium\n', 'Olivella nivea\n', 'Puncturella cucullata\n', 'Cassis flammea\n', 'Odostomia\n', 'Vitrinella multistriata\n', 'Botula californiensis\n', 'Turridae\n', 'Murex\n', 'Janthina exigua\n', 'Haliotis pourtalesi\n', 'Aldisa sanguinea\n', 'Codakia costata\n', 'Terebra protexta\n', 'Antigona\n', 'Barbatia helblingi\n', 'Margarites obsoletus\n', 'Tellina tampaensis\n', 'Lacunidae\n', 'Acanthina\n', 'Monilispira\n', 'Tetrabranchia\n', 'Crepipatella lingulata\n', 'Tellina alternata\n', 'Limopsidae\n', 'Terebra floridana\n', 'Epitonium\n', 'Clio exacuta\n', 'Diadora\n', 'Trochidae\n', 'Amaea mitchelli\n', 'Ctenoides\n', 'Opalia wroblewskii\n', 'Urosalpinx cinerea\n', 'Raeta campechensis\n', 'Acirsa borealis\n', 'Episiphon\n', 'Gaza superba\n', 'Melongena minor\n', 'Lucinisca\n', 'Lolliguncula\n', 'Trigonostoma tenerum\n', 'Prunum borealis\n', 'Littorina saxatilis\n', 'Rissoina newcombei\n', 'Tellina meropsis\n', 'Turritella\n', 'Aequipecten gibbus\n', 'Triphora pulchella\n', 'Olivella pedroana\n', 'Engina turbinella\n', 'Macoma constricta\n', 'Haliotis assimilis\n', 'Rupellaria\n', 'Mopalia wosnessenski\n', 'Crassispira tampaensis\n', 'Ostrea expansa\n', 'Cypraea spurca\n', 'Turbonilla kelseyi\n', 'Discodoris heathi\n', 'Tricolia variegata\n', 'Murex macropterus\n', 'Erato maugeriae\n', 'Dentalium sowerbyi\n', 'Pandora bushiana\n', 'Margarites umbilicalis\n', 'Perotrochus\n', 'Nucula atacellana\n', 'Sphenia\n', 'Peronidia\n', 'Spisula catilliformis\n', 'Trivia pullata\n', 'Acmaea testudinalis\n', 'Spisula similis\n', 'Microcardium peramabile\n', 'Symmetrogephyrus vestitus\n', 'Cypraea mus\n', 'Hyalina avenacea\n', 'Petricolaria\n', 'Teredo bartschi\n', 'Dinocardium robustum\n', 'Macoma balthica\n', 'Diodora cayenensis\n', 'Malletia\n', 'Cooperella subdiaphana\n', 'Pulmonata\n', 'Tenagodidae\n', 'Cypraea spadicea\n', 'Tonicella lineata\n', 'Laevicardium elatum\n', 'Terebridae\n', 'Isognomon listeri\n', 'Tremoctopus violaceus\n', 'Fusinus harfordi\n', 'Xylophaga washingtona\n', 'Diodora\n', 'Lepetidae\n', 'Zirfaea crispata\n', 'Lasaea subviridis\n', 'Bulla striata\n', 'Lyonsia\n', 'Littorina mespillum\n', 'Codakia\n', 'Thyasira bisecta\n', 'Aequipecten irradians irradians\n', 'Littorina planaxis\n', 'Lucapina\n', 'Physa\n', 'Eupleura stimpsoni\n', 'Vermicularia spirata\n', 'Rangia flexuosa\n', 'Aporrhaidae\n', 'Barbatia tenera\n', 'Nitidella nitidula\n', 'Dentalium elephantinum\n', 'Pteropoda\n', 'Bursa tenuisculpta\n', 'Tellina tenera\n', 'Trona\n', 'Marginella jaspidea\n', 'Hiatella arctica\n', 'Lacuna\n', 'Fugleria\n', 'Muricopsis hexagona\n', 'Chlamys sentis\n', 'Octopus macropus\n', 'Lucapinella limatula\n', 'Haminoea antillarum\n', 'Cardium\n', 'Architectonica nobilis\n', 'Callocardia texasiana\n', 'Scaphopoda\n', 'Cyprina\n', 'Dialula sandiegensis\n', 'Hyalina beyerleana\n', 'Pecten papyraceus\n', 'Thyasira\n', 'Cyclostrema cancellatum\n', 'Haliotis wallallensis\n', 'Xylophaga\n', 'Polinices uberinus\n', 'Solemya valvulus\n', 'Limacina balea\n', 'Litiopa melanostoma\n', 'Pseudomiltha\n', 'Heterodonax pacifica\n', 'Ensis directus\n', 'Mangelia morra\n', 'Inodrillara\n', 'Oliva reticularis\n', 'Bankiella\n', 'Cingula cerinella\n', 'Astarte borealis\n', 'Neptunea decemcostata\n', 'Macoma secta\n', 'Taras orbella\n', 'Spisula falcata\n', 'Mitromorpha\n', 'Sphenia fragilis\n', 'Lucina crenella\n', 'Torinia\n', 'Tegula funebralis\n', 'Philine lima\n', 'Persicula minuta\n', 'Cyclostrema cookeana\n', 'Macoma tenuirostris\n', 'Lepidopleuridae\n', 'Chlorostoma\n', 'Cavolinia\n', 'Protonucula\n', 'Vermicularia\n', 'Lamellaria diegoensis\n', 'Leiomya\n', 'Pterorytis nuttalli\n', 'Cochlodesma\n', 'Mitrella lunata\n', 'Chione paphia\n', 'Brachidontes hamatus\n', 'Strigilla flexuosa\n', 'Bailya parva\n', 'Strombus bituberculatus\n', 'Phacoides filosus\n', 'Latiaxis\n', 'Clio recurva\n', 'Cypraea\n', 'Arca zebra\n', 'Erosaria\n', 'Margarites groenlandica\n', 'Ischnochitoniidae\n', 'Varicorbula\n', 'Nuttallina flexa\n', 'Diplodonta orbella\n', 'Tegula excavata\n', 'Catriona aurantia\n', 'Phacoides centrifuga\n', 'Haliotis holzneri\n', 'Tectarius muricatus\n', 'Macoma\n', 'Acanthochitona astriger\n', 'Eurytellina\n', 'Petaloconchus erectus\n', 'Hipponix barbatus\n', 'Rissoina coronadoensis\n', 'Strombus pugilis\n', 'Verticordia\n', 'Calliostoma subumbilicatum\n', 'Halopsyche\n', 'Tenagodus modestus\n', 'Rocellaria cuneiformis\n', 'Conus stimpsoni\n', 'Ischnochiton ruber\n', 'Phalium cicatricosum\n', 'Seila\n', 'Morula\n', 'Calliostoma tampaense\n', 'Acmaea strigatella\n', 'Stenoplax\n', 'Rubellatoma diomedea\n', 'Astraea longispina\n', 'Solemyidae\n', 'Crassatella\n', 'Trivia solandri\n', 'Pterorytis foliata\n', 'Octopus rugosus\n', 'Boreotrophon clathratus\n', 'Eudolium crosseanum\n', 'Fissurella\n', 'Katharina tunicata\n', 'Phalium\n', 'Smaragdia weyssei\n', 'Taenioturbo\n', 'Ensis megistus\n', 'Mactra fragilis\n', 'Acmaea insessa\n', 'Turbo spenglerianus\n', 'Lucinoma\n', 'Creseis conica\n', 'Littorina obtusata\n', 'Trophonopsis tenuisculptus\n', 'Divaricella dentata\n', 'Apolymetis alta\n', 'Psephidia lordi\n', 'Lithophaga bisulcata\n', 'Lyropecten\n', 'Sanguinolaria nuttalli\n', 'Nerita\n', 'Anopsia\n', 'Glaucus forsteri\n', 'Retusa obtusa\n', 'Nucula exigua\n', 'Dentalium entale\n', 'Nerita tessellata\n', 'Busycon kieneri\n', 'Glaucus\n', 'Microgaza\n', 'Norrisia norrisi\n', 'Catriona\n', 'Scrobiculina\n', 'Gemma purpurea\n', 'Filibranchia\n', 'Cardiomya pectinata\n', 'Onchidella\n', 'Tachyrhynchus\n', 'Bittium quadrifilatum\n', 'Nassarius tegulus\n', 'Nudibranchia\n', 'Fasciolaria gigantea\n', 'Capulus californicus\n', 'Spiratella helicina\n', 'Terebra feldmanni\n', 'Buccinum glaciale\n', 'Dosinia elegans\n', 'Solariella lamellosa\n', 'Conus vanhyningi\n', 'Astyris\n', 'Acephala\n', 'Naticarius\n', 'Eulithidium variegata\n', 'Phacoides nassula\n', 'Tricolia compta\n', 'Chlamys hericius\n', 'Pedicularia\n', 'Haliotis sorenseni\n', 'Lunatia\n', 'Mercenaria texana\n', 'Crepidula plana\n', 'Pleurotomariidae\n', 'Crepidula aculeata\n', 'Solariella regalis\n', 'Spondylus americanus\n', 'Modiolus tulipa\n', 'Forreria\n', 'Serripes groenlandicus\n', 'Kelletia kelletia\n', 'Cingula asser\n', 'Barnea pacifica\n', 'Thais haemastoma\n', 'Phasianellidae\n', 'Chione fluctifraga\n', 'Placiphorella velata\n', 'Pleurobranchidae\n', 'Margarites pupillus\n', 'Neptunea lirata\n', 'Glycymeris pectinata\n', 'Macoma inflatula\n', 'Philinidae\n', 'Xancus angulatus\n', 'Bursa ponderosa\n', 'Lioberus castaneus\n', 'Polinices imperforatus\n', 'Ischnochiton mertensi\n', 'Lepidochitona hartwegi\n', 'Acmaea mitra\n', 'Tricolia pulchella\n', 'Caecum barkleyensis\n', 'Leucozonia ocellata\n', 'Macrocallista maculata\n', 'Hyalina torticula\n', 'Cavolina uncinatiformis\n', 'Acmaea jamaicensis\n', 'Clinocardium\n', 'Agriodesma\n', 'Thracia\n', 'Volsella modiolus\n', 'Phacoides pectinatus\n', 'Phyllodina\n', 'Pterynotus\n', 'Neptunea tabulata\n', 'Liotia bairdi\n', 'Sinum debile\n', 'Plumulella\n', 'Blepharopoda occidentalis\n', 'Anadara lienosa\n', 'Odostomia fetella\n', 'Nucella lapillus\n', 'Nettastomella rostrata\n', 'Polystira albida\n', 'Lithophaga antillarum\n', 'Bankia canalis\n', 'Cassis madagascariensis spinella\n', 'Dentalium filum\n', 'Echininus nodulosus\n', 'Lima multicostata\n', 'Thais lapillus\n', 'Dendrodoris fulva\n', 'Ficus carolae\n', 'Mercenaria mercenaria\n', 'Teredo diegensis\n', 'Teinostoma nesaeum\n', 'Haliotis turveri\n', 'Ilyanassa\n', 'Cadlina planulata\n', 'Haloconcha\n', 'Cremides\n', 'Solen vividis\n', 'Thais crispata\n', 'Periploma planiusculum\n', 'Volsella fornicata\n', 'Chlamys\n', 'Ensis minor\n', 'Anomia peruviana\n', 'Thais haemastoma floridana\n', 'Saxidomus giganteus\n', 'Mitromorpha aspera\n', 'Amaura\n', 'Styliola vitrea\n', 'Pseudochama exogyra\n', 'Aporrhais occidentalis\n', 'Barbatia candida\n', 'Lamellibranchia\n', 'Paleoconcha\n', 'Turbo castaneus\n', 'Acmaea limatula\n', 'Cylichna bidentata\n', 'Murex recurvirostris rubidus\n', 'Acanthodoris brunnea\n', 'Mytilopsis\n', 'Murex cabriti\n', 'Anomalocardia\n', 'Mopalia acuta\n', 'Doriopsis\n', 'Parapholas californica\n', 'Macoma calcarea\n', 'Thyasira disjuncta\n', 'Lyonsia californica\n', 'Gastropteron cinereum\n', 'Terebra pedroana\n', 'Nemocardium centifilosum\n', 'Turbonilla tridentata\n', 'Cerithiopsis grippi\n', 'Creseis\n', 'Turbinella scolyma\n', 'Pterorytis\n', 'Purpura\n', 'Strigilla carnaria\n', 'Acmaea persona\n', 'Cryptoplacidae\n', 'Trigonulina\n', 'Mitrella variegata\n', 'Varicorbula disparilis\n', 'Scaphella dubia\n', 'Epitonium reynoldsi\n', 'Myacea\n', 'Gastropteron rubrum\n', 'Haliotis imperforata\n', 'Semicassis abbreviata\n', 'Melongena bispinosa\n', 'Papyridea soleniformis\n', 'Mactra\n', 'Acanthinucella\n', 'Tegula ligulata\n', 'Tegula\n', 'Aurinia\n', 'Tonna galea\n', 'Turbonilla acra\n', 'Ostrea permollis\n', 'Volsella demissa granosissima\n', 'Murex anniae\n', 'Ficus\n', 'Granula\n', 'Pholas campechiensis\n', 'Thestyleda\n', 'Scissurella proxima\n', 'Xenophora conchyliophora\n', 'Turbo canaliculatus\n', 'Pseudochama granti\n', 'Hiatella\n', 'Purpura foliatum\n', 'Crucibulum spinosum\n', 'Aporrhais mainensis\n', 'Anodontia\n', 'Pitar morrhuana\n', 'Erycinidae\n', 'Chrysallida\n', 'Papyridea\n', 'Bornia longipes\n', 'Thais imbricatus\n', 'Alabina\n', 'Mysella pedroana\n', 'Anadara ovalis\n', 'Pollia\n', 'Cleodora exacuta\n', 'Corbula rosea\n', 'Acanthopleura\n', 'Pandora trilineata\n', 'Cylichna\n', 'Pyramidella adamsi\n', 'Diplodontidae\n', 'Octopus burryi\n', 'Brachidontes adamsianus\n', 'Crenella decussata\n', 'Cypraeolina\n', 'Pinna haudignobilis\n', 'Rissoina bryerea\n', 'Cardiomya multicostata\n', 'Peracle\n', 'Labiosa canaliculata\n', 'Phacoides nuttalli\n', 'Crassispira sanibelensis\n', 'Pyrgiscus\n', 'Rissoina sagraiana\n', 'Ischnochiton cooperi\n', 'Botula fusca\n', 'Tellina iris\n', 'Epitonium eburneum\n', 'Gymnosomata\n', 'Turritella variegata\n', 'Papyridea semisulcata\n', 'Melongena corona\n', 'Torcula\n', 'Musculus discors\n', 'Acanthochitona pygmaeus\n', 'Chemnitzia\n', 'Abra profundorum\n', 'Aplysia perviridis\n', 'Arene venustula\n', 'Tegula marcida\n', 'Alabina diegensis\n', 'Aptyxis luteopicta\n', 'Mytilus\n', 'Neosimnia acicularis\n', 'Linga\n', 'Drupa nodulosa\n', 'Caecum cayosense\n', 'Dischides\n', 'Conus spurius atlanticus\n', 'Amiantis callosa\n', 'Rhizorus aspinosus\n', 'Fraginae\n', 'Rissoina decussata\n', 'Anomiidae\n', 'Spirula spirula\n', 'Fusinus barbarensis\n', 'Dentalium antillarum\n', 'Ceratostoma foliatum\n', 'Prunum limatulum\n', 'Periploma fragile\n', 'Liotia cookeana\n', 'Aequipecten irradians amplicostatus\n', 'Barnea costata\n', 'Machaeroplax\n', 'Donax californica\n', 'Homalopoma linnei\n', 'Cingula kyskensis\n', 'Petaloconchus irregularis\n', 'Haminoea solitaria\n', 'Argonauta argo\n', 'Ringicula\n', 'Rissoina\n', 'Argonauta americana\n', 'Siliqua media\n', 'Tellina texana\n', 'Dentalium semiostriolatum\n', 'Chamidae\n', 'Amphithalamus tenuis\n', 'Hinnites multirugosus\n', 'Pododesmus\n', 'Retusa turrita\n', 'Strombidae\n', 'Pomaulax\n', 'Siliquaria\n', 'Clinocardium fucanum\n', 'Trochita radians\n', 'Verticordia ornata\n', 'Neptunea lyrata\n', 'Cerithium eburneum\n', 'Cryptomya californica\n', 'Elephantanellum\n', 'Bittium attenuatum\n', 'Murex erinaceoides rhyssus\n', 'Janthina janthina\n', 'Marginella philtata\n', 'Heterodonax bimaculata\n', 'Lima dehiscens\n', 'Musculus niger\n', 'Argina\n', 'Crepidula maculosa\n', 'Latirus mcgintyi\n', 'Kellia laperousi\n', 'Lucapina adspersa\n', 'Ancistrosyrinx radiata\n', 'Aplysia floridensis\n', 'Persicula politula\n', 'Lacuna solidula\n', 'Pleuroploca papillosa\n', 'Haliotis revea\n', 'Solemya\n', 'Ocenebra atropurpurea\n', 'Compsomyax subdiaphana\n', 'Dentalium calamus\n', 'Panope globosa\n', 'Schizotrochus\n', 'Rissoina kelseyi\n', 'Carinaria\n', 'Astraea\n', 'Haliotis diegoensis\n', 'Leucozonia nassa\n', 'Philine lineolata\n', 'Onoba\n', 'Turbo\n', 'Spisula hemphilli\n', 'Mysella\n', 'Semele rubropicta\n', 'Rubellatoma\n', 'Apolymetis\n', 'Teinostoma cryptospira\n', 'Mitra fergusoni\n', 'Amicula\n', 'Olivella\n', 'Terebra concava\n', 'Cavolina inflexa\n', 'Tindaria\n', 'Nassarius vibex\n', 'Onchidella carpenteri\n', 'Distorsio clathrata\n', 'Polinices duplicatus\n', 'Pyrulofusus\n', 'Myoforceps\n', 'Murex messorius\n', 'Trachycardium\n', 'Phalium centriquadrata\n', 'Dentalium pilsbryi\n', 'Entoconchidae note\n', 'Acteon punctostriatus\n', 'Mitrella\n', 'Tonicella\n', 'Austrotrophon\n', 'Acar\n', 'Corbula swiftiana\n', 'Tethys\n', 'Argonauta\n', 'Rupellaria tellimyalis\n', 'Gastropteron meckeli\n', 'Crepidula\n', 'Mytilimeria nuttalli\n', 'Cadulus mayori\n', 'Bulla occidentalis\n', 'Tellina punicea\n', 'Amicula stelleri\n', 'Retusa\n', 'Nuculana minuta\n', 'Krebsia\n', 'Cenchritis\n', 'Chione californiensis\n', 'Turbonilla stricta\n', 'Forreria pinnata\n', 'Isognomon\n', 'Acmaea tessulata\n', 'Tagelus gibbus\n', 'Cryptoconchus floridanus\n', 'Acanthochitona\n', 'Neosimnia inflexa\n', 'Psephidia\n', 'Nassarius perpinguis\n', 'Gibberulina pyriformis\n', 'Epitonium tollini\n', 'Cardita floridana\n', 'Anomalodesmacea\n', 'Busycon\n', 'Nuculana vaginata\n', 'Astarte nana\n', 'Cyclotellina\n', 'Xenophora radians\n', 'Dentalium occidentale\n', 'Cypraea moneta\n', 'Voluta\n', 'Acteocinidae\n', 'Cyclocardia\n', 'Lunatia triseriata\n', 'Aplysia willcoxi\n', 'Lonchaeus\n', 'Raeta canaliculata\n', 'Calliostoma roseolum\n', 'Trivia quadripunctata\n', 'Petricola\n', 'Miralda\n', 'Cuspidaria rostrata\n', 'Clinocardium nuttalli\n', 'Phalium peristephes\n', 'Emarginula phrixodes\n', 'Murex hidalgoi\n', 'Nodilittorina tuberculata\n', 'Ocenebra\n', 'Cardita carpenteri\n', 'Paroctopus\n', 'Haliotis lusus\n', 'Boreotrophon scalariformis\n', 'Anachis obesa\n', 'Calliostoma jujubinum\n', 'Glycymeris spectralis\n', 'Tagelus affinis\n', 'Acmaea fungoides\n', 'Crassispirella\n', 'Buccinum baeri\n', 'Erato\n', 'Barbarofusus\n', 'Turritella acropora\n', 'Teredo navalis\n', 'Neritina sphaera\n', 'Mya arenaria\n', 'Mitra swainsoni antillensis\n', 'Lolliguncula hemiptera\n', 'Charonia tritonis\n', 'Panope generosa\n', 'Perotrochus quoyanus\n', 'Aequipecten mayaguezensis\n', 'Tellina idae\n', 'Turbonilla buttoni\n', 'Mitra hendersoni\n', 'Bulla gouldiana\n', 'Colubraria\n', 'Brachidontes recurvus\n', 'Eulithidium rubrilineatum\n', 'Corbula disparilis\n', 'Janthina fragilis\n', 'Spiroglyphus\n', 'Hyalina\n', 'Aclididae\n', 'Cuspidaria jeffreysi\n', 'Pteria\n', 'Leptothyra\n', 'Bankia mexicana\n', 'Acmaea triangularis\n', 'Oliva sayana\n', 'Lischkeia\n', 'Lucina leucocyma\n', 'Siliqua nuttalli\n', 'Ostrea cristata\n', 'Onchidiidae\n', 'Littorina sitkana\n', 'Thracia trapezoides\n', 'Opisthobranchia\n', 'Tectarius tuberculatus\n', 'Calyptraea candeana\n', 'Pycnodonta hyotis\n', 'Acmaeidae\n', 'Rossia\n', 'Macoma indentata\n', 'Tellina tener\n', 'Odostomia helga\n', 'Limopsis minuta\n', 'Terebra flammea\n', 'Haminoea elegans\n', 'Volutopsius harpa\n', 'Lyonsia arenosa\n', 'Haliotis bonita\n', 'Chiton stokesi\n', 'Ancula\n', 'Caecum occidentale\n', 'Olividae\n', 'Arctica islandica\n', 'Bankia fimbriatula\n', 'Lima inflata\n', 'Phylloda squamifera\n', 'Nerita variegata\n', 'Nuttallina\n', 'Adesmacea\n', 'Neosimnia uniplicata\n', 'Cratena\n', 'Gaza watsoni\n', 'Prunum\n', 'Diaphana\n', 'Conus floridanus burryae\n', 'Venericardia redondoensis\n', 'Ischnochiton regularis\n', 'Turtonia minuta\n', 'Anadara chemnitzi\n', 'Turritella cooperi\n', 'Cavolina minuta\n', 'Anadara incongrua\n', 'Diastomidae\n', 'Urosalpinx perrugata\n', 'Rehderia\n', 'Strioturbonilla\n', 'Littorina irrorata\n', 'Gibberulina lacrimida\n', 'Tenagodus squamatus\n', 'Pyrula papyratia\n', 'Crassinella lunulata\n', 'Caecum\n', 'Ocenebra stearnsi\n', 'Odostomia modesta\n', 'Nassarius cooperi\n', 'Neverita\n', 'Calliostoma bairdi\n', 'Lucina\n', 'Acmaea scutum\n', 'Murex gemma\n', 'Epitonium commune\n', 'Megayoldia\n', 'Margarites\n', 'Cymatium gracile\n', 'Diaphanidae\n', 'Tagelus plebeius\n', 'Styliola conica\n', 'Hiatella pholadis\n', 'Pododesmus rudis\n', 'Opalia crenimarginata\n', 'Vesica\n', 'Chama congregata\n', 'Cylichna gouldi\n', 'Spisula solidissima\n', 'Barbatia domingensis\n', 'Cerithium muscarum\n', 'Crucibulum\n', 'Martesia cuneiformis\n', 'Solariella lacunella\n', 'Mopalia lignosa\n', 'Littorina meleagris\n', 'Nassarius obsoletus\n', 'Idioraphe\n', 'Donax denticulata\n', 'Milneria kelseyi\n', 'Searlesia dira\n', 'Aloidis\n', 'Neritina weyssei\n', 'Siliqua\n', 'Monilispira albomaculata\n', 'Corbula porcella\n', 'Odostomia farella\n', 'Potamididae\n', 'Volsella plicatula\n', 'Latirus brevicaudatus\n', 'Noetia\n', 'Zaphon\n', 'Arca reticulata\n', 'Pitar dione\n', 'Chrysodomus lirata\n', 'Murexiella\n', 'Mancinella\n', 'Amiantis\n', 'Persicula regularis\n', 'Lacuna striata\n', 'Veneridae\n', 'Sthenorytis pernobilis\n', 'Ischnochiton floridanus\n', 'Cerithidea costata\n', 'Platyodon cancellatus\n', 'Cleodora\n', 'Prunum guttatum\n', 'Spisula voyi\n', 'Conus clarki\n', 'Aequipecten irradians\n', 'Trichotropis insignis\n', 'Astralium\n', 'Prunum apicinum\n', 'Glycymeris pennacea\n', 'Conus daucus\n', 'Batillaria minima\n', 'Mitridae\n', 'Polyschides\n', 'Barbatia barbata\n', 'Pitar fulminata\n', 'Fissurella fascicularis\n', 'Acirsa\n', 'Stylidium\n', 'Cadlina flavomaculata\n', 'Lacuna unifasciata\n', 'Amaea retifera\n', 'Mitra idae\n', 'Hyalaea limbata\n', 'Murex petri\n', 'Gastropteron\n', 'Verticordia fisheriana\n', 'Raeta\n', 'Nuttallina scabra\n', 'Noetia ponderosa\n', 'Lepidopleuroides\n', 'Muricopsis floridana\n', 'Cypraea cervus\n', 'Spengleria rostrata\n', 'Liophora\n', 'Acmaea depicta\n', 'Phyllonotus\n', 'Epitonium lamellosum\n', 'Clio balantium\n', 'Solecurtus cumingianus\n', 'Periploma papyratium\n', 'Lucapinella\n', 'Boreomelon\n', 'Fissurella volcano\n', 'Rissoina dalli\n', 'Allopora californica\n', 'Ostrea rufoides\n', 'Cerithiopsis greeni\n', 'Epitonium humphreysi\n', 'Lischkeia ottoi\n', 'Malletiidae\n', 'Spiratella balea\n', 'Cyathodonta pedroana\n', 'Hinia\n', 'Cavolina elongata\n', 'Rocellaria\n', 'Antigona strigillina\n', 'Lepeta caeca\n', 'Hipponix subrufus subrufus\n', 'Bursa thomae\n', 'Petrasma\n', 'Cingula montereyensis\n', 'Marginella eburneola\n', 'Ocenebra interfossa\n', 'Homalopoma carpenteri\n', 'Octopoda\n', 'Acmaea candeana\n', 'Pseudochama radians\n', 'Pyrunculus caelatus\n', 'Ivara\n', 'Distorsio floridana\n', 'Venericardia tridentata\n', 'Nautilus pompilius\n', 'Poromya granulata\n', 'Carditamera\n', 'Cavolina inermis\n', 'Spiroglyphus lituellus\n', 'Odostomia phanea\n', 'Atlantidae\n', 'Architectonica\n', 'Nuculana sculpta\n', 'Neptunea\n', 'Brachidontes\n', 'Solen\n', 'Oxygyrus keraudreni\n', 'Acmaea antillarum\n', 'Cancellaria adelae\n', 'Erato vitillina\n', 'Lamellariidae\n', 'Psammocola\n', 'Irus lamellifera\n', 'Cirsotrema\n', 'Lepidopleurus cancellatus\n', 'Gibberulina\n', 'Aequipecten phrygium\n', 'Pandora carolinensis\n', 'Varicorbula operculata\n', 'Litiopa\n', 'Scissurellidae\n', 'Mesopleura\n', 'Glycymeris\n', 'Polystira\n', 'Anomalocardia cuneimeris\n', 'Planaxis lineatus\n', 'Polycera atra\n', 'Yoldia\n', 'Liotia\n', 'Cuvierina\n', 'Caecum hemphilli\n', 'Susania\n', 'Pinctada radiata\n', 'Astarte\n', 'Conus regius\n', 'Cymatium prima\n', 'Olivella intorta\n', 'Trigonostoma rugosum\n', 'Carditidae\n', 'Volutidae\n', 'Cymatium aquitile\n', 'Ostrea edulis\n', 'Ividella\n', 'Placopecten\n', 'Astarte subequilatera\n', 'Barbatia cancellaria\n', 'Tonna perdix\n', 'Panomya ampla\n', 'Fulguropsis\n', 'Dorytewthis plei\n', 'Bullaria\n', 'Laevicardium laevigatum\n', 'Architeuthis\n', 'Astraea imbricata\n', 'Anodontia schrammi\n', 'Teinostoma leremum\n', 'Limacina scaphoidea\n', 'Dendronotus frondosus\n', 'Antalis\n', 'Margarites lirulatus\n', 'Cardita gracilis\n', 'Nuculana fossa\n', 'Cavolina quadridentata\n', 'Penitella sagitta\n', 'Prunum roosevelti\n', 'Purpura patula\n', 'Coryphella rufibranchialis\n', 'Caecum crebricinctum\n', 'Volsella capax\n', 'Sthenorytis cubana\n', 'Mercenaria campechiensis\n', 'Tellina agilis\n', 'Cavolina angulata\n', 'Acmaea\n', 'Sulcosipho\n', 'Pteria colymbus\n', 'Acanthodoris pilosa\n', 'Olivella baetica\n', 'Mactra californica\n', 'Cardiomya\n', 'Epitonium foliaceicostum\n', 'Brachidontes stearnsi\n', 'Circinae\n', 'Martesia\n', 'Crassispira ebenina\n', 'Aeolidiidae\n', 'Conus granulatus\n', 'Aplysidae\n', 'Eubranchus pallidus\n', 'Transennella tantilla\n', 'Odostomia terricula\n', 'Dendronotidae\n', 'Natica\n', 'Lucinidae\n', 'Semele cancellata\n', 'Bursa spadicea\n', 'Calliostoma euglyptum\n', 'Polinices altus\n', 'Graptacme\n', 'Yoldia myalis\n', 'Sigatica holograpta\n', 'Busycon carica\n', 'Acmaea cubensis\n', 'Teinostoma pilsbryi\n', 'Pitarenus\n', 'Tivela\n', 'Barbatia bailyi\n', 'Semele purpurascens\n', 'Transennella stimpsoni\n', 'Diodora murina\n', 'Gutturnium\n', 'Acmaea tenera\n', 'Cirsotrema dalli\n', 'Pneumoderma\n', 'Macoma souleyetiana\n', 'Panomya arctica\n', 'Purpura crispata\n', 'Psammosolen\n', 'Moerella\n', 'Sanguinolaria\n', 'Maxwellia\n', 'Herse columnella\n', 'Mangeria\n', 'Coralliophila hindsi\n', 'Placopecten magellanicus\n', 'Amauropsis islandica\n', 'Conus juliae\n', 'Acmaea digitalis\n', 'Inodrillia aepynota\n', 'Sinum scopulosum\n', 'Fissurella crucifera\n', 'Muricanthus\n', 'Cassis tuberosa\n', 'Nitidella ocellata\n', 'Arca balesi\n', 'Isognomon alata\n', 'Pecten caurinus\n', 'Antigona rigida\n', 'Diaphana minuta\n', 'Caecum nitidum\n', 'Rocellaria ovata\n', 'Gemma gemma\n', 'Melanella bilineata\n', 'Eupleura etterae\n', 'Tellina promera\n', 'Epilucina\n', 'Mitrella tuberosa\n', 'Nitidella cribraria\n', 'Melanella gracilis\n', 'Ostrea lurida\n', 'Anomia\n', 'Echinochama\n', 'Gibberulina ovuliformis\n', 'Tonnidae\n', 'Jumala\n', 'Pedicularia californica\n', 'Vitrinella beaui\n', 'Pediculariella\n', 'Planaxis nucleus\n', 'Caecum grippi\n', 'Caecum diegense\n', 'Triphora perversa\n', 'Evalina\n', 'Peracle physoides\n', 'Anomia aculeata\n', 'Cadulus carolinensis\n', 'Scaphella schmitti\n', 'Tapes bifurcata\n', 'Cavolina intermedia\n', 'Dendrodoris\n', 'Musculus laevigatus\n', 'Lolliguncula brevis\n', 'Calliostoma zonamestum\n', 'Macoma inquinata\n', 'Pedicularia decussata\n', 'Murex carpenteri\n', 'Here\n', 'Cancellaria conradiana\n', 'Murex trialatus\n', 'Conus amphiurgus\n', 'Ocenebra poulsoni\n', 'Loligo pealei\n', 'Chama firma\n', 'Atys caribaea\n', 'Anomia simplex\n', 'Sinum perspectivum\n', 'Saxidomus\n', 'Pseudomalaxis nobilis\n', 'Diaphana globosa\n', 'Acteon vancouverensis\n', 'Rubellatoma rubella\n', 'Erato columbella\n', 'Kurtziella limonitella\n', 'Tricolia affinis\n', 'Pelecypoda\n', 'Illex illecebrosus\n', 'Zeidora\n', 'Arcidae\n', 'Margaritifera\n', 'Psammobia\n', 'Angulus\n', 'Petricola pholadiformis\n', 'Eratoidae\n', 'Littorina ziczac\n', 'Tachyrhynchus erosum\n', 'Conus stearnsi\n', 'Littorina scabra\n', 'Apolymetis biangulata\n', 'Hipponix antiquatus\n', 'Cancellaria crawfordiana\n', 'Cumingia californica\n', 'Tellina versicolor\n', 'Lasaea cistula\n', 'Ficidae\n', 'Crossata\n', 'Gyroscala\n', 'Gemma\n', 'Neosimnia variabilis\n', 'Labiosa lineata\n', 'Limacina\n', 'Barnea truncata\n', 'Anatina Schumacher\n', 'Megathura crenulata\n', 'Brachidontes exustus\n', 'Velutina undata\n', 'Rissoina bakeri\n', 'Onchidella borealis\n', 'Evalea\n', 'Hipponicidae\n', 'Planaxidae\n', 'Morum oniscus\n', 'Entemnotrochus\n', 'Amaea\n', 'Codakia filiata\n', 'Calloplax janeirensis\n', 'Busycon contrarium\n', 'Neosimnia piragua\n', 'Vermicularia knorri\n', 'Antigona rugatina\n', 'Agriopoma\n', 'Colubraria lanceolata\n', 'Calliostoma canaliculatum\n', 'Olivella mutica\n', 'Apolymetis intastriata\n', 'Tivela floridana\n', 'Acanthina lapilloides\n', 'Oudardia\n', 'Scaphella\n', 'Nassarius fossatus\n', 'Tellina elucens\n', 'Colubraria testacea\n', 'Laevicardium pictum\n', 'Fissurella barbadensis\n', 'Cantharus auritula\n', 'Rossia pacifica\n', 'Fusinus\n', 'Hipponix\n', 'Lucapina sowerbii\n', 'Philine sagra\n', 'Strigilla pisiformis\n', 'Mytilus plicatulus\n', 'Pandora bilirata\n', 'Tricolia\n', 'Solecurtus sanctaemarthae\n', 'Acmaea leucopleura\n', 'Astraea undosa\n', 'Sthenorytis\n', 'Chiton tuberculatus\n', 'Anachis translirata\n', 'Crepidula acuta\n', 'Actaeon\n', 'Melongenidae\n', 'Octopus bimaculoides\n', 'Spiratella pacifica\n', 'Schizothaerus nuttalli\n', 'Yoldia limatula gardneri\n', 'Turritella exoleta\n', 'Gibberula\n', 'Cryptochiton stelleri\n', 'Pinnidae\n', 'Limopsis\n', 'Phacoides jamaicensis\n', 'Euvola\n', 'Eucrassatella floridana\n', 'Cerithiopsis emersoni\n', 'Epitonium indianorum\n', 'Teinostoma\n', 'Bellucina\n', 'Lima tenera\n', 'Murex festivus\n', 'Hyalina californica\n', 'Nerita peloronta\n', 'Margarites parcipictus\n', 'Colubraria swifti\n', 'Chlamys hindsi\n', 'Tellina lutea\n', 'Loligo\n', 'Triphora\n', 'Septibranchia\n', 'Tellina candeana\n', 'Mysella golischi\n', 'Strigilla\n', 'Vitta\n', 'Persicula lavelleana\n', 'Dentalium floridense\n', 'Charonia tritonis nobilis\n', 'Scala\n', 'Dissentoma\n', 'Hydatinidae\n', 'Trivia californiana\n', 'Aequipecten\n', 'Tindaria brunnea\n', 'Ostreidae\n', 'Trophonopsis\n', 'Styliola\n', 'Turbinidae\n', 'Urosalpinx\n', 'Solariella obscura\n', 'Acmaea cribraria\n', 'Neritina virginea\n', 'Anadara campechiensis\n', 'Fulgur\n', 'Ocenebra lurida\n', 'Monilispira leucocyma\n', 'Boreotrophon\n', 'Protothaca laciniata\n', 'Haminoea vesicula\n', 'Teinostoma parvicallum\n', 'Bursa affinis\n', 'Tagelus subteres\n', 'Thais rustica\n', 'Collisella\n', 'Crepidula fornicata\n', 'Macoma planiuscula\n', 'Metaplysia\n', 'Crassostrea brasiliana\n', 'Cardiomya gemma\n', 'Barnea\n', 'Narona cooperi\n', 'Coralliophila costata\n', 'Retusidae\n', 'Eontia\n', 'Neptunea bicincta\n', 'Tergipedidae\n', 'Hinnites\n', 'Cyathodonta\n', 'Pleurobranchus\n', 'Haminoea glabra\n', 'Urosalpinx tampaensis\n', 'Herse\n', 'Epitonium spina-rosae\n', 'Phacoides\n', 'Odostomia seminuda\n', 'Calliostoma splendens\n', 'Acmaea spectrum\n', 'Hipponix benthophila\n', 'Buccinum\n', 'Murex tryoni\n', 'Puncturella noachina\n', 'Glossodoris\n', 'Bursa corrugata\n', 'Laevicardium serratum\n', 'Lunatia lewisi\n', 'Teredinidae\n', 'Septifer\n', 'Cyphoma signatum\n', 'Ancula cristata\n', 'Creseis vitrea\n', 'Conus jaspideus\n', 'Clionopsis\n', 'Cypraea zebra\n', 'Navicula ostrearia\n', 'Strigilla rombergi\n', 'Acanthopleura flexa\n'])

>>>
whole_list_filt = [a for a in mn if(a[0].isupper() and a[1:].islower() and len(a.split(" ")) <= 3)]

master_list_words = master_list.split("\n")

p_names = [ a.split(" ") for a in whole_list_filt]

fp_names = [b for a in p_names for b in a]

fp_names = [ a.lower() for a in fp_names if(not "." in a)]
 
intersection_se = se & dict_words_set
------
master_list = open("/Users/anna/work/web_app/perl_tf/py_server/master_words.txt").read()

master_list_words = master_list.split("\n")

master_list_words_small = [a.lower() for a in master_list_words]

master_words_set = set(master_list_words_small)

intersection_se = master_list_words_set & dict_words_set

 len(intersection_se)
-------


master_list_words = master_list.split("\n")
>>> master_list_words_small = [a.lower() for a in master_list_words]
>>> master_words_set = set(master_list_words_small)
>>> dict_list = open("/Users/anna/work/web_app/perl_tf/py_server/Nnewlist.txt").read()
>>> dict_list_words = dict_list.split("\n")
>>> dict_set = set(dict_list_words)

>>> "wild" in dict_listTrue
>>> f = open('/Users/anna/work/web_app/perl_tf/py_server/int1.txt','w')
---------
> f.close()
>>> f = open('/Users/anna/work/web_app/perl_tf/py_server/cleaned_dict.txt','w')
>>> for n in cleaned_dict_set:
...     f.write(n)
...     f.write("\n")
... 
>>> f.close()

