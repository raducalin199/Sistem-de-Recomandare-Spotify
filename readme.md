DUMITRU RADU-CALIN

# Sistem de recomandare de muzica utilizand Spotify API si ML

# Introducerea temei:

In zilele noastre, muzica se aude la orice colt de lume. Fie ca este vorba de spatiile noastre personale sau publice, ea ne influenteaza foarte mult starea in timpul activitatilor de zi cu zi. Si nu cred ca exista o aplicatie care sa produca un asemenea impact, in ceea ce priveste starea noastra personala asa cum procedeaza Spotify

Spotify reprezinta o aplicatie de streaming audio prin care i se permite utilizatorului nu doar sa-si asculte piesele preferate pe banda rulanta, dintr-o selectie fascinanta de genuri si artisti, dar de aseamana ii poate permite sa-si compune propriile playlisturi. Ceea ce apreciez foarte mult la aceasta aplicatie este faptul ca acesta poate sa furnizeze playlisturi avand diferite tipuri de clasificari, de la clasificarile standard precum cele ce tin de genul muzical sau de perioada in care a aparut melodia, la clasificari mai fine, mai subiective, care exploreaza mai mult starea pe care vrea sa ti-l ofere pe care o asculti. Si studiind despre aceasta problema, am constatat faptul ca, la fel ca orice aplicatie moderna, sunt utilizati algoritmi de Machine Learning cu scopul de a contura preferintele utilizatorilor si de a prezice melodii care sa se potriveasca stilului sau starii de ceea utilizatorul asculta.

O alta functie pe care am studiat-o in alcatuirea proiectului a fost si ceea de playlisturi radio, prin care pornind de la o melodie a unui artist sau de la artistul in sine, Spotify adduce alte piese similare cu cea sus mentionata, precum si alte melodii din repertoriul sau. Asa ca intentia mea pentru acest proiect a fost sa creez un sistem de recomandari de piese pe Spotify care sa imite aceste functionalitati

# Etapele proiectului

1.
## Prelucrarea si aprovizionarea cu resurse

Pentru a incepe proiectul, a trebuit sa stochez un numar semnificativ de melodii provenite din playlisturi si care sa incorporeze cat mai multe genuri cu putinta. Initial m-am gandit sa apelez la un set gata facut de pe Kaggle, care avea cam tot ce trebuie in materie de proprietati si de numar de piese(vazusem la un moment ca erau stocate undeva spre ordinal milioanelor). Din nefericire, cand am intrat n-am gasit setul de date propus, asa ca a trebuit sa recurg la scrierea in cod a unor functii care sa-mi poata permita extragerea melodiilor de pe Spotify. Unealta care m-a ajutat la realizarea acestei operatiuni a fost libraria spotipy prin care se face legatura cu API-ul furnizat de cei de la Spotify. Am creat astfel urmatorul obiect care imi permite interactiunea cu acel API :

![](RackMultipart20210907-4-nm9fga_html_6fe9c86433dcf210.png)

Prin metodele de mai sus am reusit sa ma autentific la interfata de dezvoltare(este necesar sa ai un cont pe Spotify si sa ai o aplicatie deja creeata pentru a a avea accesul la prelucrarea datelor) si de asemenea sa preiau pana la peste 15000 de piese(Spotify impune o limita de pana la maximum 10000 de piese pe playlist asa ca a trebuit sa fac cu randul). Toate datele preluate au fost stocate in 2 2 csv-uri: unul cu datele meta si celalalt cu proprietatile uzuale ale melodiilor(de ex.instrumentalness, speechness, danceability, etc). ![](RackMultipart20210907-4-nm9fga_html_ea4ac41a270ce676.png)

1.
## Antrenarea setului de date

