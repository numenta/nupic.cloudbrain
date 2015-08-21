import matplotlib.pyplot as plt
import csv

plt.figure()

med = []
count = 0
with open('test_set.csv', 'rb') as f:
  csv_reader = csv.reader(f)
  headers = csv_reader.next()
  csv_reader.next()
  csv_reader.next()
  
  
  for line in csv_reader:
    if 4400 < count < 5000:
      med.append(line[0])
    count +=1

'''
normal = []
with open('training_set_normal.csv', 'rb') as f:
  csv_reader = csv.reader(f)
  headers = csv_reader.next()
  
  for line in csv_reader:
    normal.append(line[1])

'''    

print med
t1 = xrange(len(med))
plt.ylim([0,1])
plt.plot(t1,med)

#t2 = xrange(len(normal))
#plt.plot(t2, normal)
plt.show()
