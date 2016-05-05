#! /usr/bin/env python
# -*- coding: latin-1 -*-

from facepy import GraphAPI
from json import loads
from time import sleep
import random
import pickle

verbose = True

def scrape(oauth):
     graph = GraphAPI(oauth)
     confess = 462508190484900
     messages = graph.get(str(confess)+'/posts',page=True,limit=100)
     words = []
     i = 0
     try:
         for posts in messages:
             sleep(.1)
             for post in posts['data']:
                 i += 1
                 words += post['message'].split()
                 words += ['eND']
             if verbose:
                 print i
     except:
         pass
     with open('confessions.pkl','w+') as f:
         pickle.dump(words,f)

class MitMarkov(object):

	def __init__(self):
		self.cache = {}
		self.words = self.file_to_words()
		self.word_size = len(self.words)
		self.database()


	def file_to_words(self):
            with open('confessions.pkl','r') as f:
                words = pickle.load(f)
            return words


	def triples(self):
		""" Generates triples from the given data string. So if our string were
				"What a lovely day", we'd generate (What, a, lovely) and then
				(a, lovely, day).
		"""

		if len(self.words) < 3:
			return

		for i in range(len(self.words) - 2):
			yield (self.words[i], self.words[i+1], self.words[i+2])

	def database(self):
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]

	def generate_markov_text(self, size=200):
	        seed_word = 'a'
                while seed_word != 'eND':
                     seed = random.randint(0, self.word_size-3)
	             seed_word, next_word = self.words[seed], self.words[seed+1]
		w1, w2 = seed_word, next_word
                stops = '#'
		gen_words = []
		for i in xrange(size):
		    gen_words.append(w1)
		    w1, w2 = w2, random.choice(self.cache[(w1, w2)])
                    if w2 == 'eND':
                        break
                return ' '.join(gen_words[1:])

markov = MitMarkov()
while True:
     text = markov.generate_markov_text()
     text = text.replace(u'\u2019',"'")
     try:
         print text.decode("unicode-escape")
     except:
         print repr(text)
     raw_input()

