#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Created on 2021 @author: Anton Shestakov e-mail: antonshe84@gmail.com
    Created for -.-.-......-..-..-
"""

import os
import re
import time
import sys
from os.path import join, exists


FILE_WORD = "file_word.txt"

MORSE_CODE_DICT_RU = {'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.', 'Д': '-..',
                      'Е': '.', 'Ж': '...-', 'З': '--..', 'И': '..', 'Й': '.---',
                      'К': '-.-', 'Л': '.-..', 'М': '--', 'Н': '-.', 'О': '---',
                      'П': '.--.', 'Р': '.-.', 'С': '...', 'Т': '-', 'У': '..-',
                      'Ф': '..-.', 'Х': '....', 'Ц': '-.-.', 'Ч': '---.', 'Ш': '----',
                      'Щ': '--.-', 'Ъ': '−−·−−', 'Ы': '-.--', 'Ь': '-..-', 'Э': '..-..', 'Ю': '..--',
                      'Я': '.-.-'
                      }  # 'Ъ': '−−·−−', или 'Ъ': '.−−.−.',
vowels_ru = {'А', 'Е', 'И', 'Й', 'О', 'У', 'Ы', 'Э', 'Ю', 'Я'}  # гласные
consonants_ru = {'Б', 'В', 'Г', 'Д', 'Ж', 'З', 'К', 'Л', 'М', 'Н', 'П', 'Р',
                 'С', 'Т', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь'}

MORSE_CODE_DICT_EN = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
                      'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
                      'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
                      'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
                      'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
                      'Z': '--..',
                      }
vowels_en = {'A', 'E', 'I', 'O', 'U', 'Y'}  # гласные
consonants_en = {'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Z'}

NUMBERS = {'1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
           '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----'
           }

SIGNS = {'.': '.-.-.-', ',': '--..--', '?': '..--..', '/': '-..-.', '-': '-....-',
         '(': '-.--.', ')': '-.--.-', '=': '-...-', '@': '.--.-.',
         '"': '.-..-.',  # двойная кавычка
         "'": '.----.',  # одинарная кавычка
         }

MORSE_CODE_DICT = {}

vowels = vowels_ru | vowels_en
consonants = consonants_ru | consonants_en


def init():
    path_output = join(os.getcwd(), 'output')
    if not exists(path_output):
        os.mkdir(path_output)
    os.chdir(path_output)
    print(f"Current directory: {os.getcwd()}")
    sys.setrecursionlimit(2000)


def encryption(message):
    """
    Encrypting a word in morse code

    :param message: the word that is encrypted
    :return: Morse code (space delimiter). If the symbol is not in the dictionary, then the question mark
    """
    my_cipher = ''
    for my_letter in message:
        if my_letter != ' ':
            if my_letter in MORSE_CODE_DICT.keys():
                my_cipher += MORSE_CODE_DICT[my_letter] + ' '
            else:
                my_cipher += '? '
        else:
            my_cipher += ' '
    return my_cipher


def decryption(message_morze):
    """
    Decryption a morse code in word

    :param message_morze: morse code to decipher
    :return: decoded word
    """
    i = 0
    decipher = ''
    my_citext = ''
    for my_letter in (message_morze + ' '):
        if my_letter != ' ':
            i = 0
            my_citext += my_letter
        else:
            i += 1
            if i == 2:
                decipher += ' '
            else:
                if my_citext == "?":
                    decipher += "?"
                else:
                    decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(my_citext)]
                my_citext = ''
    return decipher


def find_letter_vars(message_morze):
    l_vars = []
    for key, val in MORSE_CODE_DICT.items():
        l_morze = message_morze[:len(val)]
        if val == l_morze:
            l_vars.append(key)
    return l_vars


def find_letters_recurs(message_morze, v='', result=None):
    """
    Search in morse string without spaces for word variants
    Recursive function

    :param message_morze: message morze
    :param v: first letters
    :param result: list of results
    :return: Returns the first letter from the message
    """

    if result is None:
        result = []
    l_list = find_letter_vars(message_morze)
    if not l_list:  # create a new result if no intermediate was given
        result.append(v.lower())
    else:
        for l1 in l_list:
            find_letters_recurs(message_morze[len(MORSE_CODE_DICT[l1]):], v + l1, result)
    return result


def search_vars(morze_mess, rev='f'):
    """
    Searching for word variants using recursion and random sampling

    :param rev: revers or forward
    :param morze_mess: Morse code message without spaces
    :return: Returns the set of the found options
    """

    variants = []
    if (rev == 'a') or (rev == 'f'):
        start = time.perf_counter()
        print(f'-- Search for code variants "{morze_mess}" (forward order) --')
        variants = find_letters_recurs(morze_mess, '')
        print(f"-- Elapsed time: {time.perf_counter() - start: 0.2f} c --")

    if (rev == 'a') or (rev == 'r'):
        start = time.perf_counter()
        print(f'-- Search for code variants "{morze_mess[::-1]}" (revers order) --')
        variants.extend(find_letters_recurs(morze_mess[::-1], ''))
        print(f"-- Elapsed time: {time.perf_counter() - start: 0.2f} c --")

    var_set = set(variants)
    var_set.discard('')
    del(variants)
    write_to_file(FILE_WORD, var_set, sort=True)
    print(f'Variants of words are recorded in file "{FILE_WORD}"')
    print(f"Found: {len(var_set)} variants")
    print()

    return var_set


def filter_word(l_set, three_let=True, two_let=False, three_vowels=False, three_consonants=False):
    start = time.perf_counter()
    print(f"-- Start filtering of variants --")
    l_set_result = set(l_set)
    for query in set(l_set):
        for n, q in enumerate(query[:-2]):
            # выявление трех одинаковых букв подряд
            if three_let and ((q == query[n + 1]) and (q == query[n + 2])):
                l_set_result.discard(query)
                break
            # выявление трех гласных подряд
            if three_vowels and ((q in vowels) and (query[n + 1] in vowels) and (query[n + 2] in vowels)):
                l_set_result.discard(query)
                break
            # выявление трех согласных подряд
            if three_consonants and \
                    ((q in consonants) and (query[n + 1] in consonants) and (query[n + 2] in consonants)):
                l_set_result.discard(query)
                break
            # выявление двух одинаковых букв подряд
            if two_let and ((q == query[n + 1]) or (query[n + 1] == query[n + 2])):
                l_set_result.discard(query)
                break
    print(f"Filtered out {len(l_set_result)} variants from {len(l_set)}")
    print(f"-- Elapsed time: {time.perf_counter() - start: 0.2f} c --")
    print()
    return l_set_result


def write_to_file(file_name, list_set, sort=False, mode="w"):
    """
    Writing a set or list to file

    :param mode: file mode
    :param file_name: File name
    :param list_set: Set or list
    :param sort: Do I need sorting before writing
    :return: 0
    """
    if list_set:
        if sort:
            ls_sort = sorted(list(list_set), key=len)
        else:
            ls_sort = list(list_set)
        with open(file_name, mode, encoding="utf-8") as f:
            for s in ls_sort:
                f.write(str(s) + "\n")
    elif os.path.exists(file_name) and (mode == "w"):
        os.remove(file_name)
    return 0


def has_cyrillic(text):
    return bool(re.search('[а-яА-ЯёЁ]', text))


def has_english(text):
    return bool(re.search('[a-zA-Z]', text))


def sample(message):
    """
    Пример шифрования сообщения и расшифровки

    :param message: текст для шифровки
    :return: Выводит текст в коде морзе, а затем производит обратную расшифровку
    """
    print()
    print(f"-- For sample, let's encrypt phrase: {message}")
    output_morze = encryption(message.upper())
    print(f"Morse code: {output_morze}")
    print(f"If you remove spaces: {output_morze.replace(' ', '')}")

    my_morze = output_morze
    print(f"Let's decipher code: {my_morze}")
    output = decryption(my_morze).lower()
    print(f"Decryption phrase: {output}")
    print(f"-- End sample --")
    print()
    return output_morze.replace(' ', '')


def read_dictionary(len_word_from=2, lang="all"):
    """
    Reading words from a dictionary

    :param len_word_from: word length from
    :param lang: language of words
    :return: dictionary as set
    """
    print(f"-- Reading words from dictionaries --")
    start = time.perf_counter()
    list_w = set()
    list_exclude = set()
    list_lang = lang.split("+")
    if "all" in list_lang:
        list_lang = ["ru", "en", "digit", "mark"]
    for i in range(1, 10):
        file_name = f"../DICT{i}.txt"
        if exists(file_name):
            with open(file_name, "r", encoding="utf-8") as f:
                for s in f:
                    s = s.replace("\n", "")
                    for ss in s.split():
                        ss = re.sub(r'[^\w\s]', '', ss)
                        ss = re.sub(r'\d+', '', ss)
                        if len(ss) < len_word_from:
                            continue
                        elif ("ru" in list_lang) and has_cyrillic(ss):
                            list_w.add(ss.lower())
                        elif ("en" in list_lang) and has_english(ss):
                            list_w.add(ss.lower())

    file_name = f"../exclude.txt"
    if exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            for s in f:
                s = s.replace("\n", "")
                for ss in s.split():
                    list_exclude.add(ss.lower())
    len_list = len(list_w)
    list_w = list_w.difference(list_exclude)
    print(f"Exclude {len_list - len(list_w)} words")
    print(f"Words in dictionary: {len(list_w)}")
    print(f"-- Elapsed time: {time.perf_counter() - start: 0.2f} c --")
    print()
    return list_w


def words_from_word(s):
    """
    Breaks a word into words

    :param s: word
    :return: list of words
    """
    l_w = []
    for c0 in range(0, len(s)):
        s = s[c0:len(s) - c0]
        for c in range(0, len(s)):
            l_w.append(s[0:c])
            l_w.append(s[c:len(s)])
    return l_w


def search_in_dictionary(list_var, list_w):
    """
    Search for matches in a dictionary

    :param list_var: set of variants
    :param list_w: set of dictionary
    :return: returns found variants written in files of the form: result_1_word.txt, result_2_word.txt etc.
            and best matches in file "best_match.txt"
    """
    start = time.perf_counter()
    print(f"-- Start searching in dictionary --")
    res = [None, set(), set(), set(), set(), set()]
    res[1] = set()  # one word results
    res[2] = set()  # two word results
    res[3] = set()  # three word results
    res[4] = set()  # four word results
    res[5] = set()  # five word results
    sub = ['', '', '', '', '', '']  # found substrings
    r = ['', '', '', '', '', '']  # remainder
    best_match = [set(), set(), set()]
    for s in list_var:
        l_w_1 = words_from_word(s)

        for sub[1] in l_w_1:
            if sub[1] in list_w:
                r[0] = s[:s.find(sub[1])]
                r[0] += ',' if r[0] else ''
                r[1] = s[s.find(sub[1]) + len(sub[1]):]
                r[1] = ',' + r[1] if r[1] else ''
                found = f"{s}: {r[0]}{sub[1].upper()}{r[1]}"
                res[1].add(found)
                len_sub = len(sub[1])
                best_match[0].add(found + ' - 0') if (len(s) - len_sub) == 0 else ''
                best_match[1].add(found + ' - 1') if (len(s) - len_sub) == 1 else ''
                best_match[2].add(found + ' - 2') if (len(s) - len_sub) == 2 else ''

                s2 = s[s.find(sub[1]) + len(sub[1]):]
                l_w_2 = words_from_word(s2)
                for sub[2] in l_w_2:
                    if sub[2] in list_w:
                        r[1] = s2[:s2.find(sub[2])]
                        r[1] += ',' if r[1] else ''
                        r[2] = s2[s2.find(sub[2]) + len(sub[2]):]
                        r[2] = ',' + r[2] if r[2] else ''
                        found = f"{s}: {r[0]}{sub[1].upper()},{r[1]}{sub[2].upper()}{r[2]}"
                        res[2].add(found)
                        len_sub = len(sub[1]) + len(sub[2])
                        best_match[0].add(found + ' - 0') if (len(s) - len_sub) == 0 else ''
                        best_match[1].add(found + ' - 1') if (len(s) - len_sub) == 1 else ''
                        best_match[2].add(found + ' - 2') if (len(s) - len_sub) == 2 else ''

                        s3 = s2[s2.find(sub[2]) + len(sub[2]):]
                        l_w_3 = words_from_word(s3)
                        for sub[3] in l_w_3:
                            if sub[3] in list_w:
                                r[2] = s3[:s3.find(sub[3])]
                                r[2] += ',' if r[2] else ''
                                r[3] = s3[s3.find(sub[3]) + len(sub[3]):]
                                r[3] = ',' + r[3] if r[3] else ''
                                found = f"{s}: {r[0]}{sub[1].upper()},{r[1]}{sub[2].upper()}," \
                                        f"{r[2]}{sub[3].upper()}{r[3]}"
                                res[3].add(found)
                                len_sub = len(sub[1]) + len(sub[2]) + len(sub[3])
                                best_match[0].add(found + ' - 0') if (len(s) - len_sub) == 0 else ''
                                best_match[1].add(found + ' - 1') if (len(s) - len_sub) == 1 else ''
                                best_match[2].add(found + ' - 2') if (len(s) - len_sub) == 2 else ''

                                s4 = s3[s3.find(sub[3]) + len(sub[3]):]
                                l_w_4 = words_from_word(s4)
                                for sub[4] in l_w_4:
                                    if sub[4] in list_w:
                                        r[3] = s4[:s4.find(sub[4])]
                                        r[3] += ',' if r[3] else ''
                                        r[4] = s4[s4.find(sub[4]) + len(sub[4]):]
                                        r[4] = ',' + r[4] if r[4] else ''
                                        found = f"{s}: {r[0]}{sub[1].upper()},{r[1]}{sub[2].upper()}," \
                                                f"{r[2]}{sub[3].upper()},{r[3]}{sub[4].upper()}{r[4]}"
                                        res[4].add(found)
                                        len_sub = len(sub[1]) + len(sub[2]) + len(sub[3]) + len(sub[4])
                                        best_match[0].add(found + ' - 0') if (len(s) - len_sub) == 0 else ''
                                        best_match[1].add(found + ' - 1') if (len(s) - len_sub) == 1 else ''
                                        best_match[2].add(found + ' - 2') if (len(s) - len_sub) == 2 else ''

                                        s5 = s4[s4.find(sub[4]) + len(sub[4]):]
                                        l_w_5 = words_from_word(s5)
                                        for sub[5] in l_w_5:
                                            if sub[5] in list_w:
                                                r[4] = s5[:s5.find(sub[5])]
                                                r[4] += ',' if r[4] else ''
                                                r[5] = s5[s5.find(sub[5]) + len(sub[5]):]
                                                r[5] = ',' + r[5] if r[5] else ''
                                                found = f"{s}: {r[0]}{sub[1].upper()},{r[1]}{sub[2].upper()}," \
                                                        f"{r[2]}{sub[3].upper()},{r[3]}{sub[4].upper()}," \
                                                        f"{r[4]}{sub[5].upper()}{r[5]}"
                                                res[5].add(found)
                                                len_sub = len(sub[1]) + len(sub[2]) + len(sub[3]) + len(sub[4]) + len(
                                                    sub[5])
                                                best_match[0].add(found + ' - 0') if (len(s) - len_sub) == 0 else ''
                                                best_match[1].add(found + ' - 1') if (len(s) - len_sub) == 1 else ''
                                                best_match[2].add(found + ' - 2') if (len(s) - len_sub) == 2 else ''

    for i in range(1, 6):
        write_to_file(f"result_{i}_word.txt", res[i], sort=True)
        print(f'Found variants with {i} word (write to file "result_{i}_word.txt"): {len(res[i])}') if res[i] else ''

    write_to_file("best_match.txt", best_match[0], sort=True)
    write_to_file("best_match.txt", best_match[1], sort=True, mode="a")
    write_to_file("best_match.txt", best_match[2], sort=True, mode="a")
    print(f'Found variants with best match (write to file "best_match.txt"): '
          f'{len(best_match[0]) + len(best_match[1]) + len(best_match[2])}') if best_match else ''

    print(f"-- Elapsed time: {time.perf_counter() - start: 0.2f} c --")
    print()
    return 0


def create_code_table(lang="ru"):
    """
    Formation of the symbol table

    :param lang: table language and additional characters
    :return: global table MORSE_CODE_DICT
    """
    global MORSE_CODE_DICT
    lang_list = lang.split("+")
    if "all" in lang_list:
        lang_list = ["ru", "en", "digit", "mark"]
    if "ru" in lang_list:
        z = MORSE_CODE_DICT.copy()
        z.update(MORSE_CODE_DICT_RU)
        MORSE_CODE_DICT = z
    if "en" in lang_list:
        z = MORSE_CODE_DICT.copy()
        z.update(MORSE_CODE_DICT_EN)
        MORSE_CODE_DICT = z
    if "digit" in lang_list:
        MORSE_CODE_DICT.update(NUMBERS)
    if "mark" in lang_list:
        MORSE_CODE_DICT.update(SIGNS)
    else:
        z = MORSE_CODE_DICT.copy()
        z.update(MORSE_CODE_DICT_RU)
        MORSE_CODE_DICT = z

    return 0


if __name__ == '__main__':
    init()
    print(f"---- Program for decrypting a phrase written to Morse code without a character separator. \n"
          f"---- The program allows you to search for up to 5 words in a phrase\n"
          f"---- For example, enter a phrase in Russian or English. \n"
          f"---- It is possible to use punctuation marks or numbers, but the accuracy of decoding will decrease.\n"
          f"---- Words are read from dictionaries (UTF-8) with file names: DICT1.txt, DICT2.txt, ... up to 9\n"
          f'---- To exclude definite words from dictionary, add them to "exclude.txt" file\n'
          f'---- Result is saved in the "output" folder\n')

    my_message_morze = "--.---.-"  # "МАМА"

    language = input(
        "Enter language of phrase (use + for the combination) (ru/en/mark/digit/all): [ru] ").lower() or "ru"
    create_code_table(language)

    len_from = input("Enter the length of words in the dictionary, from: [4] ")
    if len_from.isdigit():
        len_from = int(len_from)
    else:
        len_from = 4

    my_message = input("Enter phrase for sample or skip: ")
    my_message_morze = sample(my_message) if my_message else my_message_morze

    my_input_morze = input(f"Enter morze code or use code from sample: [{my_message_morze}] ")
    my_message_morze = my_input_morze if my_input_morze else my_message_morze
    revers = input("Morse code in forward (f), reverse (r) or all (a) orders? (f/r/a): [f] ").lower() or 'f'

    print(f"Morze code: {my_message_morze}\n")

    # Search of variants
    list_var_set = search_vars(my_message_morze, rev=revers)

    # Filtering
    list_var_set = filter_word(list_var_set, three_let=True, two_let=False, three_vowels=False, three_consonants=False)

    # Reading the dictionary
    list_words = read_dictionary(len_word_from=len_from, lang=language)
    write_to_file("dict.txt", list_words, sort=True)

    # Search of dictionary
    search_in_dictionary(list_var_set, list_words)

    input("Press any key to exit...")
