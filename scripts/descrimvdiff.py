import csv
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

with open('submissions.csv', 'r') as csv_file:
   csv_reader = csv.reader(csv_file, delimiter=',')
   all_responses = []
   count = 0
   for row in csv_reader:
      if (count == 0):
         keys = row
         count += 1
         continue
      j = 0
      values = dict()
      for i in keys:
         values[i] = row[j]
         j += 1
      count += 1
      all_responses.append(values)
user_performance = dict()
for i in all_responses:
    response = json.loads(i['Submitted answer'])
    correct = json.loads(i['True answer'])
    opt = json.loads(i['Params'])
    answ_correct = False
    if ('answ' in correct and 'answ' in response):
        if (correct['answ']['key'] == response['answ']):
            answ_correct = True
    if (i['UID'] in user_performance):
        user_performance[i['UID']][i['Question']] = answ_correct
    else:
        user_performance[i['UID']] = dict()

del user_performance['pahp@d.umn.edu']
del user_performance['simsong@gmail.com']
del user_performance['joeroundy@gmail.com']
del user_performance['profachattop@gmail.com']
question_score = dict()
for key,value in user_performance.items():
    correct = 0
    total = 0
    for key1, value1 in value.items():
        if (key1 not in question_score):
            question_score[key1] = [0, 0]
        if (value1):
            correct += 1
            question_score[key1][0] += 1
        question_score[key1][1] += 1
        total += 1
    if (total != 0):
        user_performance[key]["Mean"] = float(correct)/float(total)
    else:
        user_performance[key]["Mean"] = 0

ranked_users = []
for key,value in user_performance.items():
    ranked_users.append((key, value['Mean']))
ranked_users = sorted(ranked_users, key=lambda tup: tup[1])
twnty_sev = int(round(.27*len(ranked_users), 0))
for key, value in question_score.items():
    lower = 0
    higher = 0
    for i in range(twnty_sev):
        try:
            if (user_performance[ranked_users[i][0]][key]):
                lower += 1
        except:
            pass
        try:
            if (user_performance[ranked_users[len(ranked_users) - 1 - i][0]][key]):
                higher += 1
        except:
            pass
            
    question_score[key].append((float(higher)/float(twnty_sev)) - (float(lower)/float(twnty_sev)))
    
questions = []
scores = []
descrimination = []
for key,value in question_score.items():
    question_score['overall'] = float(value[0])/float(value[1])
    question_score['descrimination'] = value[2]
    questions.append(key.replace("Ins_Question_", ""))
    scores.append(question_score['overall'])
    descrimination.append(question_score['descrimination'])
    

plt.scatter(scores, descrimination ,color='k')
plt.axvline(x=.2,linestyle=':',color='k')
plt.axvline(x=.9,linestyle=':',color='k')
plt.axhline(y=.2,linestyle=':',color='k')
for i, txt in enumerate(questions):
    plt.annotate(txt, (scores[i], descrimination[i]))
plt.xlabel('Item Difficulty')
plt.ylabel('Item Descrimination')
plt.xticks([0,.2,.4,.6,.8,1])
plt.yticks([0,.2,.4,.6,.8,1])
plt.savefig('graph.png')
exit(1)
                
pprint(question_score)
pprint(user_performance)
exit(1)
question_values = dict()
#pprint(all_responses[0])
for i in all_responses:
   if (i['Question'] not in question_values):
      question_values[i['Question']] = [0,0,0,0,0,0,[]] #accept, accept minor, accept major, reject, correct, incorrect, comments
   response = json.loads(i['Submitted answer'])
   correct = json.loads(i['True answer'])
   opt = json.loads(i['Params'])
   #print(i['Question'])
   #print(correct)
   answ_correct = False
   user_response = ""
   if ('answ' in correct and 'answ' in response):
      if (correct['answ']['key'] == response['answ']):
         answ_correct = True
      for l in opt['answ']:
         if (l['key'] == response['answ']):
            user_response = l['html'].replace("\n", "").replace(","," ")
   if (answ_correct):
      question_values[i['Question']][4] += 1
   else:
      question_values[i['Question']][5] += 1
   if ('accept' not in response):
      question_values[i['Question']][0] += 1
      continue
   if (response['accept'] == 'accept'):
      question_values[i['Question']][0] += 1
   elif (response['accept'] == 'acceptminor'):
      question_values[i['Question']][1] += 1
   elif (response['accept'] == 'reject'):
      question_values[i['Question']][3] += 1
   elif (response['accept'] == 'acceptmajor'):
      question_values[i['Question']][2] += 1
   else:
      print(response)
   if (user_response):
      question_values[i['Question']][6].append(user_response)
with open('output.csv', 'w') as output_file:
   for key, values in question_values.items():
      unique_response = dict()
      for i in values[6]:
         if (i in unique_response):
            unique_response[i] += 1
         else:
            unique_response[i] = 1
      output_string = ""
      for key1, value1 in unique_response.items():
         output_string += key1 + "," + str(value1) + ","
      output_file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}\n".format(key, values[0], values[1], values[2], values[3], float(values[4])/ float(values[4]+values[5]), output_string))      
