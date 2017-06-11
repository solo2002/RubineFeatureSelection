import math
import csv
import os
import glob

# cosine and sine of start angle of stroke
def getF1F2(all_data, list):
  x0 = float(all_data[0][0])
  y0 = float(all_data[0][1])
  i = 2  # to avoid ZeroDivisionError
  x2 = float(all_data[i][0])
  y2 = float(all_data[i][1])
  val_for_cos = (y2 - y0) * (y2 - y0) + (x2 - x0) * (x2 - x0)
  val_for_sin = (y2 - y0) * (y2 - y0) + (x2 - x0) * (x2 - x0)
  while (i < len(all_data) and (val_for_cos == 0 or val_for_sin == 0)): # if there is one division by zero, get the next point
    i += 1
    x2 = float(all_data[i][0])
    y2 = float(all_data[i][1])
    val_for_cos = (y2 - y0) * (y2 - y0) + (x2 - x0) * (x2 - x0)
    val_for_sin = (y2 - y0) * (y2 - y0) + (x2 - x0) * (x2 - x0)
  cos_val = round((x2 - x0) / math.sqrt(val_for_cos), 5)
  sin_val = round((y2 - y0) / math.sqrt(val_for_sin), 5)
  list.append(cos_val)
  list.append(sin_val)

# cosine of start angle of stroke
def getF1(all_data):
  x0 = float(all_data[0][0])
  y0 = float(all_data[0][1])
  x2 = float(all_data[2][0])
  y2 = float(all_data[2][1])
  return round((x2 - x0) / (math.sqrt((y2 - y0) * (y2 - y0) + (x2 - x0) * (x2 - x0))), 5)

# sine of start angle of stroke
def getF2(all_data):
  x0 = float(all_data[0][0])
  y0 = float(all_data[0][1])
  i = 2 # to avoid ZeroDivisionError
  x2 = float(all_data[i][0])
  y2 = float(all_data[i][1])
  val = (y2 - y0) * (y2 - y0) + (x2 - x0) * (x2 - x0)
  while val == 0: # if val == 0, get the next point
    i += 1
    x2 = float(all_data[i][0])
    y2 = float(all_data[i][1])
    val = (y2 - y0) * (y2 - y0) + (x2 - x0) * (x2 - x0)

  return round((y2 - y0) / (math.sqrt(val)), 5)

# the length of diagonal of bounding box of the strike
def getF3(all_data):
  xmin = float(all_data[0][0])
  xmax = float(all_data[0][0])
  ymin = float(all_data[0][1])
  ymax = float(all_data[0][1])

  for list in all_data:
    if float(list[0]) < xmin:
        xmin = float(list[0])
    if float(list[0]) > xmax:
        xmax = float(list[0])
    if float(list[1]) < ymin:
        ymin = float(list[1])
    if float(list[1]) > ymax:
        ymax = float(list[1])

  val = math.sqrt((ymax - ymin) * (ymax - ymin) + (xmax - xmin) * (xmax - xmin))
  return round(val, 5)

# the angle of diagnoal and bounding box
def getF4(all_data):
  xmin = float(all_data[0][0])
  xmax = float(all_data[0][0])
  ymin = float(all_data[0][1])
  ymax = float(all_data[0][1])

  for list in all_data:
    if float(list[0]) < xmin:
      xmin = float(list[0])
    if float(list[0]) > xmax:
      xmax = float(list[0])
    if float(list[1]) < ymin:
      ymin = float(list[1])
    if float(list[1]) > ymax:
      ymax = float(list[1])
  if xmax - xmin == 0: # to avoid ZeroDivisionError, it is a vertical line
    return 3.1415/2
  val = math.atan((ymax - ymin) / (xmax - xmin))
  return round(val, 5)

# the distance between first point and last point
def getF5(all_data):
  x0 = float(all_data[0][0])
  y0 = float(all_data[0][1])
  xlast = float(all_data[len(all_data) - 1][0])
  ylast = float(all_data[len(all_data) - 1][1])
  val = math.sqrt((ylast - y0) * (ylast - y0) + (xlast - x0) * (xlast - x0))
  return round(val, 5)

# cosine of the angle from start to endpoint
def getF6(all_data):
  x0 = float(all_data[0][0])
  xlast = float(all_data[len(all_data) - 1][0])
  val = (xlast - x0) / getF5(all_data)
  return round(val, 5)

# sine of the angle from start to endpoint
def getF7(all_data):
  y0 = float(all_data[0][1])
  ylast = float(all_data[len(all_data) - 1][1])
  val = (ylast - y0) / getF5(all_data)
  return round(val, 5)

