import re


def sort_dict(dictionary, rev=True):
    if rev is True:
        temp = dict(sorted(dictionary.items(), key=lambda x: x[1]))
    else:
        temp = dict(sorted(dictionary.items(), key=lambda x: -x[1]))
    dictionary.clear()
    for i in temp:
        dictionary[i] = temp.setdefault(i)


class Sentence:
    def __init__(self):
        self.sentence_dict = dict()

    def create_sentence_dict(self, input_string):
        sentence_num = 0
        self.sentence_dict[0] = ''
        bracket_temp = False
        for i in input_string:
            if re.match(r"[a-zA-Z]|\s", i) is not None:
                self.sentence_dict[sentence_num] += i
            elif i == '.' or i == '!' or i == '?' or i == ';':
                if self.sentence_dict[sentence_num] and not self.sentence_dict[sentence_num].isspace():
                    sentence_num += 1
                    self.sentence_dict[sentence_num] = ''
                    bracket_temp = False
            elif i == '(':
                bracket_temp = True
            elif i == ')':
                if not bracket_temp and self.sentence_dict[sentence_num] and \
                        self.sentence_dict[sentence_num].strip():
                    sentence_num += 1
                    self.sentence_dict[sentence_num] = ''
                else:
                    bracket_temp = False
        if self.sentence_dict[sentence_num].isspace() or not self.sentence_dict[sentence_num]:
            self.sentence_dict.pop(sentence_num)


class Word:

    def __init__(self):
        self.word_dict = dict()

    def create_word_dict(self, sentence):
        for i in sentence:
            self.word_dict[i] = 0
            self.word_dict[i] = len([word for word in sentence[i].split() if word.isalpha()])
        sort_dict(self.word_dict)

    def get_middle_sum(self):
        middle_sum = 0
        for i in self.word_dict:
            middle_sum += self.word_dict.setdefault(i)
        middle_sum /= len(self.word_dict)
        return middle_sum

    def print_middle_sum(self):
        print("middle num of words: ", self.get_middle_sum())

    def get_median(self):
        length = int((len(self.word_dict) - 1) / 2)
        if len(self.word_dict) % 2 == 0:
            return (self.word_dict[length] + self.word_dict[length + 1]) / 2
        else:
            return self.word_dict[length]

    def print_median(self):
        print("median:", self.get_median())


def is_int(num):
    try:
        temp = int(input())
        if temp > 0:
            return temp
        else:
            return num
    except ValueError:
        print("NO NUMBER! WHY?")
        return num
    except EOFError:
        print("No text found")
        return num


class Grams:
    def __init__(self):
        self.n_gram = dict()
        self.length_of_gram = 4
        self.top_grams_num = 10
        self.gram_top = dict()

    def get_n_grams(self, sen_dict):
        for i in sen_dict:
            i_sentence = sen_dict.setdefault(i)
            for j in range(len(i_sentence) - self.length_of_gram + 1):
                gram_str = self.create_gram(j, i_sentence)

                if len(gram_str) == self.length_of_gram:
                    self.n_gram.setdefault(gram_str[0])
                    if self.n_gram[gram_str[0]] is None:
                        self.n_gram[gram_str[0]] = dict()
                        self.add_gram(gram_str)
                    else:
                        self.add_gram(gram_str)
        for i in self.n_gram:
            sort_dict(self.n_gram.setdefault(i))

    def create_gram(self, j, i_sentence, gram_str=''):
        for t in range(j, j + self.length_of_gram):
            if re.match(r"[a-zA-Z]", i_sentence[t]):
                gram_str += i_sentence[t]
            else:
                break
        return gram_str

    def add_gram(self, gram):
        if gram not in self.n_gram[gram[0]]:
            self.n_gram[gram[0]][gram] = 0
        self.n_gram[gram[0]][gram] += 1

    def top_n_grams(self):
        num = 0
        for i in self.n_gram:
            for j in self.n_gram.setdefault(i):
                self.gram_top[j] = self.n_gram.setdefault(i).setdefault(j)
                num += 1
        sort_dict(self.gram_top, False)

    def print_top_grams(self):
        temp = 1
        memory = 0
        for i in self.gram_top:
            if temp > self.top_grams_num and memory != self.gram_top.setdefault(i):
                break
            print(temp, ".", i, " - ", self.gram_top.setdefault(i))
            memory = self.gram_top.setdefault(i)
            temp += 1

    def input_length_top(self):
        print("Do you want input new length of gram and top number?(Yes/No)")
        try:
            answer = input()
        except EOFError:
            print("No text found")
            answer = "no"
        if answer == "yes" or answer == "Yes":
            print("length:")
            self.length_of_gram = is_int(4)
            print("top:")
            Grams.top_grams_num = is_int(10)


def main():
    sentence_operations = Sentence()
    try:
        sentence_operations.create_sentence_dict(input())
    except EOFError:
        print("No text found")
    print(sentence_operations.sentence_dict)
    if sentence_operations.sentence_dict:
        words_operations = Word()
        words_operations.create_word_dict(sentence_operations.sentence_dict)
        print(words_operations.word_dict)
        words_operations.print_middle_sum()
        words_operations.print_median()

        grams_operations = Grams()
        grams_operations.input_length_top()
        grams_operations.get_n_grams(sentence_operations.sentence_dict)
        print(grams_operations.n_gram)
        grams_operations.top_n_grams()
        print(grams_operations.gram_top)
        grams_operations.print_top_grams()
    else:
        print("empty input")


if __name__ == "__main__":
    main()
