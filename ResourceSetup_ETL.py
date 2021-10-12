import csv

with open('ResourceSetup.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_ResourceSetup.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:

                resourceSetup_id = int(row[0])
                description = row[1]
                if not description :
                    description = "NULL"

                import_line = "INSERT INTO ResourceSetup (resourceSetup_id, description) VALUES ({0}, \"{1}\");\n".format(resourceSetup_id, description)
                print(import_line)
                mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
