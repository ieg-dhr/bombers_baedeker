import re

cleanText = []
firstCleaning = []
secondCleaning = []
thirdCleaning = []

inputText = open('bomber_input/BB1.txt', "r", encoding='utf-8')

# Dictionary für die zu korrigierenden Werte
replacement_values = {"1o": "10", "2o": "20", "3o": "30", "4o": "40", "5o": "50", "6o": "60", "7o": "70",
                      "8o": "80", "9o": "90",

                      "1O": "10", "2O": "20", "3O": "30", "4O": "40", "5O": "50", "6O": "60", "7O": "70",
                      "8O": "80", "9O": "90",

                      "50 ": "50'", "50 '": "50'", ",50": "50", "J55": "355", "JO": "30", "J5": "35",
                      "A8": "48",

                      "’": "'", " °": "°", "U°": "14°", "m i": "mi", "0'm": "0 m", "0'M": "0 m", " '": "'",
                      "0'N": "0 'N", "Nt": "N.", "N,": "N.", "N;": "N.", "Es": "E:", "E;": "E:", "'N": "' N",
                      "»": "'", "y;": "y)", "?": "F", "N.": " N. ", "E:": " E: ", "U°": "14°", "AO'": "40'",
                      "Ne": "N.", "E ..": "E:", "$0": "50", "AD": "40'", "AO": "40'", "B:": "E:", ".'": "'",
                      "B.": "E:", "$4°": "54°", "®": "°", "$00": "600", "^5": "48°", "JJ.": "15'", "4ß°": "48°",
                      "£:": "E:", "N -": "N:", "E.": "E:", "E": "E: ",

                      "miles;": "miles:", "m iles:": "miles:", "miles": " miles", "ndles": "miles", "ndles;": "miles:",
                      "id le s": "miles",
                      " from London: (Population ": ": (",

                      "■": "", "•": "", "«": "", "<": "", ">": "", "*": "", "$'": "", " : ; ": "",

                      "--": "", "---": "", "----": "", "-----": "", "------": "", "-------": "", "--------": "",
                      "---------": "", "----------": "", "— . „ — — —": "", " — — .— —": "", "— — - ": "",

                      " oOo-": "", "o0o-": "", "-oOo-": "", "oOo": "", "oOo—": "", "0 O 0 ": "", "oOo-": "",
                      "- 0O0-": "", " - 0 O 0 - —": "", "oOo- -": "", "-  -": "", "— — — o0": "", "-r—": "",
                      "-0O0-": "", "-— — -o0o—  -": "", "— — - —": "", "-2 0 -": "", "— — 0O0-": "", "— “ O O 0": "",
                      " — -o0o—  ": "", "o0o": "", "- - o O o -": "", "OOo": "000", "-'cOo'——": "\n", "— —o 0 ö ~ —": "",
                      "- — — 000— - ": "", " 0O 0": "", "— — 0O0— —": "", "'oüo————— ": "", "— ———": "", "— —— —": "",
                      "—-—0O0-——": "", "———0O0——": "", "—— QOO————": "", "- oO o - - ": "","- - - - - - - ":"",
                      "o\n°": "", "——————": "","—— —0O0— — ——": "", "—— ——o Oo—— —": "","—T——0O0— ——": "",
                      "-0O 0-": "",

                      " - E I": "\nEI", "BI,N": "ELN", "' E M M": "EMM", " E R F": "ERF",
                      " - — K 0": "\nKO", "————— A L": "\nAL", "A N S B A C H (Bavaria;": "\nA N S B A C H (Bavaria)",
                      "ARNST40'T": "ARNSTADT", "A U E": "AUE", "B40'EN-B40'EN": "BADEN-BADEN",
                      "See under Siegen ": "See under Siegen\n", "0 H B M W": "CHEMN", "P U L": "DÜL",
                      "g S G H W E G E":"ESCHWEGE", "FALTiERSTJEEggy": "FALLERSLEBEN", "P O R B A O H": "FORBACH",
                      "FRTtPBTnHSHAW": "FRIEDRICHHAFEN", "S E L S": "GELS", "GIBaSBK": "GIESSEN", "& L A T a": "GLATZ",
                      "GL0GAÜ": "GLOGAU", "GCPPINGaStf": "GÖPPINGEN", "& 0 R L I T Z": "GÖRLITZ",
                      "G 6 T T I N G E N": "GÖTTINGEN", "GR&NEERG": "GRÜNBERG", "HALBERST40'T": "HALBERSTADT",
                      "KAUF,": "HALLE", "———— HER": "\nHER", "Heydebreck (2)HUBEN": "Heydebreck (2)\nHUBEN",
                      "HQF": "HOF", "tt H": "H", "TDAR-OBERSTBIN": "IDAR-OBERSTBIN", "ILSM3URG": "ILSMBURG",
                      "INGOLST40'T ": "INGOLDSTADT", ". - ": "\n", "KAMP LINTFORT": "KAMP-LINTFORT",
                      "K 8 H l/Blln.": "KEHL", "KTFL": "KIEL", "K 0 S E L": "KOSEL", "K fl T H 2 N ": "KÖTHEN",
                      "KREffffpD": "KREFELD", "KpSTRIN": "KÜSTRIN",


                      "''": "'", "(2 )": "(2)", "(})": "(3)", "{": "(", "( ": "(",

                      "47°": "\n47°", "48°": "\n48°", "49°": "\n49°", "50°": "\n50°", "51°": "\n51°", "52°": "\n52°",
                      "53°": "\n53°", "54°": "\n54°", "55°": "\n55°",

                      "E:\n55°": "55°",

                      ") ": ")\n",
                      "(1)\n": "(1)", "(2)\n": "(2)", "(3)\n": "(3)",

                      "\n\n": "\n", "\n\n": "\n", ")\n-": ")-",

                      "(S ilesia)": "(Silesia)", "(S tettin)": "(Stettin)",

                      "  ": " ", "   ": " "
                      }

for line in inputText:
    firstCleaning = line.replace("{", "(")

    # Schleife die durch das replacement_values Dictionary läuft und die entsprechenden Werte im Text ersetzt
    for key in replacement_values.keys():
        firstCleaning = firstCleaning.replace(key, replacement_values[key])

    secondCleaning.append(firstCleaning)

if secondCleaning:
    print("first cleaning done!")
    print(len(secondCleaning), "charakter")

with open("out.txt", "w", encoding='utf-8') as file:
    for line in secondCleaning:
        file.write(line)

secondCleaning = []
secondCleaning = open("out.txt", "r", encoding='utf-8')

for line in secondCleaning:
    if re.findall(r'^[A-K][A-ZÄÖÜ_\s-]{3,}', line) \
            and not '(contd.)' in line \
            and not '(oontd.)' in line \
            and not '(continued.)' in line \
            and not '(continued)' in line \
            and not '(co n td .)' in line \
            and not '(conti)' in line \
            and not '(BEWAG)' in line \
            and not '(pontd.)' in line \
            and not '(c o n td .)' in line \
            and not '(oontcL )' in line \
            and not '''(Cont'd .)''' in line \
            and not '(Contd.)' in line:
        line = line.replace(" ", "") \
            .replace("(", " (") \
            .replace("near", " near ") \
            .replace("-", " ") \
            .replace("\n\n", "\n")

    thirdCleaning.append(line)

if thirdCleaning:
    print("\nsecond cleaning done!")
    print(len(thirdCleaning), "charakter")

# creates final output txt
with open("BB1_CLEAN.txt", "w", encoding='utf-8') as file:
    for line in thirdCleaning:
        file.write(line)
print("\nBB1_CLEAN.txt created")
print("preprocessing finished")