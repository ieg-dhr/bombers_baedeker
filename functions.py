# imports
import sys
import os
import os.path
import csv
from xml.etree import ElementTree as ET
import re


# open file
def file_open(textfile):
    try:
        fp = open(textfile, 'r', encoding='utf8')
    except:
        print("File not found")

    else:
        text = fp.read()
        return text

# Umwandlung der Seitenzahlen zu Tags mit URLs der UB Mainz
def generate_url(text):
    
    # Index der URLs
    index_dic = read_csv("extract_city_page_url/city_index.csv")
    
    # Formatieren der Seiten und URL im Fließtext für Sonderseiten
    special_pages = ["- T -", "- T3 -", "- PREFACE -", "- ii -", 
                     "- 32a -", "- 33a -", "- 33b -", "- 33c -", 
                     "- 33d -", "- 37a -", "- 666a -", "- 693a -"]
    
    for specials in special_pages:
        for key in index_dic:
            page = "- "+key+ " -"
            if page == specials:
                clean_special = specials.replace("-","").replace(" ","")
                xmlpage = ' <pb n="'+clean_special+'" url="'+index_dic[key][2]+'"/> ' 
                text = text.replace(page, xmlpage)
    
    # Formatieren der Seiten und URL im Fließtext
    for x in range(1, 1000): 
        for key in index_dic:
            page = "- "+str(x)+ " -"
            if key == str(x):
                xmlpage = ' <pb n="'+str(x)+'" url="'+index_dic[key][2]+'"/> ' 
                text = text.replace(page, xmlpage)
                
    return text

def find_cities_detailed(text, volume):

    # Volume spezifische Informationen, x = Erster Stadteintrag, Regex = Erkennungsmuster für Städte
    if volume == 1:
        x = 67
        regex = r'^[A-K][A-ZÄÖÜ_\s-]{3,}'

    else:
        x = 26
        regex = r'^[L-Z][A-ZÄÖÜ_\s-]{3,}'

    # Liste der Städtenamen
    city_names = []

    # Check Variable für korrekte Ergebnisse
    is_valid = False

    # Aufsplitten des Textes in Zeilen
    text_split = text.splitlines()

    # Hilfsvariablen
    i = 1

    # Die Zeile nach der aktuellen Zeile
    next_line = None

    # Durchlaufen des Textes
    for index, line in enumerate(text_split):

        # Überspringen der Titel- und Innenseite
        if i > x:

            # Zwischenspeichern der nächsten Zeile
            if index < (len(text_split) - 1):
                next_line = text_split[index + 1]

            # Zwischenspeichern des Stadtnamens
            city_name_temp = re.findall(regex, line)

            # Check ob Koordinaten vorhanden sind
            if "miles:" in next_line and bool(re.search(r'[°]', next_line)):
                is_valid = True

            # Speichern des Städtenamens wenn Koordinaten gefunden wurden
            if city_name_temp and city_name_temp not in city_names and is_valid == True:
                city_names.append(city_name_temp)

                # Zurücksetzen der Check-Variable
                is_valid = False

        else:
            i += 1

    # Säubern der Ergebnisse
    city_names_clean_detailed = []

    for city in city_names:

        # Herausnehmen von Leerzeichen
        clean_city = str(city[0]).replace(' ', '')

        # Nur Begriffe die jetzt immernoch aus min. 3 Zeichen bestehen werden gespeichert
        if clean_city not in city_names_clean_detailed and len(clean_city) > 2:
            city_names_clean_detailed.append(clean_city)

    return city_names_clean_detailed


