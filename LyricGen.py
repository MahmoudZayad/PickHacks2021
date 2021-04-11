import os
import random as r


class Grams:
    grams = {}
    keys = []

    def __init__(self, text):
        self.mapping(text)
        self.map_to_vector(self.grams, self.keys)

    def mapping(self, text):
        ctr = 1
        first = True
        word = None  # queue
        window = []
        first_window = []
        with open(text, 'r') as f:
            for line in f:
                for word in line.split():  # Grabs words delimited by whitespace
                    if ctr == 3:
                        if first:
                            first = False
                        temp_gram = word
                        self.gramming(window, temp_gram, word, ctr)
                    else:  # used for the creation of the first window
                        window.append(word)
                        if (first):
                            first_window.append(word)
                    ctr += 1

        for w in first_window:  # gram edge cases
            if ctr == 3:
                temp_gram = w
                self.gramming(window, temp_gram, w, ctr)
            else:
                window.append(word)
            ctr += 1
    
        f.close()


    def gramming(self, window, temp_gram, value, ctr):
        values = []
        values.append(value)
    
        if window in self.grams.keys():  # if window does exist in the map
            val = self.grams.get(window)
            self.grams.update({window: val.append(value)})
            window.pop(0)  # dequeue
            window.append(temp_gram)
            ctr -= 1
        else:
            self.grams[window] = values
            window.pop(0)  # dequeue
            window.append(temp_gram)
            ctr -= 1
        return ctr, temp_gram, value, window
    
    
    def map_to_vector(self, grams, keys):
        for key in grams:
            keys.append(key)
    
    
    def random_text_gen(self, grams, keys, words):
        print("...", end="")
    
        last_words = 280 % 3
        key = None
        for words in range(1, int(words / 3)):
            ranVal = grams[key].size() - 1
            key = keys[r.randint(0, keys.size() - 1)]
            print(grams.get(key) + " " + grams[key][r.randint(0, ranVal)])
    
        last_words_string = None
        key = keys[r.randint(0, keys.size() - 1)]
        ranVal = grams.get(key)
        last_words_string = grams.get(key)
        last_words_string = last_words_string + " " + grams[key][r.randint(0, ranVal)]
        print(last_words_string)


b = Grams("PickHacks2021/doja cat.txt")