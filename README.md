# Bomber's Baedeker

## Automatische Extraktion strukturierter Daten mit Python

Dieses Projekt beinhaltet die automatische Extraktion strukturierter Daten aus Text und deren Speicherung
in XML-Format.

Dieses README liefert einen Überblick über die Funktionsweise des Programmcodes. Bei Fragen können Sie gerne
Kontakt aufnehmen.

### Starten des Programms

Für das Ausführen des Programms muss ledeglich die Datei "run_extraction.py"
ausgeführt werden. Dabei ist zu beacheten, dass in dieser die Dateipfade für die Eingabedokumente (die 2 Bände des Bomber's Baedker)
sowie die der auszugebenden XML-Dateien festgelegt werden. Falls Sie das Programm lokal durchführen wollen, müssen die Pfade eventuell dementsprechend angepasst werden.

### Ein- und Ausgabe

Die Eingabedateien befinden sich im Ordner "bomber_input": 
* BB1_CLEAN_H_C_V2.txt für Band 1
* BB2_CLEAN_H_C_V2.txt für Band 2 

Die Ausgabedateien befinden sich im Ordner "bomber_output":
* bomber_output_part1.xml für Band 1
* bomber_output_part2.xml für Band 2

#### Ergänzung
Im Verzeichnis "bomber_output_ext" befinden sich nochmals überabeitete Ausgabedateien (Postscripts und Karten mit URLs hinzugefügt, fehlende Prios mit (N/A) ergänzt).

### Funktionsweise des Algorithmus

Der Algorithmus lässt sich in 3 Schritte aufteilen:
* Erkennen von Mustern im Text
* Sammeln der erkannten Textinhalte
* Speichern der gesammelten Daten im XML-Format

#### Erkennen von Mustern im Text

Die Funktionen mit denen gearbeitet wird befinden sich in der Datei "functions.py".
Für die Erkennung der Textmuster gibt es folgende Funktionen:
* find_cities_detailed für Städtenamen
* find_city_state für das Bundesland
* find_city_coordinates für die Koordinaten
* find_city_distances für die Entfernungen der Städte zu London
* find_city_population für die Einwohnerzahl
* extract_description für die Beschreibung, sowie die strategischen Ziele jeder Stadt
* generate_url Erzeugt anhand einer URL-Liste, zu jeder Seitenzahl, die passende URL der UB Mainz

Für das Erkennen der Städtenamen wurde mit regulären Ausdrücken gearbeitet. Beispielsweise können alle Städtenamen von A-K mit folgendem Ausdruck erkannt werden:
> regex = r'^[A-K][A-ZÄÖÜ_\s-]{3,}'

Dieser legt fest, dass das aktuelle Element nur aus Großbuchstaben von A-Z (inkl. Umlaute) bestehen darf und mindestens 3 Zeichen lang sein muss. Da der Text Zeile für Zeile untersucht wird und die Städtenamen im Originaltext
immer in Großbuchstaben dargestellet werden, können so die Städte erkannt werden.
Diese Zeilen dienen auch als Identifikation für den Beginn eines Eintrages zu einer Stadt. Ausserdem werden sie benutzt um das Bundesland zu finden, dieses folgt immmer in Klammern auf einen Stadtnamen.

Die auf einen Stadtnamen folgende Zeile ist immer die, die die Koordinaten, Entfernung zu London und die Einwohnerzahlen beinhaltet. 
Diese Zeile wird von den entsprechenden Funktionen aufgeteilt um Informationen ausfindig zu machen.
Im Falle der Koordinaten wird nach dem Zeichen "°" gesucht, da dieses immer enthalten sein muss. Bei der Entfernung zu London wird nach dem Ausdruck "miles:" gesucht. Da nun zwei von drei Elementen dieser Zeile identifiziert 
werden können, wird die Einwohnerzahl als das dritte Element definiert, also das, auf das keine der beiden vorhergehenden Muster zutreffen.

Bei den Beschreibungstexten wird das ganze etwas komplexer. Hier wurde per Hand eine Liste der strategischen Kategorien definiert, die in einer Stadt vorkommen können. Sobald einer dieser im Fließtext auftaucht, wird der
darrauffolgende Text, bis zum nächsten Vorkommen einer Kategorie, mit dem Kategorienamen gespeichert. Der Text, der vor der ersten Kategorie vorkommt, wird als allgemeine Beschreibung übergeben.

### Sammeln der erkannten Textinhalte

Jede der oben genannten Funktionen liefert eine Liste der erkannten Inhalte. Diese haben alle die gleiche Länge, ein Eintrag pro Eintrag im Original. Das bedeutet der 3. Eintrag in der Liste der Einwohnerzahlen, gehört zum
3. Eintrag in der Städteliste. Für die weitere Verarbeitung werden diese Listen nun in der Funktion "create_data_dic" in eine Dictionary umgewandelt. Im Gegensatz zu einer Liste die Werte enthält ([A, B, C]), wird bei einem
Dictionary jedem Wert ein Schlüssel zugeordnet ({Key1: A, Key2: B, Key3: C}). Dadurch können die Daten nun so gespeichert werden, dass klar ist welche Informationen sie enthalten ({'cities': city_names}).
Auf diese Weise haben wir eine Dictionary mit Listen erstellt, die schon alle benötigten Informationen enthalten.

### Speichern der gesammelten Daten im XML-Format

Im letzten Schritt muss dieses Dictionary dann in eine XML-Datei eingefügt werden. Die Grundstruktur diese wurde vorher schon erstellt, damit nicht in eine komplett leere Datei geschrieben wird.
Der gesamte Prozess des Exports wird mithilfe der Funktion "insert_cities_xml" durchgeführt. 
Nun werden alle Inhalte aus dem Data-Dictionary eingelesen, sowie, aus einer externen CSV-Datei, die Seitenzahlen aus dem Originaldokument. Nun kann eine XML-Baumstruktur erzeugt werden, an die zuerst die Städtenamen angefügt
werden. Anschließend wird jeder Stadt-Eintrag mit den dazugehörigen Informationen gefüllt.
Als letzten Schritt wird die XML-Datei exportiert und entstandene HTML-Entitäten werden aufgelöst.



### Legende zu Änderungen im Raw-ABBYY-Digitalisat des Bombers Baedeker

Diese Änderungen sind notwendig, damit die Python-Pipeline fehlerfrei laufen kann:

1. "PRIORITY RATING" der "LOCATIONS" wurden mit "(N/A)" aufgefüllt, wenn keine Priorität angegeben wurden.

2. Mehrfachklammern 
)								(3)
) (3) wurden umgeschrieben zu   (3)
) 								(3)

