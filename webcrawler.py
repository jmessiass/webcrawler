from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
import re


print(42 * '-')
print('          W E B C R A W L E R')
print(42 * '-')
print('\033[32m' + ' by Jonathan Messias | jmcybers@gmail.com' + '\033[0m')
print(42 * '-')
print(42 * ' ')
print('1. Set an URL (http://target.com)')
# print('2. Set any URLs (/tmp/target.txt)')
print(42 * ' ')
print(42 * '-')


def input_validation():
    """ validate input data """
    while True:
        try:
            option = int(input('$ Choose an option [1]: '))
            print(42 * '-')
            if option < 2:
                return option
            else:
                print('\033[31m' + '$ %d is an invalid option !!!' % option + '\033[0m')
                print(42 * '-')
        except ValueError as e:
            print(42 * '-')
            print('\033[31m' + '$ %s is not a valid option !!!'
                  % e.args[0].split(': ')[1] + '\033[0m')
            print(42 * '-')


def set_target(option):
    """ choose an option and validade that """
    if option == 1:
        while True:
            try:
                # define global variable
                global url
                url = input('[{0}] URL: '.format(option))
                print(42 * '-')
                page = urlopen(url)
                return option, page
            except(URLError, ValueError):
                print('\033[33m' + '$ Error in your URL, try again !!!' + '\033[0m')
                print(42 * '-')


def extract_text(option, page):
    """ get all html text from target """
    if option == 1:
        html = page.read()
        bs_html = BeautifulSoup(html, 'lxml')
        return get_words(bs_html)


def get_words(text):
    """ extract words from html tags """
    words = text.find_all({'h1', 'h2', 'h3',
                           'h4', 'h5', 'h6',
                           'h7', 'a', 'p',
                           'span'})
    # remove tags
    list_words = remove_tags(words)
    # split words
    blank_words = split_words(list_words)
    # remove special characters
    regex_words = remove_special_characters(blank_words)
    # remove duplicates values
    clean_words = list(set(regex_words))
    # remove empty values
    clean_words = list(filter(None, clean_words))
    return clean_words


def remove_tags(words):
    """ remove tags and blank spaces """
    list_words = []
    for word in words:
        list_words.append(word.get_text().strip())
    return list_words


def split_words(words):
    """ split words with blank space """
    list_words = []
    for word in words:
        for word in word.split(' '):
            list_words.append(word)
    return list_words


def remove_special_characters(words):
    """ remove special characters """
    list_words = []
    for word in words:
        list_words.append(re.sub(r'([.,#!@$)\]\[(}{;:?>\'\"/\\<~^-_=+&])', r'', word))
    return list_words


def create_file(words):
    """ create the word list """
    url_split = url.split('//')
    url_domain = url_split[1].split('.')
    file_title = 'wordlist_{0}.txt'.format(url_domain[0])
    file = open(file_title, 'w+')
    for word in words:
        file.write('%s\n' % word)
    file.close()


def upper_words(words):
    """ generate words upper from word list """
    list_words = []
    for word in words:
        list_words.append(word.upper())
    return list_words


def lower_words(words):
    """ generate words lower from word list """
    list_words = []
    for word in words:
        list_words.append(word.lower())
    return list_words


if __name__ == "__main__":
    """ main method """
    # input validation
    option = input_validation()
    # set the target
    option, page = set_target(option)
    # extract all text from target
    list_words = extract_text(option, page)
    # convert words in upper case
    words_upper = upper_words(list_words)
    list_words.extend(words_upper)
    # convert words in lower case
    words_lower = lower_words(list_words)
    list_words.extend(words_lower)
    # generate file
    create_file(list_words)
