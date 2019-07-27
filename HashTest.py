# George Dunnery - CS 5800

from Node import *
from Hash import *
import unittest


# Test class that focuses on Node class functionality
class NodeTest(unittest.TestCase):
    # Verify that the word and count are stored correctly
    def test_create(self):
        okay = Node("okay", None)
        self.assertEqual("okay", okay.word)
        self.assertEqual(1, okay.count)
        hello = Node("hello", None)
        self.assertEqual("hello", hello.word)
        self.assertEqual(1, hello.count)
        goodbye = Node("goodbye", None)
        self.assertEqual("goodbye", goodbye.word)
        self.assertEqual(1, goodbye.count)

    # Verify the lengths are computed properly
    def test_list_length(self):
        okay = Node("okay", None)
        hello = Node("hello", None)
        goodbye = Node("goodbye", None)
        okay.next = hello
        hello.next = goodbye
        self.assertEqual(1, goodbye.list_length())
        self.assertEqual(2, hello.list_length())
        self.assertEqual(3, okay.list_length())

    # Verify words can be detected in the linked list
    def test_in_list(self):
        okay = Node("okay", None)
        hello = Node("hello", None)
        goodbye = Node("goodbye", None)
        okay.next = hello
        hello.next = goodbye
        # These words are in the list
        self.assertTrue(okay.in_list("okay"))
        self.assertTrue(okay.in_list("hello"))
        self.assertTrue(okay.in_list("goodbye"))
        # These words are not in the list
        self.assertFalse(okay.in_list("bonjour"))
        self.assertFalse(okay.in_list("algorithms"))
        self.assertFalse(okay.in_list("computer"))
        self.assertFalse(okay.in_list("hello-world"))

    # Verify that prepend works properly
    def test_prepend(self):
        okay = Node("okay", None)
        hello = Node("hello", None)
        goodbye = Node("goodbye", None)
        self.assertEqual(1, goodbye.list_length())
        goodbye.prepend(hello)
        self.assertEqual(2, hello.list_length())
        hello.prepend(okay)
        self.assertEqual(3, okay.list_length())

    # Verify the tuple is returned as expected
    def test_stats(self):
        okay = Node("okay", None)
        self.assertEqual(("okay", 1), okay.stats())
        hello = Node("hello", None)
        self.assertEqual(("hello", 1), hello.stats())
        goodbye = Node("goodbye", None)
        self.assertEqual(("goodbye", 1), goodbye.stats())

    # Verify the info for the list is returned as expected
    def test_list_info(self):
        okay = Node("okay", None)
        hello = Node("hello", None)
        goodbye = Node("goodbye", None)
        goodbye.prepend(hello)
        hello.prepend(okay)
        expected_info = [("okay", 1),
                         ("hello", 1),
                         ("goodbye", 1)]
        self.assertEqual(expected_info, okay.list_info())

    # Verify that find returns the count as expected
    def test_node_find(self):
        okay = Node("okay", None)
        hello = Node("hello", None)
        goodbye = Node("goodbye", None)
        goodbye.prepend(hello)
        hello.prepend(okay)
        # List is okay -> hello -> goodbye
        self.assertEqual(1, okay.find("okay"))
        self.assertEqual(1, okay.find("hello"))
        self.assertEqual(1, okay.find("goodbye"))
        # -1 when not found
        self.assertEqual(-1, okay.find("algorithms"))
        self.assertEqual(-1, okay.find("computer"))
        self.assertEqual(-1, hello.find("okay"))

    # Verify that the string representation is returned correctly
    def test_list_all_nodes(self):
        okay = Node("okay", None)
        hello = Node("hello", None)
        goodbye = Node("goodbye", None)
        goodbye.prepend(hello)
        hello.prepend(okay)
        # List is okay -> hello -> goodbye
        expected_str = "okay 1\n" \
                       "hello 1\n" \
                       "goodbye 1\n"
        self.assertEqual(expected_str, okay.list_all_nodes())

    # Verify that nodes are deleted from linked list properly
    # 'Delete head' by calling from a different node
    def test_delete_node(self):
        okay = Node("okay", None)
        hello = Node("hello", None)
        goodbye = Node("goodbye", None)
        goodbye.prepend(hello)
        hello.prepend(okay)
        # List is okay -> hello -> goodbye
        okay.delete_node("hello")
        expected_str = "okay 1\n" \
                       "goodbye 1\n"
        self.assertEqual(expected_str, okay.list_all_nodes())
        okay.delete_node("goodbye")
        expected_str = "okay 1\n"
        self.assertEqual(expected_str, okay.list_all_nodes())


