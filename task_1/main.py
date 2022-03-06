import re

sentence_dict = dict()
word_dict = dict()

length_of_gram = 4
top_grams_num = 10
n_gram = dict()


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


def sort_dict(dictionary, rev=True):
    if rev == True:
        temp = dict(sorted(dictionary.items(), key=lambda x: x[1]))
    else:
        temp = dict(sorted(dictionary.items(), key=lambda x: -x[1]))
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


def get_n_grams(gram_dict, dictionary, num):
    for i in dictionary:
        i_sentence = dictionary.setdefault(i)
        for j in range(len(i_sentence) - num + 1):
            gram_str = create_gram(j, i_sentence, num)

            if len(gram_str) == num:
                gram_dict.setdefault(gram_str[0])
                if gram_dict[gram_str[0]] is None:
                    gram_dict[gram_str[0]] = dict()
                    add_gram(gram_dict, gram_str)
                else:
                    add_gram(gram_dict, gram_str)
    for i in gram_dict:
        sort_dict(gram_dict.setdefault(i))


def top_n_grams(gram_dict):
    gram_top = dict()
    num = 0
    for i in gram_dict:
        for j in gram_dict.setdefault(i):
            gram_top[j] = gram_dict.setdefault(i).setdefault(j)
            num += 1
    sort_dict(gram_top, False)
    return gram_top


def print_top_grams(gram_top, top):
    boolean = True
    temp = 1
    memory = 0
    for i in gram_top:
        if gram_top.setdefault(i) == memory:
            boolean = True
        else:
            boolean = False
        if temp > top and memory != gram_top.setdefault(i):
            break
        print(temp, ".", i, " - ", gram_top.setdefault(i))
        memory = gram_top.setdefault(i)
        temp += 1


def create_gram(j, i_sentence, num, gram_str=''):
    for t in range(j, j + num):
        if re.match(r"[a-zA-Z]", i_sentence[t]):
            gram_str += i_sentence[t]
        else:
            break
    return gram_str


def add_gram(dictionary, gram):
    if gram not in dictionary[gram[0]]:
        dictionary[gram[0]][gram] = 0
    dictionary[gram[0]][gram] += 1


create_sentence_dict(sentence_dict, input())
print(sentence_dict)
create_word_dict(word_dict, sentence_dict)
print(word_dict)
print("middle num of words: ", get_middle_sum(word_dict))
print("median:", get_median(word_dict))

get_n_grams(n_gram, sentence_dict, length_of_gram)
print(n_gram)
print(top_n_grams(n_gram))
print_top_grams(top_n_grams(n_gram), top_grams_num)
