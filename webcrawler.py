from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup


print(42 * '-')
print('          W E B C R A W L E R')
print(42 * '-')
print('\033[32m' + ' by Jonathan Messias | jmcybers@gmail.com' + '\033[0m')
print(42 * '-')
print('1. Write an URL   >>>>> http://target.com')
print('2. Set any URLs   >>>>>>> /tmp/target.txt')
print(42 * '-')


def input_validation():
    """ validate input data """
    while True:
        try:
            option = int(input('$ Choose an option [1-2]: '))
            print(42 * '-')
            if option < 3:
                return option
            else:
                print('\033[31m' + '$ %d is an invalid option !!!' % option + '\033[0m')
                print(42 * '-')
        except ValueError as e:
            print(42 * '-')
            print('\033[31m' + '$ %s is not a valid option !!!'
                  % e.args[0].split(': ')[1] + '\033[0m')
            print(42 * '-')


def choose_option(option):
    """ choose an option and validade that """
    if option == 1:
        text = 'URL: '
        value = input('[{0}] {1}'.format(option, text))
        print(42 * '-')
        try:
            page = urlopen(value)
            return option, page
        except(URLError, ValueError):
            print('\033[33m' + '$ Error in your URL, try again !!!' + '\033[0m')
            print(42 * '-')
            choose_option(option)
    elif option == 2:
        print('\033[33m' + '[2] Sorry, this tool is not availabe =^(' + '\033[0m')
        print(42 * '-')
        # text = 'FILE: '

    return input_validation()


def get_text(option, page):
    """ get all html text from target """
    if option == 1:
        try:
            html = page.read()
        except URLError:
            print('Error in your URL, try again !!!')
            get_text()

    bs_html = BeautifulSoup(html, 'lxml')
    return get_words(bs_html)


def get_words(text):
    """ extract words from html tags """
    words = text.find_all({'h1', 'h2', 'h3',
                           'h4', 'h5', 'h6',
                           'h7', 'a', 'p',
                           'span'})

    list_words = []
    clean_words = []

    for value in words:
        # remove tags and blank spaces
        list_words.append(value.get_text().strip())

    # remove empty values
    list_words = list(filter(None, list_words))

    for value in list_words:
        # split words with blank space
        for word in value.split(' '):
            clean_words.append(word)

    # remove ',' from list
    clean_words = [value.replace(',', '') for value in clean_words]
    # remove '.' from list
    clean_words = [value.replace('.', '') for value in clean_words]

    return clean_words


if __name__ == "__main__":
    option = input_validation()
    option, page = choose_option(option)
    print(get_text(option, page))
