# change data into form of
# |-TID
# |-age_group
# |-workclass
# |-fnlwgt_group
# |-education, education_num
# |-marital_status
# |-occupation
# |-relationship
# |-race
# |-sex
# |-capital-gain_group, capital-loss_group, hours-per-week_group
# |-native-country
# |-income label


def data_analy(datafile):
    age_min = 0
    age_max = 0
    age_sum = 0

    fnlwgt_min = 0
    fnlwgt_max = 0
    fnlwgt_sum = 0

    capital_gain_min = 0
    capital_gain_max = 0
    capital_gain_sum = 0

    capital_loss_min = 0
    capital_loss_max = 0
    capital_loss_sum = 0

    hours_min = 0
    hours_max = 0
    hours_sum = 0

    lines = 0
    with open(datafile, 'r') as fin:
        for each_line in fin:
            lines += 1
            temp = each_line.strip('\n').split(', ')
            # print(temp)
            age = temp[0]
            if age == '?':
                age = 0
            else:
                age = int(age)
                if age <= age_min:
                    age_min = age
                if age >= age_max:
                    age_max = age
                age_sum += age

            fnlwgt = temp[2]
            if fnlwgt == '?':
                fnlwgt = 0
            else:
                fnlwgt = int(fnlwgt)
                if fnlwgt <= fnlwgt_min:
                    fnlwgt_min = fnlwgt
                if fnlwgt >= fnlwgt_max:
                    fnlwgt_max = fnlwgt
                fnlwgt_sum += fnlwgt

            capital_gain = temp[10]
            if capital_gain == '?':
                capital_gain = 0
            else:
                capital_gain = int(capital_gain)
                if capital_gain <= capital_gain_min:
                    capital_gain_min = capital_gain
                if capital_gain >= capital_gain_max:
                    capital_gain_max = capital_gain
                capital_gain_sum += capital_gain

            capital_loss = temp[11]
            if capital_loss == '?':
                capital_loss = 0
            else:
                capital_loss = int(capital_loss)
                if capital_loss <= capital_loss_min:
                    capital_loss_min = capital_loss
                if capital_loss >= capital_loss_max:
                    capital_loss_max = capital_loss
                capital_loss_sum += capital_loss

            hours_per_week = temp[12]
            if hours_per_week == '?':
                hours_per_week = 0
            else:
                hours_per_week = int(hours_per_week)
                if hours_per_week <= hours_min:
                    hours_min = hours_per_week
                if hours_per_week >= hours_max:
                    hours_max = hours_per_week
                hours_sum += hours_per_week
    print('lines', lines)
    print('age', age_min, age_max, age_sum / lines)
    print('fnlwgt', fnlwgt_min, fnlwgt_max, fnlwgt_sum / lines)
    print('capital_gain', capital_gain_min, capital_gain_max, capital_gain_sum / lines)
    print('capital_loss', capital_loss_min, capital_loss_max, capital_loss_sum / lines)
    print('hours-per-week', hours_min, hours_max, hours_sum / lines)


