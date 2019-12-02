import time
#data_set = [['I1', 'I2', 'I5'], ['I2', 'I4'], ['I2', 'I3'], ['I1', 'I2', 'I4'], ['I1', 'I3'],
#            ['I2', 'I3'], ['I1', 'I3'], ['I1', 'I2', 'I3', 'I5'], ['I1', 'I2', 'I3']]
min_support = 6512


def count_freq(data_set, temp_set=set()):
    # count the frequency of itemset(temp_set) in data_set, return the frequency
    count = 0
    for each in data_set:
        if temp_set.issubset(each):
            count += 1
    return count


def check_subsets(candidates, superlist):
    # check whether the k-1-length subsets of candidates are all frequent
    length = len(superlist)
    for i in range(length):
        superlist_copy = superlist[:]
        superlist_copy.pop(i)
        # find a k-1-length subset of superset, check whether it is an element in candidates

        if len(superlist_copy) == 1:
            if not set(superlist_copy).issubset(set(candidates)):
                return False
        else:
            if not tuple(superlist_copy) in set(candidates):
                return False
    return True


def get_join_freq(candidates_list, data_set):
    # detect all possible join operation of elements in (k-1)-length itemsets, return qualified candiates
    length = len(candidates_list)
    # use a dict to save the join results, in case of creating same results by different combinations
    result_set = {}

    # change the type into list
    candidates_list = list(candidates_list)
    for i in range(length):
        # for each element, search the rest undetected elements
        for each in candidates_list[i+1:]:
            if isinstance(each, str):
                temp_set = set.union({candidates_list[i]}, {each})
                original_length = 1
            else:
                temp_set = set.union(set(each), set(candidates_list[i]))
                original_length = len(each)
            temp_length = len(temp_set)

            # if the length of temp_set is one more than the original, then they can be joint
            if temp_length == (original_length + 1):
                # check k-1-length subsets, if not True, pass this candidate
                if not check_subsets(candidates_list, sorted(temp_set)):
                    continue

                # if pass subset testing, count to check whether the result is frequent
                temp_count = count_freq(data_set, temp_set)

                if temp_count >= min_support:
                    key = tuple(sorted(temp_set))
                    if key not in result_set:
                        result_set[key] = temp_count
    return result_set


def search_one_patterns(data_set):
    # search for possible 1-itemset, return in form of {('I1'), ('I2', 'I3'), ('I2', 'I5')}
    elements = dict()
    for each_transaction in data_set:
        # avoid an item occurs many times in one transaction
        temp = set(each_transaction)
        for ele in temp:
            if ele in elements:
                elements[ele] += 1
            else:
                elements[ele] = 1

    # save the qualified 1-itemset
    for each in list(elements.keys())[:]:
        if elements[each] < min_support:
            del elements[each]

    return elements


def main(datafile):
    data_set = []
    with open(datafile, 'r') as f:
        lines = 0
        for each_line in f:
            data_set.append(each_line.strip('\n').split(' ')[1:])
            lines += 1
            if lines == 32560:
                break

    '''data_set = [['M', 'O', 'N', 'K', 'E', 'Y'], ['D', 'O', 'N', 'K', 'E', 'Y'], ['M', 'A', 'K', 'E'],
                ['M', 'U', 'C', 'K', 'Y'], ['C', 'O', 'K', 'I', 'E']]'''
    # frequent itemsets will be shown in the form of [('I1',), ('I2'), ('I3, I4'), ('I1', 'I2', 'I5')]
    freq_patterns = {}
    current_candidates = search_one_patterns(data_set)
    for each in current_candidates:
        freq_patterns[(each, )] = current_candidates[each]  # add 1-length itemsets into final frequent patterns set

    check_length = len(current_candidates)  # check whether candidates set is empty
    while check_length > 0:
        print('processing....')
        # join with itself to get a k+1 length itemsets
        current_candidates = get_join_freq(current_candidates.keys(), data_set)
        check_length = len(current_candidates)
        if check_length != 0:
            for each in current_candidates:
                freq_patterns[each] = current_candidates[each]

    print('pattern dict:', freq_patterns)
    final_fp = sorted(list(freq_patterns.keys()))
    final_fp = sorted(final_fp, key=lambda x: len(x))
    print('frequent patterns: ', final_fp)
    print('total frequent patterns number: ', len(final_fp))

start = time.time()
main('adult_processed.txt')
end = time.time()
print('Apriori rt: ', end-start)


