from japanese_verb_conjugator_v2 import Formality, Polarity, Tense, VerbClass, JapaneseVerbFormGenerator as jvfg

test1 = jvfg.generate_plain_form("飲む", VerbClass.GODAN, Tense.NONPAST, Polarity.POSITIVE) # returns '飲む'
test2 = jvfg.generate_plain_form("飲む", VerbClass.GODAN, Tense.NONPAST, Polarity.NEGATIVE) # returns '飲まない'

print(test2)