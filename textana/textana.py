# -*- coding: utf-8 -*-
import string, os
from textprocessing import TextProcessing


class ProcessText(object):
    def __init__(self):
        self.ta = TextProcessing()

    def process(self, obj):
        for t in obj:
            obj[t]['results'] = self.processText(obj[t]['text'])
        return obj

    def processText(self, text):

        phrases = []
        #stemmedphrases = []
        sentences = []
        richnessOfPosts = []
        contacts = []

        richnessOfPost = 0.0
        hasBadWords = False
        hasSlang = False
        hasNetLingo = False
        hasLink = False
        hasQualifier = False
        hasReTweet = False

        # fixup text
        text = text.replace(u"\u2019", "'")
        text = text.replace("&amp;", "&")
        text = text.replace("&#34;", "\"").replace("&quot;", "\"").replace("&ldquo;", "\"").replace("&rdquo;",
                                                                                                    "\"").replace('"',
                                                                                                                  ' " ')

        # experimental: convert non-digit single characters to periods so that they cause sentence breaks.
        # character must have space before and after itself to qualify.
        text = self.ta.convertSingleCharacterSymbolsToPeriods(text)

        # extract URIs
        uris = self.ta.extractURIs(text)
        if len(uris) > 0:
            hasLink = True

        # decode html entity characters
        text = self.ta.decodeSpecialChars(text)

        #  extract contacts
        contacts = self.ta.extractContacts(text)
        if len(contacts) > 0:
            hasQualifier = True

        # extract topics
        topics = self.ta.extractTopics(text)
        topics = self.ta.cleanupUnicodeCharsInTopics(topics)
        topics = self.ta.removePreceedingPoundChar(topics)
        if len(topics) > 0:
            hasQualifier = True

        # remove urls from text
        for url in uris:
            text = text.replace(url, " ")

        # remove contacts from text
        for contact in contacts:
            text = text.replace(contact, " ")

        # convert text to one or more sentences
        sentences = self.ta.convertToSentences(text)

        for aSentence in sentences:
            text = " ".join(aSentence)

            # remove special characters
            text = self.ta.stripSpecialChars(text)

            # this may be the single most important step before using textana!
            # Eliminate non printable characters, namely unicode chars!
            text = filter(lambda x: x in string.printable, text)

            # Cleanup elipsees on words - found in sentenses where a sentence thought trails...
            newWordList = []
            wordList = text.lower().split(" ")
            for w in wordList:
                w = self.ta.stripTrailingPeriods(w)
                newWordList.append(w)
            wordList = newWordList

            # transpose words like can't and won't
            newWordList = []
            for w in wordList:
                w = self.ta.transpose(w)
                if w.endswith("'s"):
                    w = w[:-2] + ' is'
                if w.find(' ') > -1:
                    for nw in w.split(' '):
                        newWordList.append(nw)
                else:
                    newWordList.append(w)
            wordList = newWordList

            # ensure that we have single word lists
            wordList = self.ta.splitWords(wordList)

            #if self.ta.isEnglish(wordList) == False:
            #	print "Not english:", text
            #	continue;

            # remove excess qoutes
            wordList = self.ta.removeQoutes(wordList)

            # remove commas
            wordList = self.ta.removeCommas(wordList)

            # ensure that we have single word lists
            wordList = self.ta.splitWords(wordList)

            # handle time
            newWordList = []
            for w in wordList:
                w = self.ta.fixTime(w)
                if w.find(' ') > -1:
                    for nw in w.split(' '):
                        newWordList.append(nw)
                else:
                    # if word contains a colon and was not a time, remove colon from word
                    if self.ta.isTime(w) == False:
                        w = w.replace(":", " ")
                    newWordList.append(w)

            wordList = newWordList

            # ensure that we have single word lists
            wordList = self.ta.splitWords(wordList)

            # clean-up non-dates
            newWordList = []
            for w in wordList:
                if w.count("/") > 0 or w.count("-") > 0:
                    w = self.ta.handleEmbeddedDash(w)
                    if self.ta.isDate(w) == False:
                        if w == "w/":
                            w = "with"
                        if w == "w/o":
                            w = "without"
                        w = w.replace("/", " ") #.replace("-"," ")
                newWordList.append(w)

            wordList = newWordList

            # ensure that we have single word lists
            wordList = self.ta.splitWords(wordList)

            # remove periods
            wordList = self.ta.removePeriods(wordList)

            # remove invalid words
            newWordList = []
            for w in wordList:
                exclude = False
                tup = self.ta.largestRepeatingPattern(w)
                if tup[1] > 2:
                    exclude = True
                if self.ta.hasTrailingChar(w) == True:
                    exclude = True
                if exclude == False:
                    newWordList.append(w)
            wordList = newWordList

            # ensure that we have single word lists
            #wordList = self.ta.splitWords(wordList)

            # check for ReTweet
            for w in wordList:
                if w == "rt":
                    hasReTweet = True
                    break

            wordList = self.ta.removeWordsFromList(wordList, ["@", "rt"])
            #wordList = self.ta.removeWord(wordList, "rt")

            # remove unicode chars
            wordList = self.ta.removeUnicodeChars(wordList)

            # Remove stray chars
            wordList = self.ta.cleanupStrayChars(wordList)

            # check for qualifiers
            for w in wordList[:]:
                if self.ta.isEmail(w) == False and w.startswith('@'):
                    hasQualifier = True
                    #contacts.append(w)
                    wordList.remove(w)

            # after translate functions above we want to ensure that we have single word lists
            wordList = self.ta.splitWords(wordList)

            # has bad words or slang?
            if hasBadWords == False:
                hasBadWords = self.ta.hasBadWords(wordList)
            if hasSlang == False:
                hasSlang = self.ta.hasSlang(wordList)
            if hasNetLingo == False:
                hasNetLingo = self.ta.hasNetLingo(wordList)

            # remove suppress words.  Those are words which add little meaning
            wordList = self.ta.removeSuppressWords(wordList)

            # after translate functions above we want to ensure that we have single word lists
            wordList = self.ta.splitWords(wordList)

            # fixing misspellings, translating twitter, net and slang lingo
            newWordList = []
            for w in wordList:
                if self.ta.isURI(w):
                    w = " "
                else:
                    w = self.ta.removeLeadingChar(w, "`")
                    w = self.ta.removeLeadingChar(w, "'")
                    w = self.ta.removeLeadingChar(w, "<")
                    w = self.ta.removeLeadingChar(w, ">")
                    w = self.ta.removeLeadingChar(w, "&")
                    w = self.ta.removeLeadingChar(w, "-")
                    w = self.ta.removeLeadingChar(w, "/")
                    w = self.ta.removeLeadingChar(w, "\"")
                    w = self.ta.fixSpelling(w)
                    w = self.ta.transNetLingo(w)
                    #w = self.ta.fixSlangLingo(w)
                    w = self.ta.twitterTranslate(w)
                    #w = self.ta.transDoubleWord(w)

                #if self.ta.dictionaryWord(w) == False and self.ta.isName(w) == False:
                #	if len(w) > 2 and w.endswith('in') == True:
                #		nw = w + 'g'
                #		if self.ta.dictionaryWord(nw) == True:
                #			w = nw
                #			hasSlang = True
                #		if self.ta.dictionaryWord(nw[:-3]) == True:
                #			w = nw[:-3]
                #			#hasSlang = True
                #	if w.endswith('z') == True:
                #		nw = w[:-1]
                #		if self.ta.dictionaryWord(nw) == True:
                #			w = nw
                #			#hasSlang = True
                newWordList.append(w)

            wordList = newWordList

            # again, after translate functions above we want to ensure that we have single word lists
            wordList = self.ta.splitWords(wordList)

            # Check again, because above translation may have introduced new bad,slang or netlingo terms
            if hasBadWords == False:
                hasBadWords = self.ta.hasBadWords(wordList)
            if hasSlang == False:
                hasSlang = self.ta.hasSlang(wordList)
            if hasNetLingo == False:
                hasNetLingo = self.ta.hasNetLingo(wordList)

            # append to list of phrases
            #self.ta.findPhrases(wordList, phrases, stemmedphrases)
            self.ta.findPhrases(wordList, phrases, None)

            # determine richness of post
            postScale = 1.0  #don't scale at this time
            richnessOfPost = self.ta.richnessOfText(wordList) * postScale * 100.0
            if hasReTweet == True:  # if retweet then the user didn't really say this so reduce score
                richnessOfPost = richnessOfPost * 0.25
            if len(phrases) > 1:
                richnessOfPost = richnessOfPost + (len(phrases) * 0.75)
            if len(contacts) > 1:
                richnessOfPost = richnessOfPost + 2.0

            if hasBadWords == True:
                richnessOfPost = richnessOfPost * 0.01

            if richnessOfPost > 100:
                richnessOfPost = 100
            richnessOfPosts.append(richnessOfPost)

        # compute average richnessOfPost
        richnessOfPost = 0.0
        if len(richnessOfPosts) > 0:
            richnessOfPost = sum(richnessOfPosts) / len(richnessOfPosts)

        js = {
            'uris': uris,
            'contacts': contacts,
            'topics': topics,
            'subphrases': phrases,
            #'stemmedSubPhrases':stemmedphrases,
            'richnessOfPost': "%.2f" % richnessOfPost,
            'hasBadWords': hasBadWords,
            'hasSlang': hasSlang,
            'hasNetLingo': hasNetLingo,
            'hasLink': hasLink,
            'hasQualifier': hasQualifier,
            'hasReTweet': hasReTweet
        }
        return js
