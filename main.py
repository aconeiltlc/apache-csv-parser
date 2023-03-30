import re
import sys
import csv

with open('ApacheData.csv', "w", newline='') as file:
    fieldnames = ['stemhandle', 'note', 'source', 'stemform', 'abbreviation', 'grammar_note', 'brackets',
                  'positional', 'compounds', 'wordform', 'trans', 'trans_note', 'usage_note', 'verb_class',
                  'see', 'dv']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    raw_text = sys.stdin.read()

    def clean(raw_text):
        clean_text = []
        raw_text = raw_text.split('\r\n')
        for text in raw_text:
            if text in ("" ,None):
                continue
            else:
                clean_text.append(text)
        return clean_text

    text = clean(raw_text)
    pp_flag = 0
    comp_flag = 0
    stemform = ''
    note = ''
    segment = ''
    stemhandle = ''
    source = ''
    end = ''
    abb = ''
    #for line in text:
    for index in range(0, len(text)):
        line = text[index];
        line.strip()
        stemline = re.match(r"^([A-Z\/]*[ ]*[0-9]*[\/]*[A-Z]*)[ ]*([\[][^\]]*[\]])[ 	]+", line)
        if stemline == None:
            ppost = re.match(r"With Postpositional stems preceding:", line)
            if ppost != None:
                pp_flag = 1
            if "Compounds:" in line:
                pp_flag = 0
                comp_flag = 1
            dv = re.match(r"(dv:)(.*)", line)
            see_also = re.match(r"(see also:)(.*)", line)
            if dv == None and see_also == None:
                see_also = [see_also[2] if see_also else '']
                definition = re.search(r"(it|they|s/he|you|something|we|I|he|his|one|there|body|let|it/s/he|s/he/it|many|this|unique|our|worthless/valueless|that|she|the|drive)(/|[ ]|$)", line)
                if definition != None:
                    defpart = re.split(definition[1], line)
                    pnote = re.search(r'\(.*\)', defpart[1])
                    pnote = [pnote[0] if pnote else '']
                    dnote = re.search(r'\[.*\]', defpart[1])
                    dnote = [dnote[0] if dnote else '']
                    definition = str(definition[1]) + str(defpart[1])
                    cnote = re.search(r'(ANO|BC|FFO|HVO|LM|LPB|MM|NCM|OC|PFO|PLO1|PLO2|SFO|SPR|SRO|SSO)', line)
                    cnote = [cnote[0] if cnote else '']
                    wordform = defpart[0]
                #check ahead one for dv
                # dvIndex = index + 1
                # dvString = ""
                # while dvIndex < len(text) and re.match(r"(dv:)(.*)", text[dvIndex]) != None:
                #     if dvString != '':
                #         dvString += '; '
                #     dvString += re.match(r"(dv:)(.*)", text[dvIndex])[2]
                #     dvIndex += 1
                #check ahead for see also
                dsIndex = index + 1
                dvString = ""
                saString = ""
                while dsIndex < len(text) and ((re.match(r"(dv:)(.*)", text[dsIndex]) != None) or (re.match(r"(see also:)(.*)", text[dsIndex]) != None))Bray :
                    if dvString != '':
                        dvString += '; '
                    dvString += re.match(r"(dv:)(.*)", text[dsIndex])[2]
                    dsIndex += 1
                    if saString != '':
                        saString += '; '
                    saString += re.match(r"(see also:)(.*)", text[dsIndex])[2]
                    dsIndex += 1
                writer.writerow({'stemhandle': stemhandle, 'note': note, 'source': source, 'stemform': stemform, 'abbreviation': abb,
                                 'wordform': str(wordform),'trans': str(definition),
                                 'usage_note': str(pnote), 'trans_note': str(dnote), 'see': saString,
                                 'verb_class': str(cnote), 'positional': pp_flag, 'compounds': comp_flag, 'dv': dvString})
                continue
        else:
            pp_flag=0
            comp_flag=0
            #print(stemline[0])
            #print("ENTRY", line)
            stemform = re.findall(r"\-[^0-9][\(\)-–łíįāēóéáúōǫęṉńąa-z/'’’ʾʼ]*", line)
            note = re.findall(r"\([^‘].*\) ", line)
            segment = re.split(r'\[', line)
            stemhandle = stemline[1]
            source = stemline[2]
            end = re.split(r'\t', segment[1])
            #end_bracket = re.findall(r'\[.*\]', end[-1])
            abb = end[-1]
            #abbreviation = re.findall(r"[A-Z]", segment[1])
            #note = re.findall(r"\(.*\)", line)
            # print(line)
            writer.writerow({'stemhandle': stemhandle, 'note': note, 'source': source, 'stemform': stemform, 'abbreviation': abb})
                #writer.writerow({stemhandle, note, source, stemform, abb, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0})
            #print("stemhandle:", stemhandle, "note", note, "source:", source, "stemform:", stemform, "abbreviation:", abbreviation)

    #  cat BrayPredicativeVerbalClassifiedByRootCombined.txt | python3 main.py
    # if line is postpos flag the next lines until there is a blank line or the next line is compounds