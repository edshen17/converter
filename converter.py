import sys
import csv
# todo: throw error if more than 2 and less than 2 input and print order of commands
# check to make sure "g" is provided

def float_to_fixed(n, convertType):
    if convertType == "4g":
        return (n + 4) * 512
    else:
        return (n + 2) * 1024

def fixed_to_float(n, convertType):
    if convertType == "4g":
        return (n - 2048) / 512
    else:
        return (n - 2048) / 1024

# command line input check
if len(sys.argv) > 3 or len(sys.argv) < 3:
    print("Make sure you input the correct number of arguments. Example: python converter.py input.csv 4g")
    exit()
if not(".csv" in sys.argv[1]):
    print("Input file must be a .csv format! Erroneous input: " + sys.argv[1])
    exit()
if not(sys.argv[2] == "2g" or sys.argv[2] == "4g"):
    print("Make sure the second argument of the script is 2g or 4g. Erroneous input: " + sys.argv[2])
    exit()

# Open CSV file and parse it
with open(sys.argv[1]) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    # array of original floating points from given csv
    original = []

    # array of converted fixed points
    converted_fixed = [] 

    # array of floating points that are converted from converted_fixed to check diff from original was 0
    reconverted_floating = [] 

    for i, row in enumerate(readCSV):
        if i > 0: #skip first row with letters av, al, af
            convertType = int(sys.argv[2][0]) # 2 or 4
            for floating_point in row:
                if (-1 * convertType) <= float(floating_point) < convertType:
                    original.append(float(floating_point))
                    converted = float_to_fixed(float(floating_point), sys.argv[2])
                    converted_fixed.append(int(converted))
                else:
                    error = str(floating_point) + "is not in the range of " + "+/- " + sys.argv[2]
                    print(error)
                    break

    # convert all the floating points to fixed
    for fixed_point in converted_fixed:
        reconverted = fixed_to_float(fixed_point, sys.argv[2])
        reconverted_floating.append(reconverted)


    # if converted numbers are equal to original float values, output the final cvs file
    if reconverted_floating == original:
        fields = ["af", "av", "al"]
        rows = []
        for i, fixed_point in enumerate(converted_fixed):
            if i % 3 == 0:
                temp = []
                temp.append(converted_fixed[i + 2]) # af
                temp.append(fixed_point) # av
                temp.append(converted_fixed[i + 1]) # al
                rows.append(temp)
                
        # write the output file
        filename = sys.argv[1].split('.')[0] + "_FixedConverted.csv"
        with open(filename, 'w', newline='') as csvfile:  
            csvwriter = csv.writer(csvfile)  
            csvwriter.writerow(fields)  
            csvwriter.writerows(rows) 
        print("File written to " + filename)
    else:
        print("Reconverted values do not match original float values. Below is the difference:")
        listDiff = list(set(original) - set(reconverted_floating))
        print(listDiff)