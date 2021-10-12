import csv

with open('Process.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_Process.sql", "a") as mmi:
        function_ids = set()

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:

                if(row[0] in function_ids):
                    line_count+=1
                    continue

                process_id = int(row[0])
                description = row[1]

                import_line = "INSERT INTO Process (process_id, location_id, state_id, operation_id, resource_id, processType_id, duration, description) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, \"{7}\");\n".format(process_id, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", description)
                print(import_line)
                mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
