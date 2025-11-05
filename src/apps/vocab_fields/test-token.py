from gensim.models import KeyedVectors
import fugashi
import os

from jisho_api.word import Word

word = Word()

result = word.request("食べる")
# print(result)
senses = result.data[0].senses
for sense in senses:
    print(sense.english_definitions)


# print(result.data[0].senses[0].english_definitions)
print(result.data[0].senses)
# print(result[0]['japanese'][0]['word'], result[0]['senses'][0]['english_definitions'])

exit()


from pprint import pprint

print(f"LOADEDING MODEL")
model = KeyedVectors.load_word2vec_format("cc.ja.300.vec", binary=False, limit=10000)
print(f"LOADED MODEL: {model}")
tagger = fugashi.Tagger()


field_words = ['牛',
 '羊',
 '豚',
 '鶏',
 '犬',
 '猫',
 '熊',
 '鹿',
 '虎',
 '肉',
 '魚',
 '馬',
 '鳥',
 '動物',
 '狼',
 '獣',
 '蛇']

# ["牛", "羊", "豚", "鶏",   # farm
#  "犬", "猫",         # domestic
#  "熊", "鹿", "虎"]                 # wild
#["牛", "羊", "豚", "鶏"]
# ["動物"]
# ["犬", "馬", "鳥"]  # your animal seeds
word = "猫"


while True:
    similar_vecs = model.most_similar(positive=field_words, topn=20)
    similar_words = [w for w, score in similar_vecs]  # extract only the words
    os.system("cls")
    pprint(field_words)
    pprint(similar_vecs)

    print('NEW INPUT (n to skip)')
    user_input = input("WORD: ")
    if user_input == "n":
        continue
    elif user_input in similar_words:
        field_words.append(user_input)
        print(f"'{user_input}' added to the field!")
    else:
        print(f"'{user_input}' not similar enough to the field, skipped.")

    


# from PyQt6.QtCore import *
# from PyQt6.QtWidgets import * 
# from PyQt6.QtGui import *

# from src.helper_functions import *
# from src.helper_classes import *
# from .blueprint import Blueprint
# from src.components import *
# from .blueprint import Blueprint

# from gensim.models import KeyedVectors
# import fugashi

# """
# Close methods
# Ctrl+k + Ctrl+0

# Open Methods 
# Ctrl+k + Ctrl+J
# """
# class Logic(Blueprint):

    # typing_area: QTextEdit
    # vec_view: QLabel
    # view: QLabel
    # prev_btn: QPushButton
    # next_btn: QPushButton

#     def __init__(self, component):
#         super().__init__()
#         self._map_widgets(component)
#         self.component = component

#         self.recall_tracker = RecallTracker()
#         self.stored_words = list(self.recall_tracker.get_stored_words())
#         self.stored_word_idx = 0
#         self.allowed_words_idx = 0
#         self.allowed_words = []
#         self.not_allowed_words = []
#         print("Loading MODEL")
#         self.model = KeyedVectors.load_word2vec_format("cc.ja.300.vec", binary=False, limit=10000)
#         print(f"LOADED MODEL: {self.model}")
#         self.tagger = fugashi.Tagger()
#         self.find_words()

#     def tokenize(self, text):
#         return [word.surface for word in self.tagger(text)]

#     def tokenize_lem(self, text):
#         # Use lemma (feature.lemma), fallback to surface if missing
#         return [w.feature.lemma if w.feature.lemma != "*" else w.surface for w in self.tagger(text)]

#     def find_words(self):
#         print("Finding Words")
#         for word in self.stored_words:
#             for token in self.tokenize(word):
#                 if token in self.model:
#                     self.allowed_words.append(token)
#                 else:
#                     self.not_allowed_words.append(token)

#         print(f"allowed ({len(self.allowed_words)}): \t{self.allowed_words}")
#         print(f"NOT allowed ({len(self.not_allowed_words)}): \t{self.not_allowed_words}")

#     def get_prev_word(self):
#         if self.allowed_words_idx == 0:
#             print(self.allowed_words_idx)
#             print("No more prev words")
#             self.view.setText("No more prev words")

#         else:
#             self.allowed_words_idx -= 1
#             word = self.allowed_words[self.allowed_words_idx]
#             self.view.setText(word)

#             similar_vecs = self.model.most_similar(positive=[word], topn=20) #self.model.most_similar(word)
#             vecs_as_str = self.word_str(similar_vecs)
#             self.vec_view.setText(vecs_as_str)

#     def get_next_word(self):
#         if self.allowed_words_idx >= len(self.stored_words):
#             print(self.allowed_words_idx)
#             print("No more next words")
#             self.view.setText("No more next words")
#         else:
#             self.allowed_words_idx += 1
#             word = self.allowed_words[self.allowed_words_idx]
#             self.view.setText(word)

#             similar_vecs = self.model.most_similar(positive=[word], topn=20) #self.model.most_similar(word)
#             vecs_as_str = self.word_str(similar_vecs)
#             self.vec_view.setText(vecs_as_str)

            
#     def word_str(self, vecs: list):
#         return "\n".join([t[0] for t in vecs])
    
#     def print_words(self):
#         print(self.stored_words)
#         # text = self.typing_area.toPlainText()


    
