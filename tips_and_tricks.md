# Tips and tricks

- Taskurile sunt facute de oameni. CTF-urile sunt atat jocuri tehnice cat si psihologice. Asta implica (cel putin) 2 chestii:
    - Oamenii pot gresi -> pot exista si solutii unintended (fie mai usoare fie mai grele)
    - Ca teoretic ai putea sa faci un reverse engineering pe thought process sa te prinzi de unde a scos problema si ce vrea de la tine
        - In general taskurile mai au un context care poate da de gol multe informatii:
            - Nume:
            - Cerinta, Descriere
            - Numar puncte (daca sunt cotate corect nu are rost sa faci super exploit pt ceva de 50p)


- Din ce am vazut, anul trecut au fost cateva taskuri de "actualitate": cele de compression side channel care erau in trend cu atacurile BEAST, CRIME, BREACH, etc. Pentru alea deja se gasea cod scris, explicat plus paper. Poate gasiti si anul asta ceva de actualitate cu bucati partial scrise
- De asemenea, trebuie sa va ganditi ca la cate taskuri de CTF au fost pana acum, e posibil sa existe deja rezolvare ori la un task asemanator ori la o subproblema din taskul curent.  Poate autorul chiar la asta s-a gandit si a facut taskul multi-stage ca sa fie mai greu. In cazul asta e evident ca n-o sa ai timp sa faci toate stage-urile daca le iei de la zero (time is precious).
- Legat de writeupuri, daca nu mai e un site online, incercati google cache. Daca nici asa atunci poate e arhivat pe https://web.archive.org


## Exploit
- nu uitati conventiile de apel al functiilor:
    - x86: pe stiva
    - x86_64 in registri (dar difera ordinea pe linux si pe windows)
