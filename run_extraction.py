from functions import *

print("Starting...\n\n")

# Band 1
volume = 1
input_file = "bomber_input/BB1_CLEAN_H_C.txt"
output_file = "bomber_output/bomber_output_part1.xml"

print("Configuration:\nVolume:", volume, "\nInput file:", input_file, "\nOutput file:", output_file)

# Öffnen und Speichern des Textes in einer Variable
bomber_text = file_open(input_file)

# Extrahieren und Speichern der Daten:
bomber_dic = create_data_dic(bomber_text, volume)

# Export der Daten als XML-Datei
insert_cities_xml("bomber_xml", bomber_dic, output_file)

print("\nSuccess!\n\n")

# Band 2
volume = 2
input_file = "bomber_input/BB2_CLEAN_H_C.txt"
output_file = "bomber_output/bomber_output_part2.xml"

print("Configuration:\nVolume:", volume, "\nInput file:", input_file, "\nOutput file:", output_file)

# Öffnen und Speichern des Textes in einer Variable
bomber_text = file_open(input_file)

# Extrahieren und Speichern der Daten:
bomber_dic = create_data_dic(bomber_text, volume)

# Export der Daten als XML-Datei
insert_cities_xml("bomber_xml", bomber_dic, output_file)

print("\n\nFinished!")
