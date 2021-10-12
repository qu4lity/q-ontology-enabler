import csv

with open('Resource_ResourceFailure.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_ResourceFailure.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:
                resource_id = int(row[0])

                for x in range(5):
                    resourceFailure_id = int(row[2+(2*x)])
                    resourceFailure_description = row[3+(2*x)]

                    import_line = "INSERT INTO ResourceFailure (resourceFailure_id, description, occuranceDate, failureType_id) VALUES ({0}, \"{1}\", {2}, {3});\n".format(resourceFailure_id, resourceFailure_description, "NULL", "NULL")
                    print(import_line)
                    mmi.write(import_line)

                    import_line = "INSERT INTO Resource_ResourceFailure (resource_id, resourceFailure_id) VALUES ({0}, {1});\n".format(resource_id, resourceFailure_id)
                    print(import_line)
                    mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
