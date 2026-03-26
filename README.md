# 1. praktiskais darbs studiju kursā "Mākslīgā Intelekta Pamati"

Šis projekts veidots mācību nolūkiem studiju kursā "Mākslīgā Intelekta Pamati", lai apgūtu pamatzināšanas par spēļu kokiem un to algoritmiem.

## Apraksts

Spēles sākumā cilvēks-spēlētājs norāda spēlē izmantojamas skaitļu virknes garumu, kas var būt diapazonā no 15 līdz 25 skaitļiem. Spēles programmatūra gadījuma ceļā saģenerē skaitļu virkni atbilstoši uzdotajam garumam, tajā iekļaujot skaitļus no 1 līdz 9. 
Spēles sākumā ir dota ģenerētā skaitļu virkne. Katram spēlētājam ir 0 punktu. Spēlētāji izpilda gājienus secīgi. Gājiena laikā spēlētājs aizvieto jebkuru skaitļu pāri (divus blakus stāvošus skaitļus), pamatojoties uz šādiem principiem: 
ja divu blakus stāvošu skaitļu summa ir lielāka par 7, tad skaitļu pāri aizvieto ar 1 un savam punktu skaitam pieskaita 2 punktus; 
ja divu blakus stāvošu skaitļu summa ir mazāka par 7, tad skaitļu pāri aizvieto ar 3 un no pretinieka punktu skaita atņem 1 punktu; 
ja divu blakus stāvošu skaitļu summa ir vienāda ar 7, tad skaitļu pāri aizvieto ar 2 un no sava punktu skaita atņem 1 punktu. 
Spēle beidzas, kad skaitļu virknē paliek tikai viens skaitlis. Uzvar spēlētājs, kam ir vairāk punktu

### Projekta instalācija

Pārliecinies, ka tavā datorā ir instalēts **Python 3.8** vai jaunāka versija.

1. Klonē repozitoriju
2. Izveido virtuālo vidi ar komandu ```python -m venv venv``` un aktivizē to ar komandu ```venv\Scripts\activate```
3. Ielādē nepieciešamās bibliotēkas ar komandu ```pip install -r requirements.txt```
4. Palaid programmu ar komandu ```python main.py```

Palaižot programmu, izveidosies spēles logs, kur augšā jāievada sākotnējie spēles nosacījumi.
