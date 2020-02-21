import os
import make_bigrams
import Write_CSV
import random

def make_dataset(autors, files, symbols):
    # parameters
    path_to_autors = 'uploads/classes/'
    path_to_predict = 'uploads/test_file/'

    # how many sybols 2 - bigrams
    hms = 1
    ishod_alf = make_bigrams.make_alf(hms)
    # print(ishod_alf)

    num_of_auth = int(autors)
    num_of_files = int(files)
    num_of_symb = int(symbols)

    test_files = os.listdir(path_to_predict)

    for i in range(0, len(test_files)):
        test_file = path_to_predict+test_files[i]

        print('file - ', test_file)
        try:
            ngrams = make_bigrams.ngrams_from_file(test_file, num_of_symb, hms)
            # l_temp = make_bigrams.label_vec(1, 1)

            for z in range(0, len(ngrams)):
                try:
                    # print(bigrams[i])
                    vect = make_bigrams.make_nul_vec(len(ishod_alf))
                    x = ishod_alf.index(ngrams[z])
                    vect = make_bigrams.one_hot_vec(vect, x)

                    res = ''.join(str(e) for e in vect)

                    Write_CSV.test_to_csv(res, str(i))

                except Exception as m:
                    print(m)
                    continue

        except Exception as msg:
            print(msg[2])



    # paths_to_files = []
    d_names = os.listdir(path_to_autors)
    #
    # for dirpath, dnames, fnames in os.walk(path_to_autors):
    #     for f in fnames:
    #         paths_to_files.append(os.path.join(dirpath, f))
    #
    # print(d_names)
    # print(paths_to_files)



    names = random.sample(d_names, num_of_auth)

    temp_count = 0
    for i in range(0, len(names)):
        temp_name = names[i]
        temp_path = path_to_autors + temp_name
        temp_files = os.listdir(temp_path)

        print(temp_name)

        for j in range(0, num_of_files):
            try:
                print('file - ', temp_files[j])
                ngrams = make_bigrams.ngrams_from_file(temp_path + '/' + temp_files[j], num_of_symb, hms)
                l_temp = make_bigrams.label_vec(len(names), i)

                for z in range(0, len(ngrams)):
                    try:
                        # print(bigrams[i])
                        vect = make_bigrams.make_nul_vec(len(ishod_alf))
                        x = ishod_alf.index(ngrams[z])
                        vect = make_bigrams.one_hot_vec(vect, x)

                        res = ''.join(str(e) for e in vect)

                        Write_CSV.write_to_csv(res, l_temp)

                    except Exception as m:
                        print(m)
                        continue

            except Exception as msg:
                print('min files')
                continue

            temp_count += 1

    return names, test_files
