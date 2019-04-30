import json
import csv

# def main():

def do_something_with(line):
  line1 = line.lstrip("[")
  x = line1.replace("]", "")
  y = json.loads(x)
  print(y)

def ProcessLargeTextFile():
  with open("test2.json") as infile:
    for line in infile:
      do_something_with(line)

  
  # some JSON:
  # x =  '{ "name":"John", "age":30, "city":"New York"}'

  # parse x:
  # y = json.loads(x)

  # the result is a Python dictionary:
  # print(y["age"])

  # data_parsed = json.loads(Data)

  # header = data_parsed[0].keys()
  # csv_writer.writerow(header)
  #
  # for i in range(0,length_data)
  #     meetup = data_parsed[i].values()
  #     csv_writer.writerow([meetup])

if __name__ == "__main__":
    ProcessLargeTextFile()
