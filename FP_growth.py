import time
from itertools import chain, combinations

min_support = 6512


class Tree_node:
    # node in tree, initial with label, support, parent
    def __init__(self, label, parent, support=1):
        self.label = label
        self.count = support
        self.parent = parent
        self.children = []

    # rewrite __str__ to show tree friendly
    def __str__(self, level=0):
        result = '\t' * level + self.label + ":" + str(self.count) + "\n"
        for child in self.children:
            result += child.__str__(level+1)
        return result

    def accumulate(self, number=1):
        self.count += number

    def add_node(self, newnode):
        self.children.append(newnode)


class Header_node:
    # node in the link list of header, initial with its tree-node information
    def __init__(self, treenode=Tree_node(None, None)):
        self.treeinfo = treenode
        self.next = None

    # rewrite to show header nodes friendly
    def __str__(self):
        return self.treeinfo.label + ":" + str(self.treeinfo.count)

    def add_node(self, new_node):
        self.next = new_node


class Header_list:
    # Headlist, initial with all 1-itemset and create node for them
    def __init__(self, one_itemlabel):
        self.eledict = {}
        for each in one_itemlabel:
            self.eledict[each] = None

    def add_node(self, label, new_header):
        # label = 'A', add the node into dict

        # if have added node in this label, add the new_header to the end
        if self.eledict[label]:
            end = self.eledict[label]
            while end.next:
                end = end.next

            end.next = new_header
        else:
            self.eledict[label] = new_header

    def count(self, label):
        # label = 'A_123'
        link_node = self.eledict[label]
        count = link_node.treeinfo.count
        while link_node.next:
            link_node = link_node.next
            count += link_node.treeinfo.count
        return count


def search_one_patterns(data_set):
    # search for possible 1-itemset, return in descending support [('I1', maxsup), ('I2', secondtomax)]
    elements = dict()
    for each_transaction in data_set:
        # avoid an item occurs many times in one transaction
        temp = set(each_transaction)
        for ele in temp:
            if ele in elements:
                elements[ele] += 1
            else:
                elements[ele] = 1
    # sorted with value of support and save the qualified 1-itemset
    elements = sorted(elements.items(), key=lambda x: x[1], reverse=True)
    result_list = []
    for each in elements:
        if int(each[1]) >= min_support:
            result_list.append((each[0], int(each[1])))    # set type can only add tuple as elements

    return result_list


# this function references an example of Python itertools official website, in order to get all subsets of a set
def powerset(iterable):
    "powerset([1,2,3]) --> (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))


def sort_transaction(transaction, one_itemlabel):
    # resort the transaction into order
    result = []
    for order_refer in one_itemlabel:
        for each_ele in transaction:
            if each_ele == order_refer:
                result.append(each_ele)
    return result


def gen_tree(headerlist, transaction, current, root):
    # generate a tree, get its respective headerlist in the meanwhile
    if current == len(transaction):
        return

    check_flag = 0  # represent have not find one
    for each_child in root.children:
        # if find, move on to next element and check in the children of root
        if each_child.label == transaction[current]:
            # print('checking children of', root.label, 'find', transaction[current])
            check_flag = 1
            each_child.accumulate()
            gen_tree(headerlist, transaction, current + 1, each_child)

    # if not find, create all rest elements as a new branch
    if check_flag == 0:
        current_root = root
        for each_label in transaction[current:]:
            # print('creating label', each_label, 'as child of', current_root.label)
            temp_node = Tree_node(each_label, current_root)
            temp_header = Header_node(temp_node)

            current_root.add_node(temp_node)
            headerlist.add_node(each_label, temp_header)
            current_root = temp_node


def gen_conditionalbase(headerlist, suffix):
    # prune suffix, store the rest paths in the tree
    conditional_base = []
    link_node = headerlist.eledict[suffix]

    temp_base = []  # store one path

    while link_node.next:
        if link_node.treeinfo.parent.label == 'null':
            pass
        else:
            t_node = link_node.treeinfo.parent
            while t_node.parent.label != 'null':
                temp_base.append(t_node.label)
                t_node = t_node.parent
            temp_base.append(t_node.label)

            temp_base.reverse()
            for i in range(link_node.treeinfo.count):
                conditional_base.append(temp_base)
            temp_base = []

        link_node = link_node.next

    if link_node.treeinfo.parent.label == 'null':
        pass
    else:
        t_node = link_node.treeinfo.parent
        while t_node.parent.label != 'null':
            temp_base.append(t_node.label)
            t_node = t_node.parent
        temp_base.append(t_node.label)

        temp_base.reverse()
        for i in range(link_node.treeinfo.count):
            conditional_base.append(temp_base)

    return conditional_base


