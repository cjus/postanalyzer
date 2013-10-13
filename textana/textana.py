# -*- coding: utf-8 -*-
""" Text processing library interface
Tailors text processing based on application domain
Copyright (c) 2013, Carlos Justiniano
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import string
from textprocessing import TextProcessing


class ProcessText(object):
    def __init__(self):
        self.ta = TextProcessing()

    def process(self, obj):
        for t in obj:
            obj[t]['results'] = self.process_text(obj[t]['text'])
        return obj

    def process_text(self, text):

        phrases = []
        #stemmed_phrases = []
        richness_of_posts = []

        has_bad_words = False
        has_slang = False
        has_net_lingo = False
        has_link = False
        has_qualifier = False
        has_retweet = False

        # fixup text
        text = text.replace(u"\u2019", "'")
        text = text.replace("&amp;", "&")
        text = text.replace("&#34;", "\"").replace("&quot;", "\"").replace("&ldquo;", "\"").replace("&rdquo;",
                                                                                                    "\"").replace('"',
                                                                                                                  ' " ')

        # experimental: convert non-digit single characters to periods so that they cause sentence breaks.
        # character must have space before and after itself to qualify.
        text = self.ta.convert_single_character_symbols_to_periods(text)

        # extract URIs
        uris = self.ta.extract_URIs(text)
        if len(uris) > 0:
            has_link = True

        # decode html entity characters
        text = self.ta.decode_special_chars(text)

        #  extract contacts
        contacts = self.ta.extract_contacts(text)
        if len(contacts) > 0:
            has_qualifier = True

        # extract topics
        topics = self.ta.extract_topics(text)
        topics = self.ta.cleanup_unicode_chars_in_topics(topics)
        topics = self.ta.remove_preceeding_pound_char(topics)
        if len(topics) > 0:
            has_qualifier = True

        # remove urls from text
        for url in uris:
            text = text.replace(url, " ")

        # remove contacts from text
        for contact in contacts:
            text = text.replace(contact, " ")

        # convert text to one or more sentences
        sentences = self.ta.convert_to_sentences(text)

        for aSentence in sentences:
            text = " ".join(aSentence)

            # remove special characters
            text = self.ta.strip_special_chars(text)

            # this may be the single most important step before using textana!
            # Eliminate non printable characters, namely unicode chars!
            text = filter(lambda x: x in string.printable, text)

            # Cleanup elipsees on words - found in sentenses where a sentence thought trails...
            new_word_list = []
            word_list = text.lower().split(" ")
            for w in word_list:
                w = self.ta.strip_trailing_periods(w)
                new_word_list.append(w)
            word_list = new_word_list

            # transpose words like can't and won't
            new_word_list = []
            for w in word_list:
                w = self.ta.transpose(w)
                if w.endswith("'s"):
                    w = w[:-2] + ' is'
                if w.find(' ') > -1:
                    for nw in w.split(' '):
                        new_word_list.append(nw)
                else:
                    new_word_list.append(w)
            word_list = new_word_list

            # ensure that we have single word lists
            word_list = self.ta.split_words(word_list)

            #if self.ta.is_english(word_list) == False:
            #	print "Not english:", text
            #	continue;

            # remove excess qoutes
            word_list = self.ta.remove_quotes(word_list)

            # remove commas
            word_list = self.ta.removeCommas(word_list)

            # ensure that we have single word lists
            word_list = self.ta.split_words(word_list)

            # handle time
            new_word_list = []
            for w in word_list:
                w = self.ta.fix_time(w)
                if w.find(' ') > -1:
                    for nw in w.split(' '):
                        new_word_list.append(nw)
                else:
                    # if word contains a colon and was not a time, remove colon from word
                    if not self.ta.is_time(w):
                        w = w.replace(":", " ")
                    new_word_list.append(w)

            word_list = new_word_list

            # ensure that we have single word lists
            word_list = self.ta.split_words(word_list)

            # clean-up non-dates
            new_word_list = []
            for w in word_list:
                if w.count("/") > 0 or w.count("-") > 0:
                    w = self.ta.handle_embedded_dash(w)
                    if not self.ta.isDate(w):
                        if w == "w/":
                            w = "with"
                        if w == "w/o":
                            w = "without"
                        w = w.replace("/", " ")  # .replace("-"," ")
                new_word_list.append(w)

            word_list = new_word_list

            # ensure that we have single word lists
            word_list = self.ta.split_words(word_list)

            # remove periods
            word_list = self.ta.remove_periods(word_list)

            # remove invalid words
            new_word_list = []
            for w in word_list:
                exclude = False
                tup = self.ta.largest_repeating_pattern(w)
                if tup[1] > 2:
                    exclude = True
                if self.ta.has_trailing_char(w):
                    exclude = True
                if not exclude:
                    new_word_list.append(w)
            word_list = new_word_list

            # ensure that we have single word lists
            #word_list = self.ta.split_words(word_list)

            # check for ReTweet
            for w in word_list:
                if w == "rt":
                    has_retweet = True
                    break

            word_list = self.ta.remove_words_from_list(word_list, ["@", "rt"])
            #word_list = self.ta.remove_word(word_list, "rt")

            # remove unicode chars
            word_list = self.ta.remove_unicode_chars(word_list)

            # Remove stray chars
            word_list = self.ta.cleanup_stray_chars(word_list)

            # check for qualifiers
            for w in word_list[:]:
                if not self.ta.isEmail(w) and w.startswith('@'):
                    has_qualifier = True
                    #contacts.append(w)
                    word_list.remove(w)

            # after translate functions above we want to ensure that we have single word lists
            word_list = self.ta.split_words(word_list)

            # has bad words or slang?
            if not has_bad_words:
                has_bad_words = self.ta.has_bad_words(word_list)
            if not has_slang:
                has_slang = self.ta.has_slang(word_list)
            if not has_net_lingo:
                has_net_lingo = self.ta.has_net_lingo(word_list)

            # remove suppress words.  Those are words which add little meaning
            word_list = self.ta.remove_suppress_words(word_list)

            # after translate functions above we want to ensure that we have single word lists
            word_list = self.ta.split_words(word_list)

            # fixing misspellings, translating twitter, net and slang lingo
            new_word_list = []
            for w in word_list:
                if self.ta.is_URI(w):
                    w = " "
                else:
                    w = self.ta.remove_leading_char(w, "`")
                    w = self.ta.remove_leading_char(w, "'")
                    w = self.ta.remove_leading_char(w, "<")
                    w = self.ta.remove_leading_char(w, ">")
                    w = self.ta.remove_leading_char(w, "&")
                    w = self.ta.remove_leading_char(w, "-")
                    w = self.ta.remove_leading_char(w, "/")
                    w = self.ta.remove_leading_char(w, "\"")
                    w = self.ta.fix_spelling(w)
                    w = self.ta.trans_net_lingo(w)
                    #w = self.ta.fix_slang_lingo(w)
                    w = self.ta.twitter_translate(w)
                    #w = self.ta.trans_double_word(w)

                #if self.ta.dictionary_word(w) == False and self.ta.is_name(w) == False:
                #	if len(w) > 2 and w.endswith('in') == True:
                #		nw = w + 'g'
                #		if self.ta.dictionary_word(nw) == True:
                #			w = nw
                #			has_slang = True
                #		if self.ta.dictionary_word(nw[:-3]) == True:
                #			w = nw[:-3]
                #			#has_slang = True
                #	if w.endswith('z') == True:
                #		nw = w[:-1]
                #		if self.ta.dictionary_word(nw) == True:
                #			w = nw
                #			#has_slang = True
                new_word_list.append(w)

            word_list = new_word_list

            # again, after translate functions above we want to ensure that we have single word lists
            word_list = self.ta.split_words(word_list)

            # Check again, because above translation may have introduced new bad,slang or netlingo terms
            if not has_bad_words:
                has_bad_words = self.ta.has_bad_words(word_list)
            if not has_slang:
                has_slang = self.ta.has_slang(word_list)
            if not has_net_lingo:
                has_net_lingo = self.ta.has_net_lingo(word_list)

            # append to list of phrases
            # self.ta.find_phrases(word_list, phrases, stemmed_phrases)
            self.ta.find_phrases(word_list, phrases, None)

            # determine richness of post
            post_scale = 1.0  # don't scale at this time
            richness_of_post = self.ta.richness_of_text(word_list) * post_scale * 100.0

            if has_retweet:  # if retweet then the user didn't really say this so reduce score
                richness_of_post *= 0.25
            if len(phrases) > 1:
                richness_of_post += len(phrases) * 0.75
            if len(contacts) > 1:
                richness_of_post += 2.0
            if has_bad_words:
                richness_of_post *= 0.01
            if richness_of_post > 100:
                richness_of_post = 100
            richness_of_posts.append(richness_of_post)

        # compute average richness_of_post
        richness_of_post = 0.0
        if len(richness_of_posts) > 0:
            richness_of_post = sum(richness_of_posts) / len(richness_of_posts)

        js = {
            'uris': uris,
            'contacts': contacts,
            #'topics': topics,
            'subphrases': phrases,
            #'stemmedSubPhrases': stemmed_phrases,
            'richness_of_post': "%.2f" % richness_of_post,
            'has_bad_words': has_bad_words,
            'has_slang': has_slang,
            'has_net_lingo': has_net_lingo,
            'has_link': has_link,
            'has_qualifier': has_qualifier,
            #'has_retweet': has_retweet
        }
        return js
