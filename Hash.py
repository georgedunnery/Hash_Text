# George Dunnery - CS 5800
import urllib
from Node import *
from urllib import request


# Class implementation of a hash table for text as (word : count)
# Collision Strategy: Chaining with singly linked list
# Insertion Strategy: Two Cases -
#  new word: prepend to linked list
#  duplicate word: increment count, splice out node, prepend to linked list
# Not case sensitive, see process(str)
class TextHash:

    # Construct the hash object
    #  seed: prime number to use for letter-wise key generation
    #  m: size of table, also prime number (modulo m in hash_word(str))
    # Recommendation: seed = 17, m = 701
    def __init__(self, seed: int, m: int):
        self.seed = seed
        # Variable m chosen for consistency with textbook CLRS 3rd ed.
        self.m = m
        self.table = [None] * self.m

    def __str__(self) -> str:
        return "m = " + str(self.m) + ", seed = " + str(self.seed)

    # Function to generate a hash key (index) for a string
    #  word: string, the word to generate a hash key for
    # Returns int, the hashed key
    def hash_word(self, word: str) -> int:
        key = self.seed
        # Based on "djb2" hashing algorithm for letters
        for i in range(len(word)):
            key = (key * 33) + key + ord(word[i])
        return key % self.m

    # Function to add a single word to the hash table
    # Entire string inserted as word - use process to parse a string!
    # Refer to insertion & collision strategy in class comment
    #  word: string, the word to be added to the hash table
    # Returns nothing
    def insert(self, word: str) -> None:
        # Generate the key index for the given word
        key = self.hash_word(word)
        # If the index is unused, simply insert the new node there
        if self.table[key] is None:
            self.table[key] = Node(word, None)
        # Otherwise, it must be inserted
        else:
            # If the word is new (not in_list), then prepend with count 1
            if not self.table[key].in_list(word):
                new_node = Node(word, None)
                self.table[key].prepend(new_node)
                self.table[key] = new_node
            else:
                # If it is: extract (inc count & splcie out), then prepend
                duplicate = self.table[key].extract(word)
                # Only prepend if the node is not already the head!
                if self.table[key] != duplicate:
                    self.table[key].prepend(duplicate)
                    # Set new list head
                    self.table[key] = duplicate

    # Function to process the words in a string into the hash table (split " ")
    # Punctuation is ignored (except apostrophe and hyphen) & not case sensitive
    # Can be called repeatedly on the same hash table
    #   sentence: string, the sentence of words to add to the hash table
    # Returns nothing
    def process(self, sentence: str) -> None:
        ignored_characters = ['.', '!', '?',
                              '"', ',', ':', ';',
                              '/', '\\',
                              '(', ')',
                              '[', ']',
                              '{', '}']
        delineate = [' ', '\n', '\r']
        # Concatenated string to track letters in the current word, start empty
        cat = ""
        # Process letter by letter, cleaning out ignored_characters
        for i in range(len(sentence)):
            if sentence[i] not in ignored_characters:
                letter = str(sentence[i]).lower()
                # Split on delineate: insert the letters as a word and reset cat string
                if letter in delineate:
                    # Do not insert empty string
                    if cat != "":
                        self.insert(cat)
                        cat = ""
                # Concatenate letters to build the string
                else:
                    cat += letter
            # Special case: The last word may not have a trailing delineation
            if i == len(sentence) - 1 and cat != "":
                self.insert(cat)

    # Function to list all the keys in the hash table as ('word', count)
    # Returns the list as a string, with tuples separated by new lines
    def list_all_keys(self) -> str:
        all_keys = ""
        for i in range(len(self.table)):
            # Skip an unused space in sparse table
            if self.table[i] is not None:
                all_keys += self.table[i].list_all_nodes()
        return all_keys

    # Function to query the count of a particular word
    #  word: string, the word to lookup in the hash table
    # Returns count of the word or -1 when not found
    def find(self, word: str) -> int:
        key = self.hash_word(word)
        # If the index is not empty, and if it exists in the list
        if self.table[key] is not None:
            return self.table[key].find(word)
        else:
            return -1

    # Function to save the hash table to a .txt file
    #  filename: string, the name of the output file like 'output.txt'
    # Returns nothing
    def save(self, filename: str) -> None:
        file = open(filename, 'w')
        file.write(self.list_all_keys())
        file.close()

    # Function for inserting words from an internet .txt file into the hash table
    #  web: string, the url of the file
    # Returns nothing
    def process_web_text(self, web: str) -> None:
        # Using urllib.request, open the .txt file
        web_file = urllib.request.urlopen(web)
        # Then read the file into a string
        web_text = web_file.read().decode('utf-8', 'ignore')
        # Close the connection and process the text that was gathered
        web_file.close()
        self.process(web_text)

    # Function to query the lengths of all the linked lists in the table
    # Returns list of integers, the linked list lengths by table index
    def chain_lengths(self) -> list:
        lengths = []
        for i in range(len(self.table)):
            if self.table[i] is not None:
                lengths.append(self.table[i].list_length())
        return lengths

    # Function to calculate the average number of collisions
    # Returns float, the average collision rate
    def average_collisions(self) -> float:
        total = 0
        for i in range(len(self.table)):
            if self.table[i] is not None:
                total += self.table[i].list_length()
        return total / self.m

    # Function to delete a key (node) from the hash table
    #  word: string, the word of the node to delete
    # Returns nothing
    def delete_key(self, word: str) -> None:
        key = self.hash_word(word)
        node = self.table[key]
        if node is not None and node.in_list(word):
            # If it is the head element, change table pointer to its next
            if node.word == word:
                self.table[key] = node.next
            # Otherwise, delete it from elsewhere in the list
            else:
                node.delete_node(word)