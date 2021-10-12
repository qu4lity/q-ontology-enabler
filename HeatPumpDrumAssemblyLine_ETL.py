import csv

with open('AssemblyLine.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    with open("import_tobe.sql", "a") as mmi:

        station_id=0
        journalDetails_id = 0

        for index, row in enumerate(csv_reader):
            if index == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
            elif index == 1:
                continue
            else:
                if not row[5].isdigit() and not row[7].isdigit() and  not row[9].isdigit():
                    continue

                if row[0] and int(row[0])>0:
                    journalDetails_id = int(row[0])
                    if row[1]:
                        journalDetails_description = row[1].rstrip().strip().replace("\n", " ")
                    else:
                        journalDetails_description  = "NULL"

                    if row[2] and int(row[2])>0:
                        station_id = int(row[2])

                        import_line = "INSERT INTO JournalDetails(journalDetails_id, journal_id,description,overallResult,dateTime,overallDefectCode,station_id) VALUES({0}, {1}, \"{2}\",\"{3}\",\"{4}\", {5}, {6});\n".format(journalDetails_id, 1, journalDetails_description, "OK", "2021-06-04 09:43:54", "NULL", station_id)
                        #import_line = "UPDATE JournalDetails SET station_id={0} WHERE journalDetails_id={1};\n".format(station_id, journalDetails_id)
                        mmi.write(import_line)

                    else:
                        print("Missing station_id on line {0}".format(index+1))
                        exit(1)

                    # this is useless #########################################################
                    if row[3]:
                        station_description = row[3].strip()
                    else:
                        station_description  = "NULL"
                    ###########################################################################

                    if row[5] and int(row[5])>0:
                        operation_id = int(row[5])
                        import_line = "INSERT INTO JournalDetails_Operation(journalDetails_id, operation_id) VALUES({0},{1});\n".format(journalDetails_id, operation_id)
                        mmi.write(import_line)

                    else:
                        print("Missing operation_id on line {0}".format(index+1))
                        exit(1)

                else:
                    if row[5] and int(row[5])>0:
                        print("Another operation_id for same station_id: {0}".format(station_id))
                    else:
                        print("Missing journalDetails_id on line {0}".format(index+1))
                        exit(1)

                # this is useless #########################################################
                if row[6]:
                    operation_description = row[6].strip()
                else:
                    operation_description  = "NULL"
                ###########################################################################

                if row[7]: # and int(row[7])>0:
                    process_id = row[7]#int(row[7])
                    import_line = "UPDATE Process SET operation_id={0} WHERE process_id={1};\n".format(operation_id, process_id)
                    mmi.write(import_line)
                else:
                    print("Missing process_id on line {0}".format(index+1))
                    exit(1)

                # this is useless #########################################################
                if row[8]:
                    process_description = row[8].strip()
                else:
                    process_description  = "NULL"
                ###########################################################################

                if row[9] and int(row[9])>0:
                    resource_id = int(row[9])
                    import_line = "UPDATE Process SET resource_id={0} WHERE process_id={1};\n".format(resource_id, process_id)
                    mmi.write(import_line)
                else:
                    print("Missing resource_id on line {0}".format(index+1))
                    exit(1)

                # this is useless #########################################################
                if row[10]:
                    resource_description = row[10].strip()
                else:
                    resource_description  = "NULL"
                ###########################################################################

                if row[11] and int(row[11])>0:
                    material_carrier_id = int(row[11])
                    import_line = "UPDATE Operation SET materialUsedAsCarrier_id={0} WHERE operation_id={1};\n".format(material_carrier_id, operation_id)
                    mmi.write(import_line)
                else:
                    print("Missing material_carrier_id on line {0}".format(index+1))
                    material_carrier_id = "NULL"

                # this is useless #########################################################
                if row[12]:
                    material_carrier_description = row[12].strip()
                else:
                    material_carrier_description  = "NULL"
                ###########################################################################

                if row[13] and int(row[13])>0:
                    material_object_id = int(row[13])
                    import_line = "UPDATE Operation SET materialUsedAsTarget_id={0} WHERE operation_id={1};\n".format(material_object_id, operation_id)
                    mmi.write(import_line)
                else:
                    print("Missing material_object_id on line {0}".format(index+1))
                    material_object_id = "NULL"

                # this is useless #########################################################
                if row[14]:
                    material_object_description = row[14].strip()
                else:
                    material_object_description  = "NULL"
                ###########################################################################

                if row[15] and int(row[15])>0:
                    material_transformation_id = int(row[15])
                    import_line = "UPDATE Operation SET materialTransformation_id={0} WHERE operation_id={1};\n".format(material_transformation_id, operation_id)
                    mmi.write(import_line)
                else:
                    print("Missing material_transformation_id on line {0}".format(index+1))
                    material_transformation_id = "NULL"

                # this is useless #########################################################
                if row[16]:
                    material_transformation_description = row[16].strip()
                else:
                    material_transformation_description  = "NULL"
                ###########################################################################

                for i in range(0,100,2):
                    try:
                        if row[17+i] and int(row[17+i])>0:
                            function_id = int(row[17+i])
                            import_line = "INSERT INTO Process_Function(process_id, function_id) VALUES({0},{1});\n".format(process_id, function_id)
                            mmi.write(import_line)
                        else:
                            print("Missing function_id on line {0}".format(index+1))
                            function_id = "NULL"

                        # this is useless #########################################################
                        if row[18+i]:
                            function_description = row[18+i].strip()
                        else:
                            function_description  = "NULL"
                    except IndexError:
                        print("Missing function_id on line {0}".format(index+1))
                        function_id = "NULL"
                ###########################################################################

        mmi.close()
    print(f'Processed {line_count} lines.')
