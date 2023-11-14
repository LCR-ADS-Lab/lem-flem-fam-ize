#tokenizer, flemmatizer, lemmatizer, and familizer

#from pylats import lats #there are some problems with pylats

import glob
import spacy
nlp = spacy.load("en_core_web_sm") #must install spacy and download this model

def dicter(database):
	out_dict = {}
	for items in database:
		item = items.split("\t")
		for words in item:
			out_dict[words] = item[0]
	return (out_dict)

def flemFam(word,tDict):
	if word not in tDict:
		return(word)
	else:
		return(tDict[word])

def tokenize(text,flemD,famD):
	textDict = {"tokens" : [],"lemmas" : [], "flemmas" : [], "families" : []}
	doc = nlp(text)
	for token in doc:
		#print(token.text, token.pos_)
		if token.pos_ in ["PUNCT","SYM", "X","_SP","_"]: #skip non-words
			continue
		elif token.text in ["","\n","\t"]:
			continue
		else:
			#tokens
			textDict["tokens"].append(token.text.lower())
			
			#flemmas
			textDict["flemmas"].append(flemFam(token.text.lower(),flemD))
			#lemmas
			lemmatok = token.lemma_.lower() #lemma
			upos = token.pos_ #large-grain pos tag
			textDict["lemmas"].append("_".join([lemmatok,upos]))

			#families
			textDict["families"].append(flemFam(token.text.lower(),famD))

	return(textDict)

def fileDicter(loFnames):
	outd = {}
	for fname in loFnames:
		outd[fname] = open(fname, errors = "ignore").read().strip()
	return(outd)

def tokenizeMulti(doTexts,flemD,famD): #format: {"fname" : text}
	outd = {}
	for text in doTexts:
		outd[text] = tokenize(doTexts[text],flemD,famD)
	return(outd)

def write2target(doTokenized,location,ftype = ".txt"):
	for text in doTokenized:
		simpleFname = text.split("/")[-1].replace(ftype,"") #get final filename
		for tokenType in doTokenized[text]:
			outf = open(location + simpleFname + "-" + tokenType + ftype, "w")
			outf.write("\n".join(doTokenized[text][tokenType]))
			outf.flush()
			outf.close()

#load dictionaries
flemmaDict = dicter(open("antbnc_lemmas_ver_004.txt").read().strip().replace("\t->","").split("\n")) #from https://www.laurenceanthony.net/software/antconc/ | https://www.laurenceanthony.net/resources/wordlists/antbnc_lemmas_ver_004.zip
flemmaDict["n't"] = "not" #update for spacy tokenization

familyDict = dicter(open("familizer_dict.txt").read().strip().split("\n")) #from bnc coca; converted from files available at https://www.laurenceanthony.net/software/antwordprofiler/
familyDict["n't"] = "not" #update for spacy tokenization


#tests, templates, etc.
# test = "This is a <sample> text?"
# tokenize(test,flemmaDict,familyDict)

# sampleDict = fileDicter(glob.glob('/_practice_2/*.txt')) #create filename : text dictionary
# tokDict = tokenizeMulti(sampleDict,flemmaDict,familyDict) #tokenize, etc. each text
# write2target(tokDict,"sample_output/") #write different versions of each file