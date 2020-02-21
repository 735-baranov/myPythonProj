import sqlite3
import make_bigrams
import Write_CSV
from random import sample

def get_feedbacks(n):# n - сколько вытащить с базы
    conn = sqlite3.connect("DataSet.db")
    cursor = conn.cursor()
    d = {}
    for i in range(1, n + 1):
        cursor.execute("SELECT feedback, score FROM DataSet WHERE id = " + str(i))
        res = cursor.fetchone()
        feedback = res[0]
        score = res[1]
        if i == 1:
            d = dict.fromkeys([feedback], score)
        else:
            d.setdefault(feedback, score)

    conn.close()
    return d


def vectorization():
    print('hello')

if __name__ == '__main__':

    ocenki = ['1','2','3','4','5']
    # !!!!!!!!!!!!!!!!!!!!!!!
    num_otz = 10
    # how many symbols(2 - bigrams)
    hms = 1

    # test_part
    procent = 0.0
    sampl = int(num_otz*procent)
    test_index = sample(range(0, num_otz), sampl)
    print(test_index)

    if procent == 0.0 or sampl==0:
        Write_CSV.test_to_csv('', '')


    ishod_alf = make_bigrams.make_alf(hms)

    print(len(ishod_alf))

    dict_otz = get_feedbacks(num_otz)


    temp_count = 0
    for key, value in dict_otz.items():
        try:
            ng_list = make_bigrams.ngrams_from_text(key, hms)
            label_list = make_bigrams.label_vec(len(ocenki), ocenki.index(value))


            res = ''
            for z in range(0, len(ng_list)):
                try:
                    # print(bigrams[i])
                    vect = make_bigrams.make_nul_vec(len(ishod_alf))
                    x = ishod_alf.index(ng_list[z])
                    vect = make_bigrams.one_hot_vec(vect, x)

                    res += ''.join(str(e) for e in vect)

                except Exception as m:
                    print(m)
                    continue

            if any(temp_count == k for k in test_index):
                print(temp_count)
                Write_CSV.test_to_csv(res, label_list)
            else:
                Write_CSV.write_to_csv(res, label_list)

        except:
            continue

        temp_count += 1
