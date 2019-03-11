import matplotlib.pyplot as plt
import csv
from pprint import pprint

questions = []
accept = []
accept_min = []
accept_maj = []
rej = []
total = []
with open('Accept_Reject.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        questions.append(row[0].replace("Ins_Question_","").replace("-",""))
        accept.append(int(row[1]))
        accept_min.append(int(row[2]))
        accept_maj.append(int(row[3]))
        rej.append(int(row[4]))
        total.append(int(row[1]) + int(row[2]) + int(row[3])+ int(row[4]))
for i in range(len(accept)):
    accept[i] = max(float(accept[i])/float(total[i]), 0)
    accept_min[i] = max(float(accept_min[i])/float(total[i]), 0)
    accept_maj[i] = max(float(accept_maj[i])/float(total[i]), 0)
    rej[i] = max(float(rej[i])/float(total[i]), 0)
    print(accept[i], total[i], rej[i] , accept_maj[i], accept_min[i])



plt.bar(questions, accept, color='g')
plt.bar(questions, accept_min, color='y', bottom=accept)
plt.bar(questions, accept_maj, color='c', bottom=[accept[j] +accept_min[j] for j in range(len(accept))])
plt.bar(questions, rej, color='r', bottom=[accept[j] +accept_min[j] +accept_maj[j] for j in range(len(accept))])
plt.xlabel('Question Status')
plt.ylabel('Percentage')
plt.savefig('bar.png', dpi=400)