# Funktion die Namen der Bundesländer speichert
def find_city_state(text, city_names, volume):

    # Volume spezifische Informationen, x = Erster Stadteintrag
    if volume == 1:
        x = 67

    else:
        x = 26

    # Liste der Bundesländer
    state_list = []

    # Aufsplitten des Textes in Zeilen
    text_split = text.splitlines()

    # Hilfsvariablen
    i = 1

    # Durchlaufen des Textes
    for index, line in enumerate(text_split):

        # Überspringen der Titel- und Innenseite
        if i > x:

            # Durchlaufen der Städteliste
            for city in city_names:

                # Überprüfen ob das erste Element der Zeile komplett mit dem Stadtnamen übereinstimmt
                if city == line.split(" ")[0]:

                    # Check ob in der nächsten Zeile Koordinaten vorkommen
                    # Zeile muss kürzer als 50 Zeichen sein, um Fließtext auszuschließen
                    if "miles:" in text_split[index + 1] and len(text_split[index + 1]) < 50:

                        # Erneute Überprüfung ob die nächste Zeile Koordinaten enthält
                        if bool(re.search(r'[°]', text_split[index + 1])):

                            # Ausplitten der gefundenen Zeile an der öffnenen Klammer
                            split = line.split("(")

                            # Abfangen von Städten die kein Bundesland angegeben haben
                            try:
                                # Wenn es ein Bundesland gibt
                                state = split[1]

                                # wird es ohne die schließende Klammer an die Ergebnisliste angefügt
                                state_list.append(state.strip(')'))

                            # gibt es kein Bundesland
                            except IndexError:

                                # wird der Stadtname als Bundesland eingetragen
                                state_list.append(split[0])
        else:
            i += 1

    return state_list


# Funktion die Geokoordinaten speichert
def find_city_coordinates(text, city_names, volume):

    # Volume spezifische Informationen, x = Erster Stadteintrag
    if volume == 1:
        x = 67

    else:
        x = 26

    # Liste der Koordinaten
    coordinates_list = []

    # Aufsplitten des Textes in Zeilen
    text_split = text.splitlines()

    # Hilfsvariablen
    i = 1

    # Durchlaufen des Textes
    for index, line in enumerate(text_split):

        # Überspringen der Titel- und Innenseite
        if i > x:

            # Durchlaufen der Städteliste
            for city in city_names:

                # Überprüfen ob das erste Element der Zeile komplett mit dem Stadtnamen übereinstimmt
                if city == line.split(" ")[0]:

                    # Check ob in der nächsten Zeile Koordinaten vorkommen
                    # Zeile muss kürzer als 50 Zeichen sein, um Fließtext auszuschließen
                    if "miles:" in text_split[index + 1] and len(text_split[index + 1]) < 50:

                        # Erneute Überprüfung ob die nächste Zeile Koordinaten enthält
                        if bool(re.search(r'[°]', text_split[index + 1])):
                            # Auswahl der Koordinatenzeile
                            next_line = (text_split[index + 1])

                            # Aufteilen der Zeile in 3 Elemente anhand der Doppelpunkte und Auswahl des ersten Objekts
                            temp = next_line.split(":")[0]

                            # Umformen in neues Koordinatenformat
                            temp = temp.replace("°", ".")
                            temp = temp.replace("'", "")
                            temp = temp.replace("E", "")
                            temp = temp.replace(".E", "")
                            temp = temp.replace("N.", ",")
                            temp = temp.replace(".N", ",")
                            temp = temp.replace(" ", "")
                            final = temp.replace("' E", "")

                            # Speichern der Koordinaten
                            coordinates_list.append(final)

        else:
            i += 1

    return coordinates_list


# Funktion um die Entfernung zu London zu speichern
def find_city_distances(text, city_names, volume):

    # Volume spezifische Informationen, x = Erster Stadteintrag
    if volume == 1:
        x = 67

    else:
        x = 26

    # Liste der Entfernungen zu London
    distances_list = []

    # Aufsplitten des Textes in Zeilen
    text_split = text.splitlines()

    # Hilfsvariablen
    i = 1

    # Durchlaufen des Textes
    for index, line in enumerate(text_split):

        # Überspringen der Titel- und Innenseite
        if i > x:

            # Durchlaufen der Städteliste
            for city in city_names:

                # Überprüfen ob das erste Element der Zeile komplett mit dem Stadtnamen übereinstimmt
                if city == line.split(" ")[0]:

                    # Check ob in der nächsten Zeile Koordinaten vorkommen
                    # Zeile muss kürzer als 50 Zeichen sein, um Fließtext auszuschließen
                    if "miles:" in text_split[index + 1] and len(text_split[index + 1]) < 50:

                        # Erneute Überprüfung ob die nächste Zeile Koordinaten enthält
                        if bool(re.search(r'[°]', text_split[index + 1])):
                            # Auswahl der Koordinatenzeile
                            next_line = (text_split[index + 1])

                            # Aufteilen der Zeile in 3 Elemente anhand der Doppelpunkte und Auswahl des zweiten Objekts
                            distance = next_line.split(":")[1]

                            # Anhängen der Entfernung an die Ergebnisliste
                            distances_list.append(distance)

        else:
            i += 1

    return distances_list