- si pt syscalluri (when in doubt check http://security.cs.pub.ro/hexcellents/wiki/)
- intai jucati-va cu programul sa incepeti reversingul cu mai multa informatie asupra functionalitatii
- daca reusiti sa-l faceti sa crape si mai bine (dar nu va opriti la primul crash, poate sa fie red herring)
- explorati toate caile programului, nimic nu e pus intamplator (am patit-o o data cu un task unde vulnerabilitatea era in partea de Help unde nu se uita nimeni)
- daca e un binar linkat static
    - vedeti stubul initial care apeleaza libc_start_main + main + constructori + destructori si incepeti de acolo.
    - compilati de mana un program linkat static si deschideti in paralel in IDA/Hopper si vedeti cum arata puts, printf, malloc, etc
- luati in considerare urmatoarele diferente
    - daca taskul e direct pe un port versus ssh ;pe ssh e mai greu de facut setupul deci posibil sa existe o noima (un ulimit, un shellcode in ENV, alte smecherii)
    - daca taskul e redirectat pe port versus daca deschide el un socket si accepta conexiuni; in cazul 2 se refoloseste spatiul de adresa => ASLR e usor de scos, canary-ul poate fi scos byte cu byte daca ai un overflow variabil
- NU cititi tot codul de asamblare linie cu linie din prima pasa
- NU cititi tot codul de asamblare linie cu linie !!! Insist pentru ca poate cauza pierderea de foarte mult timp total aiurea.
- In schimb abordati problema de la nivel macro la nivel micro:
- vedeti ce face functia in sine , print-uri, accesari de variabile globale etc si numiti-o (sau lasati comentarii)
- redenumiti variabilele: atat globale cat si pe stiva cat mai sugestiv
- comasati array-urile
- faceti structuri
- Uitati-va orientativ pe codul C scos de hopper (pentru chestii macro de functionalitate, control flow dar si pentru chestii micro gen folosirea de variabile fara semn unde trebuiau cu semn etc)
- Dupa ce ati gasit vulnerabilitatea vedeti daca depinde de sistemul remote (adica daca n-are system sau binsh importate probabil va trebuie libc-ul). Fie refolositi un task anterior de exploit rezolvat (sau un ssh) pentru investigatii fie leakuiti un GOT rezolvat si vedeti cu libc-database
- Daca merge local si nu merge remote incercati sa debug-uiti direct remote dar aveti grija sa nu va fure altii munca:
    - verificati unde poti scrie "anonim" gen in /tmp (ls pe /tmp ar trebui sa nu mearga), numele directoarelor sa fie neghicibile
    - verificati ca nu se logheaza history
    - verificati ca /proc nu e montat. Daca e montat atunci poti sa vezi userii pe unde sunt si ce fac fie din /proc/pid/cwd fie din top.
    - vedeti dmesg-ul (asta e putin in the gray zone): daca gasiti crashuri la o adresa care e din program (0x0804.... sau 0x40.... ) e posibil si probabil sa fie acolo vulnerabilitatea pt binarul respectiv
    - Daca merge oricare din anterioarele, alertati-i pe organizatori sa repare
- Daca vi se da codul si e foarte mult luati in considerare ca probabil nu l-au scris ei, ci l-au luat de undeva open source (eventual github), cautati-l si vedeti unde a fost modificat pentru eventuale leaduri.

## Crypto
- la RSA de obicei se dau multe informatii despre un modulus (N)  gen
    - mai multe mesaje criptate cu acelasi N si exponent mic  (rezolvat cu Chinese Remainder)
    - exponent de criptare foarte mare (Wiener attack)
    - bucati (biti) din cheie  (https://github.com/ctfs/write-ups-2014/tree/master/plaid-ctf-2014/rsa)
    - mesaje criptate neindependente linar (https://ctf-team.vulnhub.com/picoctf-2014-rsa-mistakes/)

- Daca nu e una din astea puteti presupune ca e ceva legat de modulus insusi:
    - p si q apropiate -> se rezolva cu Fermat
    - p sau q comune cu altceva dat prin text
    - p si q sau N au o structura observabila si exploatabila
    - modulus deja factorizat pe factordb.com

In cel mai rau caz va trebui sa-l spargeti de mana (figurat vorbind, ca doar e pe calculator) cu tooluri:
- cryptool (nu foarte eficient)
- sage (mai eficient)
- ecm (mult mai eficient dar doar pe anumite cazuri) http://www.alpertron.com.ar/ECM.HTM

- Intotdeauna verificati side channel-urile. Poate leakuieste ceva prin delay, poate printr-o eroare (gen padding oracle) poate prin altceva mai ezoteric gen puterea consumata (http://wiki.yobi.be/wiki/CHES2015_Writeup#Second_step)


## Reversing
- investigati atat dinamic cat si static
    - ltrace (daca nu e static)
    - strace
- daca are ptrace vedeti daca foloseste rezultatul pe undeva. daca nu, poate fi scos fara probleme.
- patch-uiti din IDA fie cu octeti stiuti deja (90, C3, CD80, etc) sau scosi cu rasm2, sau direct din IDA (Assemble) si apoi puteti da Apply patches to input file (nu uitati de backupuri). Verificati functionalitatea inainte si dupa patch
- daca vedeti constante dubioase, cautati-le pe net atat in format hex cat si decimal (eventual adaugati un plugin de crypto signature search direct in ida) ca ar putea fi chestii comune de genul MD5, sha1, AES Sbox etc
- investiti un pic de timp in materialele de pe binary-auditing,com (s-ar putea sa va fie foarte util sa recunoasteti si sa interpretati corect si repede diverse tipuri de loop si if)
    - decompilatorul s-ar putea sa nu va fie intotdeauna foarte util (e.g. cod obfuscat, junk intre instructiuni, stiva nealiniata, ...)
    - movzx -> unsigned, ja/jb sunt jump conditional dupa compare pe valori unsigned
    - movsx -> signed, jg/jl sunt jump conditional dupa compare pe valori signed
    - registri de FPU
    - ar trebui sa fie si instructiuni de tipul fild/fist la inceputul/sfarsitul codului de FPU care sa va ajute sa identificati cu ce valori se lucreaza
    - stiva rotativa
    - ideea NU e sa cititi linie cu linie ASM-ul ci sa stiti pe ce portiuni sa va concentrati
- se intampla foarte des sa dati de algoritmi reversibili
    - daca se foloeseste xor/rol/add intr-o bucla de criptare de obicei poate fi decriptat relativ usor, daca are si feedback (i.e. input prin care s-a trecut e folosit la pasul urmator) s-ar putea ca decriptarea sa inceapa de la coada
    - daca algoritmul arata mai mult a hash (i.e. output de lungime fixa, indiferent de lungimea input-ului) puteti sa scrieti voi un bruteforcer sau sa folositi z3
    - in unele cazuri ar putea fi dificil sa scrieti formula in z3, daca spatiul de cautare este destul de redus puteti scrie bruteforcer
    - daca spatiul de cautare este foarte mare (e.g. un bruteforce chior ar dura foarte mult) z3 s-ar putea sa va fie de folos
- multe taskuri de tip "keygen" sau "find the key" pot avea side-channel (e.g. VM-ul de la calificari la fel ca alte challenge-uri cu VM pot avea astfel de probleme):
    - uneori side-channel-ul poate fi mai greu de identificat, aici incercati sa acordati prioritate taskurilor, aveti timp limitat
    - ar putea sa va fie foarte util sa scriptati un debugger
    - exemplele inscount* din PIN tool ar putea fi utile
- nu va temeti sa patchuiti programul daca asta va ajuta
    - daca puteti, sa scapati de rutine de debug usor sau de junk-code
    - puteti sa incercati sa dati si un trace la bucle obfuscate si apoi sa eliminati intr-un text-editor instructiunile redundante (sau sa simplificati instructiunile)
- exersati si pe executabile native de Windows (sunt sanse mari sa primiti asa ceva)
    - obisnuiti-va cu SEH (foarte frecvent folosit si ca anti-debug) si fiti atenti la registrul segment fs (SEH/TEB/PEB)
    - daca executabilul este packed cu ceva non-standard si nu puteti sa ajungeti la entrypoint poate puteti sa faceti dump la proces si asta sa va ajute
    - codul obfuscat de multe ori e generat prin macro-uri, asta inseamna ca sunt scrise de oameni deci probabil au o logica
- algoritmi de decompresie:
    - mov dl, 80h / cld la inceputul unei bucle relativ mari -> algoritm de decompresie LZ+gamma_encoding (e.g. aPLib, NRV)
    - constante de tip 400h sau 4000400h in array de dimensiune 736h / 0e6ch / 1cd8h -> LZMA
    - PEiD + KryptAnalyzer / signsrch ar putea fi util sa identificati si algoritmi de decompresie si de criptare
- problemele mai avansate de reverse pot cere cunostinte si din alte domenii (de cele mai multe ori crypto)

## Web
- in primul rand cititi cu atentie descrierea task-ului pentru ca de multe ori iti poti da seama ce vulnerabilitate trebuie sa cauti.
- verificati versiunile de software, se pot da si CVE-uri gen task-ul cu Struts2.
- uitati-va la codul sursa. De multe ori se pun hint-uri comentate in codul html al paginii web.
- incercati sa folositi un web debugger. Va recomand BurpSuite.
- aveti mare grija la encoding. Majoritatea limbajelor fac un urldecode pe valoarea parametrului accesat, dar nu fac urldecode cand obtin acea valoare din alte surse.
- Daca task-ul e unul de javascript, va recomand Firefox browser cu extensia "JavaScript Deobfuscator".
- In ceea ce priveste SQL Injection:
    - verificati daca se poate face bypass cu %bf (Korean style).
    - verificati daca puteti escapa  dintr-un parametru caracterul ' sau " si inserati cod SQL in alt parametru.
    - poate nu e filtrat nimic si puteti sa produceti un delay:
             union select SLEEP(5)--   (mysql)
             and BENCHMARK(19900000,MD5(CHAR(116)))# (mysql)
             WAITFOR DELAY '0:1:9'--  (MSQL)
             daca e  oracle cautati Oracle Heavy Queries
- Daca nu e SQL a doua problema care ar putea fi si am intalnit-o foarte des a fost un Local File Inclusion:
    - In versiunile de PHP de la 5.4 nu se mai poate comenta cu %00 # sau ?.
    - Pentru a verifica se poate folosi: php://filter/read=convert.base64-encode/resource=convert.base64-encode/resource=
    - Mai sus am folosit base64 de doua ori fiindca am avut niste probleme cu unele task-uri cand faceam doar odata base64.
    - daca nu e cod php, incercat sa comentati cu null char (%00)

- Am observat niste task-uri care presupun sa treci de un web app firewall (WAF).  Incercat sa faceti bypass cu:
    ```
    X-Forward-For: 127.0.0.1
    X-Forwarded-For: 127.0.0.2
    X-remote-IP: 127.0.0.3
    X-remote-addr: 127.0.0.4
    CLIENT_IP: 127.0.0.15
    X-originating-IP: 127.0.0.6
    ```

- Vulnerabilitatea XXE:
    - cautati locuri unde trimiteti cod xml
    - cautati locuri in care  se genereaza dinamic cod xml
    - poate puteti face upload de  .doc, .xlt, .docx, etc. Toate aceste documente sunt fisiere zip ce contin fisiere XML.
    - cand vreti sa confirmati o posibila vulnerabilitate incercati sa faceti o conexiune cu un server pe care il controlati (ascultati cu un nc -lvp 8080 pe el):
                            <?xml version="1.0" encoding="utf-8"?><!DOCTYPE roottag [ <!ENTITY send SYSTEM "http://ip.address:8080/">]><roottag>&send;</roottag>
    - daca nu merge asta, incercati sa cititi un fisier local.


## Forensics / stegano

- vizualizati fisierele si altfel decat intended:
- metadate metadate metadate: timpii de scriere, acces, etc.
- verificati entropia fisierelor cu binwalk
- vizualizati spectrograma cu sonic visualizer (calitatea imaginii e mai buna ca cea din Audacity si am avut un caz in care nu se vedea clar decat cu sonic visualizer)
- pe imagini utilizati stegsolve sa vedeti plane-urile pe bucati (http://www.caesum.com/handbook/Stegsolve.jar)
- cautati poze similare pe net (sau poate chiar pe site), preferabil exact la fel, si faceti xor sa vedeti diferentele
- google image search si TinEye reverse image search pot sa ajute masiv in a gasi poza originala
- variante populare de softuri care implementeaza steganografie in poze sunt Steghide (http://steghide.sourceforge.net/) si Paranoia (https://ccrma.stanford.edu/~eberdahl/Projects/Paranoia/)
- pentru PNG-uri pngcheck va poate spune unde e buba in general (un CRC gresit, lungimi de chunk-uri, etc), iar tweakpng (https://github.com/jsummers/tweakpng) va ajuta sa modificati din GUI atribute
- pentru audio/video exista tool-uri care extrag metadate, dar sunt dependente de format, nu exista ceva unificat
- pentru sisteme de fisiere EXT(2/3/4) extundelete poate recupera fisierele sterse de pe o imagine de filesystem, cu tot cu atribute (inode number, extended attributes, selinux labels, etc)
- pentru firmware-uri squashfs-tools compilat cu suport LZMA e in general o abordare buna
- in general squashfs-tools din package manager nu vine cu suport LZMA deci e o idee buna sa vi-l compilati de mana
- in general daca va trebuie un tool anume (tweakpng, squashfs-tools, extundelete) e mai bine sa vi-l compilati de mana deoarece ultima varianta, bazata pe surse, are fie functionalitati suplimentare, fie mai bine puse la punct
- daca sunt chestii mai ezoterice de procesat semnale (in speta audio), gnuradio companion e o solutie completa, dar necesita niste munca si niste cunostinte despre filtre si procesare de semnale
- pentru retea Wireshark sau NetworkMiner pot fi folosite sa extraga fisiere transferate; NetworkMiner e ceva mai bun la partea asta, dar e pe Windows/Wine si accepta doar capturi PCAP, nu PCAP-NG
- pentru decriptat SSL, daca traficul in puteti genera voi, atunci poate fi o solutie fisierul de debug SSL (https://jimshaver.net/2015/02/11/decrypting-tls-browser-traffic-with-wireshark-the-easy-way/)
- in general cand va uitati peste o captura, doua puncte de plecare sunt lista de conversatii si graficul I/O
- pentru procesare mai avansata scapy e cea mai la indemana solutie
- daca vreti sa faceti un server cu scapy trebuie sa rulati si o comanda de genul "iptables -A INPUT -i $INTERFATA -p tcp --dport $PORT -j DROP" unde $INTERFATA si $PORT sunt specifice problemei; altfel, kernelul va bloca pachetele inainte sa ajunga la programul vostru

## Mobile
- uitati-va intai la cum se comporta aplicatia, ce functionalitate expune, fie pe un telefon, fie cu emulatorul
- urmariti de-a lungul vietii aplicatiei ce se afiseaza in log-uri; din cadrul SDK-ului de android DDMS sau Monitor pot face asta si au si un filter box, ca sa urmariti doar mesajele aplicatiei de interes
- folositi apktool (https://ibotpeaches.github.io/Apktool/) ca sa extrageti continutul APK-ului; o sa va ofere manifest-ul in format XML, resursele aplicatiei si codul intermediar de tip smali
- daca aplicatia nu are componenta nativa, care sa fie dependenta de arhitectura, o idee buna e sa o instalati pe un emulator x86; ar trebui sa fie mai responsiv decat daca ati testa pe un dispozitiv care emuleaza ARM
- daca vreti sa va injectati cod in aplicatie, cel mai bine e sa editati codul smali, sa il reimpachetati in APK folosind apktool, iar la final sa semnati APK-ul cu dex2jar (http://sourceforge.net/projects/dex2jar/); nu veti putea sa instalati un APK nesemnat
- pentru decompilare e bine sa folositi mai multe variante daca sunteti nesiguri sau sa tineti cont de limitarile solutiilor existente:
    - jd-gui (http://jd.benow.ca/) e cel mai vechi dar e facut pentru JVM clasic, nu pentru Dalvik; cele doua implementari sunt semnificativ diferite asa ca asteptati-va la rateuri din partea jd-gui
    - androguard (https://github.com/androguard/androguard) e o suita cu binding-uri si consola interactiva, deci permite analiza scriptabila a APK-ului (in Python); da cel mai complet output, dar da gres cand afiseaza array-uri de char deoarece in Java, char-urile sunt pe 16 biti; in general un array de char-uri in androguard o sa aibe zerouri din 2 in 2 elemente
    - mobsf (https://github.com/ajinabraham/Mobile-Security-Framework-MobSF) da un output cam ca al lui jd-gui si fara gafele din androguard, dar daca e un cod mai obfuscat poate sa omita informatii
    - http://www.javadecompilers.com/apk e un decompilator online; rezultatele sunt mediocre, dar te scuteste de efortul de a-ti instala ceva pe calculator
- mobsf are si o masina virtuala auxiliara pentru a analiza dinamic aplicatia, prin apelare automata a elementelor de interfata
- mobsf suporta si aplicatii IOS, presupunand ca aveti un Mac si utilitarele de dezvoltare pentru IOS instalate
- daca vedeti multe clase cu nume precum a, aa, c.f.e, etc. inseamna ca aplicatia a fost obfuscata cu ProGuard, mecanismul implicit de obfuscare; nu exista ceva care sa recupereze numele originale pentru ca acea informatie nu este pastrata
- cand aveti de-a face cu obfuscare, un punct de pornire este sa va uitati dupa string-urile folosite, gen un mesaj de debug sau ceva transmis pe retea sau catre un serviciu
- daca apktool esueaza in timpul extragerii informatiilor din APK, atunci trebuie folosit unzip + tool-urile din SDK; de exemplu, daca problema e la extragerea resurselor, se foloseste aapt dump pentru a lista resursele plus ID-ul lor; ID-ul resursei poate fi corelat cu numarul folosit in cod si asa va dati seama ce text sau poza e solicitata la un anumit punct