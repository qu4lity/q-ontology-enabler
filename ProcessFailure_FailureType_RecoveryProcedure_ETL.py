import csv

with open('ProcessFailure_FailureType_RecoveryProcedure.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    with open("import_ProcessFailure_FailureType_RecoveryProcedure.sql", "a") as mmi:

        for row in csv_reader:
            if line_count == 0:
                import_line = "USE whr_mpfq_relational;\n"
                mmi.write(import_line)
                line_count += 1

            else:
                processFailure_id = int(row[0])
                processFailure_description = row[1]

                for x in range(4):
                    failureType_id = int(row[2+(4*x)])
                    failureType_description = row[3+(4*x)]
                    recoveryProcedure_id = int(row[4+(4*x)])
                    recoveryProcedure_description = row[5+(4*x)]

                    if "Failure 4" in processFailure_description:
                        failureType_id = failureType_id+10
                        recoveryProcedure_id = recoveryProcedure_id+10

                    import_line = "INSERT INTO FailureType (failureType_id, description, note) VALUES ({0}, \"{1}\", {2});\n".format(failureType_id, failureType_description, "NULL")
                    print(import_line)
                    mmi.write(import_line)

                    import_line = "INSERT INTO RecoveryProcedure(recoveryProcedure_id, failureType_id, description) VALUES ({0}, {1}, \"{2}\");\n".format(recoveryProcedure_id, failureType_id, recoveryProcedure_description)
                    print(import_line)
                    mmi.write(import_line)

                    # import_line = "UPDATE ProcessFailure SET failureType_id={0} WHERE processFailure_id={1};\n".format(failureType_id, processFailure_id)
                    # print(import_line)
                    # mmi.write(import_line)

                line_count += 1

        mmi.close()
    print(f'Processed {line_count} lines.')
