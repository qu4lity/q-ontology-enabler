import csv

with open('Function.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_Function.sql", "a") as mmi:
        function_ids = set()

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:

                function_id = int(row[0])
                if not function_id or function_id == "0":
                    continue
                if function_id in function_ids :
                    function_id += 1
                function_ids.add(function_id)

                materialUsedAsCarrier_id = row[2]
                if not materialUsedAsCarrier_id or materialUsedAsCarrier_id == "0":
                    continue

                carrier = row[3].strip()
                if not carrier or carrier == "0":
                    continue

                function = row[4].strip()
                if not type or type == "0":
                    continue

                materialUsedAsObject_id = row[5]
                if not materialUsedAsObject_id or materialUsedAsObject_id == "0":
                    continue

                object = row[6].strip()
                if not object or object == "0":
                    continue

                description = row[1].strip()
                if not description or description == "0":
                    continue

                import_line = "INSERT INTO Function (function_id, process_id, description, materialUsedAsCarrier_id, carrier, function, materialUsedAsObject_id, object) VALUES ({0}, {1}, \"{2}\", {3}, \"{4}\", \"{5}\", {6}, \"{7}\");\n".format(function_id, "NULL", description, materialUsedAsCarrier_id, carrier, function, materialUsedAsObject_id, object)
                mmi.write(import_line)
                print(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
