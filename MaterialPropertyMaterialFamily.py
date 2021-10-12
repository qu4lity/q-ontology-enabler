import csv

with open('MaterialPropertyMaterialFamily.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')

    with open("import_MaterialPropertyMaterialFamily.sql", "a") as mmi:
        materialFamily_ids = set()

        for index, row in enumerate(csv_reader):
            if index == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
            else:

                material_id = int(row[0])
                materialProperty_id = int(row[1])
                materialProperty_description = row[2].strip()

                materialProperty1 = row[3].strip()
                materialProperty2 = row[4].strip()
                materialProperty3 = row[5].strip()
                materialProperty4 = row[6].strip()
                materialProperty5 = row[7].strip()


                materialFamily_id = int(row[8])
                materialFamily_description = row[9].strip()
                if materialFamily_id not in materialFamily_ids and materialFamily_id!=0 :
                    import_line = "INSERT INTO MaterialFamily (materialFamily_id, description) VALUES ({0}, \"{1}\");\n".format(materialFamily_id, materialFamily_description)
                    print(import_line)
                    mmi.write(import_line)
                    materialFamily_ids.add(materialFamily_id)


                import_line = "INSERT INTO Property (property_id, description, property1, property2, property3, property4, property5) VALUES ({0}, \"{1}\", \"{2}\", \"{3}\", \"{4}\", \"{5}\", \"{6}\");\n".format(materialProperty_id, materialProperty_description, materialProperty1, materialProperty2, materialProperty3, materialProperty4, materialProperty5)
                print(import_line)
                mmi.write(import_line)

                if materialFamily_id!=0 :
                    import_line = "UPDATE Material SET property_id={0},materialFamily_id={1} WHERE material_id={2};\n".format(materialProperty_id, materialFamily_id, material_id)
                    print(import_line)
                    mmi.write(import_line)
                else:
                    import_line = "UPDATE Material SET property_id={0} WHERE material_id={1};\n".format(materialProperty_id, material_id)
                    print(import_line)
                    mmi.write(import_line)

        mmi.close()
    print(f'Processed {index} lines.')
