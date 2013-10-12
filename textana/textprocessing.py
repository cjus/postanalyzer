# -*- coding: utf-8 -*-

# Copyright 2009 Carlos Justiniano. All Rights Reserved.
#
# Text processing library based on ZoeyBot textprocessing.dll
# Enhanced using the Natural Language Tool Kit library (NLTK)
#

'''A library that provides text processing functionality'''

import string
import re
import stemmer
import nltk
import textana_corpus


class TextProcessing:
    _VOWELS = ""
    _suppressList = []
    _dictionary = []
    _knownPhrases = []
    _badwords = ""
    _noiseWords = []
    _namecallingWords = []
    _nameWords = []
    _misspelledWords = {}
    _daleWords = []
    _domainExtensions = []
    _doublewords = {}
    _twitterCommonWords = []
    _commonPhrases = []
    _transposeMap = {}
    _twlingo = {}
    _netlingo = {}
    _slangLingo = {}

    pStemmer = stemmer.PorterStemmer()

    def __init__(self):
        self._VOWELS = "aeiouy"
        self._suppressList = ["lol"]
        self._loadCorpora()

    def _loadCorpora(self):
        # load english dictionary
        self._dictionary = textana_corpus.dictionary

        # load badwords corpus
        self._badwords = textana_corpus.badwords

        # load noise words corpus
        self._noiseWords = textana_corpus.noiseWords

        # load name calling corpus
        self._namecallingWords = textana_corpus.namecallingWords

        # load name corpus
        self._nameWords = textana_corpus.nameWords

        # load misspelling corpus
        self._misspelledWords = textana_corpus.misWords

        # load dale corpus
        self._daleWords = textana_corpus.daleWords

        # load transpose map corpus
        self._transposeMap = textana_corpus.transposeMap

        # load twitter common words corpus
        self._twitterCommonWords = textana_corpus.twitterCommonWords

        # load double words corpus
        self._doublewords = textana_corpus.doubleWords

        # load twitter lingo corpus
        self._twlingo = textana_corpus.twlingo

        # load slang corpus
        self._slangLingo = textana_corpus.slangLingo

        # load netlingo corpus
        self._netlingo = textana_corpus.netlingo

        # load domain extenstions corpus
        self._domainExtensions = textana_corpus.domainExtensions

        # load common phrases corpus
        self._commonPhrases = textana_corpus.commonPhrases

        # load known phrases corpus
        self._knownPhrases = textana_corpus.knownPhrases

    def binarySearch(self, lst, target):
        lo = 0
        hi = len(lst)
        while lo < hi:
            mid = (lo + hi) / 2
            midval = lst[mid]
            if midval < target:
                lo = mid + 1
            elif midval > target:
                hi = mid
            else:
                return mid
        return -1


    def dictionaryWord(self, word):
        r = self.binarySearch(self._dictionary, word)
        return r != -1


    def vowels(self, word):
        word = word.lower()
        cnt = 0
        for ch in word:
            if ch in self._VOWELS:
                cnt += 1
        return cnt

    def consonants(self, word):
        word = word.lower()
        cnt = 0
        for ch in word:
            if not (ch in self._VOWELS):
                cnt += 1
        return cnt


    def syllables(self, word):
        word = word.lower()
        cnt = 0
        for i in range(len(word)):
            if word[i] in self._VOWELS:
                #check if not a vowel cluster or silent 'e'
                if ((i - 1 ) < 0 or self._VOWELS.find(word[i - 1]) < 0) and (
                                        i + 1 == len(word) and i - 1 > 0 and self._VOWELS.find(word[i - 1]) < 0 and
                            word[i] == 'e') != True:
                    cnt += 1
        if cnt == 0:
            cnt = 1
        return cnt


    def relevance(self, word):
        v = 0.1
        c = 0.1
        l = len(word)
        syllableWeight = 0.0034
        v += self.vowels(word)
        c = c + l - v
        if c == 0.0:
            c = 0.1
        r = l + (v / c)
        a = r + ((self.syllables(word) * syllableWeight))
        return a


    def hasTrailingChar(self, word):
        if len(word) < 1:
            return False
        char = word[-1]
        cnt = 0
        for i in range(len(word) - 1, -1, -1):
            if word[i] == char:
                cnt += 1
                if cnt > 2:
                    return True
        return False


    def hasBadWords(self, wordList):
        if wordList is None:
            return wordList
        for w in wordList:
            if self.isBadWord(w):
                return True
        return False


    def hasSlang(self, wordList):
        if wordList is None:
            return wordList
        for w in wordList:
            if w in self._slangLingo:
                return True
        return False


    def hasNetLingo(self, wordList):
        if wordList is None:
            return wordList
        for w in wordList:
            if w in self._netlingo:
                return True
        return False


    def transpose(self, word):
        if word in self._transposeMap:
            return self._transposeMap[word]
        return word


    def fixTime(self, word):
        r = re.compile(r"([0-9]?[0-9]?[:]?[0-9]+[a|p])")
        if r.findall(word) == []:
            return word
        return word.replace("am", " am").replace("pm", " pm")


    def fixSpelling(self, word):
        if word in self._misspelledWords:
            return self._misspelledWords[word]
        return word


    def fixSlangLingo(self, word):
        if word in self._slangLingo:
            return self._slangLingo[word]
        return word


    def twitterTranslate(self, word):
        if word in self._twlingo:
            return self._twlingo[word]
        return word


    def transNetLingo(self, word):
        if word in self._netlingo:
            return self._netlingo[word]
        return word


    def transDoubleWord(self, word):
        if word in self._doublewords:
            return self._doublewords[word]
        return word


    def convertSingleCharacterSymbolsToPeriods(self, text):
        wordList = []
        words = text.split(" ")
        for w in words:
            if len(w) == 1 and self.isNumber(w) == False:
                wordList.append(". ")
                continue
            wordList.append(w)
        return " ".join(wordList)


    def stripSpecialChars(self, text):
        return text.replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("(", " ").replace(")",
                                                                                                       " ").replace(
            "[", " ").replace("]", " ").replace(";", " ").replace("!", " ").replace("~", " ").replace("%", " ").replace(
            "*",
            " ").replace("?", " ").replace("+", " ").replace("=", " ").replace("~", " ").replace("`", "'").replace("|",
                                                                                                                   " ").replace(
            "#", " ")


    def stripTrailingPeriods(self, word):
        while word.endswith("."):
            word = word[:-1]
        return word


    def decodeSpecialChars(self, text):
        # note double quoutes converted to single quoute on purpose! Since they will be removed anyway
        htmlEntityTranslation = {
            "&#34;": "\"",
            "&#39;": "'",
            "&#96;": "'",
            "&acute;": "'",
            "&lsquo;": "'",
            "&rsquo;": "'",
            "&#8216;": "'",
            "&#8217;": "'",
            "&#8230;": "...",
            "&#38;": "&",
            "&#60;": "<",
            "&#62;": ">",
            "&quot;": "'",
            "&ldquo;": "'",
            "&rdquo;": "'",
            "&apos;": "'",
            "&amp;": "&",
            "&lt;": "<",
            "&gt;": ">",
            "&#160;": " ",
            "&nbsp;": " ",
            "&#09;": " ",
            "&#10;": " ",
            "&hearts;": " love ",
            "&#176;": " degrees ",
            "&deg;": " degrees "
        }
        r = re.compile(r"&[#0-9a-z]+[;]")
        newText = text.replace("&amp;", "&").replace("''", "'")
        lst = r.findall(newText)
        if lst == []:
            return newText
        for pat in lst:
            try:
                p = htmlEntityTranslation[pat]
                newText = newText.replace(pat, p)
            except:
                newText = newText.replace(pat, " ")
        return newText


    def extractUnicodeNumber(self, word):
        r1 = re.compile(r"&[#0-9a-z]+[;]")
        r2 = re.compile(r"[0-9]+")
        newWord = word.replace("&amp;", "&").replace("''", "'")
        lst = r1.findall(newWord)
        if lst == []:
            return int(0)
        ll = r2.findall(newWord)
        if ll == []:
            return int(0)
        return int(ll[0])


    def extractURIs(self, text):
        r = re.compile(r"(http://[^ ]+)")
        uris = r.findall(text)
        newuris = []
        for uri in uris:
            u = re.sub(r'\.+$', '', uri)
            newuris.append(u)
        return newuris


    def extractContacts(self, text):
        lst = []
        r = re.compile(r"([\@][a-z0-9^.]+)")
        lst = r.findall(text)
        for item in lst[:]:
            if '.' in item:
                lst.remove(item)
        return lst


    def extractTopics(self, text):
        r = re.compile(r"(#\w+)")
        return r.findall(text)


    def handleEmbeddedDash(self, word):
        r = re.compile(r"([a-z]+)[\-]([a-z]+)")
        res = r.findall(word)
        l = len(res)
        if l != 1:
            return word
        word1 = res[0][0]
        word2 = res[0][1]
        if len(word1) > 2:
            if word1 == "pre" or word1 == "post": # exception for pre-school, pre-calculus etc...
                return word
            if self.dictionaryWord(word1) == True and self.dictionaryWord(word2) == True:
                pair = word1 + " " + word2
                return pair
        return word


    def isDaleWord(self, word):
        r = self.binarySearch(self._daleWords, word)
        if r != -1:
            return True
        return False


    def isTwitterCommonWord(self, word):
        r = self.binarySearch(self._twitterCommonWords, word)
        if r != -1:
            return True
        return False


    def isNoiseWord(self, word):
        r = self.binarySearch(self._noiseWords, word)
        if r != -1:
            return True
        return False


    def isBadWord(self, word):
        r = self.binarySearch(self._badwords, word)
        if r != -1:
            return True
        return False


    def isNameCallingWord(self, word):
        r = self.binarySearch(self._namecallingWords, word)
        if r != -1:
            return True
        return False


    def isTime(self, word):
        r = re.compile(r"[0-9]+\:[0-9]+")
        if r.findall(word) == []:
            return False
        return True


    def isURI(self, word):
        return "http://" in word


    def isEmail(self, word):
        return ('@' in word and '.' in word and self.isDomain(word) == True)


    def isCommaInNumber(self, text):
        r = re.compile(r"([0-9]+,[0-9]+)")
        if r.match(text) is None:
            return False
        return True


    def isDecimal(self, text):
        r = re.compile(r"([0-9]+\.[0-9]+)")
        if r.match(text) is None:
            return False
        return True


    def isNumber(self, text):
        try:
            num = text.replace(",", "").replace(".", "")
            float(num)
            return True
        except ValueError:
            pass
        return False


    def isMoney(self, text):
        r = re.compile(r"(^[$]+[0-9]+[\.]?[0-9]?)")
        if r.match(text) == None:
            return False
        return True


    def isDate(self, text):
        r1 = re.compile(r"([0-9]?[0-9]+[.\-/]+[0-9]?[0-9]+[.\-/]+[0-9]?[0-9]?[0-9]?[0-9]?)")
        if r1.match(text) == None:
            r2 = re.compile(r"([0-9]?[0-9]?[\-/]+[0-9]?[0-9]?)")
            if r2.match(text) == None:
                return False
        return True


    def isName(self, word):
        r = self.binarySearch(self._nameWords, word)
        if r != -1:
            return True
        return False


    def isDomain(self, word):
        r = self.binarySearch(self._domainExtensions, word)
        if r != -1:
            return True
        return False


    def isCommonPhrase(self, text):
        r = self.binarySearch(self._commonPhrases, text)
        if r != -1:
            return True
        return False


    def isKnownPhrase(self, text):
        r = self.binarySearch(self._knownPhrases, text)
        if r != -1:
            return True
        return False


    def isSentenceEnd(self, text):
        return text[-1:]


    def isEnglish(self, wordList):
        if wordList == None:
            return wordList
        cnt = 0.0
        wll = len(wordList)
        if wll == 0:
            return False
        for w in wordList:
            word = w.lower()
            un = self.extractUnicodeNumber(word)
            if (un > 190 and un < 256):
                return False
            elif self.isNoiseWord(word):
                cnt += 1
            elif self.isDaleWord(word):
                cnt += 1
            elif self.dictionaryWord(word):
                cnt += 1
        percent = (cnt / wll) * 100.0
        if percent > 30.0:
            return True
        return False


    def findPhrases(self, wordList, phrases, stemmedphrases):
        if wordList is None:
            return
        text = nltk.word_tokenize("".join(w + " " for w in wordList))
        lst = nltk.pos_tag(text)
        bigram = nltk.bigrams(lst)
        trigram = nltk.trigrams(lst)

        #words = {}

        # handle unigrams
        for i in range(len(lst)):
            word = lst[i][0]
            if self.dictionaryWord(word) or self.isDaleWord(word) or self.isNoiseWord(word) or self.isBadWord(
                    word) or self.isTwitterCommonWord(word) or self.isName(word) or self.isNameCallingWord(
                    word) or word == "am" or word == "pm":
                continue

            bcon = False
            for token in ['s', 'er', 'ings', 'ing', 'in']:
                if len(lst[i][0]) <= len(token):
                    continue
                word = lst[i][0]
                if word.endswith(token):
                    word = word[:-len(token)]
                    if self.dictionaryWord(word) or self.isNoiseWord(word) or self.isBadWord(
                            word) or self.isTwitterCommonWord(word) or self.isName(word) or self.isNameCallingWord(
                            word):
                        bcon = True
                        break

            if bcon:
                continue

            if lst[i][1].startswith("N") and self.dictionaryWord(lst[i][0]) == False:
                word = lst[i][0]
                if not self.isCommonPhrase(word):
                    phrases.append(word)
                    if stemmedphrases is not None:
                        stemmedphrases.append(self.stemWord(word))

        # handle bigrams
        for phrase in bigram:
            testPhrase = phrase[0][0] + " " + phrase[1][0]
            if self.isKnownPhrase(testPhrase):
                phrases.append(testPhrase)
                continue

            #if self.isDaleWord(phrase[0][0]) and self.isDaleWord(phrase[1][0]):
            #	continue
            #if self.isBadWord(phrase[0][0]) or self.isBadWord(phrase[1][0]):
            #	continue
            #if self.isNameCallingWord(phrase[0][0]) or self.isNameCallingWord(phrase[1][0]):
            #	continue
            #if phrase[0][0].endswith("am") == True or phrase[0][0].endswith("pm"):
            #	continue
            #if phrase[1][0].endswith("am") == True or phrase[1][0].endswith("pm"):
            #	continue

            w1 = False
            w2 = False
            if (phrase[0][1]).startswith("N") or (phrase[0][1]).startswith("CD"):
                w1 = True
            if (phrase[1][1]).startswith("N") or (phrase[1][1]).startswith("CD"):
                w2 = True
            if w1 == True and w2 == True:
                testPhrase = phrase[0][0] + " " + phrase[1][0]
                if not self.isCommonPhrase(testPhrase):
                    phrases.append(testPhrase)
                    if stemmedphrases is not None:
                        stemmedphrases.append(self.stemWord(phrase[0][0]) + " " + self.stemWord(phrase[1][0]))
                        #if self.isKnownPhrase(testPhrase): # is a known phrase so remove phrase sub words
                        #	words = testPhrase.split(' ')
                        #	for i in range(len(words)):
                        #		self.removeSingleWordFromList(phrases, words[i])
                        #		if stemmedphrases != None:
                        #			self.removeSingleWordFromList(stemmedphrases, self.stemWord(words[i]))

        # handle trigrams
        for phrase in trigram:
            testPhrase = phrase[0][0] + " " + phrase[1][0] + " " + phrase[2][0]
            if self.isKnownPhrase(testPhrase):
                phrases.append(testPhrase)
                continue

            #if self.isDaleWord(phrase[0][0]) and self.isDaleWord(phrase[1][0]) and self.isDaleWord(phrase[2][0]):
            #	continue
            #if self.isBadWord(phrase[0][0]) or self.isBadWord(phrase[1][0]) or self.isBadWord(phrase[2][0]):
            #	continue
            #if self.isNameCallingWord(phrase[0][0]) or self.isNameCallingWord(phrase[1][0]) or self.isNameCallingWord(phrase[2][0]):
            #	continue
            #if phrase[0][0].endswith("am") == True or phrase[0][0].endswith("pm"):
            #	continue
            #if phrase[1][0].endswith("am") == True or phrase[1][0].endswith("pm"):
            #	continue
            #if phrase[2][0].endswith("am") == True or phrase[2][0].endswith("pm"):
            #	continue
            w1 = False
            w2 = False
            w3 = False
            if (phrase[0][1]).startswith("N") or (phrase[0][1]).startswith("CD"):
                w1 = True
            if (phrase[1][1]).startswith("N") or (phrase[1][1]).startswith("CD") or (phrase[1][1]).startswith("JJ"):
                w2 = True
            if (phrase[2][1]).startswith("N") or (phrase[2][1]).startswith("CD"):
                w3 = True
            if w1 == True and w2 == True and w3 == True:
                testPhrase = phrase[0][0] + " " + phrase[1][0] + " " + phrase[2][0]
                if not self.isCommonPhrase(testPhrase):
                    phrases.append(testPhrase)
                    if stemmedphrases is not None:
                        stemmedphrases.append(
                            self.stemWord(phrase[0][0]) + " " + self.stemWord(phrase[1][0]) + " " + self.stemWord(
                                phrase[2][0]))
                        #if self.isKnownPhrase(testPhrase): # is a known phrase so remove phrase sub words
                        #	words = testPhrase.split(' ')
                        #	for i in range(len(words)):
                        #		self.removeSingleWordFromList(phrases, words[i])
                        #		if stemmedphrases != None:
                        #			self.removeSingleWordFromList(stemmedphrases, self.stemWord(words[i]))


    def richnessOfText(self, wordList):
        if wordList is None:
            return 0
        if not len(wordList):
            return 0
        text = nltk.word_tokenize("".join(w + " " for w in wordList))
        lst = nltk.pos_tag(text)
        ll = len(lst)
        score = 0.0
        for i in range(ll):
            if (lst[i][1]).startswith("NNPS"):
                score += 0.05
            elif (lst[i][1]).startswith("NNP"):
                score += 0.02
            elif (lst[i][1]).startswith("NNS"):
                score += 0.08
            elif (lst[i][1]).startswith("NN"):
                score += 0.03
            elif (lst[i][1]).startswith("CD"):
                score += 0.10
            elif (lst[i][1]).startswith("JJ"):
                score += 0.20
            elif (lst[i][1]).startswith("NNS"):
                score += 0.08
            elif (lst[i][1]).startswith("V"):
                score += 0.02

        # testing:  nltk.pos_tag(nltk.word_tokenize("Which means that there is the equivalent of 4-5 people in this room, despite the fact that only two of us breathe oxygen."))
        return score


    def getNounCount(self, wordList):
        if wordList is None:
            return wordList
        text = nltk.word_tokenize("".join(w + " " for w in wordList))
        lst = nltk.pos_tag(text)
        nouns = 0
        for i in range(len(lst)):
            if (lst[i][1]).startswith("N"):
                nouns += 1
        return nouns

    def removePeriods(self, wordList):
        if wordList is None:
            return wordList
        exceptions = ["dr.", "gen.", "mr.", "ms.", "mrs.", "jr.", "sr.", "maj.", "st.", "lt.", "sen.", "dir.", "vp."]
        newList = []
        personTag = False
        for w in wordList:
            if len(w) == 0:
                continue
            personTag = w in exceptions
            if (personTag == False) and (self.isMoney(w) == False) and (self.isNumber(w) == False) and (
                    self.isDomain(w) == False): # and (self.isSentenceEnd(w) == True):
                wl = w.split('.')
                for aw in wl:
                    if len(aw) > 0:
                        newList.append(aw)
            else:
                while w.endswith("."):
                    w = w[:-1]
                newList.append(w)
        return newList


    def removeQoutes(self, wordList):
        if wordList is None:
            return wordList
        newList = []
        for w in wordList:
            if len(w) == 0:
                continue
            if w.startswith("'"):
                w = w[1:]
            if w.endswith("'"):
                w = w[:-1]
            if w.endswith("'."):
                w = w[:-2]

            if w.startswith('`'):
                w = w[1:]
            if w.endswith("`"):
                w = w[:-1]
            if w.endswith("`."):
                w = w[:-2]

            if w.startswith('"'):
                w = w[1:]
            if w.endswith('"'):
                w = w[:-1]
            if w.endswith('".'):
                w = w[:-2]
            newList.append(w)
        return newList


    def removeCommas(self, wordList):
        if wordList is None:
            return wordList
        newList = []
        for w in wordList:
            if len(w) == 0:
                continue
            if not self.isCommaInNumber(w):
                s = w.split(",")
                for sw in s:
                    newList.append(sw)
            else:
                newList.append(w)
        return newList


    def removeUnicodeChars(self, wordList):
        if wordList is None:
            return wordList
        newList = []
        r = re.compile(r"&#([0-9][0-9][0-9])")
        for w in wordList:
            if len(w) == 0:
                continue
            res = r.findall(w)
            if len(res) < 1:
                newList.append(w)
        return newList


    def removeLeadingChar(self, word, char):
        newWord = ""
        if word.startswith(char):
            newWord = word[1:]
        else:
            newWord = word
        return newWord


    def removeLeadingChars(self, word, charlist):
        newWord = word
        for char in charlist:
            if newWord[0] == char:
                newWord = newWord[1:]
        return newWord


    def cleanupUnicodeCharsInTopics(self, wordList):
        if wordList is None:
            return wordList
        newList = []
        r = re.compile(r"#([0-9][0-9][0-9])")
        for w in wordList:
            if len(w) == 0:
                continue
            res = r.findall(w)
            if len(res) < 1:
                newList.append(w)
        return newList


    def cleanupStrayChars(self, wordList):
        if wordList is None:
            return wordList
        newList = []
        for w in wordList:
            wl = len(w)
            if wl == 0:
                continue
            w = w.replace("?", " ")
            w = w.replace("\\", " ")
            w = w.replace("^", " ")
            if wl == 1:
                w = w.replace("&", " ")
            w = w.replace("_", " ")
            w = w.replace("(", " ")
            w = w.replace("(", " ")
            w = w.replace("{", " ")
            w = w.replace("}", " ")
            w = w.replace("[", " ")
            w = w.replace("]", " ")
            if wl == 1:
                w = w.replace("-", " ")
            w = w.replace("!", " ")
            w = w.replace("'", " ")
            if len(w) > 0:
                newList.append(w)
        return newList


    def removePreceedingPoundChar(self, wordList):
        if wordList is None:
            return wordList
        newList = []
        for w in wordList:
            if len(w) == 0:
                continue
            w = w.replace("#", "")
            if len(w) > 0:
                newList.append(w)
        return newList


    def re_show(self, pat, s):
        print re.compile(pat, re.M).sub("{\g<0>}", s.rstrip()), '\n'


    def stemWord(self, word):
        return self.pStemmer.stem(word, 0, len(word) - 1)


    def stemWordList(self, wordList):
        if wordList is None:
            return wordList
        newList = []
        for i in range(len(wordList)):
            newList.append(self.pStemmer.stem(wordList[i], 0, len(wordList[i]) - 1))
        return newList


    def splitWords_old(self, wordList):
        if wordList is None:
            return wordList
        newList = []
        tt = string.maketrans(" -", "..")
        for w in wordList:
            if ' ' in w or '-' in w:
                for nw in w.translate(tt).split('.'):
                    newList.append(nw)
            else:
                newList.append(w)
        return newList


    def splitWords(self, wordList):
        if wordList is None:
            return wordList
        newList = []
        for w in wordList:
            if ' ' in w:
                nw = w.split(' ')
                newList.append(nw[0])
                newList.append(nw[1])
            else:
                newList.append(w)
        return newList


    def removeWord(self, wordList, removeWord):
        if wordList is None:
            return wordList
        newList = []
        for w in wordList:
            if w == removeWord:
                continue
            newList.append(w)
        return newList


    def removeSingleWordFromList(self, wordList, text):
        if wordList is None:
            return wordList
        if text in wordList:
            wordList.remove(text)


    def removeWordsFromList(self, wordList, removeWordList):
        if wordList is None:
            return wordList
        newList = []
        for w in wordList:
            if not (w in removeWordList):
                newList.append(w)
        return newList


    def removeWordEnding(self, wordList, ending):
        if wordList is None:
            return wordList
        newList = []
        for w in wordList:
            if not w.endswith(ending):
                newList.append(w)
            else:
                newList.append(w[-len(ending)])
        return newList


    def removeSuppressWords(self, wordList):
        if wordList is None:
            return wordList
        newList = []
        for w in wordList:
            if not (w in self._suppressList):
                newList.append(w)
        return newList


    def largestRepeatingPattern(self, text):
        pat = ''
        cnt = 0
        largestPattern = ""
        largestPatternCnt = 0
        testText = text
        tl = len(testText)
        testText += (" " * tl)
        for s in range(1, 5):
            for i in range(0, tl):
                cnt = 0
                pat = testText[i:i + s].rstrip()
                for j in range(i, tl, s):
                    if pat == testText[j:j + s].rstrip():
                        cnt += 1
                        if largestPatternCnt < cnt:
                            largestPatternCnt = cnt
                            largestPattern = pat
                    else:
                        break
        return (largestPattern, largestPatternCnt)


    def convertToSentences(self, text):
        if not text.endswith("."):
            text = text + "."
        sentences = []
        swl = []
        wordList = text.split(" ")

        newWordList = []
        for w in wordList:
            a = self.largestRepeatingPattern(w)
            if a[1] > 2:
                b = []
                if a[0] == ".":
                    b = w.split(".")
                elif a[0] == "-":
                    b = w.split("-")
                for entry in b:
                    if entry != "":
                        newWordList.append(entry)
            else:
                newWordList.append(w)

        for w in newWordList:
            if w != "":
                swl.append(w)
            if w.endswith(".") or w.endswith("!") or w.endswith("?") or w.endswith(":") or w.endswith(
                    ",") or w.endswith(
                    ";") or w.endswith(")") or w.endswith("("):
                sentences.append(swl)
                swl = []

        if len(sentences) == 0:
            ds = []
            ds.append(swl)
            return ds

        return sentences

