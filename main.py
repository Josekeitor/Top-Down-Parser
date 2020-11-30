''' Top Down parser (non-recursive)

This is a script to generate strings from a grammar that is represented as a dictionary, using productions.

The script builds a tree as it tries to construct the string, it keeps the tree properly pruned
in order to save memory and it takes in a maximum depth value to prevent infinite runtime.

This script accepts external .txt files formated in the following manner:

    - The first line indicates the set of non-terminal symbols separated by commas, only one uppercase character.

    - The second line indicates the set of terminal symbols separated by commas, only one lowercase character.

    - The third line indicates the start symbol.

    - The following lines indicate the productions of the grammar in the following format:

    non_terminal_symbol - > chain terminals or non-terminal symbol

    Example, the following line:\n
    S->BA\n
    indicates that the gramamr includes a production from S to BA

'''

class TreeNode:
    '''
    Class to represent the node of a tree, each node contains a value, depth and children.

    Attributes:
    ------------
    value (str): The value of the node itself
    depth (int): Reference of depth in the tree
    children (TreeNode[]): List of children nodes to this node

    '''
    def __init__(self, value, depth):
        self.value = value
        self.depth = depth
        self.children = []
    def __str__(self):
        return self.value

def parseGramarFromFile(file_number):
    '''


    :param file_number: An integer denoting the file number to load the grammar from ex: if file_number = 2
                        the loaded file will be test2
    :return: grammar_info - a list of all of the information in the parsed file as well as the dictionary
             representation of the gramar
    '''

    # Build the file path and open the file
    path = 'Files/test' + test_case + '.txt'
    file = open(path, 'r')

    # Initialize the grammar (represented as a dictionary)
    grammar = {}

    # Get non terminal symbols, terminal symbols and the start symbol from the file
    non_terminal_symbols = set(file.readline().strip().split(","))
    terminal_symbols = set(file.readline().strip().split(","))
    start_symbol = file.readline().strip()

    # For each of the remaining lines in the file, parse the grammar and represent it as a dictionary
    # with non terminal symbols as keys and a list of productions as value
    for line in file:
        input_array = line.strip().split('->')

        non_terminal_symbol = input_array[0]
        production = input_array[1]

        if non_terminal_symbol not in grammar:
            grammar[non_terminal_symbol] = [production]
        else:
            grammar[non_terminal_symbol].append(production)

    # Initialize list to return
    grammar_info = []

    # Add all parsed information into the list
    grammar_info.append(start_symbol)
    grammar_info.append(non_terminal_symbols)
    grammar_info.append(terminal_symbols)
    grammar_info.append(grammar)

    # Return the list
    return grammar_info




def pprint_tree(node, file=None, _prefix="", _last=True):
    """
        Function to print a tree given the root node

        Parameters:
        ---------------
        node (TreeNode()): The root node of a tree
        file (any): Forwarded to print
        _prefix (str): Used between recursive calls
        _last (str): Used between recursive calls

        Returns:
        ---------------
        None

          """
    print(_prefix, "`- " if _last else "|- ", node.value, sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    new_test_file = 'y'
    while new_test_file == 'y':
        # Ask which structure the user wants to use for the grammar, in order to pull information from that file
        test_case = input('please enter the number of the test you want to run (from 1 to 4) \n')

        # If the input for the number of the file is invalid, keep asking until it is valid
        while int(test_case) < 1 or int(test_case) > 4:
            print("Please enter a valid test number ")
            test_case = input()

        grammar_info = parseGramarFromFile(test_case)

        start_symbol = grammar_info[0]
        non_terminal_symbols = grammar_info[1]
        terminal_symbols = grammar_info[2]
        grammar = grammar_info[3]
        # Print informtation to validate
        print()
        print("non terminal symbols: ", non_terminal_symbols)
        print("terminal symbols: ", terminal_symbols)
        print("start symbol: ", start_symbol)
        print()
        # Print the grammar for validation
        print("grammar: ", grammar)
        print()

        # Initialize queue and ask user for target string
        q = []
        answer = 'y'
        while(answer == 'y'):

            target = input('Enter a string to build: ')
            max_depth = int(input('Enter the maximum depth of the tree: '))

            # Set root of tree to start symbol and add the root to the queue
            root = TreeNode(start_symbol, 0)
            q.append(root)

            # While the queue is not empty do the following
            while q:
                # Get the next element in the queue
                element = q.pop(0)

                # Find the left most variable (non terminal symbol)
                for i in range(len(element.value)):
                    if element.value[i] in non_terminal_symbols:
                        left_most_variable = element.value[i]
                        break
                # Assing the string as the value of the node being analyzed
                string = element.value

                # For each rule in the list of the left most non terminal symbol do the following
                for rule in grammar[left_most_variable]:
                    # If we exceed the max depth, exit the cycle
                    if element.depth >= max_depth:
                        break
                    # Replace the first instance of the non terminal symbol with its corresponding production
                    result = string.replace(left_most_variable, rule, 1)
                    # If there are more non terminal symbols in the string being built do the following
                    if len(non_terminal_symbols.intersection(set(result))) >= 1:

                        # Traverse the target string and do the following
                        for i in range(len(target)):
                            # If we ran out of characters in the result, exit
                            if len(result) < i:
                                break
                            # If we find a non terminal symbol means all previous characters matched so do the following
                            if (result[i] in non_terminal_symbols):
                                # Create a new TreeNode with the modified string as its value and assign its depth
                                # as the previous node's depth + 1
                                node_to_add = TreeNode(result, element.depth + 1)
                                '''print('added ', result, ' as a child of node ', element, ' current depth ', node_to_add.depth)
                                '''
                                # Add the new node to the queue and to the tree
                                q.append(node_to_add)
                                element.children.append(node_to_add)
                                break
                            # If we find a character that does not match, exit
                            if result[i] != target[i]:
                                break
                            # If the modified string is the target string we are done
                            if result == target:
                                break
                    # If the modified string is the target, add the result to the tree and exit the cycle
                    if result == target:
                        element.children.append(TreeNode(result, element.depth + 1))
                        break
                # Since we already found the target string, exit all cycles
                if result == target:
                    break
                # If we exceed the max depth, exit all cycles
                if element.depth >= max_depth:
                    break

            # If we were able to build the string, accept it and print the tree
            # otherwise, indicate that no solution was found and print the tree
            if result == target:
                print()
                print('Accepted')
                print()
                pprint_tree(root)
                print()
                print('string built ', result)
                print()
            else:
                print()
                pprint_tree(root)
                print()
                print('No solution was found for the string')
                print()
            # Ask if the user wants to process another string with the same file
            answer = input('would you like to process another string? (y/n) \n')
        # If the user does not want to process
        if answer == 'n':
            new_test_file = input('would you like to load a new test file? (y/n) \n')

