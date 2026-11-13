import math


class CountVectorizer:
    def __init__(self, lowercase=True, ngram_size=1):
        self._vocabulary = {}
        self.lowercase = lowercase
        self.ngram_size = ngram_size

    @property
    def vocabulary(self):
        if self._vocabulary is None:
            return {}
        return self._vocabulary

    @vocabulary.setter
    def vocabulary(self, new_vocabulary):
        if not isinstance(new_vocabulary, dict):
            raise ValueError("Новое значение должно быть словарем")

        indexes = list(new_vocabulary.values())

        if sorted(indexes) != list(range(len(indexes))):
            raise ValueError("Индексы должны быть от 0 до длинны словаря - 1")

        self._vocabulary = new_vocabulary.copy()

    @vocabulary.deleter
    def vocabulary(self):
        self._vocabulary = None

    def add_word(self, word):
        if word not in self.vocabulary:
            self.vocabulary[word] = len(self.vocabulary)
        return self.vocabulary[word]

    @classmethod
    def from_dict(cls, recording):
        vectorizer = cls(
            lowercase=recording["lowercase"],
            ngram_size=recording["ngram_size"]
        )

        vectorizer.vocabulary = recording["vocabulary"].copy()

        return vectorizer

    def tokenize(self, text):
        if self.lowercase:
            text = text.lower()
        words = text.split()
        if len(words) < self.ngram_size:
            return []

        tokens = []

        for i in range(len(words) - (self.ngram_size - 1)):
            token = " ".join(words[i:i + self.ngram_size])
            tokens.append(token)

        return tokens

    def fit(self, corpus):
        temp_vectorizer = CountVectorizer(
            lowercase=self.lowercase,
            ngram_size=self.ngram_size
        )

        for text in corpus:
            tokens = self.tokenize(text)

            for token in tokens:
                temp_vectorizer.add_word(token)

        if len(temp_vectorizer.vocabulary) == 0:
            raise ValueError("Корпус не содержит подходящих токенов")

        self.vocabulary = temp_vectorizer.vocabulary
        return self

    def transform(self, corpus):

        if not self.vocabulary:
            raise RuntimeError("Словарь пустой, объект надо сначала обучить")

        corpus_transformed = []
        for text in corpus:
            tokens = self.tokenize(text)

            text_transformed = [0] * len(self.vocabulary)

            for token in tokens:
                if token in self.vocabulary:
                    text_transformed[self.vocabulary[token]] += 1

            corpus_transformed.append(text_transformed)

        return corpus_transformed

    def get_feature_names(self):
        return sorted(self.vocabulary, key=lambda word: self.vocabulary[word])

    def fit_transform(self, corpus):
        self.fit(corpus)
        return self.transform(corpus)

    def to_dict(self):
        return {
            "lowercase": self.lowercase,
            "ngram_size": self.ngram_size,
            "vocabulary": self.vocabulary.copy()
        }


class BinaryVectorizer(CountVectorizer):

    def transform(self, corpus):

        if not self.vocabulary:
            raise RuntimeError("Словарь пустой, объект надо сначала обучить")

        corpus_transformed = []
        for text in corpus:
            tokens = set(self.tokenize(text))

            text_transformed = [0] * len(self.vocabulary)

            for token in tokens:
                if token in self.vocabulary:
                    text_transformed[self.vocabulary[token]] = 1

            corpus_transformed.append(text_transformed)

        return corpus_transformed


