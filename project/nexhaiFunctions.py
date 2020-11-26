def security_id_check(string):
  
  string = str(string).replace(' ', '')
  control1 = '376189452'
  control2 = '5432765432'
  k1 = 0

  if (int(string[0]) < 0 or int(string[0]) > 3):
    test = False

  elif len(string) !=11:
    test = False
  else:
    for i in range(len(control1)):
      k1 += int(string[i])*int(control1[i])
    k1 = (11-k1)%11
    
    k2 = 0
    for i in range(len(control2)):
      k2 += int(string[i])*int(control2[i])
    k2 = (11-k2)%11
      
    if ((k1 != int(string[9])) or (k2 != int(string[10])) or (k1 > 9) or (k2 > 9)):
      test = False
    else:
      test = True
  return test


'''
def acc_num_gen(m=1000):
  from random import sample
   
  value_array = sample(range(100000, 999999),m)

  affiliation = '3141' # identifies the bank
  control = '2345672345'
  k1 = 0
  numbers=[]
  for n in range(len(value_array)): 
    for i in range(len(control)):
      bank_number = affiliation + str(value_array[n])
      k1 += int(control[i])*int(bank_number[i])
    bank_number += str(k1)
    numbers.append(bank_number)
  return numbers

'''