3. Fehler und Abweichungen durch Verfasser für "industrial headings" wurden korrigiert.

4. Fehler und Abweichungen durch Verfasser für Formatierungen wurden korrigiert.

5. Einfügen beschreibender Seitenzahlen z.B. "- T -" für den Buchtitel.

6. Abgekürzte "industrial headings", wenn diese im Fließtext vorkommen:
	"Transportation" => Tr.
	"Public Utility Services" => Pus.
	"Solid Fuels" => SolF.
	"Liquid Fuels and Substitutes" => LqiFaS.
	"Shipbuilding" => Sb.
	"Engineering and Armaments" => EngA.
	"Chemicals and Explosives" => CaE.
	"Textiles, Rayon, Pulp and Paper" => TRPP.
	"Iron and Steel" => IrSt.
	"Rubber and Tyres" => RuTy.
	"Leather" => Leat.
	"Foodstuffs" => Foods.
	"Non-Ferrous Metal Manufacture and Fabrication" => NFmmaF.
	"Iron, Steel and Ferro-Alloys" => ISaFA.

7. Ergänzung fehlender Metadaten
	Betroffen sind: BRAUBACH (Rhineland), BRAUNSCHWEIG (Brunswick), BURSCHEID (Rhineland)
	Ergänzt wurde jeweils: 10° 10' N. 10° 10' E: 100 miles: ( )


