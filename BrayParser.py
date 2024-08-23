import re
import sys
import csv

with open('ApacheData.csv', "w", newline='') as file:
    fieldnames = ['unified_root', 'unified_trans', 'stemhandle', 'note', 'source', 'stemform', 'abbreviation', 'grammar_note', 'brackets',
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
        line = text[index]
        line.strip()
        #match line beginning with capital letters, space, number, space, code in brackets and store as stemline
        stemline = re.match(r"^([A-Z\/]*[ ]*[0-9]*[\/]*[A-Z]*)[ ]*([\[][^\]]*[\]])[ 	]+", line)
        # if not a stemline
        if pp_flag == 1:
            if re.match(r"^([a-z])", line):
                pp_input = line
                pp_flag = 0
        else:
            pp_input = ''
        if comp_flag == 1:
            if re.match(r"^([a-z])", line):
                comp_line = re.search(r"(it|they|s/he|you|something|we|I|he|his|one|there|body|let|it/s/he|s/he/it|many|this|unique|our|worthless/valueless|that|she|the|drive)(/|[ ]|$)", line)
                if comp_line != None:
                    defpart = re.split(comp_line[1], line)
                    pnote = re.search(r'\(.*\)', defpart[1])
                    pnote = [pnote[0] if pnote else '']
                    dnote = re.search(r'\[.*\]', defpart[1])
                    dnote = [dnote[0] if dnote else '']
                    definition = str(comp_line[1]) + str(defpart[1])
                    cnote = re.search(r'(ANO|BC|FFO|HVO|LM|LPB|MM|NCM|OC|PFO|PLO1|PLO2|SFO|SPR|SRO|SSO)', line)
                    cnote = [cnote[0] if cnote else '']
                    wordform = defpart[0]
            else:
                comp_flag = 0
        if stemline == None:
            # match lines about postpositional stems
            ppost = re.match(r"With Postpositional stems preceding:", line)
            # if there is a postpositional stem preceding, add flag 1
            if ppost != None:
                pp_flag = 1
            # if there is a compound preceding, reset pp_flag and increase comp_flag
            if "Compounds:" in line:
                pp_flag = 0
                comp_flag = 1
            # look for derivative and store in dv
            dv = re.match(r"(dv:)(.*)", line)
            # look for see also and store
            see_also = re.match(r"(see also:)(.*)", line)
            # if the line isn't dv or see also, look for a definition starting with these words
            if dv == None and see_also == None:
                # see_also equals see_also index 2 if it exists
                see_also = [see_also[2] if see_also else '']
                definition = re.search(r"(it|they|s/he|you|something|we|I|he|his|one|there|body|let|it/s/he|s/he/it|many|this|unique|our|worthless/valueless|that|she|the|drive)(/|[ ]|$)", line)
                # for matched defintions
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
                #as long as index isn't more than length of text and there's a dv or see also match
                while dsIndex < len(text) and ((re.match(r"(dv:)(.*)", text[dsIndex]) != None) or (re.match(r"(see also:)(.*)", text[dsIndex]) != None)):
                    if re.match(r"(dv:)(.*)", text[dsIndex]):
                        dvString += re.match(r"(dv:)(.*)", text[dsIndex])[2]
                        dsIndex += 1
                    else:
                        re.match(r"(see also:)(.*)", text[dsIndex])
                        saString += re.match(r"(see also:)(.*)", text[dsIndex])[2]
                        dsIndex += 1
                # if dvString != '':
                #     dvString += '; '
                # dvString += re.match(r"(dv:)(.*)", text[dsIndex])[2]
                # dsIndex += 1
                # if saString != '':
                #     saString += '; '
                # saString += re.match(r"(see also:)(.*)", text[dsIndex])[2]
                # dsIndex += 1
                    writer.writerow({'unified_root': unified_root,'unified_trans':unified_trans, 'stemhandle': stemhandle, 'note': note, 'source': source, 'stemform': stemform, 'abbreviation': abb,
                             'wordform': str(wordform),'trans': str(definition),
                             'usage_note': str(pnote), 'trans_note': str(dnote), 'see': saString,
                             'verb_class': str(cnote), 'positional': pp_input, 'compounds': comp_flag, 'dv': dvString})
                continue
        # if not a part of the definition
        else:
            pp_flag=0
            comp_flag=0
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
            unified = re.match(r"(^-.*)\s(.*)", text[index + 1])
            unified_root = re.split(r"\s", unified[0])[0]
            unified_trans = re.split(r"\s", unified[0])[1]
            writer.writerow({'unified_root': unified_root, 'unified_trans':unified_trans, 'stemhandle': stemhandle, 'note': note, 'source': source, 'stemform': stemform, 'abbreviation': abb})
                #writer.writerow({stemhandle, note, source, stemform, abb, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0})
            #print("stemhandle:", stemhandle, "note", note, "source:", source, "stemform:", stemform, "abbreviation:", abbreviation)

    #  cat BrayPredicativeVerbalClassifiedByRootCombined.txt | python3 main.py
    # if line is postpos flag the next lines until there is a blank line or the next line is compounds