import csv

with open('Function_MeasureType.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_Function_MeasureType.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:

                function_id = int(row[0])


                for index in range(0, 54, 2):
                    measureType = row[index+8]
                    if measureType == "NULL" or measureType == "" or measureType == " ":
                        continue
                    import_line = "INSERT INTO Function_MeasureType (function_id, measureType) VALUES ({0}, \"{1}\");\n".format(function_id, measureType)
                    print(import_line)
                    mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
