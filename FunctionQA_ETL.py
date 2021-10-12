import csv

with open('FunctionQA.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_FunctionQA.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:

                functionQA_id = int(row[0])
                used = 1 if row[1] == "yes" else 0
                function_id =  int(row[2])
                if function_id == 0:
                    continue

                functionQA1 = float(row[9].replace(",","."))
                functionQA2 = float(row[10].replace(",","."))
                functionQA3 = float(row[11].replace(",","."))
                functionQA4 = float(row[12].replace(",","."))
                functionQA5 = float(row[13].replace(",","."))

                import_line = "INSERT INTO FunctionQA (functionQA_id, used, function_id, qa1_drying_performance, qa2_noise, qa3_energy_consumption, qa4_component_failure, qa5_perceived_quality) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7});\n".format(int(line_count), used, function_id, functionQA1, functionQA2, functionQA3, functionQA4, functionQA5)
                print(import_line)
                mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