class TfidfVectorizer(CountVectorizer):

    def __init__(self, lowercase=True, ngram_size=1, use_idf=True):
        super().__init__(lowercase, ngram_size)
        self.use_idf = use_idf
        self._idf = []

    @property
    def idf(self):
        return self._idf.copy()

    @classmethod
    def from_config(cls, config):
        return cls(
            lowercase=config.get("lowercase", True),
            use_idf=config.get("use_idf", True)
        )

    def fit(self, corpus):
        super().fit(corpus)

        if not self.use_idf:
            self._idf = []
            return self

        N = len(corpus)
        df = [0] * len(self.vocabulary)

        for text in corpus:
            tokens = set(self.tokenize(text))

            for token in tokens:
                if token in self.vocabulary:
                    index = self.vocabulary[token]
                    df[index] += 1

        self._idf = []

        for frequency in df:
            idf_value = math.log((N + 1) / (frequency + 1)) + 1
            self._idf.append(idf_value)

        return self

    def transform(self, corpus):
        if not self.vocabulary:
            raise RuntimeError("Словарь пустой, объект надо сначала обучить")

        corpus_transformed = []

        for text in corpus:
            tokens = self.tokenize(text)
            text_transformed = [0] * len(self.vocabulary)

            for token in tokens:
                if token in self.vocabulary:
                    index = self.vocabulary[token]
                    text_transformed[index] += 1

            total_words = sum(text_transformed)

            if total_words == 0:
                corpus_transformed.append([0.0] * len(self.vocabulary))
                continue

            tfidf = []

            for i in range(len(self.vocabulary)):
                tf = text_transformed[i] / total_words

                if self.use_idf:
                    tf *= self._idf[i]

                tfidf.append(tf)

            corpus_transformed.append(tfidf)

        return corpus_transformed


class KeywordExtractor:

    def __init__(self, vectorizer, top_n=3):
        self.vectorizer = vectorizer
        self.top_n = top_n

        if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n <= 0:
            raise ValueError("top_n должен быть целым числом больше 0")

    @property
    def top_n(self):
        return self._top_n

    @top_n.setter
    def top_n(self, value):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError("top_n должен быть целым числом больше 0")

        self._top_n = value

    def fit(self, corpus):
        self.vectorizer.fit(corpus)
        return self

    def extract(self, corpus):
        matrix = self.vectorizer.transform(corpus)
        feature_names = self.vectorizer.get_feature_names()

        result = []

        for row in matrix:
            words = []

            for i, weight in enumerate(row):
                if weight > 0:
                    words.append((feature_names[i], weight))

            words.sort(key=lambda x: (-x[1], x[0]))

            result.append(words[:self.top_n])

        return result


# Обучающие сообщения
TRAIN_CORPUS = [
    "Марс сигнал сигнал",
    "Марс пыль",
    "Марс сигнал антенна"
]

# Сообщения для проверки
CHECK_CORPUS = [
    "СИГНАЛ шум сигнал",
    "антенна пыль",
    "марс марс марс",
    "комета",
    ""
]


def demo():
    train_corpus = [
        "Марс сигнал сигнал",
        "Марс пыль",
        "Марс сигнал антенна"
    ]

    check_corpus = [
        "СИГНАЛ шум сигнал",
        "антенна пыль",
        "марс марс марс",
        "комета",
        ""
    ]

    print("Сценарий 1")

    tfidf = TfidfVectorizer.from_config({})
    results_fit_transform = tfidf.fit_transform(train_corpus)
    results_transform = tfidf.transform(train_corpus)

    print("Слова", tfidf.get_feature_names())
    print("idf", tfidf.idf)
    print("Corpus fit_transform")
    print(results_fit_transform)
    print("Corpus transform")
    print(results_transform)

    idf_copy = tfidf.idf
    idf_copy.clear()

    print("idf", tfidf.idf)

    print("\nСценарий 2")

    tf_vectorizer = TfidfVectorizer.from_config({
        "lowercase": False,
        "use_idf": False
    })

    tf_corpus = [
        "Марс марс",
        "МАРС сигнал"
    ]

    tf_results = tf_vectorizer.fit_transform(tf_corpus)

    print("cлова", tf_vectorizer.get_feature_names())
    print("idf", tf_vectorizer.idf)
    print("TF", tf_results)

    tfidf.fit(["Венера облака"])

    print("cлова", tfidf.get_feature_names())
    print("idf", tfidf.idf)
    print("TF", tfidf.transform(["Марс Венера облака"]))

    print("\nСценарий 3")

    extractor = KeywordExtractor(tfidf, top_n=2)
    extractor.fit(train_corpus)

    print("ключевые слова, top_n=2:")
    print(extractor.extract(check_corpus))

    extractor.top_n = 1

    print("ключевые слова, top_n=1:")
    print(extractor.extract(check_corpus))

    try:
        extractor.top_n = 0
    except ValueError as error:
        print("Ошибка:", error)


if __name__ == "__main__":
    demo()