def preprocessing(datafile, outputfile):
    with open(datafile, 'r') as fin:
        with open(outputfile, 'w') as fout:
            lines = 1
            for eachline in fin:
                temp = eachline.strip('\n').split(', ')
                print(temp)
                age = temp[0]
                if age != '?':
                    age = int(age)
                    if 0 <= age < 10:
                        age = 'age:0~10'
                    elif 10 <= age < 20:
                        age = 'age:10~20'
                    elif 20 <= age < 30:
                        age = 'age:20~30'
                    elif 30 <= age < 40:
                        age = 'age:30~40'
                    elif 40 <= age < 50:
                        age = 'age:40~50'
                    elif 50 <= age < 60:
                        age = 'age:50~60'
                    elif 60 <= age < 70:
                        age = 'age:60~70'
                    elif 70 <= age < 80:
                        age = 'age:70~80'
                    else:
                        age = 'age:80~90'

                workclass = temp[1]
                fnlwgt = temp[2]
                if fnlwgt != '?':
                    fnlwgt = int(fnlwgt)
                    if 0 <= fnlwgt < 100000:
                        fnlwgt = 'wgt:0~100k'
                    elif 100000 <= fnlwgt < 200000:
                        fnlwgt = 'wgt:100k~200k'
                    elif 200000 <= fnlwgt < 300000:
                        fnlwgt = 'wgt:200k~300k'
                    elif 300000 <= fnlwgt < 400000:
                        fnlwgt = 'wgt:300k~400k'
                    elif 400000 <= fnlwgt < 500000:
                        fnlwgt = 'wgt:400k~500k'
                    elif 500000 <= fnlwgt < 600000:
                        fnlwgt = 'wgt:500k~600k'
                    elif 600000 <= fnlwgt < 700000:
                        fnlwgt = 'wgt:600k~700k'
                    elif 700000 <= fnlwgt < 800000:
                        fnlwgt = 'wgt:700k~800k'
                    elif 800000 <= fnlwgt < 900000:
                        fnlwgt = 'wgt:800k~900k'
                    elif 900000 <= fnlwgt < 1000000:
                        fnlwgt = 'wgt:900k~1M'
                    else:
                        fnlwgt = 'wgt:>=1M'

                education = temp[3]
                education_num = temp[4]
                marital_status = temp[5]
                occupation = temp[6]
                relationship = temp[7]
                race = temp[8]
                sex = temp[9]
                capital_gain = temp[10]
                if capital_gain != '?':
                    capital_gain = int(capital_gain)
                    if 0 <= capital_gain < 5000:
                        capital_gain = 'capital_gain:0~5k'
                    elif 5000 <= capital_gain < 10000:
                        capital_gain = 'capital_gain:5k~10k'
                    elif 10000 <= capital_gain < 15000:
                        capital_gain = 'capital_gain:10k~15k'
                    elif 15000 <= capital_gain < 20000:
                        capital_gain = 'capital_gain:15k~20k'
                    elif 20000 <= capital_gain < 25000:
                        capital_gain = 'capital_gain:20k~25k'
                    elif 25000 <= capital_gain < 30000:
                        capital_gain = 'capital_gain:25k~30k'
                    else:
                        capital_gain = 'capital_gain:>30k'

                capital_loss = temp[11]
                if capital_loss != '?':
                    capital_loss = int(capital_loss)
                    if 0 <= capital_loss < 1000:
                        capital_loss = 'capital_loss:0~1k'
                    elif 1000 <= capital_loss < 2000:
                        capital_loss = 'capital_loss:1k~2k'
                    elif 2000 <= capital_loss < 3000:
                        capital_loss = 'capital_loss:2k~3k'
                    elif 3000 <= capital_loss < 4000:
                        capital_loss = 'capital_loss:3k~4k'
                    else:
                        capital_loss = 'capital_loss:4k~5k'

                hours_per_week = temp[12]
                if hours_per_week != '?':
                    hours_per_week = int(hours_per_week)
                    if 0 <= hours_per_week < 20:
                        hours_per_week = 'hours:0~20'
                    elif 20 <= hours_per_week < 40:
                        hours_per_week = 'hours:20~40'
                    elif 40 <= hours_per_week < 60:
                        hours_per_week = 'hours:40~60'
                    elif 60 <= hours_per_week < 80:
                        hours_per_week = 'hours:60~80'
                    else:
                        hours_per_week = 'hours:80~100'

                native_country = temp[13]
                income = temp[14]

                fout.write('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13} {14} {15}'.format(
                    str(lines), age, workclass, fnlwgt, education, education_num, marital_status, occupation,
                    relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country, income
                ))
                fout.write('\n')
                lines += 1
    print(lines)


preprocessing('adult.txt', 'adult_processed.txt')