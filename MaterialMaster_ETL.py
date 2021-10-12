import csv

with open('MaterialMaster.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_MaterialMaster.sql", "a") as mmi:
        material_ids = set()
        whr_material_ids = set()

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)

                import_line = "INSERT INTO EngineeringBoM (engineeringBoM_id, description) VALUES ({0}, \"{1}\");\n".format(1, "EngineeringBoM")
                mmi.write(import_line)

                line_count += 1

            else:
                if(row[7]):
                    whr_material_id = row[7].strip()
                    whr_material_description = row[8].strip().replace("\"","'")

                    materialRevisionECN = row[10].strip()
                    if(not materialRevisionECN):
                        materialRevisionECN = "NULL"

                    materialDrawingNumber = row[12].strip()
                    if(not materialDrawingNumber):
                        materialDrawingNumber = "NULL"

                    if(whr_material_id not in whr_material_ids):
                        if (materialRevisionECN != "NULL" and materialDrawingNumber != "NULL"):
                            import_line = "INSERT INTO WhirlpoolMaterial (whr_material_id, description, materialRevisionECN, materialDrawingNumber) VALUES ({0}, \"{1}\", \"{2}\", \"{3}\");\n".format(whr_material_id, whr_material_description, materialRevisionECN, materialDrawingNumber)
                        elif (materialRevisionECN != "NULL" and materialDrawingNumber == "NULL"):
                            import_line = "INSERT INTO WhirlpoolMaterial (whr_material_id, description, materialRevisionECN, materialDrawingNumber) VALUES ({0}, \"{1}\", \"{2}\", {3});\n".format(whr_material_id, whr_material_description, materialRevisionECN, materialDrawingNumber)
                        elif (materialRevisionECN == "NULL" and materialDrawingNumber != "NULL"):
                            import_line = "INSERT INTO WhirlpoolMaterial (whr_material_id, description, materialRevisionECN, materialDrawingNumber) VALUES ({0}, \"{1}\", {2}, \"{3}\");\n".format(whr_material_id, whr_material_description, materialRevisionECN, materialDrawingNumber)
                        elif (materialRevisionECN == "NULL" and materialDrawingNumber == "NULL"):
                            import_line = "INSERT INTO WhirlpoolMaterial (whr_material_id, description, materialRevisionECN, materialDrawingNumber) VALUES ({0}, \"{1}\", {2}, {3});\n".format(whr_material_id, whr_material_description, materialRevisionECN, materialDrawingNumber)

                        mmi.write(import_line)
                        whr_material_ids.add(whr_material_id)


                if(row[0]): # and row[0]!=row[7]):
                    material_id = row[0].strip()
                    material_description = row[1].strip().replace("\"","'")

                    function_unit_id = row[6].strip()
                    if(not function_unit_id):
                        function_unit_id = "NULL"

                    if(material_id not in material_ids):
                        materialModel = "{0}{1}".format(55, material_id)
                        import_line = "INSERT INTO Material (material_id, description, materialModel, materialFamily_id, functionUnit_id) VALUES ({0}, \"{1}\", {2}, {3}, {4});\n".format(material_id, material_description, materialModel, "NULL", function_unit_id)
                        mmi.write(import_line)
                        material_ids.add(material_id)

                        if "Spare" not in material_description:
                            quantity = 1
                        else:
                            quantity = 0
                        import_line = "INSERT INTO EngineeringBoM_Material (engineeringBoM_id, material_id, quantity) VALUES ({0}, {1}, {2});\n".format(1, material_id, quantity)
                        mmi.write(import_line)


                    if(whr_material_id and material_id):
                        import_line = "INSERT INTO Material_WhirlpoolMaterial (material_id, whr_material_id) VALUES ({0}, {1});\n".format(material_id, whr_material_id)
                        mmi.write(import_line)


                if(row[2] and row[3]):
                    second_material_id = row[2].strip()
                    second_material_description = row[3].strip().replace("\"","'")

                    function_unit_id = row[6].strip()
                    if(not function_unit_id):
                        function_unit_id = "NULL"

                    if(second_material_id not in material_ids):
                        materialModel = "{0}{1}".format(55, second_material_id)
                        import_line = "INSERT INTO Material (material_id, description, materialModel, materialFamily_id, functionUnit_id) VALUES ({0}, \"{1}\", {2}, {3}, {4});\n".format(second_material_id, second_material_description, materialModel, "NULL", function_unit_id)
                        mmi.write(import_line)
                        material_ids.add(second_material_id)

                        if "Spare" not in second_material_description:
                            quantity = 1
                        else:
                            quantity = 0
                        import_line = "INSERT INTO EngineeringBoM_Material (engineeringBoM_id, material_id, quantity) VALUES ({0}, {1}, {2});\n".format(1, second_material_id, quantity)
                        mmi.write(import_line)

                    if(whr_material_id and second_material_id):
                        import_line = "INSERT INTO Material_WhirlpoolMaterial (material_id, whr_material_id) VALUES ({0}, {1});\n".format(second_material_id, whr_material_id)
                        mmi.write(import_line)

                if(row[4] and row[5]):
                    third_material_id = row[4].strip()
                    third_material_description = row[5].strip().replace("\"","'")

                    function_unit_id = row[6].strip()
                    if(not function_unit_id):
                        function_unit_id = "NULL"

                    if(third_material_id not in material_ids):
                        materialModel = "{0}{1}".format(55, third_material_id)
                        import_line = "INSERT INTO Material (material_id, description, materialModel, materialFamily_id, functionUnit_id) VALUES ({0}, \"{1}\", {2}, {3}, {4});\n".format(third_material_id, third_material_description, materialModel, "NULL", function_unit_id)
                        mmi.write(import_line)
                        material_ids.add(third_material_id)

                        if "Spare" not in third_material_description:
                            quantity = 1
                        else:
                            quantity = 0
                        import_line = "INSERT INTO EngineeringBoM_Material (engineeringBoM_id, material_id, quantity) VALUES ({0}, {1}, {2});\n".format(1, third_material_id, quantity)
                        mmi.write(import_line)

                    if(whr_material_id and third_material_id):
                        import_line = "INSERT INTO Material_WhirlpoolMaterial (material_id, whr_material_id) VALUES ({0}, {1});\n".format(third_material_id, whr_material_id)
                        mmi.write(import_line)

                line_count += 1
                #if line_count % 20 == 0 :
                #    input("Press Enter to continue...")

        import_line = "INSERT INTO Material (material_id, description, materialModel, materialFamily_id, functionUnit_id) VALUES ({0}, \"{1}\", {2}, {3}, {4});\n".format(40001070012, "BRACKET MOTOR BASE", "NULL", "NULL", "NULL")
        mmi.write(import_line)

        import_line = "INSERT INTO EngineeringBoM_Material (engineeringBoM_id, material_id, quantity) VALUES ({0}, {1}, {2});\n".format(1, 40001070012, 1)
        mmi.write(import_line)

        mmi.close()
    print(f'Processed {line_count} lines.')
