# -*- coding: utf-8 -*-

""" Text processing library based on ZoeyBot textprocessing.dll
Enhanced using the Natural Language Tool Kit library (NLTK)
Copyright 2009 Carlos Justiniano. All Rights Reserved.
"""

__author__ = ('Carlos Justiniano (carlos.justiniano@gmail.com)',)

import string
import re
import stemmer
import nltk
import textana_corpus


class TextProcessing:
    def __init__(self):
        self.pstemmer = stemmer.PorterStemmer()

        self.VOWELS = "aeiouy"
        self.suppress_list = ["lol"]

        # load english dictionary
        self.dictionary = textana_corpus.dictionary

        # load bad words corpus
        self.bad_words = textana_corpus.bad_words

        # load noise words corpus
        self.noise_words = textana_corpus.noise_words

        # load name calling corpus
        self.name_calling_words = textana_corpus.name_calling_words

        # load name corpus
        self.name_words = textana_corpus.name_words

        # load misspelling corpus
        self.misspelled_words = textana_corpus.mis_words

        # load dale corpus
        self.dale_words = textana_corpus.dale_words

        # load transpose map corpus
        self.transpose_map = textana_corpus.transpose_map

        # load twitter common words corpus
        self.twitter_common_words = textana_corpus.twitter_common_words

        # load double words corpus
        self.double_words = textana_corpus.double_words

        # load twitter lingo corpus
        self.twlingo = textana_corpus.twlingo

        # load slang corpus
        self.slang_lingo = textana_corpus.slang_lingo

        # load netlingo corpus
        self.net_lingo = textana_corpus.net_lingo

        # load domain extensions corpus
        self.domain_extensions = textana_corpus.domain_extensions

        # load common phrases corpus
        self.common_phrases = textana_corpus.common_phrases

        # load known phrases corpus
        self.known_phrases = textana_corpus.known_phrases

    def binary_search(self, lst, target):
        lo = 0
        hi = len(lst)
        while lo < hi:
            mid = (lo + hi) / 2
            mid_val = lst[mid]
            if mid_val < target:
                lo = mid + 1
            elif mid_val > target:
                hi = mid
            else:
                return mid
        return -1

    def dictionary_word(self, word):
        r = self.binary_search(self.dictionary, word)
        return r != -1

    def vowels(self, word):
        word = word.lower()
        cnt = 0
        for ch in word:
            if ch in self.VOWELS:
                cnt += 1
        return cnt

    def consonants(self, word):
        word = word.lower()
        cnt = 0
        for ch in word:
            if not (ch in self.VOWELS):
                cnt += 1
        return cnt

    def syllables(self, word):
        word = word.lower()
        cnt = 0
        for i in range(len(word)):
            if word[i] in self.VOWELS:
                #check if not a vowel cluster or silent 'e'
                if ((i - 1) < 0 or self.VOWELS.find(word[i - 1]) < 0) and not (i + 1 == len(word) and i - 1 > 0 and self.VOWELS.find(word[i - 1]) < 0 and word[i] == 'e'):
                        cnt += 1
        if cnt == 0:
            cnt = 1
        return cnt

    def relevance(self, word):
        v = 0.1
        c = 0.1
        l = len(word)
        syllable_weight = 0.0034
        v += self.vowels(word)
        c = c + l - v
        if c == 0.0:
            c = 0.1
        r = l + (v / c)
        a = r + ((self.syllables(word) * syllable_weight))
        return a

    def has_trailing_char(self, word):
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

    def has_bad_words(self, word_list):
        if word_list is None:
            return word_list
        for w in word_list:
            if self.is_bad_word(w):
                return True
        return False

    def has_slang(self, word_list):
        if word_list is None:
            return word_list
        for w in word_list:
            if w in self.slang_lingo:
                return True
        return False

    def has_net_lingo(self, word_list):
        if word_list is None:
            return word_list
        for w in word_list:
            if w in self.net_lingo:
                return True
        return False

    def transpose(self, word):
        if word in self.transpose_map:
            return self.transpose_map[word]
        return word

    def fix_time(self, word):
        r = re.compile(r"([0-9]?[0-9]?[:]?[0-9]+[a|p])")
        if r.findall(word) is []:
            return word
        return word.replace("am", " am").replace("pm", " pm")

    def fix_spelling(self, word):
        if word in self.misspelled_words:
            return self.misspelled_words[word]
        return word

    def fix_slang_lingo(self, word):
        if word in self.slang_lingo:
            return self.slang_lingo[word]
        return word

    def twitter_translate(self, word):
        if word in self.twlingo:
            return self.twlingo[word]
        return word

    def trans_net_lingo(self, word):
        if word in self.net_lingo:
            return self.net_lingo[word]
        return word

    def trans_double_word(self, word):
        if word in self.double_words:
            return self.double_words[word]
        return word

    def convert_single_character_symbols_to_periods(self, text):
        word_list = []
        words = text.split(" ")
        for w in words:
            if len(w) == 1 and self.is_number(w) == False:
                word_list.append(". ")
                continue
            word_list.append(w)
        return " ".join(word_list)

    def strip_special_chars(self, text):
        return text.replace("\n", " ").replace("\r", " ").\
            replace("\t", " ").replace("(", " ").replace(")", " ").\
            replace("[", " ").replace("]", " ").replace(";", " ").\
            replace("!", " ").replace("~", " ").replace("%", " ").\
            replace("*", " ").replace("?", " ").replace("+", " ").\
            replace("=", " ").replace("~", " ").replace("`", "'").\
            replace("|", " ").replace("#", " ")

    def strip_trailing_periods(self, word):
        while word.endswith("."):
            word = word[:-1]
        return word

    def decode_special_chars(self, text):
        # note double quotes converted to single quotes on purpose! Since they will be removed anyway
        html_entity_translation = {
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
        new_text = text.replace("&amp;", "&").replace("''", "'")
        lst = r.findall(new_text)
        if lst == []:
            return new_text
        for pat in lst:
            try:
                p = html_entity_translation[pat]
                new_text = new_text.replace(pat, p)
            except:
                new_text = new_text.replace(pat, " ")
        return new_text

    def extract_unicode_number(self, word):
        r1 = re.compile(r"&[#0-9a-z]+[;]")
        r2 = re.compile(r"[0-9]+")
        new_word = word.replace("&amp;", "&").replace("''", "'")
        lst = r1.findall(new_word)
        if lst is []:
            return int(0)
        ll = r2.findall(new_word)
        if ll is []:
            return int(0)
        return int(ll[0])

    def extract_URIs(self, text):
        r = re.compile(r"(http://[^ ]+)")
        uris = r.findall(text)
        new_uris = []
        for uri in uris:
            u = re.sub(r'\.+$', '', uri)
            new_uris.append(u)
        return new_uris

    def extract_contacts(self, text):
        lst = []
        r = re.compile(r"([\@][a-z0-9^.]+)")
        lst = r.findall(text)
        for item in lst[:]:
            if '.' in item:
                lst.remove(item)
        return lst

    def extract_topics(self, text):
        r = re.compile(r"(#\w+)")
        return r.findall(text)

    def handle_embedded_dash(self, word):
        r = re.compile(r"([a-z]+)[\-]([a-z]+)")
        res = r.findall(word)
        l = len(res)
        if l != 1:
            return word
        word1 = res[0][0]
        word2 = res[0][1]
        if len(word1) > 2:
            if word1 == "pre" or word1 == "post":  # exception for pre-school, pre-calculus etc...
                return word
            if self.dictionary_word(word1) and self.dictionary_word(word2):
                pair = word1 + " " + word2
                return pair
        return word

    def is_dale_word(self, word):
        r = self.binary_search(self.dale_words, word)
        if r != -1:
            return True
        return False

    def is_twitter_common_word(self, word):
        r = self.binary_search(self.twitter_common_words, word)
        if r != -1:
            return True
        return False

    def is_noise_word(self, word):
        r = self.binary_search(self.noise_words, word)
        if r != -1:
            return True
        return False

    def is_bad_word(self, word):
        r = self.binary_search(self.bad_words, word)
        if r != -1:
            return True
        return False

    def is_name_calling_word(self, word):
        r = self.binary_search(self.name_calling_words, word)
        if r != -1:
            return True
        return False

    def is_time(self, word):
        r = re.compile(r"[0-9]+\:[0-9]+")
        if r.findall(word) == []:
            return False
        return True

    def is_URI(self, word):
        return "http://" in word

    def isEmail(self, word):
        return '@' in word and '.' in word and self.is_domain(word)

    def is_comma_in_number(self, text):
        r = re.compile(r"([0-9]+,[0-9]+)")
        if r.match(text) is None:
            return False
        return True

    def is_decimal(self, text):
        r = re.compile(r"([0-9]+\.[0-9]+)")
        if r.match(text) is None:
            return False
        return True

    def is_number(self, text):
        try:
            num = text.replace(",", "").replace(".", "")
            float(num)
            return True
        except ValueError:
            pass
        return False

    def is_money(self, text):
        r = re.compile(r"(^[$]+[0-9]+[\.]?[0-9]?)")
        if r.match(text) is None:
            return False
        return True

    def isDate(self, text):
        r1 = re.compile(r"([0-9]?[0-9]+[.\-/]+[0-9]?[0-9]+[.\-/]+[0-9]?[0-9]?[0-9]?[0-9]?)")
        if r1.match(text) is None:
            r2 = re.compile(r"([0-9]?[0-9]?[\-/]+[0-9]?[0-9]?)")
            if r2.match(text) is None:
                return False
        return True


    def is_name(self, word):
        r = self.binary_search(self.name_words, word)
        if r != -1:
            return True
        return False

    def is_domain(self, word):
        r = self.binary_search(self.domain_extensions, word)
        if r != -1:
            return True
        return False

    def is_common_phrase(self, text):
        r = self.binary_search(self.common_phrases, text)
        if r != -1:
            return True
        return False

    def is_known_phrase(self, text):
        r = self.binary_search(self.known_phrases, text)
        if r != -1:
            return True
        return False

    def is_sentence_end(self, text):
        return text[-1:]

    def is_english(self, word_list):
        if word_list is None:
            return word_list
        cnt = 0.0
        wll = len(word_list)
        if wll == 0:
            return False
        for w in word_list:
            word = w.lower()
            un = self.extract_unicode_number(word)
            if un > 190 and un < 256:
                return False
            elif self.is_noise_word(word):
                cnt += 1
            elif self.is_dale_word(word):
                cnt += 1
            elif self.dictionary_word(word):
                cnt += 1
        percent = (cnt / wll) * 100.0
        if percent > 30.0:
            return True
        return False

    def find_phrases(self, word_list, phrases, stemmed_phrases):
        if word_list is None:
            return
        text = nltk.word_tokenize("".join(w + " " for w in word_list))
        lst = nltk.pos_tag(text)
        bigram = nltk.bigrams(lst)
        trigram = nltk.trigrams(lst)

        #words = {}

        # handle unigrams
        for i in range(len(lst)):
            word = lst[i][0]
            if self.dictionary_word(word) or self.is_dale_word(word) or self.is_noise_word(word) or self.is_bad_word(
                    word) or self.is_twitter_common_word(word) or self.is_name(word) or self.is_name_calling_word(
                    word) or word == "am" or word == "pm":
                continue

            bcon = False
            for token in ['s', 'er', 'ings', 'ing', 'in']:
                if len(lst[i][0]) <= len(token):
                    continue
                word = lst[i][0]
                if word.endswith(token):
                    word = word[:-len(token)]
                    if self.dictionary_word(word) or self.is_noise_word(word) or self.is_bad_word(
                            word) or self.is_twitter_common_word(word) or self.is_name(word) or self.is_name_calling_word(
                            word):
                        bcon = True
                        break

            if bcon:
                continue

            if lst[i][1].startswith("N") and self.dictionary_word(lst[i][0]) == False:
                word = lst[i][0]
                if not self.is_common_phrase(word):
                    phrases.append(word)
                    if stemmed_phrases is not None:
                        stemmed_phrases.append(self.stem_word(word))

        # handle bigrams
        for phrase in bigram:
            test_phrase = phrase[0][0] + " " + phrase[1][0]
            if self.is_known_phrase(test_phrase):
                phrases.append(test_phrase)
                continue

            #if self.is_dale_word(phrase[0][0]) and self.is_dale_word(phrase[1][0]):
            #	continue
            #if self.is_bad_word(phrase[0][0]) or self.is_bad_word(phrase[1][0]):
            #	continue
            #if self.is_name_calling_word(phrase[0][0]) or self.is_name_calling_word(phrase[1][0]):
            #	continue
            #if phrase[0][0].endswith("am") or phrase[0][0].endswith("pm"):
            #	continue
            #if phrase[1][0].endswith("am") or phrase[1][0].endswith("pm"):
            #	continue

            w1 = False
            w2 = False
            if (phrase[0][1]).startswith("N") or (phrase[0][1]).startswith("CD"):
                w1 = True
            if (phrase[1][1]).startswith("N") or (phrase[1][1]).startswith("CD"):
                w2 = True
            if w1 and w2:
                test_phrase = phrase[0][0] + " " + phrase[1][0]
                if not self.is_common_phrase(test_phrase):
                    phrases.append(test_phrase)
                    if stemmed_phrases is not None:
                        stemmed_phrases.append(self.stem_word(phrase[0][0]) + " " + self.stem_word(phrase[1][0]))
                        #if self.is_known_phrase(test_phrase): # is a known phrase so remove phrase sub words
                        #	words = test_phrase.split(' ')
                        #	for i in range(len(words)):
                        #		self.remove_single_word_from_list(phrases, words[i])
                        #		if stemmedphrases != None:
                        #			self.remove_single_word_from_list(stemmedphrases, self.stem_word(words[i]))

        # handle trigrams
        for phrase in trigram:
            test_phrase = phrase[0][0] + " " + phrase[1][0] + " " + phrase[2][0]
            if self.is_known_phrase(test_phrase):
                phrases.append(test_phrase)
                continue

            #if self.is_dale_word(phrase[0][0]) and self.is_dale_word(phrase[1][0]) and self.is_dale_word(phrase[2][0]):
            #	continue
            #if self.is_bad_word(phrase[0][0]) or self.is_bad_word(phrase[1][0]) or self.is_bad_word(phrase[2][0]):
            #	continue
            #if self.is_name_calling_word(phrase[0][0]) or self.is_name_calling_word(phrase[1][0]) or self.is_name_calling_word(phrase[2][0]):
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
            if w1 and w2 and w3:
                test_phrase = phrase[0][0] + " " + phrase[1][0] + " " + phrase[2][0]
                if not self.is_common_phrase(test_phrase):
                    phrases.append(test_phrase)
                    if stemmed_phrases is not None:
                        stemmed_phrases.append(
                            self.stem_word(phrase[0][0]) + " " + self.stem_word(phrase[1][0]) + " " + self.stem_word(
                                phrase[2][0]))
                        #if self.is_known_phrase(test_phrase): # is a known phrase so remove phrase sub words
                        #	words = test_phrase.split(' ')
                        #	for i in range(len(words)):
                        #		self.remove_single_word_from_list(phrases, words[i])
                        #		if stemmedphrases != None:
                        #			self.remove_single_word_from_list(stemmedphrases, self.stem_word(words[i]))

    def richness_of_text(self, word_list):
        if word_list is None:
            return 0
        if not len(word_list):
            return 0
        text = nltk.word_tokenize("".join(w + " " for w in word_list))
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

    def get_noun_count(self, word_list):
        if word_list is None:
            return word_list
        text = nltk.word_tokenize("".join(w + " " for w in word_list))
        lst = nltk.pos_tag(text)
        nouns = 0
        for i in range(len(lst)):
            if (lst[i][1]).startswith("N"):
                nouns += 1
        return nouns

    def remove_periods(self, word_list):
        if word_list is None:
            return word_list
        exceptions = ["dr.", "gen.", "mr.", "ms.", "mrs.", "jr.", "sr.", "maj.", "st.", "lt.", "sen.", "dir.", "vp."]
        new_list = []
        for w in word_list:
            if len(w) == 0:
                continue
            person_tag = w in exceptions
            if (not person_tag) and (not self.is_money(w)) and (not self.is_number(w)) and (
                    not self.is_domain(w)):  # and (self.is_sentence_end(w) == True):
                wl = w.split('.')
                for aw in wl:
                    if len(aw) > 0:
                        new_list.append(aw)
            else:
                while w.endswith("."):
                    w = w[:-1]
                new_list.append(w)
        return new_list

    def remove_quotes(self, word_list):
        if word_list is None:
            return word_list
        new_list = []
        for w in word_list:
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
            new_list.append(w)
        return new_list

    def removeCommas(self, word_list):
        if word_list is None:
            return word_list
        new_list = []
        for w in word_list:
            if len(w) == 0:
                continue
            if not self.is_comma_in_number(w):
                s = w.split(",")
                for sw in s:
                    new_list.append(sw)
            else:
                new_list.append(w)
        return new_list

    def remove_unicode_chars(self, word_list):
        if word_list is None:
            return word_list
        new_list = []
        r = re.compile(r"&#([0-9][0-9][0-9])")
        for w in word_list:
            if len(w) == 0:
                continue
            res = r.findall(w)
            if len(res) < 1:
                new_list.append(w)
        return new_list

    def remove_leading_char(self, word, char):
        newWord = ""
        if word.startswith(char):
            newWord = word[1:]
        else:
            newWord = word
        return newWord

    def remove_leading_chars(self, word, char_list):
        new_word = word
        for char in char_list:
            if new_word[0] == char:
                new_word = new_word[1:]
        return new_word

    def cleanup_unicode_chars_in_topics(self, word_list):
        if word_list is None:
            return word_list
        new_list = []
        r = re.compile(r"#([0-9][0-9][0-9])")
        for w in word_list:
            if len(w) == 0:
                continue
            res = r.findall(w)
            if len(res) < 1:
                new_list.append(w)
        return new_list

    def cleanup_stray_chars(self, word_list):
        if word_list is None:
            return word_list
        new_list = []
        for w in word_list:
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
                new_list.append(w)
        return new_list

    def remove_preceeding_pound_char(self, word_list):
        if word_list is None:
            return word_list
        new_list = []
        for w in word_list:
            if len(w) == 0:
                continue
            w = w.replace("#", "")
            if len(w) > 0:
                new_list.append(w)
        return new_list

    def re_show(self, pat, s):
        print re.compile(pat, re.M).sub("{\g<0>}", s.rstrip()), '\n'

    def stem_word(self, word):
        return self.pstemmer.stem(word, 0, len(word) - 1)

    def stemWordList(self, word_list):
        if word_list is None:
            return word_list
        new_list = []
        for i in range(len(word_list)):
            new_list.append(self.pstemmer.stem(word_list[i], 0, len(word_list[i]) - 1))
        return new_list

    def split_words_old(self, word_list):
        if word_list is None:
            return word_list
        new_list = []
        tt = string.maketrans(" -", "..")
        for w in word_list:
            if ' ' in w or '-' in w:
                for nw in w.translate(tt).split('.'):
                    new_list.append(nw)
            else:
                new_list.append(w)
        return new_list


    def split_words(self, word_list):
        if word_list is None:
            return word_list
        new_list = []
        for w in word_list:
            if ' ' in w:
                nw = w.split(' ')
                new_list.append(nw[0])
                new_list.append(nw[1])
            else:
                new_list.append(w)
        return new_list

    def remove_word(self, word_list, remove_word):
        if word_list is None:
            return word_list
        new_list = []
        for w in word_list:
            if w == remove_word:
                continue
            new_list.append(w)
        return new_list

    def remove_single_word_from_list(self, word_list, text):
        if word_list is None:
            return word_list
        if text in word_list:
            word_list.remove(text)

    def remove_words_from_list(self, word_list, remove_word_list):
        if word_list is None:
            return word_list
        new_list = []
        for w in word_list:
            if not (w in remove_word_list):
                new_list.append(w)
        return new_list

    def remove_word_ending(self, word_list, ending):
        if word_list is None:
            return word_list
        new_list = []
        for w in word_list:
            if not w.endswith(ending):
                new_list.append(w)
            else:
                new_list.append(w[-len(ending)])
        return new_list

    def remove_suppress_words(self, word_list):
        if word_list is None:
            return word_list
        new_list = []
        for w in word_list:
            if not (w in self.suppress_list):
                new_list.append(w)
        return new_list

    def largest_repeating_pattern(self, text):
        largest_pattern = ""
        largest_pattern_count = 0
        test_text = text
        tl = len(test_text)
        test_text += (" " * tl)
        for s in range(1, 5):
            for i in range(0, tl):
                cnt = 0
                pat = test_text[i:i + s].rstrip()
                for j in range(i, tl, s):
                    if pat == test_text[j:j + s].rstrip():
                        cnt += 1
                        if largest_pattern_count < cnt:
                            largest_pattern_count = cnt
                            largest_pattern = pat
                    else:
                        break
        return largest_pattern, largest_pattern_count

    def convert_to_sentences(self, text):
        if not text.endswith("."):
            text += "."
        sentences = []
        swl = []
        word_list = text.split(" ")

        new_word_list = []
        for w in word_list:
            a = self.largest_repeating_pattern(w)
            if a[1] > 2:
                b = []
                if a[0] == ".":
                    b = w.split(".")
                elif a[0] == "-":
                    b = w.split("-")
                for entry in b:
                    if entry != "":
                        new_word_list.append(entry)
            else:
                new_word_list.append(w)

        for w in new_word_list:
            if w != "":
                swl.append(w)
            if w.endswith(".") or w.endswith("!") or w.endswith("?") or w.endswith(":") or w.endswith(
                    ",") or w.endswith(
                    ";") or w.endswith(")") or w.endswith("("):
                sentences.append(swl)
                swl = []

        if len(sentences) == 0:
            return [swl]

        return sentences

