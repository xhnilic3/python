#!/usr/bin/python3
# vim: tabstop=4 shiftwidth=4 expandtab
from random import randint, seed, choice


def lorem_ipsum(textfile, how_many_words):
    def update_collocations(line, collocations):
        words = line.split(' ')
        if not words:
            return

        previous = words[0]
        for i in range(1, len(words)):
            key = (previous, words[i])
            collocations[key] = collocations.get(key, 0) + 1
            previous = key[1]

    all_collocations = {}

    file = open(textfile, "r")
    for line in file.readlines():
        update_collocations(line, all_collocations)

    
    def get_random_collocation(collocations):
        return choice(list((collocations.keys())))

    def get_next_collocation(collocations, stopping_point):
        stop_at = randint(1, stopping_point)
        i = collocations[0][1]

        for collocation in collocations:
            i += collocation[1]
            if i > stop_at:
                return collocation[0]

        return collocations[0][0]

    current_collocation = get_random_collocation(all_collocations)
    lastword = current_collocation[1]
    text = current_collocation[0]

    for _ in range(how_many_words):
        text += " " + lastword
        
        relevant_collocations = []
        relevant_sum = 0
        for col in all_collocations.items():
            if col[0][0] == lastword:
                relevant_collocations.append(col)
                relevant_sum += col[1]
        relevant_collocations.sort(reverse=True)

        if relevant_sum < 1:
            current_collocation = get_random_collocation(all_collocations)
        else:
            current_collocation = get_next_collocation(relevant_collocations, relevant_sum)

        lastword = current_collocation[1]

    print(text)


def main():
    seed(42)
    lorem_ipsum("long_text.txt", 500)


if __name__ == "__main__":
    main()
