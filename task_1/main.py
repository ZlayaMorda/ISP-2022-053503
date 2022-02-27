import re

regex_sentence = re.compile(r'\D*[.]')
sentence_dict = dict()
word_dict = dict()
sorted_num_word = list()


def input_sentence_dict(sentence):
    input_string = input()
    sentence_num = 0
    sentence[0] = ''
    bracket_temp = False
    for i in input_string:
        if i != '.' and re.match(r'\D', i) is not None:
            sentence[sentence_num] += i
        elif i == '.' or i == '!' or i == '?' or i == ';':
            sentence_num += 1
            sentence[sentence_num] = ''
        elif i == '(' or i == '[' or i == '{':
            bracket_temp = True
            #доделать скобки и убрать остальные знаки


input_sentence_dict(sentence_dict)
print(sentence_dict)
