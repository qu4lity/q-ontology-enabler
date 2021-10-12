import csv

with open('Material_MeasureType.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_Material_MeasureType.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:

                material_id = int(row[0])


                for index in range(0, 50, 2):
                    measureType = row[index+4]
                    if measureType == "NULL" or measureType == "" or measureType == " ":
                        continue
                    import_line = "INSERT INTO Material_MeasureType (material_id, measureType) VALUES ({0}, \"{1}\");\n".format(material_id, measureType)
                    print(import_line)
                    mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
