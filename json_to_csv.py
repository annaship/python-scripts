import json
import csv

# def main():

def do_something_with(line):
  line1 = line.lstrip("[")
  x = line1.replace("]", "")
  data_parsed = json.loads(x)
  print(data_parsed)
  # w.writelines(bunch)
  header = data_parsed.keys()
  print(header)
  
  # csv_writer.writerow(header)

  # for i in range(0,length_data)
      # meetup = data_parsed[i].values()
      # csv_writer.writerow([meetup])
  

def ProcessLargeTextFile():
  file_in = "test2.json"
  file_out = "test2_out.json"
  with open(file_in) as infile, open(file_out, "w") as out_file:
    for line in infile:
      do_something_with(line)



  # header = data_parsed[0].keys()
  # csv_writer.writerow(header)
  #
  # for i in range(0,length_data)
  #     meetup = data_parsed[i].values()
  #     csv_writer.writerow([meetup])

if __name__ == "__main__":
    ProcessLargeTextFile()
