import sys
import csv
# todo: throw error if more than 2 and less than 2 input and print order of commands
# check to make sure "g" is provided

def float_to_fixed(n, convertType):
    if convertType == "4g":
        return (n + 4) * 512
    else:
        return (n + 4) * 1024 # double check for 2g...

def fixed_to_float(n, convertType):
    if convertType == "4g":
        return (n - 2048) / 512
    else:
        return (n - 2048) / 1024

# Open CSV file and parse it
with open(sys.argv[1]) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    original = []
    # array of converted fixed points
    converted_fixed = [] 
    # array of floating points that are converted from converted_fixed to check diff from original was 0
    reconverted_floating = [] 

    for i, row in enumerate(readCSV):
        if i > 0: #skip first row with letters
            convertType = int(sys.argv[2][0])
            for floating_point in row:
                if (-1 * convertType) < float(floating_point) < convertType:
                    original.append(float(floating_point))

                    converted = float_to_fixed(float(floating_point), sys.argv[2])
                    converted_fixed.append(int(converted))
                else:
                    error = str(floating_point) + "is not in the range of " + "+/- " + sys.argv[2][0]
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
                temp.append(converted_fixed[i + 2])
                temp.append(fixed_point)
                temp.append(converted_fixed[i + 1])
                rows.append(temp)
                
        # write the output file
        filename = sys.argv[1] + "_FixedConverted"
        with open(filename, 'w') as csvfile:  
            csvwriter = csv.writer(csvfile)  
            csvwriter.writerow(fields)  
            csvwriter.writerows(rows) 
        

print(converted_fixed)
