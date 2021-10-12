import csv

with open('ProcessProcessTypeLocationState.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_ProcessProcessTypeLocationState.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                line_count += 1

            else:

                process_id = int(row[0])
                processType_id = int(row[2])
                if processType_id != 0:
                    import_line = "UPDATE Process SET processType_id={0} WHERE process_id={1};\n".format(processType_id, process_id)
                    print(import_line)
                    mmi.write(import_line)

                location_id = int(row[4])
                if location_id != 0:
                    import_line = "UPDATE Process SET location_id={0} WHERE process_id={1};\n".format(location_id, process_id)
                    print(import_line)
                    mmi.write(import_line)

                state_id = int(row[6])
                if state_id != 0:
                    import_line = "UPDATE Process SET state_id={0} WHERE process_id={1};\n".format(state_id, process_id)
                    print(import_line)
                    mmi.write(import_line)


                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