# Funktion für Preface extraktion
def get_preface(text, volume):
    
    pre_text = ""
    
    # Volume spezifische Informationen, x = Erster Stadteintrag, alles davor als Preface verwenden
    if volume == 1:
        x = 69

    else:
        x = 26
        
    text_split = text.splitlines()
    
    # Hilfsvariablen
    i = 1
    
    # Durchlaufen des Textes
    for index, line in enumerate(text_split):

        # Titel- und Innenseite
        if i <= x:
            pre_text += line + " "
    
        i += 1
    
    # Doppelte Leerzeichen löschen
    pre_text = re.sub(' +', ' ', pre_text)
    
    return pre_text

# Funktion um die Einwohnerzahl zu speichern
def find_city_population(text, city_names, volume):

    # Volume spezifische Informationen, x = Erster Stadteintrag
    if volume == 1:
        x = 67

    else:
        x = 26

    # Liste der Einwohnerzahlen
    population_list = []

    # Aufsplitten des Textes in Zeilen
    text_split = text.splitlines()

    # Hilfsvariablen
    i = 1

    # Durchlaufen des Textes
    for index, line in enumerate(text_split):

        # Überspringen der Titel- und Innenseite
        if i > x:

            # Durchlaufen der Städteliste
            for city in city_names:

                # Überprüfen ob das erste Element der Zeile komplett mit dem Stadtnamen übereinstimmt
                if city == line.split(" ")[0]:

                    # Check ob in der nächsten Zeile Koordinaten vorkommen
                    # Zeile muss kürzer als 50 Zeichen sein, um Fließtext auszuschließen
                    if "miles:" in text_split[index + 1] and len(text_split[index + 1]) < 50:

                        # Erneute Überprüfung ob die nächste Zeile Koordinaten enthält
                        if bool(re.search(r'[°]', text_split[index + 1])):
                            # Auswahl der Koordinatenzeile
                            next_line = (text_split[index + 1])

                            # Aufteilen der Zeile in 3 Elemente anhand der Doppelpunkte und Auswahl des dritten Objekts
                            # print(city)
                            population = next_line.split(":")[2]

                            # Entfernen der Klammern
                            population = (re.sub(r"[\(\)]", "", population))

                            # Ersetzen des Dezimalkommas und Anhängen an die Ergebnisliste
                            population_list.append(population.replace(",", "."))

        else:
            i += 1

    return population_list


