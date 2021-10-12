import csv

with open('Resource.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_Resource.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:

                resource_id = int(row[0])
                description = row[1]
                if not description :
                    description = "NULL"

                import_line = "INSERT INTO Resource (resource_id, description, resourceType_id, resourceSetup_id) VALUES ({0}, \"{1}\", {2}, {3});\n".format(resource_id, description, "NULL", "NULL")
                print(import_line)
                mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
