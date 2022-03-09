import re

sentence_dict = dict()


def sort_dict(dictionary, rev=True):
    if rev is True:
        temp = dict(sorted(dictionary.items(), key=lambda x: x[1]))
    else:
        temp = dict(sorted(dictionary.items(), key=lambda x: -x[1]))
    dictionary.clear()
    for i in temp:
        dictionary[i] = temp.setdefault(i)


class Word:
    word_dict = dict()

    def create_word_dict(self, sentence):
        for i in sentence:
            Word.word_dict[i] = 0
            Word.word_dict[i] = len([word for word in sentence[i].split() if word.isalpha()])
        sort_dict(Word.word_dict)

    def get_middle_sum(self):
        middle_sum = 0
        for i in Word.word_dict:
            middle_sum += Word.word_dict.setdefault(i)
        middle_sum /= len(Word.word_dict)
        return middle_sum

    def print_middle_sum(self):
        print("middle num of words: ", self.get_middle_sum())

    def get_median(self):
        length = int(len(Word.word_dict) / 2)
        if len(Word.word_dict) % 2 == 0:
            return (Word.word_dict[length] + Word.word_dict[length + 1]) / 2
        else:
            return Word.word_dict[length]

    def print_median(self):
        print("median:", self.get_median())


class Grams:
    n_gram = dict()
    length_of_gram = 4
    top_grams_num = 10
    gram_top = dict()

    def get_n_grams(self, sen_dict):
        for i in sen_dict:
            i_sentence = sen_dict.setdefault(i)
            for j in range(len(i_sentence) - Grams.length_of_gram + 1):
                gram_str = self.create_gram(j, i_sentence)

                if len(gram_str) == Grams.length_of_gram:
                    Grams.n_gram.setdefault(gram_str[0])
                    if Grams.n_gram[gram_str[0]] is None:
                        Grams.n_gram[gram_str[0]] = dict()
                        self.add_gram(gram_str)
                    else:
                        self.add_gram(gram_str)
        for i in Grams.n_gram:
            sort_dict(Grams.n_gram.setdefault(i))

    def create_gram(self, j, i_sentence, gram_str=''):
        for t in range(j, j + Grams.length_of_gram):
            if re.match(r"[a-zA-Z]", i_sentence[t]):
                gram_str += i_sentence[t]
            else:
                break
        return gram_str

    def add_gram(self, gram):
        if gram not in Grams.n_gram[gram[0]]:
            Grams.n_gram[gram[0]][gram] = 0
        Grams.n_gram[gram[0]][gram] += 1

    def top_n_grams(self):
        num = 0
        for i in Grams.n_gram:
            for j in Grams.n_gram.setdefault(i):
                Grams.gram_top[j] = Grams.n_gram.setdefault(i).setdefault(j)
                num += 1
        sort_dict(Grams.gram_top, False)

    def print_top_grams(self):
        boolean = True
        temp = 1
        memory = 0
        for i in Grams.gram_top:
            if Grams.gram_top.setdefault(i) == memory:
                boolean = True
            else:
                boolean = False
            if temp > Grams.top_grams_num and memory != Grams.gram_top.setdefault(i):
                break
            print(temp, ".", i, " - ", Grams.gram_top.setdefault(i))
            memory = Grams.gram_top.setdefault(i)
            temp += 1

    def input_length_top(self):
        print("Do you want input new length of gram and top number?(Yes/No)")
        if input() == "yes" or "Yes":
            print("length:")
            Grams.length_of_gram = self.is_int()
            print("top:")
            Grams.top_grams_num = self.is_int()

    def is_int(self):
        try:
            temp = int(input())
            return temp
        except ValueError:
            print("NO NUMBER! WHY?")



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


create_sentence_dict(sentence_dict, input())
print(sentence_dict)

words_operations = Word()
words_operations.create_word_dict(sentence_dict)
print(words_operations.word_dict)
words_operations.print_middle_sum()
words_operations.print_median()

grams_operations = Grams()
grams_operations.input_length_top()
grams_operations.get_n_grams(sentence_dict)
print(grams_operations.n_gram)
grams_operations.top_n_grams()
print(grams_operations.gram_top)
grams_operations.print_top_grams()
