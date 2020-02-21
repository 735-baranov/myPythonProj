import csv


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