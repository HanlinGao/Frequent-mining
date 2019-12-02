import time

# data in form of ['TID', 'I1', 'I2'...]
DATA_SIZE = 32560
min_support = 6512
PARTITION_SIZE = 1628    # Here we suppose each partition has the same size
GROUPS = DATA_SIZE / PARTITION_SIZE


def partition_database(datafile):
    # partition the database into n partitions, return them
    partitions = []

    with open(datafile, 'r') as f:
        count = PARTITION_SIZE
        temp = []
        lines = 0
        for each_line in f:
            temp.append(each_line.strip('\n').split(' '))
            count -= 1
            # reset the counter and the container if a partition is completed
            if count == 0:
                partitions.append(temp)
                temp = []
                count = PARTITION_SIZE

            lines += 1
            if lines == DATA_SIZE:
                break
    return partitions


def one_itemsets(partition):
    # search for 1-itemset, return in form of {ele: [TIDlist]...}
    elements = dict()
    for each_transaction in partition:
        # temp will be needed if want to avoid counting an item occurs many times in one transaction
        # temp = set(each_transaction)
        for ele in each_transaction[1:]:    # jump the first element, since it is TID
            if ele in elements:
                elements[ele].append(each_transaction[0])
            else:
                elements[ele] = [each_transaction[0]]

    # check the qualified 1-itemsets
    elements = {key: value for key, value in elements.items() if len(elements[key]) >= min_support / GROUPS}

    return elements


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


def get_join_fp(candidate_dict=dict()):
    # return qualified Lk from L(k-1)
    elements_list = list(candidate_dict.keys())
    length = len(elements_list)
    result = {}
    for i in range(length):
        for the_other in elements_list[i+1:]:
            # for 1-itemset, the keys are str, but for k-itemset, the keys are tuple
            if isinstance(the_other, str):
                temp_set = set.union({elements_list[i]}, {the_other})
                original_length = 1
            else:
                temp_set = set.union(set(elements_list[i]), set(the_other))
                original_length = len(the_other)
            temp_length = len(temp_set)

            # if the length of temp_set is one more than the original, then they are joint successfully
            if temp_length == (original_length + 1):
                # check k-1-length subsets, if not True, ignore this candidate
                if not check_subsets(elements_list, sorted(temp_set)):
                    continue
                # if pass subset testing, construct its tidlist and check whether to be included
                temp_tidlist = set(candidate_dict[elements_list[i]]) & set(candidate_dict[the_other])
                temp_count = len(temp_tidlist)

                if temp_count >= min_support / GROUPS:
                    key = tuple(sorted(temp_set))
                    if key not in result:
                        result[key] = list(temp_tidlist)
    return result


def gen_large_itemsets(partition):
    # return local fp for this partition
    local_fp = dict()
    local_one = one_itemsets(partition)
    temp = local_one
    # temp represents Lk(k-itemsets). while k-itemsets is not none, keep find the (k+1)-itemsets
    while temp:
        temp = get_join_fp(temp)
        local_fp = {**local_fp, **temp}
    return local_one, local_fp


def partition_mining(datafile):
    partitions = partition_database(datafile)
    print('processing....')
    # first scan: get the global fp candidates
    global_one = dict()
    global_fp = dict()
    for each in partitions:
        local_one, local_fp = gen_large_itemsets(each)
        global_one = {**global_one, **local_one}
        global_fp = {**global_fp, **local_fp}

    # set global dict to zero, in order to serve as counter
    for each in global_one:
        global_one[each] = []
    for each in global_fp:
        global_fp[each] = 0

    # second scan: count each candidates
    for each in partitions:
        # generate 1-itemsets tidlist
        for each_transaction in each:
            for ele in each_transaction[1:]:  # jump the first element, since it is TID
                if ele in global_one:
                    global_one[ele].append(each_transaction[0])
                else:
                    global_one[ele] = [each_transaction[0]]

    for elements in global_fp:
        templist = set(global_one[elements[0]])
        for ele in elements[1:]:
            templist = set(global_one[ele]) & templist
        global_fp[elements] = len(templist)

    # check the count
    global_one = {key: value for key, value in global_one.items() if len(global_one[key]) >= min_support}
    global_fp = {key: value for key, value in global_fp.items() if global_fp[key] >= min_support}

    # output the result
    final_fp = {**global_one, **global_fp}
    print('total frequent pattern number:', len(final_fp))


start = time.time()
partition_mining('adult_processed.txt')
end = time.time()
print('partition rt: ', end-start)