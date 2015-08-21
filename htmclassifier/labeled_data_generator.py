label_dataset_file = open('training_data.csv', 'wb')
med_data_file = open('training_set_meditation.csv', 'rb')
normal_data_file = open('training_set_normal.csv', 'rb')
test_data_file = open('test_set.csv', 'rb')

import csv

csv_writer = csv.writer(label_dataset_file)
headers = ['metric', 'label']
csv_writer.writerow(headers)

csv_writer.writerow(['float','int'])
csv_writer.writerow([None,'C'])

  
csv_reader = csv.reader(normal_data_file)
csv_reader.next()
label = 0
count = 0
for row in csv_reader:
  csv_writer.writerow([row[1], label])
  count +=1

csv_reader = csv.reader(med_data_file)
csv_reader.next()
label = 1
count = 0
for row in csv_reader:
  csv_writer.writerow([row[1], label])
  count +=1
  

  
csv_reader = csv.reader(test_data_file)
csv_reader.next()
csv_reader.next()
csv_reader.next()
label = 1
count = 0
for row in csv_reader:
  csv_writer.writerow([row[0], label])
  count +=1
  
label_dataset_file.close()