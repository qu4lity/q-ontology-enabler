import csv

with open('Process_ProcessFailure.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_ProcessFailure.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:
                process_id = int(row[0])

                for x in range(5):
                    processFailure_id = int(row[2+(2*x)])
                    processFailure_description = row[3+(2*x)]

                    if x == 3:
                        processFailure_id = processFailure_id+1

                    import_line = "INSERT INTO ProcessFailure (processFailure_id, description, occuranceDate, failureType_id) VALUES ({0}, \"{1}\", {2}, {3});\n".format(processFailure_id, processFailure_description, "NULL", "NULL")
                    print(import_line)
                    mmi.write(import_line)

                    import_line = "INSERT INTO Process_ProcessFailure (process_id, processFailure_id) VALUES ({0}, {1});\n".format(process_id, processFailure_id)
                    print(import_line)
                    mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
