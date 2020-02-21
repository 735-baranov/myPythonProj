from keras.preprocessing.text import Tokenizer
import csv
import numpy as np
from os import listdir
from random import sample

def read_file_chars(path, num_of_chars):
    file = open(path, 'r', encoding='utf-8')
    text = file.read(num_of_chars)
    # print(text)
    return text

def write_to_csv(data, l_data):
    with open('data.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        writer.writerow(data)

    with open('labels.csv', 'a', newline='') as csv_file:
        lab_wr = csv.writer(csv_file, delimiter=',')
        lab_wr.writerow(l_data)
        # for line in l_data:
        #     lab_wr.writerow(line)


def test_to_csv(data, l_data):
    with open('test.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        writer.writerow(data)

    with open('testlabels.csv', 'a', newline='') as csv_file:
        lab_wr = csv.writer(csv_file, delimiter=',')
        lab_wr.writerow(l_data)


path_to_names = 'X:\\python_base\\'

num_of_auth = 5
num_of_files = 2
num_of_symb = 3000
procent = 0.25

all_names = listdir(path_to_names)
print(all_names, ' ', len(all_names))

names = sample(all_names, num_of_auth)

alf = ''
for j in range(32, 127):
    alf+=chr(j)
alf+='\t\n'
for i in range(1040, 1104):
    alf+=chr(i)

# TEST_SAMPLE!!!!!!!!!!!!!!!!!
sampl = int(num_of_files*num_of_auth*procent)
# count = 0
num_of_index = sample(range(0, num_of_files*num_of_auth), sampl)

# for i in range(0, num_of_files*len(names)):
#     if count!=sampl:
#         num_of_index.append(random.randint(1, num_of_files*len(names))+1)
#         count+=1
#     else:
#         break
print(num_of_index)
# #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
t_d = Tokenizer(num_words=len(alf),
              filters='',
              lower = 'True',
              split='',
              char_level='True')
# # #
t_d.fit_on_texts(alf)

t_l = Tokenizer()
t_l.fit_on_texts(names)

l_list = t_l.texts_to_matrix(names)

temp_count = 0
for i in range(0, len(names)):
    temp_name = names[i]
    temp_path = path_to_names+temp_name
    temp_files = listdir(temp_path)

    print(temp_name)

    for j in range(0, num_of_files):
        try:
            temp_count+=1
            temp_text = read_file_chars(temp_path+'\\'+temp_files[j], num_of_symb)

            list = t_d.texts_to_matrix(temp_text)
            temp = np.asarray(list, dtype=int)

            vect = ''
            for x in temp:
                vect+=''.join(map(str, x))

            l_temp = np.asarray(l_list[i], dtype=int)

            # !!!!!!!
            if any(temp_count==k for k in num_of_index):
                print(temp_count, ' ', end='')
                test_to_csv(vect, l_temp)
            else:
                write_to_csv(vect, l_temp)
        except:
            continue