Acum ca avem setul de date pregatit, m-am gandit ce metoda sa pot folosi pentru a crea un model cat mai viabil penru a forma playlisturi cat mai clare. Am folosit metode prin care am determinat numarul optim de grupuri de piese, avand in vedere faptul ca nu aveam un set foarte mare de date cat sa pot sa aplic antrenamente de date folosind retele neurale. Prima metoda folosita a fost calcularea PCA-ului(analiza de componenta principala. Am facut transformarea urmatoarelor coloane:

![](RackMultipart20210907-4-nm9fga_html_c0f7ab96b5f4d9e1.png)

-fiecare rand reprezinta proprietatile de masurat pentru fiecare melodie stocata

![](RackMultipart20210907-4-nm9fga_html_18ff3386c4f0729c.png)

-aici am aplicat transformare prin scalare folosind scalarea in minim si maxim(scalarea fiecarei proprietati in limitele date)

Cu ajutorul rezultatelor din PCA a rezultat urmatorul grafic 3D, unde am luat in considerare numarul de grupuri de 5 calculat folosind Kmeans:

![](RackMultipart20210907-4-nm9fga_html_ac6f2733a410210b.png)

Am considerat ca numarul de grupuri, conform graficului, se potriveste cu ceea ce imi doream.

Cele 5 grupuri reprezinta categoria principala a pieselor. Problema este ca sunt pana la 3000 de piese in unele grupuri, asa ca a trebuit sa alimentezi setul de date folosit(&#39;muzica&#39;) cu alte coloane precum tempo, durata cantecului si anul aparitiei si am reapelat Kmeans. Urmatoarea clasare a fost determinate prin metoda Silhouette(desi graficul imi dadea puncta mai joase, am ales numarul care determina distantele cele mai mici). Am constatat faptul ca va fii necesara o impartire in 200 de categorii mijlocii. Ultima categorie consta scalare standard a tuturor datelor numerice colectate, si impartirea in 280 de piese cu scopul de a putea avea cel putin 50 de piese per playlist.

1.
## Creearea de playlisturi

Avand la indemana toate transformarile si grupele create, a urmat partea cea mai interesanta a acestui si anume crearea playlistului. Apeland inca o data la conexiunea cu API-ul celor de la Spotify, am creeat urmatoarele metode prin care sa-mi pot crea playlisturile asa cum mi-am dorit. Mai intai am testat metodele prin care sa pot creea playlisturi folosind piese deja existente in setul de date. Asa ca luand la intamplare cel putin o piesa, am reusit sa creez un playlist de piese care sa apartina unei clase mai mici si atunci cand sunt luate toate piesele din clasa repsectiva, sa preia piesele de la cea mai apropiata clasa fata de ultima piesa selectata.

O alta de idee de creeare de playlisturi la care m-am gandit intre timp tine cont maim ult de distantele dintre melodii. Astfel, fiecare melodie are, datorita calculelor facute in sectiunea precedenta, inca 2 valori: cea mai scurta distanta de la punct si indexul vecinului celui mai apropiat. Playlisturile create vor avea cate o limita stabilita de numar de piese. De asemenea, am luat in considerare si ideea de a folosi muzica salvata de utilizator ca set de date pentru crearea acestor tipuri de liste.

Crearea propriu-zisa de playlisturi se refera la preluarea variabilelor returnate din apelul functiilor noastre si convertirea acestora in playlisturi Spotify folosind API-ul.

1.
## Alte Observatii

In afara crearii de liste, am mai facut si niste analize pe baza relatiilor dintre proprietatile unei melodii.

Aceasta constatare s-a facut folosind un heatmap:

![](RackMultipart20210907-4-nm9fga_html_3fc59d2dc96e0544.png)

Conform diagramei de mai sus vedem faptul ca sunt influente mult mai puternice in ceea ce privesc relatiile dintre zgomot(loudness) si energie – scor 0.8

- Valenta si dansabilitate – 0.5
- Acusticitate si instrumentalitate – 0.5

De asemenea, se remarca faptul ca acusticitatea nu determina deloc nivelul de energie transmis intr-o piesa si se opune zgomotului. Acelasi lucru putem spune si despre nivelul de muzicitate(instrumentalness) .

# Concluzii

Toate metodele explicate si implementate pentru acest se concentreaza asupra melodiilor pe care le-ar asculta un utlizator. Iar pentru viitor, mi-ar placea sa explor mai mult cu aceste proprietati cu conditia de a incerca si o comparare a playlisturilor altor utlizatori. Am in plan crearea unor metode care sa permita crearea unei liste de recomandari in cazul pieselor preferate oferite de mai multi utilizatori.