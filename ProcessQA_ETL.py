import csv

with open('ProcessQA.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_ProcessQA.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:

                processQA_id = int(row[0])
                used = 1 if row[1] == "yes" else 0
                process_id =  int(row[2])
                if process_id == 0:
                    continue

                processQA1 = float(row[4].replace(",",".").replace("N","0.0"))
                processQA2 = float(row[5].replace(",",".").replace("N","0.0"))
                processQA3 = float(row[6].replace(",",".").replace("N","0.0"))
                processQA4 = float(row[7].replace(",",".").replace("N","0.0"))
                processQA5 = float(row[8].replace(",",".").replace("N","0.0"))

                import_line = "INSERT INTO ProcessQA (processQA_id, used, process_id, qa1_drying_performance, qa2_noise, qa3_energy_consumption, qa4_component_failure, qa5_perceived_quality) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7});\n".format(int(line_count), used, process_id, processQA1, processQA2, processQA3, processQA4, processQA5)
                print(import_line)
                mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