def min_sup(beta, headerlist):
    # beta: (A, B)
    min_value = 99999
    for each in beta:
        temp = headerlist.count(each)
        if temp < min_value:
            min_value = temp
    return min_value


def show_headers(header=Header_list([])):
    for row in header.eledict.keys():
        result = str(row) + ":" + str(header.eledict[row])
        node = header.eledict[row]
        while node.next:
            node = node.next
            result += "--> " + str(node)
        print(result)


def fp_mine(tree, label_add, headerlist, fp_results, suffixorder):
    # check whether contains a single path
    check_single_path = True
    single_path = []
    length = len(tree.children)
    while length > 0:   # still have children
        if length > 1:
            check_single_path = False
            break
        else:
            child = tree.children[0]
            single_path.append(child.label)
            tree = child
            length = len(tree.children)

    # if Tree contains a single path
    if check_single_path:
        possible_combinations = list(powerset(single_path))      # [(A, B), (A, C)...]
        for beta in possible_combinations:
            if len(label_add) == 0:
                pattern = beta
            else:
                pattern = list(beta)
                pattern.extend(list(label_add))
                pattern = tuple(pattern)

            fp_results[pattern] = min_sup(beta, headerlist)
    else:
        for each in suffixorder:
            if len(label_add) == 0:
                pattern = (each, )
            else:
                pattern = [each]
                pattern.extend(list(label_add))
                pattern = tuple(pattern)

            fp_results[pattern] = headerlist.count(each)

            # construct beta's conditional pattern base and beta's conditional FP_tree
            conditional_base = gen_conditionalbase(headerlist, each)
            fp_con_root = Tree_node('null', None)

            one_items = search_one_patterns(conditional_base)
            one_labels = [x[0] for x in one_items]
            con_headerlist = Header_list(one_labels)

            for each_transaction in conditional_base:
                transaction_sorted = sort_transaction(each_transaction, one_labels)
                gen_tree(con_headerlist, transaction_sorted, 0, fp_con_root)

            orders = list(reversed(one_labels))
            if len(fp_con_root.children) != 0:
                fp_mine(fp_con_root, pattern, con_headerlist, fp_results, orders)


def fp_growth(datafile):
    print('processing...')
    # generate data_set in form of [[...], [....], [....]]
    data_set = []
    with open(datafile, 'r') as f:
        lines = 0
        for each_line in f:
            data_set.append(each_line.strip('\n').split(' ')[1:])
            lines += 1
            if lines == 32560:
                break

    '''data_set = [['I1', 'I2', 'I5'], ['I2', 'I4'], ['I2', 'I3'], ['I1', 'I2', 'I4'], ['I1', 'I3'],
                ['I2', 'I3'], ['I1', 'I3'], ['I1', 'I2', 'I3', 'I5'], ['I1', 'I2', 'I3']]'''

    fp_results = {}     # store the final results
    one_itemsets = search_one_patterns(data_set)    # [(A, A_sup), (B, B_sup)...]
    one_itemlabel = [x[0] for x in one_itemsets]    # get label order [A, B, C....]

    # create FP-tree and its respective headerlist
    root = Tree_node('null', None)
    header_list = Header_list(one_itemlabel)
    for each in data_set:
        transaction_sorted = sort_transaction(each, one_itemlabel)
        # create branch
        gen_tree(header_list, transaction_sorted, 0, root)

    '''create conditional database and its respective conditional FP-tree and conditional headerlist'''

    suffix_order = list(reversed(one_itemlabel))  # search the last element first
    fp_mine(root, '', header_list, fp_results, suffix_order)
    print('frequent pattern dict: ', fp_results)
    final_fp = sorted(list(fp_results.keys()))
    final_fp = sorted(final_fp, key=lambda x: len(x))
    print('frequent patterns: ', final_fp)
    print('total frequent patterns number', len(final_fp))


start = time.time()
fp_growth('adult_processed.txt')
end = time.time()
print('FP-growth rt: ', end-start)