# Funktion die Beschreibungen extrahiert
def extract_description(text, city_names, volume):

    # Volume spezifische Informationen, x = Erster Stadteintrag
    if volume == 1:
        x = 67

    else:
        x = 26

    # Liste der Beschreibungen
    descriptions_list = []

    # Liste der Kategorien
    categories = ['Transportation', 'Public Utility Services', 'Solid Fuels', 'Liquid Fuels and Substitutes',
                  'Iron, Steel and Ferro-Alloys',
                  'Non-Ferrous Metal Manufacture and Fabrication', 'Aircraft and Aero-Engines', 'Shipbuilding',
                  'Engineering and Armaments',
                  'Chemicals and Explosives', 'Textiles, Rayon, Pulp and Paper', 'Rubber and Tyres', 'Leather',
                  'Foodstuffs']
    
    # Aufsplitten des Textes in Zeilen
    text_split = text.splitlines()

    # Hilfsvariablen
    i = 1
    # Durchlaufen des Textes
    for index, line in enumerate(text_split):

        # Überspringen der Titel- und Innenseite
        if i > x:

            # Durchlaufen der Städteliste
            for city_index, city in enumerate(city_names):
                # Überprüfen ob das erste Element der Zeile komplett mit dem Stadtnamen übereinstimmt
                if city == line.split(" ")[0] and "miles:" in text_split[index + 1] and len(
                        text_split[index + 1]) < 50 and bool(re.search(r'[°]', text_split[index + 1])):
                    # Durchlaufen der nächsten Zeilen bis der nächste Eintrag gefunden wird
                    next_entry = False
                    last_city = False
                    try:
                        next_city = city_names[city_index + 1]
                    except IndexError:
                        last_city = True
                        next_entry = True

                    j = 2
                    # Speichern des kompletten Fließtextes der Stadt als Beschreibung
                    description = ""
                    if last_city:
                        while index + j < len(text_split):
                            description = description + text_split[index + j]
                            j += 1

                    while not next_entry:
                        if text_split[index + j] != "":
                            description = description + text_split[index + j]
                            j += 1
                        else:
                            j += 1
                        if text_split[index + j].split(" ")[0] == next_city and len(
                                text_split[index + j + 1]) < 50 and bool(re.search(r'[°]', text_split[index + j + 1])):
                            next_entry = True

                    # Sortieren der Kategorien
                    sort_categories = []

                    # Suchen und Speichern der Kategorien die im Text der aktuellen Stadt vorkommen
                    for category in categories:
                        if category in description:
                            sort_categories.append(description.find(category))
                        else: 
                            sort_categories.append(99999999999)

                        # Sortiert die Kategorien nach Auftreten in Text
                    sort_categories = [categories for _,categories in sorted(zip(sort_categories,categories))]
                            
                    # Unterteilen des Textes
                    current_categories = []
                    
                    # Suchen und Speichern der Kategorien die im Text der aktuellen Stadt vorkommen
                    for category in sort_categories:
                        if category in description:
                            current_categories.append(category)
                            
                    description_dic = {}

                    # Wenn es keine Kategorien gibt wird nur die Beschreibung gespeichert
                    if not current_categories:
                        description_dic['Description'] = description

                    first = True
                    # Durchlaufen der Kategorien innerhalb des Fließtextes
                    for current_category_index, current_category in enumerate(current_categories):

                        # Speichern der Beschreibung, einmalig pro Text
                        if first:
                            description_dic['Description'] = description[:description.index(current_category)]
                            first = False

                        # Speichern aller Kategorien die nach der aktuellen Kategorie im Text vorkommen
                        next_categories = []
                        for category in current_categories:
                            if category is not current_category and description.index(category) > description.index(
                                    current_category):
                                next_categories.append(description.index(category))

                        # Auswahl des Textes zwischen der aktuellen Kategorie und der nächsten vorkommenden Kategorie
                        if next_categories and current_category_index <= len(current_categories):
                            description_dic[current_category] = description[description.index(current_category):min(
                                next_categories)].replace(current_category, '')
                            current_category_index += 1
                        else:
                            # Speichern der letzten Kategorie, oder der einzigen falls es nur eine gibt
                            description_dic[current_category] = description[
                                                                description.index(current_category):].replace(
                                current_category, '')

                    # Speichern der Beschreibungen
                    descriptions_list.append(description_dic)

        else:
            i += 1
    return descriptions_list


# Erstellen des Dictionaries mit allen Daten
def create_data_dic(text, volume):

    # Check ob eine existierende Volume angegeben wurde
    if volume not in [1, 2]:
        print("Bitte 1 für Band 1 oder 2 für Band 2 eingeben.")
        exit()

    city_names = find_cities_detailed(text, volume)
    descriptions = extract_description(text, city_names, volume)
    data_dic = {'preface': get_preface(text, volume), 'volume': volume, 'cities': city_names,
                'states': find_city_state(text, city_names, volume),
                'coordinates': find_city_coordinates(text, city_names, volume),
                'distances': find_city_distances(text, city_names, volume),
                'population': find_city_population(text, city_names, volume),
                'description': descriptions,
                }

    return data_dic


