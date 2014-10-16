# -*- coding: utf-8 -*-
import sys
from nltk.corpus import stopwords
import nltk
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
import string

from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from itertools import chain

stop = stopwords.words('english')

porter = PorterStemmer()

def compare_overlaps_greedy(context, synsets_signatures):
  
  max_overlaps = 0; lesk_sense = None
  for ss in synsets_signatures:
    overlaps = set(synsets_signatures[ss]).intersection(context)
    if len(overlaps) > max_overlaps:
      lesk_sense = ss
      max_overlaps = len(overlaps)    
  return lesk_sense

def compare_overlaps(context, synsets_signatures, \
                     nbest=False, keepscore=False, normalizescore=False):
  overlaplen_synsets = [] # a tuple of (len(overlap), synset).
  for ss in synsets_signatures:
    overlaps = set(synsets_signatures[ss]).intersection(context)
    overlaplen_synsets.append((len(overlaps), ss))

  # Rank synsets from highest to lowest overlap.
  ranked_synsets = sorted(overlaplen_synsets, reverse=True)
  
  # Normalize scores such that it's between 0 to 1. 
  if normalizescore:
    total = float(sum(i[0] for i in ranked_synsets))
    ranked_synsets = [(i/total,j) for i,j in ranked_synsets]
    
  if not keepscore: # Returns a list of ranked synsets without scores
    ranked_synsets = [i[1] for i in sorted(overlaplen_synsets, reverse=True)]
    
  if nbest: # Returns a ranked list of synsets.
    return ranked_synsets
  else: # Returns only the best sense.
    return ranked_synsets[0]

def original_lesk(context_sentence, ambiguous_word, dictionary=None):
  if not dictionary:
    dictionary = {ss:ss.definition.split() for ss in wn.synsets(ambiguous_word)}
  best_sense = compare_overlaps_greedy(context_sentence.split(), dictionary)
  return best_sense    

def simple_signature(ambiguous_word, pos=None, stem=True, \
                     hyperhypo=True, stop=True):
  synsets_signatures = {}
  for ss in wn.synsets(ambiguous_word):
    # If POS is specified.
    if pos and str(ss.pos) is not pos:
      continue
    signature = []
    # Includes definition.
    signature+= ss.definition.split()
    # Includes examples
    signature+= list(chain(*[i.split() for i in ss.examples]))
    # Includes lemma_names.
    signature+= ss.lemma_names
    # Optional: includes lemma_names of hypernyms and hyponyms.
    if hyperhypo == True:
      signature+= list(chain(*[i.lemma_names for i \
                               in ss.hypernyms()+ss.hyponyms()]))
    # Optional: removes stopwords.
    if stop == True:
      signature = [i for i in signature if i not in stopwords.words('english')]    
    # Matching exact words causes sparsity, so optional matching for stems.
    if stem == True: 
      signature = [porter.stem(i) for i in signature]
    synsets_signatures[ss] = signature
  return synsets_signatures

def simple_lesk(context_sentence, ambiguous_word, \
                pos=None, stem=True, hyperhypo=True, \
                nbest=False, keepscore=False, normalizescore=False):
  # Get the signatures for each synset.
  ss_sign = simple_signature(ambiguous_word, pos, stem, hyperhypo)
  print ("==================SS_SIGN=======================")
  print (ss_sign)
  # Disambiguate the sense in context.
  context_sentence = [porter.stem(i) for i in context_sentence.split()]
  best_sense = compare_overlaps(context_sentence, ss_sign, \
                                nbest=nbest, keepscore=keepscore, \
                                normalizescore=normalizescore)  
  return best_sense

def adapted_lesk(context_sentence, ambiguous_word, \
                pos=None, stem=True, hyperhypo=True, stop=True, \
                nbest=False, keepscore=False, normalizescore=False):
  # Get the signatures for each synset.
  ss_sign = simple_signature(ambiguous_word, pos, stem, hyperhypo)
  for ss in ss_sign:
    related_senses = list(set(ss.member_holonyms() + ss.member_meronyms() + 
                             ss.part_meronyms() + ss.part_holonyms() + 
                             ss.similar_tos() + ss.substance_holonyms() + 
                             ss.substance_meronyms()))
    
    print (related_senses)
    signature = list([j for j in chain(*[i.lemma_names for i in \
                      related_senses]) if j not in stop])    
    # Matching exact words causes sparsity, so optional matching for stems.
    if stem == True: 
      signature = [porter.stem(i) for i in signature]
    ss_sign[ss]+=signature
  
  # Disambiguate the sense in context.
  context_sentence = [porter.stem(i) for i in context_sentence.split()]
  best_sense = compare_overlaps(context_sentence, ss_sign, \
                                nbest=nbest, keepscore=keepscore, \
                                normalizescore=normalizescore)
  return best_sense