# stroke length
def getF8(all_data):
  sum = 0
  prex = float(all_data[0][0])
  prey = float(all_data[0][1])
  for list in all_data:
    sum += math.sqrt((float(list[0]) - prex) * (float(list[0]) - prex) + (float(list[1]) - prey) * (float(list[1]) - prey))
    prex = float(list[0])
    prey = float(list[1])
  return round(sum, 5)

# relative rotation, aboslute rotation, and sharpness
def getF91011(all_data, list):
  prex = float(all_data[0][0])
  prey = float(all_data[0][1])
  sum1 = 0
  sum2 = 0
  sum3 = 0
  for i in range(1, len(all_data) - 2):
    curx = float(all_data[i][0])
    cury = float(all_data[i][1])
    dx1 = curx - prex
    dy1 = cury - prey
    dx2 = float(all_data[i + 1][0]) - curx
    dy2 = float(all_data[i + 1][1]) - cury
    prex = curx
    prey = cury
    if dx2 * dx1 + dy2 * dy1 == 0:  # to avoid ZeroDivisionError
      continue
    val = (dx2 * dy1 - dx1 * dy2) / (dx2 * dx1 + dy2 * dy1)
    sum1 += math.atan(val)
    sum2 += abs(math.atan(val))
    sum3 += math.atan(val) * math.atan(val)
  list.append(round(sum1, 5))
  list.append(round(sum2, 5))
  list.append(round(sum3, 5))

# max speed
def getF12(all_data):
  pret = float(all_data[0][2])
  prex = float(all_data[0][0])
  prey = float(all_data[0][1])
  max = 0
  for i in range(1, len(all_data) - 1):
    dx = float(all_data[i + 1][0]) - prex
    dy = float(all_data[i + 1][1]) - prey
    dt = float(all_data[i + 1][2]) - pret
    val = (dx * dx + dy * dy) / (dt * dt)
    if (max < val):
      max = val
    pret = float(all_data[i + 1][2])
    prex = float(all_data[i + 1][0])
    prey = float(all_data[i + 1][1])
  return round(max, 5)

# the length of time
def getF13(all_data):
  t0 = float(all_data[0][2])
  tlast = float(all_data[len(all_data) - 1][2])
  return tlast - t0

def main():
  directory = "letters-txt"
  outfile = open('letters.csv', 'w')
  sub = [x[0] for x in os.walk(directory)]
  sorted(sub)
  # sub = ['letters-txt', 'letters-txt/a', 'letters-txt/b', 'letters-txt/c', 'letters-txt/d', 'letters-txt/e', 'letters-txt/f',
  # 'letters-txt/g', 'letters-txt/h', 'letters-txt/i', 'letters-txt/j', 'letters-txt/k', 'letters-txt/l', 'letters-txt/m',
  #'letters-txt/n', 'letters-txt/o', 'letters-txt/p', 'letters-txt/q', 'letters-txt/r', 'letters-txt/s', 'letters-txt/t',
  #'letters-txt/u', 'letters-txt/v', 'letters-txt/w', 'letters-txt/x', 'letters-txt/y', 'letters-txt/z']

  cwd = os.getcwd()
  dirs = os.listdir(cwd)
  str = "\"class\",\"f1\",\"f2\",\"f3\",\"f4\",\"f5\",\"f6\",\"f7\",\"f8\",\"f9\",\"f10\",\"f11\"," \
        "\"f12\",\"f13\""
  outfile.write(str + '\n') # write table head

  for i in range(1, len(sub)):
    dir = glob.glob(cwd + '/' + sub[i])
    for subdir in dir: # for each letter sub-directory, i.e. /a
      files = glob.glob(subdir + '/*.txt')
      for file in files: # i. e., a_1.txt
        print "Now processing ", file
        outfile.write("\"" + sub[i][12] + "\",")
        infile = open(file, 'r')

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

        list9 = [] # to save feature 9, 10, 11
        getF91011(all_data, list9)
        list12 = [] # to save feature 1, 2
        getF1F2(all_data, list12)
        res = [list12[0], list12[1], getF3(all_data),getF4(all_data),
                      getF5(all_data), getF6(all_data), getF7(all_data), getF8(all_data), list9[0], list9[1],
                      list9[2], getF12(all_data), getF13(all_data)]

        writer = csv.writer(outfile)
        writer.writerow(res)

####################### main #########################
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print "[FATAL] " + str(e)
        raise