# Funktion, die die Ergebnisse an eine vorhandene (manuell erstellte) XML-Datei anfügt
def insert_cities_xml(xml_file, data_dic, temp_file):

    text_split = file_open(input_file).splitlines()
    
    # Initialisieren des XML-Trees
    tree = ET.parse(xml_file)

    # Zuweisen der Wurzel des XML-Trees
    root = tree.getroot()

    # Städtenamen
    city_names = data_dic['cities']

    # Bundesländer
    state_list = data_dic['states']

    # Koordinaten
    coordinates_list = data_dic['coordinates']

    # Entfernungen zu London
    distances_list = data_dic['distances']

    # Einwohnerzahlen
    population_list = data_dic['population']

    # Beschreibungen
    description_list = data_dic['description']

    # Durchlaufen aller Elemente "book" im XML-Tree
    for book in root.iter('book'):
    
        #Titel, Untertitel, Teil und Preface erstellen
        sub = ET.SubElement(book, 'title')
        sub.text = "THE BOMBER'S BAEDEKER"
        
        sub = ET.SubElement(book, 'subtitle')
        if volume == 1:
            sub.text = 'AACHEN-KÜSTRIN'
        else:
            sub.text = 'LAHR - ZWICKAU'
        
        sub = ET.SubElement(book, 'part')
        sub.text = str(data_dic['volume'])
        
        sub = ET.SubElement(book, 'preface')
        sub.text = data_dic['preface']
    
        # Durchlaufen der Städteliste
        for city in city_names:
            # Anfügen eines neuen Sub-Elements "city" mit dem Stadtnamen als Wert des Attributs "name"
            sub = ET.SubElement(book, 'city')
            sub.set('name', city)

    # Durchlaufen aller Elemente "city" im XML-Tree
    for index, city in enumerate(root.iter('city')):

        # Anfügen eines Sub-Elements "state" an das Element "city"
        sub_state = ET.SubElement(city, 'state')

        # Check, dass es nicht mehr Elemente "city", als Einträge in der Bundesland-Liste gibt
        if index < len(state_list):
            # Das aktuelle Element "state" bekommt als Text-Wert den passenden Eintrag aus der Bundesland-Liste
            sub_state.text = state_list[index]

        # Anfügen eines Sub-Elements "coordinates" an das Element "city"
        sub_coordinates = ET.SubElement(city, 'coordinates')

        # Check, dass es nicht mehr Elemente "city", als Einträge in der Koordinaten-Liste gibt
        if index < len(coordinates_list):
            # Das aktuelle Element "coordinates" bekommt als Text-Wert den passenden Eintrag aus der Koordinaten-Liste
            sub_coordinates.text = coordinates_list[index]

        # Anfügen eines Sub-Elements "distance" an das Element "city"
        sub_distances = ET.SubElement(city, 'distance')

        # Check, dass es nicht mehr Elemente "city", als Einträge in der Entfernungen-Liste gibt
        if index < len(distances_list):
            # Das aktuelle Element "distances" bekommt als Text-Wert den passenden Eintrag aus der Entfernungen-Liste
            sub_distances.text = distances_list[index]

        # Anfügen eines Sub-Elements "population" an das Element "city"
        sub_population = ET.SubElement(city, 'population')

        # Check, dass es nicht mehr Elemente "city", als Einträge in der Einwohnerzahlen-Liste gibt
        if index < len(population_list):
            # Das aktuelle Element "population" bekommt als Text-Wert den passenden Eintrag aus der Einwohnerzahlen-Liste
            sub_population.text = population_list[index]

        # Check, dass es nicht mehr Elemente "city", als Einträge in der Beschreibungsliste gibt
        if index < len(description_list):

            # Einfügen der Beschreibung sowie der einzelnen Kategorien
            for key in description_list[index]:
                sub_details = ET.SubElement(city, key.replace(" ", "_").replace(",", "_"))
                sub_details.text = re.sub(' +',' ',description_list[index][key])
            
    tree.write(temp_file, encoding="UTF-8", xml_declaration=True)


def read_csv(file):
    index_dic = {}
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for index, row in enumerate(csv_reader):
            if index != 0:
                # town, page, page2, url
                index_dic[row[0]] = row[1:]
            else:
                index += 1

    return index_dic


# Funktion zum Export als CSV-Datei
def write_csv(data_dic):
    # Öffnen der Datei, in die die Ergebnisse geschrieben werden
    with open('bomber.csv', mode='w') as bomber_out:
        # Initialisieren des CSV-Writers
        csv_writer = csv.writer(bomber_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Städtenamen
        city_names = data_dic['cities']

        # Koordinaten
        coordinates_list = data_dic['coordinates']

        # Speichern der Spalten-Überschriften (Vorgabe von DARIAH)
        csv_writer.writerow(
            ['Address', 'Longitude', 'Latitude', 'TimeSpan:begin', 'TimeSpan:end', 'GettyID', 'TimeStamp'])

        # Durchlaufen der Städtenamen
        for index, city in enumerate(city_names):
            # Aufteilen der passenden Koordinaten in Längen- und Breitengrad
            latitude = coordinates_list[index].split(",")[0]

            longitude = coordinates_list[index].split(",")[1]

            # Schreiben der Informationen in die CSV-Datei
            csv_writer.writerow([city, longitude, latitude, '', '', '', ''])
