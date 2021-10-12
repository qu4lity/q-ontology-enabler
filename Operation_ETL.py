import csv

with open('Operation.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_Operation.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:

                operation_id = int(row[0])
                description = row[1]


                import_line = "INSERT INTO Operation (operation_id, description, note, materialUsedAsCarrier_id, materialUsedAsTarget_id, materialTransformation_id) VALUES ({0}, \"{1}\", {2}, {3}, {4}, {5});\n".format(operation_id, description, "NULL",  "NULL",  "NULL",  "NULL")
                print(import_line)
                mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
