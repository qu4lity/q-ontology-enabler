import csv

with open('MaterialQA.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_MaterialQA.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:

                materialQA_id = int(row[0])
                used = 1 if row[1] == "yes" else 0
                material_id =  int(row[2])
                if material_id == 0:
                    continue

                materialQA1 = float(row[6].replace(",","."))
                materialQA2 = float(row[7].replace(",","."))
                materialQA3 = float(row[8].replace(",","."))
                materialQA4 = float(row[9].replace(",","."))
                materialQA5 = float(row[10].replace(",","."))

                import_line = "INSERT INTO MaterialQA (materialQA_id, used, material_id, qa1_drying_performance, qa2_noise, qa3_energy_consumption, qa4_component_failure, qa5_perceived_quality) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7});\n".format(int(line_count), used, material_id, materialQA1, materialQA2, materialQA3, materialQA4, materialQA5)
                print(import_line)
                mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
