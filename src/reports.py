from typing import List, Callable, TypeVar
import nltk

T1 = TypeVar('T')
T2 = TypeVar('T')
T3 = TypeVar([str, List[str]])


class tokenize_report():
    def __init__(self, file_list: List[str]) -> None:
        self.text_content = []
        self.files_text = []
        self.files = file_list
        for file in file_list:
            with open(file) as f:
                self.files_text.append(f.read())

    @staticmethod 
    def get_ngrams(myString: str, num: int) -> T3:
        
        def stem_remove_list(my_text: T3) -> T3:
            stemming = nltk.stem.PorterStemmer()
            tokenizer = nltk.RegexpTokenizer(r"\w+")
            stop = list(set(nltk.corpus.stopwords.words("english")))
            my_list = tokenizer(my_text)
            stemmed_list = [stemming.stem(word) for word in my_list]
            meaningful_words = [w for w in stemmed_list if w not in stop]
            meaningful_words = [word for word in meaningful_words if word.isalnum()]  # noqa: E501
            return(meaningful_words)

        n_grams = nltk.ngrams(stem_remove_list(myString), num)
        return(n_grams)
    
    @classmethod
    def apply_all_documents(cls, function: Callable[..., List[T2]] = 
                            get_ngrams, num: str = 3, 
                            reset_content: bool = True) -> List[T3]:
        if reset_content is True:
            cls.text_content = []

        if num is None:
            for text in cls.files_text:
                try:
                    cls.text_content.append(function(myString=text, num=num))

                except Exception as e:
                    print(str(e))

        return(cls.text_content)
