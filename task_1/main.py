import re

sentence_dict = dict()
word_dict = dict()
sorted_num_word = list()


def create_sentence_dict(sentence, input_string):
    sentence_num = 0
    sentence[0] = ''
    bracket_temp = False
    for i in input_string:
        if re.match(r"[a-zA-Z]|\s", i) is not None:
            sentence[sentence_num] += i
        elif i == '.' or i == '!' or i == '?' or i == ';':
            if sentence[sentence_num] and sentence[sentence_num].strip():
                sentence_num += 1
                sentence[sentence_num] = ''
                bracket_temp = False
        elif i == '(':
            bracket_temp = True
        elif i == ')':
            if not bracket_temp:
                sentence_num += 1
                sentence[sentence_num] = ''
            else:
                bracket_temp = False


create_sentence_dict(sentence_dict, input())
print(sentence_dict)
