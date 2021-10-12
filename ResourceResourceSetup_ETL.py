import csv

with open('ResourceResourceSetup.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_ResourceResourceSetup.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:

                resource_id = int(row[0])
                resource_description = row[1]
                if not resource_description :
                    resource_description = "NULL"
                    import_line = "INSERT INTO Resource (resource_id, description, resourceType_id) VALUES ({0}, {1}, {2});\n".format(resource_id, resource_description, "NULL")
                else:
                    import_line = "INSERT INTO Resource (resource_id, description, resourceType_id) VALUES ({0}, \"{1}\", {2});\n".format(resource_id, resource_description, "NULL")

                print(import_line)
                mmi.write(import_line)

                for i in range(0,20,2):
                    resourceSetup_id = int(row[i+2])
                    resourceSetup_description = row[i+1+2]
                    import_line = "INSERT INTO ResourceSetup (resourceSetup_id, description) VALUES ({0}, \"{1}\");\n".format(resourceSetup_id,resourceSetup_description)
                    print(import_line)
                    mmi.write(import_line)

                    import_line = "INSERT INTO Resource_ResourceSetup (resource_id, resourceSetup_id) VALUES ({0}, {1});\n".format(resource_id,resourceSetup_id)
                    print(import_line)
                    mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
