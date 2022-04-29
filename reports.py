from typing import Dict, List, Tuple, Callable, TypeVar
import nltk
from google.cloud import storage
import json

T1 = TypeVar('T')
T2 = TypeVar('T')
T3 = TypeVar([str, List[str]])


class report():
    def __init__(self, file_list: List[str] = None, files_text: Dict[str, str] = None) -> None:
        self.text_content = {}
        self.files_text = None
        if files_text is not None:
            self.files_text = files_text
        else:
            self.files_list = file_list
            self.files_text = []
            for file in self.files_list:
                with open(file) as f:
                    self.files_text.append(f.read())

    @staticmethod
    def get_ngrams(myString: str, num: int) -> T3:
        def stem_remove_list(my_text: T3) -> T3:
            stemming = nltk.stem.PorterStemmer()
            tokenizer = nltk.tokenize.regexp.RegexpTokenizer(r"\w+")
            stop = list(set(nltk.corpus.stopwords.words("english")))
            my_list = tokenizer.tokenize(my_text)
            stemmed_list = [stemming.stem(word) for word in my_list]
            meaningful_words = [w for w in stemmed_list if w not in stop]
            meaningful_words = [word for word in meaningful_words if word.isalnum()]  # noqa: E501
            return(meaningful_words)
        words = stem_remove_list(myString)
        n_grams = nltk.ngrams(words, num)
        temp = []
        for grams in n_grams:
            temp.append(grams)
        return(temp)

    def apply_all_documents(self, function: Callable[..., List[T2]], 
                            num: str = 3, reset_content: bool = True) -> None:
        if reset_content is True:
            self.text_content = {}

        if num is not None:
            for key, value in self.files_text.items():
                try:
                    self.text_content[key] = function(myString=value, num=num)
                except Exception as e:
                    print(str(e))
                    
    def subset_ngram(self, sub: Tuple[str, ...]) -> None:
        temp = {}
        for key, ngram in self.text_content.items():
            temp[key] = []
            for gram in ngram:
                cond = True
                if len(sub) == 1:
                    if gram[0] not in sub:
                        cond = False
                else:
                    for i in range(0, len(sub)):
                        if gram[i] not in sub[i]:
                            cond = False
                if cond:
                    temp[key].append(gram)
        return(temp)

    @staticmethod
    def create_json(json_object: str, filename: str, bucket_name: str):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(filename)
        # upload the blob 
        blob.upload_from_string(
            data=json.dumps(json_object),
            content_type='application/json'
            )
        result = filename + ' upload complete'
        return {'response': result}