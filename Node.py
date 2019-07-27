# George Dunnery - CS 5800


# Class to represent a node in a singly linked list
class Node:

    # Node object constructor
    #  word: string, the word to store at this node
    #  nxt: Node, the next node in the linked list
    # Constructs the Node object
    def __init__(self, word: str, nxt):
        self.count = 1
        self.word = word
        self.next = nxt

    # Function to query the info about this node
    # Returns a string of the form "word, integer"
    def __str__(self) -> str:
        return self.word + ' ' + str(self.count)

    # Function to query the length of the linked list
    # Returns the length as an integer
    def list_length(self) -> int:
        head = self
        return self.list_length_aux(head, 0)

    # Auxiliary function to list_length, please use list_length instead
    #  node: Node, the head element
    #  count: start at 0 to count the elements in the linked list
    # Returns the length as an integer
    def list_length_aux(self, node, count: int) -> int:
        if not node:
            return count
        else:
            count += 1
            return self.list_length_aux(node.next, count)

    # Function to check if a word is in the linked list
    #  word: string, the word to search for
    # Returns bool, true if the word is in the list, otherwise false
    def in_list(self, word: str) -> bool:
        node = self
        return self.in_list_aux(word, node)

    # Auxiliary function to in_list, please use in_list instead
    #  word: string, the word to search for
    #  node: Node, the head of the linked list
    # Returns bool, true if the word is in the list, otherwise false
    def in_list_aux(self, word: str, node) -> bool:
        if not node:
            return False
        elif word == node.word:
            return True
        else:
            return self.in_list_aux(word, node.next)

    # Function to prepend an element as the new head of the linked list
    #  new_head: Node, the new head of the list
    #  ex. to create x -> y, call y.prepend(x)
    # Returns nothing
    def prepend(self, new_head) -> None:
        new_head.next = self

    # Function to query the stats of a node as a tuple
    # Returns a tuple in the form ("word", count)
    def stats(self) -> tuple:
        return self.word, self.count

    # Function to return the list info as "word, count\n"
    # Call on the head of the linked list
    # Returns a string
    def list_info(self) -> list:
        node = self
        info = []
        return self.list_info_aux(node, info)

    # Auxiliary function to list_info, please use list_info instead
    #  node: Node, the head node in the linked list
    #  info: list, tuples of the form ('word', count)
    def list_info_aux(self, node, info: list) -> list:
        if not node:
            return info
        else:
            info.append(node.stats())
            node = node.next
            return self.list_info_aux(node, info)

    # Function to find and extract the repeated word
    #  word: string, the repeated word to locate
    # Returns Node object, which should be prepended by calling function
    def extract(self, word: str) -> object:
        # Maintain reference to previous node (due to singly linked list)
        prev = None
        node = self
        while node:
            # Error checking to avoid infinite loop if list broken
            if not node:
                raise Exception("Chain broken: None unexpectedly encountered.")
            # When the words match, the node is found
            elif node.word == word:
                # Inc count, splice out node by changing previous node's next
                node.count += 1
                # prev is None when the duplicate is already the head of the list
                if prev is not None:
                    prev.next = node.next
                return node
            # Otherwise, keep looking (already determined node exists)
            else:
                prev = node
                node = node.next

    # Function to lookup the count for a particular word
    # Meant to work in tandem with the find function in HashText
    #  word: string, the word to search for
    # Returns the count of the word or 0 if not found
    def find(self, word: str) -> int:
        node = self
        return self.find_aux(node, word)

    # Auxiliary function to find, please use find instead
    #  node: Node, the head of the linked list
    #  word: string, the word to search for
    # Returns the count of the word or -1 when not found
    def find_aux(self, node, word: str) -> int:
        if not node:
            return -1
        elif word == node.word:
            return node.count
        else:
            return self.find_aux(node.next, word)

    # Function to list all the nodes as a string
    def list_all_nodes(self) -> str:
        cat = ""
        node = self
        return self.list_all_nodes_aux(node, cat)

    # Auxiliary function to list_all_nodes, please use list_all_nodes instead
    #  node: Node, the head of the linked list
    #  cat: string, to concatenate the information stored in tuples as a string
    # Returns a string, representing the tuples ('word', count) in the linked list
    def list_all_nodes_aux(self, node, cat: str) -> str:
        if not node:
            return cat
        else:
            cat += node.__str__() + '\n'
            return self.list_all_nodes_aux(node.next, cat)

    # Function to delete a node from the linked list
    #  word: string, the word of the node to delete
    # Returns nothing
    def delete_node(self, word) -> None:
        prev = None
        node = self
        self.delete_node_aux(node, prev, word)

    # Auxiliary function to delete_node, please use delete_node instead
    #  node: Node, the current node
    #  prev: Node, the previous node
    #  word: string, the word of the node to delete
    # Returns nothing
    def delete_node_aux(self, node, prev, word: str) -> None:
        # Assume head check takes place in hash delete_key
        if node.word == word:
            if prev is not None:
                prev.next = node.next
        else:
            self.delete_node_aux(node.next, node, word)
