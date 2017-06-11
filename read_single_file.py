
import csv
import os
import glob
import read_letters_csv as rc

def main():
  cwd = os.getcwd()
  dirs = os.listdir(cwd)
  dir =cwd + '/sample-txt'
  files = glob.glob(dir + '/*.txt')

  outfile = open('sample.csv', 'w')
  str = "\"class\",\"f1\",\"f2\",\"f3\",\"f4\",\"f5\",\"f6\",\"f7\",\"f8\",\"f9\",\"f10\",\"f11\"," \
        "\"f12\",\"f13\""
  outfile.write(str + '\n')  # write table head
  i = 1
  for f in files:
    infile = open(f, 'r')
    outfile.write('\"shape ')
    outfile.write('%d' % i)
    outfile.write('\",')
    i += 1
    pre_content0 = ''
    pre_content1 = ''
    pre_last = ''
    all_data = []
    for line in infile:
      list = []
      content = line.split(', ')
      assert len(content) == 3
      last = content[2].strip().split(';')  # remove '\n'
      assert content[0].isdigit()
      assert content[1].isdigit()
      assert last[0].isdigit()
      if pre_content0 == content[0] and pre_content1 == content[1]:
        continue  # skip same position point, while keep the first one
      if pre_last == last[0]:
        continue  # skip the second same time data, while keep the first one

      list.append(content[0])
      list.append(content[1])
      list.append(last[0])
      pre_content0 = content[0]
      pre_content1 = content[1]
      pre_last = last[0]
      all_data.append(list)


    list12 = []
    rc.getF1F2(all_data, list12)
    list9 = []
    rc.getF91011(all_data, list9)

    res = [list12[0], list12[1], rc.getF3(all_data), rc.getF4(all_data),
           rc.getF5(all_data), rc.getF6(all_data), rc.getF7(all_data), rc.getF8(all_data), list9[0], list9[1],
           list9[2], rc.getF12(all_data), rc.getF13(all_data)]

    writer = csv.writer(outfile)
    writer.writerow(res)



