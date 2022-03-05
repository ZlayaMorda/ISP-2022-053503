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
    sentence.pop(sentence_num)


def create_word_dict(words, sentence):
    for i in sentence:
        words[i] = 0
        words[i] = len([word for word in sentence[i].split() if word.isalpha()])
    sort_dict(words)


def sort_dict(dictionary):
    temp = dict(sorted(dictionary.items(), key=lambda x: x[1]))
    dictionary.clear()
    for i in temp:
        dictionary[i] = temp.setdefault(i)


def get_middle_sum(dictionary):
    temp_sum = 0
    for i in dictionary:
        temp_sum += dictionary.setdefault(i)
    temp_sum /= len(dictionary)
    return temp_sum


def get_median(dictionary):
    length = int(len(dictionary) / 2)
    if len(dictionary) % 2 == 0:
        return (dictionary[length] + dictionary[length + 1]) / 2
    else:
        return dictionary[length]


create_sentence_dict(sentence_dict, input())
print(sentence_dict)
create_word_dict(word_dict, sentence_dict)
print(word_dict)
print("middle num of words: ", get_middle_sum(word_dict))
print("median:", get_median(word_dict))
