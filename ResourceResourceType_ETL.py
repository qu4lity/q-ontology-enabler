import csv

with open('ResourceResourceType.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_ResourceResourceType.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                line_count += 1

            else:

                resource_id = row[0]
                resourceType_id = row[2]
                if resourceType_id != 0:
                    import_line = "UPDATE Resource SET resourceType_id={0} WHERE resource_id={1};\n".format(resource_id, resourceType_id)
                    print(import_line)
                    mmi.write(import_line)
                else:
                    continue

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
