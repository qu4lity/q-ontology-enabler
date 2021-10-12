import csv

with open('ProductLineStation.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_ProductionLineStation.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                line_count += 1

            else:
                productionName = row[0].strip()
                productionDescription = row[1].strip()

                productionNote = "NULL"
                if row[3]:
                    productionNote = "a) {0}".format(row[3].strip())
                    if row[4]:
                        productionNote += ", b) {0}".format(row[4].strip())
                        if row[5]:
                            productionNote += ", c) {0}".format(row[5].strip())
                            if row[6]:
                                productionNote += ", d) {0}".format(row[6].strip())
                                if row[7]:
                                    productionNote += ", e) {0}".format(row[7].strip())

                station_id = row[8]
                if not station_id or station_id == "0":
                    continue

                description = row[9].strip()
                if not description or description == "0":
                    continue

                note = row[10].replace("\n", ",").strip()

                import_line = "INSERT INTO ProductionLine (name, description, note) VALUES (\"{0}\", \"{1}\", \"{2}\");\n".format(productionName, productionDescription, productionNote)
                print(import_line)
                mmi.write(import_line)

                import_line = "INSERT INTO Station (station_id, description, note) VALUES ({0}, \"{1}\", \"{2}\");\n".format(station_id, description, note)
                print(import_line)
                mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