# ---------------------------------------------------------------------------------------
# Test class that focuses on TextHash class functionality
class HashTest(unittest.TestCase):
    # Verify that attributes are set properly
    def creation(self):
        t = TextHash(17, 701)
        expected_table = [None]*701
        self.assertEqual(17, t.seed)
        self.assertEqual(701, t.m)
        self.assertEqual(expected_table, t.table)

    # Check that the hash function is consistent (same word has same key)
    def test_consistency(self):
        t = TextHash(17, 701)
        self.assertEqual(t.hash_word("stop"), t.hash_word("stop"))
        self.assertEqual(t.hash_word("pots"), t.hash_word("pots"))
        self.assertEqual(t.hash_word("tops"), t.hash_word("tops"))
        self.assertEqual(t.hash_word("post"), t.hash_word("post"))
        self.assertEqual(t.hash_word("spot"), t.hash_word("spot"))

    # Check permutations of "stop" are all unique
    def test_permutations(self):
        t = TextHash(17, 701)
        keys = []
        keys.append(t.hash_word("stop"))
        keys.append(t.hash_word("pots"))
        keys.append(t.hash_word("tops"))
        keys.append(t.hash_word("post"))
        keys.append(t.hash_word("spot"))
        # Compare all pairs, except when word == word
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                if j <= len(keys):
                    self.assertNotEqual(keys[i], keys[j])

    # Verify that the fixed length table is created correctly
    # In python, must initialize list first to make it behave as an array
    # Method: Initialize all M places to None
    def test_table_initialization(self):
        # Validate methodology
        blank_table = [None]*701
        for i in range(len(blank_table)):
            self.assertIsNone(blank_table[i])
        # Validate implementation
        t = TextHash(17, 701)
        for i in range(t.m):
            self.assertIsNone(t.table[i])

    # Check if new_node successfully inserted into free table space
    def test_simple_insert(self):
        # Using table size 1 to guarantee location
        t = TextHash(17, 1)
        t.insert("test")
        self.assertEqual("test", t.table[0].word)

    # Check that collisions where the word is new are handled correctly
    def test_collision_insert(self):
        # Using table size 1 to guarantee locations
        t = TextHash(17, 1)
        # All subsequent inserts should be added to the front of the list
        t.insert("fourth")
        t.insert("third")
        t.insert("second")
        t.insert("first")
        expected_info = [('first', 1),
                         ('second', 1),
                         ('third', 1),
                         ('fourth', 1)]
        self.assertEqual(expected_info, t.table[0].list_info())

    # Check collision handled when duplicate at end of list
    def test_collision_duplicate_end(self):
        t = TextHash(17, 1)
        t.insert("hello")
        t.insert("goodbye")
        t.insert("okay")
        t.insert("algorithms")
        t.insert("hello")
        expected_info = [('hello', 2),
                         ('algorithms', 1),
                         ('okay', 1),
                         ('goodbye', 1)]
        self.assertEqual(expected_info, t.table[0].list_info())

    # Check collision handled when duplicate inside the list
    def test_collision_duplicate_inner(self):
        t = TextHash(17, 1)
        t.insert("hello")
        t.insert("goodbye")
        t.insert("repeat")
        t.insert("algorithms")
        t.insert("computer")
        t.insert("repeat")
        expected_info = [('repeat', 2),
                         ('computer', 1),
                         ('algorithms', 1),
                         ('goodbye', 1),
                         ('hello', 1)]
        self.assertEqual(expected_info, t.table[0].list_info())

    # Check collision handled when duplicate is the head of list
    def test_collision_duplicate_head(self):
        t = TextHash(17, 1)
        t.insert("hello")
        t.insert("goodbye")
        t.insert("okay")
        t.insert("hello")
        t.insert("hello")
        t.insert("hello")
        t.insert("hello")
        expected_info = [('hello', 5),
                         ('okay', 1),
                         ('goodbye', 1)]
        self.assertEqual(expected_info, t.table[0].list_info())

    # Verify string is filtered, parsed, & inserted (e.g. processed) correctly
    def test_process(self):
        t = TextHash(17, 1)
        t.process("Colorless green ideas sleep furiously.")
        expected_info = [('furiously', 1),
                         ('sleep', 1),
                         ('ideas', 1),
                         ('green', 1),
                         ('colorless', 1)]
        self.assertEqual(expected_info, t.table[0].list_info())
        t.process("Colorless green ideas sleep furiously.")
        expected_info = [('furiously', 2),
                         ('sleep', 2),
                         ('ideas', 2),
                         ('green', 2),
                         ('colorless', 2)]
        self.assertEqual(expected_info, t.table[0].list_info())

    # Verify the string representation of keys and counts is correct
    def test_list_all_keys(self):
        t = TextHash(17, 5)
        t.process("Colorless green ideas sleep furiously.")
        expected_str = "colorless 1\n" \
                       "sleep 1\n" \
                       "ideas 1\n" \
                       "green 1\n" \
                       "furiously 1\n"
        self.assertEqual(expected_str, t.list_all_keys())

    # Verify that find returns the correct count when looking up words
    def test_hash_find(self):
        t = TextHash(17, 7)
        t.insert("goodbye")
        t.insert("goodbye")
        t.insert("goodbye")
        t.insert("hello")
        t.insert("hello")
        t.insert("okay")
        self.assertEqual(3, t.find("goodbye"))
        self.assertEqual(2, t.find("hello"))
        self.assertEqual(1, t.find("okay"))
        self.assertEqual(-1, t.find("algorithms"))
        self.assertEqual(-1, t.find("computer"))
        self.assertEqual(-1, t.find("science"))

    # Verify the save function writes to file properly
    def test_save(self):
        t = TextHash(17, 7)
        t.insert("okay")
        t.insert("hello")
        t.insert("goodbye")
        t.insert("goodbye")
        t.insert("hello")
        t.insert("hello")
        t.insert("hello")
        t.insert("hello")
        t.save("test.txt")
        expected_output = "goodbye 2\n" \
                          "okay 1\n" \
                          "hello 5\n"
        file = open("test.txt", "r")
        text = file.read()
        self.assertEqual(expected_output, text)
        file.close()

    # Verify keys are deleted properly - end node
    def test_delete_end(self):
        t = TextHash(17, 1)
        t.insert("goodbye")
        t.insert("hello")
        t.insert("okay")
        t.delete_key("goodbye")
        expected_info = [('okay', 1),
                         ('hello', 1)]
        self.assertEqual(expected_info, t.table[0].list_info())

    # Verify keys are deleted properly - inside list
    def test_delete_inner(self):
        t = TextHash(17, 1)
        t.insert("goodbye")
        t.insert("hello")
        t.insert("okay")
        t.delete_key("hello")
        expected_info = [('okay', 1),
                         ('goodbye', 1)]
        self.assertEqual(expected_info, t.table[0].list_info())

    # Verify keys are deleted properly - head node
    def test_delete_head(self):
        t = TextHash(17, 1)
        t.insert("goodbye")
        t.insert("hello")
        t.insert("okay")
        t.delete_key("okay")
        expected_info = [('hello', 1),
                         ('goodbye', 1)]
        self.assertEqual(expected_info, t.table[0].list_info())


def main():
    # Run all the tests
    unittest.main(verbosity=3)


main()
