import re

regex_sentence = re.compile(r'\D*[.]')
sentence_dict = dict()
word_dict = dict()
sorted_num_word = list()


def input_sentence_dict(sentence):
    input_string = input()
    sentence_num = 0
    sentence[0] = ''
    for i in input_string:
        if i != '.':
            sentence[sentence_num] += i
        else:
            sentence_num += 1
            sentence[sentence_num] = ''


input_sentence_dict(sentence_dict)
print(sentence_dict)
