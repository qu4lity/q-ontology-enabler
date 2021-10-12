import csv
from string import digits
from datetime import datetime

with open('DrumMeasure2019.csv') as measures_file, open('DrumResult2019.csv') as tests_file, open("import_measures.sql", "a") as mmi:

    mmi.write("USE whr_mpfq_relational;\n")

    tests_csv = csv.reader(tests_file, delimiter=';')

    measures_csv = csv.reader(measures_file, delimiter=';')

    tests_line_count = 0
    measures_line_count = 0

    measure_id=0
    process_id=0

    test_results = {}

    for row in tests_csv:

        if row:
            if tests_line_count == 0 :
                tests_line_count +=1
                continue

            test_id = row[2].strip()
            product_id = row[5].strip()
            result = row[6]
            test_timestamp = row[10]
            if not test_timestamp :
                continue

            test_results[test_id] = result

            tests_line_count+=1
            print(f'Processed {tests_line_count} tests_lines.')


    for row in measures_csv:

        if row:

            if measures_line_count == 0 :
                measures_line_count +=1
                continue

            creation_date = row[1]
            operation_id = row[2]
            measure_timestamp = row[3]
            if not measure_timestamp :
                continue
            inner_product_id = row[4][3:15].strip()
            measureDescription = row[4][17:].strip()

            failureType_id = "NULL"
            description = row[5].strip()
            descriptionType = 1 # 1 DRUM LIFTER ASSEMBLY - 2 DRUM DIMENSIONAL CHECK
            if description.startswith("Torque Measurement") :
                description = "DRUM LIFTER ASSEMBLY "+ description
                descriptionType = 1
                if description.endswith("1"):
                    failureType_id = 6025911
                elif description.endswith("2"):
                    failureType_id = 6026311
                elif description.endswith("3"):
                    failureType_id = 6026711
                elif description.endswith("4"):
                    failureType_id = 6027111
                elif description.endswith("5"):
                    failureType_id = 6027511
                elif description.endswith("6"):
                    failureType_id = 6027911
            elif description.startswith("PreTorque Measurement") :
                description = "DRUM LIFTER ASSEMBLY "+ description
                descriptionType = 1
                if description.endswith("1"):
                    failureType_id = 6026011
                elif description.endswith("2"):
                    failureType_id = 6026411
                elif description.endswith("3"):
                    failureType_id = 6026811
                elif description.endswith("4"):
                    failureType_id = 6027211
                elif description.endswith("5"):
                    failureType_id = 6027611
                elif description.endswith("6"):
                    failureType_id = 6028011
            elif description.startswith("Angle Measurement") :
                description = "DRUM LIFTER ASSEMBLY "+ description
                descriptionType = 1
                if description.endswith("1"):
                    failureType_id = 6026111
                elif description.endswith("2"):
                    failureType_id = 6026511
                elif description.endswith("3"):
                    failureType_id = 6026911
                elif description.endswith("4"):
                    failureType_id = 6027311
                elif description.endswith("5"):
                    failureType_id = 6027711
                elif description.endswith("6"):
                    failureType_id = 6028111
            elif description.startswith("Depth Measurement") :
                description = "DRUM LIFTER ASSEMBLY "+ description
                descriptionType = 1
                if description.endswith("1"):
                    failureType_id = 6026211
                elif description.endswith("2"):
                    failureType_id = 6026611
                elif description.endswith("3"):
                    failureType_id = 6027011
                elif description.endswith("4"):
                    failureType_id = 6027411
                elif description.endswith("5"):
                    failureType_id = 6027811
                elif description.endswith("6"):
                    failureType_id = 6028211
            elif description.startswith("Concentricity Measurement") :
                description = "DRUM DIMENSIONAL CHECK "+ description
                descriptionType = 2
                if description.endswith("1"):
                    failureType_id = 6023611
                elif description.endswith("2"):
                    failureType_id = 6023621
                elif description.endswith("3"):
                    failureType_id = 6023631
                elif description.endswith("4"):
                    failureType_id = 6023641
                elif description.endswith("5"):
                    failureType_id = 6023651
            elif description.startswith("Planarity Measurement") :
                description = "DRUM DIMENSIONAL CHECK "+ description
                descriptionType = 2
                if description.endswith("1"):
                    failureType_id = 6023711
                elif description.endswith("2"):
                    failureType_id = 6023721
                elif description.endswith("3"):
                    failureType_id = 6023731
                elif description.endswith("4"):
                    failureType_id = 6023741
                elif description.endswith("5"):
                    failureType_id = 6023751
            elif description.startswith("Height Measurement") :
                description = "DRUM DIMENSIONAL CHECK "+ description
                descriptionType = 2
                if description.endswith("1"):
                    failureType_id = 6023811
                elif description.endswith("2"):
                    failureType_id = 6023821
                elif description.endswith("3"):
                    failureType_id = 6023831
                elif description.endswith("4"):
                    failureType_id = 6023841
                elif description.endswith("5"):
                    failureType_id = 6023851

            v_min =  row[6]
            if v_min == "NA" or v_min == "nan":
                v_min = "NULL"
            v_max =  row[7]
            if v_max == "NA" or v_max == "nan":
                v_max = "NULL"
            value =  row[8]
            measureDimension =  row[9].strip()

            measureType = ""
            if measureDimension == "mm" :
              measureType = "Dimensional"
            elif measureDimension == "Nm" :
              measureType = "Torque"
            elif measureDimension == "Degree" :
              measureType = "Angular"
            else :
              measureType = "Unknown"

            #adding Measure
            mmi.write("INSERT INTO Measure (description, measureDimension, measureType, dataDivisor, measure_prog_id, dateTime, dataSeriesValue, dataSeriesUSL, dataSeriesLSL, dataSingleValue, usl, lsl) VALUES (\"{0}\", \"{1}\", {2}, {3}, {4}, \"{5}\", {6}, {7}, {8}, {9}, {10}, {11} );\n".format(description, measureDimension, 1, "NULL", "NULL", measure_timestamp, "NULL", "NULL", "NULL", value, v_max, v_min))
            measure_id += 1

            # adding MeasureResult
            test_id = row[4].split("-")[0].strip()
            result = test_results.get(test_id)
            if result != "OK" :
                mmi.write("INSERT INTO MeasureFailure (measure_id, failureType_id, description, recoveryTime) VALUES ({0}, {1}, \"{2}\", {3});\n".format(measure_id, failureType_id, f'Failure at {measure_timestamp}', 60))

            measures_line_count +=1
            print(f'Processed {measures_line_count} measures_lines.')

            if descriptionType == 1 :
                if description.startswith("DRUM LIFTER ASSEMBLY Torque Measurement") :
                    index = 0
                elif description.startswith("DRUM LIFTER ASSEMBLY PreTorque Measurement") :
                    index = 1
                elif description.startswith("DRUM LIFTER ASSEMBLY Angle Measurement") :
                    index = 2
                elif description.startswith("DRUM LIFTER ASSEMBLY Depth Measurement") :
                    index = 3
                else:
                    continue


                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351024, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351016, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351017, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351018, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351005, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351008, measure_id))

                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351022, measure_id))

                ##################################################################################################################


                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001035003, measure_id))

                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001035004, measure_id))


                ##################################################################################################################

                multiplier = int(description[-1])
                resource_id = 259 + (4*(multiplier-1)) + index
                mmi.write("INSERT INTO Resource_Measure (resource_id, measure_id) VALUES ({0}, {1});\n".format(resource_id, measure_id))

            elif descriptionType == 2:
                if description.startswith("DRUM DIMENSIONAL CHECK Concentricity Measurement") :
                    index = 0
                elif description.startswith("DRUM DIMENSIONAL CHECK Planarity Measurement") :
                    index = 1
                elif description.startswith("DRUM DIMENSIONAL CHECK Height Measurement") :
                    index = 2
                else:
                    continue

                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351007, measure_id))

                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351024, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351016, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351017, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351018, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351005, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351008, measure_id))

                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351011, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351012, measure_id))

                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351013, measure_id))

                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351032, measure_id))

                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351020, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351019, measure_id))
                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351021, measure_id))

                mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351015, measure_id))

                ##################################################################################################################

                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001035018, measure_id))

                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001035003, measure_id))

                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001035000, measure_id))
                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001035019, measure_id))

                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001035001, measure_id))

                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001035009, measure_id))

                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001070009, measure_id))
                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001070011, measure_id))
                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001070012, measure_id))
                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001070013, measure_id))

                mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001035010, measure_id))

                ##################################################################################################################

                resource_id = 236 + index
                mmi.write("INSERT INTO Resource_Measure (resource_id, measure_id) VALUES ({0}, {1});\n".format(resource_id, measure_id))

            else:
                continue

mmi.close()
