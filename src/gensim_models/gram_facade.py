
BIGRAMS_PHRASER_FILENAME   = 'bigrams_phraser'
BIGRAMS_PHRASES_FILENAME   = 'bigrams_phrases'
TRIGRAMS_PHRASER_FILENAME   = 'trigrams_phraser'
TRIGRAMS_PHRASES_FILENAME   = 'trigrams_phrases'
BIGRAMS_PICKLE  = 'trigrams.p'
TRIGRAMS_PICKLE = 'bigrams.p'




from gensim.models.phrases import Phraser, Phrases
class GramFacade:

    def __init__(self, model_dir, bigrams_threshold=0.88, trigrams_threshold=0.88):
        self.model_dir = model_dir
        self.bigrams_threshold=bigrams_threshold
        self.trigrams_threshold=trigrams_threshold

    def load_models(self):
        self.bigrams_phraser = Phraser.load(self.model_dir + '/' + BIGRAMS_PHRASER_FILENAME)
        self.trigrams_phraser = Phraser.load(self.model_dir + '/' + TRIGRAMS_PHRASER_FILENAME)

    def load_phrases(self):
        self.bigrams_phrases = Phrases.load(self.model_dir + '/' + BIGRAMS_PHRASES_FILENAME)
        self.trigrams_phrases = Phrases.load(self.model_dir + '/' + TRIGRAMS_PHRASES_FILENAME)

    def export_bigrams(self, docs):
         return  [self.bigrams_phraser[doc] for doc in  docs]

    def export_trigrams(self, bigrams):
        return [self.trigrams_phraser[bigram] for bigram in bigrams]


    def phrase(self, doc):
        bigrams = self.bigrams_phraser[doc]
        trigrams = self.trigrams_phraser[bigrams]
        return trigrams


    def create_model(self, doc_list):
        self.bigrams_phrases = Phrases(doc_list, scoring='npmi', threshold=self.bigrams_threshold)
        self.bigrams_phraser = Phraser(self.bigrams_phrases)
        self.trigrams_phrases = Phrases(self.bigrams_phraser[doc_list], scoring='npmi', threshold=self.trigrams_threshold)
        self.trigrams_phraser = Phraser(self.trigrams_phrases)
        self.bigrams_phraser.save(self.model_dir + '/' + BIGRAMS_PHRASER_FILENAME)
        self.trigrams_phraser.save(self.model_dir + '/' + TRIGRAMS_PHRASER_FILENAME)
        self.bigrams_phrases.save(self.model_dir + '/' + BIGRAMS_PHRASES_FILENAME)
        self.trigrams_phrases.save(self.model_dir + '/' + TRIGRAMS_PHRASES_FILENAME)

    def words_not_in_vocab(self, tok_doc, threshold):
        word_not_in_doc =set([ x for x in tok_doc if self.trigrams_phrases.vocab[str.encode(x)] < threshold ])
        return word_not_in_doc


    def retrieve_grams(self):
        pgrams = self.trigrams_phraser.phrasegrams
        gram_list = []
        for word, values in pgrams.items():
            gram = b'_'.join(word)
            count, score = values[0], values[1]
            gram_list.append({"gram": gram.decode("utf-8"), "count": count, "score": score})
        gram_sorted = sorted(gram_list, key=lambda x: x["score"], reverse=True )
        return gram_sorted