from datetime import datetime
import time
from string import digits
import csv
specificationTypes = [
                "vRMSfreqPump",
                "aRMSfreqPUMP",
                "aPeaktimePUMP",
                "unbalance",
                "misalignment",
                "BearingPUMPnt",
                "BearingPUMPdi",
                "BearingMotor6",
                "PumpPiston",
                "PressureSensor1",
                "PressureSensor2",
                "PressureSensor3",
                "PressureSensor4"
]

measureDescriptions = [
                "DRUM Hydraulic Punching SeriesMeasure vRMSfreqPUMP speed",
                "DRUM Hydraulic Punching SeriesMeasure aRMSfreqPUMP acceleration",
                "DRUM Hydraulic Punching SeriesMeasure aPeaktimePUMP acceleration",
                "DRUM Hydraulic Punching SeriesMeasure unbalance speed",
                "DRUM Hydraulic Punching SeriesMeasure misalignment speed",
                "DRUM Hydraulic Punching SeriesMeasure BearingPUMPnt acceleration",
                "DRUM Hydraulic Punching SeriesMeasure BearingPUMPdi acceleration",
                "DRUM Hydraulic Punching SeriesMeasure BearingMotor acceleration",
                "DRUM Hydraulic Punching SeriesMeasure PumpPiston acceleration",
                "DRUM Hydraulic Punching SeriesMeasure PressureSensor1 pressure",
                "DRUM Hydraulic Punching SeriesMeasure PressureSensor2 pressure",
                "DRUM Hydraulic Punching SeriesMeasure PressureSensor3 pressure",
                "DRUM Hydraulic Punching SeriesMeasure PressureSensor4 pressure"
]

# measureDescriptions = [
#                         "Controllo vibrazione (attraverso la misurazione la velocita RMS)della pompa durante la lavorazione del ciclo. verifica se i valori non sono all'interno del range la lavorazione.",
#                         "Controllo vibrazione (attraverso la misurazione l'accelerazione RMS)della pompa durante la lavorazione del ciclo. verifica se i valori non sono all'interno del range la lavorazione.",
#                         "Controllo vibrazione (attraverso la misurazione l'accelerazione di picco RMS)della pompa durante la lavorazione del ciclo. verifica se i valori non sono all'interno del range la lavorazione.",
#                         "Controllo pressione dell'olio durante la lavorazione del ciclo. sempre se i valori non sono all'interno del range la lavorazione non ha avuto esito positivo.",
#                         "Controllo pressione dell'olio durante la lavorazione del ciclo. sempre se i valori non sono all'interno del range la lavorazione non ha avuto esito positivo.",
#                         "Controllo vibrazione (attraverso la misurazione l'accelerazione RMS)della pompa durante la lavorazione del ciclo. verifica se i valori non sono all'interno del range la lavorazione.",
#                         "Controllo vibrazione (attraverso la misurazione l'accelerazione RMS)della pompa durante la lavorazione del ciclo. verifica se i valori non sono all'interno del range la lavorazione.",
#                         "Controllo vibrazione (attraverso la misurazione l'accelerazione RMS)della pompa durante la lavorazione del ciclo. verifica se i valori non sono all'interno del range la lavorazione.",
#                         "Controllo vibrazione (attraverso la misurazione l'accelerazione RMS)della pompa durante la lavorazione del ciclo. verifica se i valori non sono all'interno del range la lavorazione.",
#                         "Controllo pressione dell'olio durante la lavorazione del ciclo. sempre se i valori non sono all'interno del range la lavorazione non ha avuto esito positivo.",
#                         "Controllo pressione dell'olio durante la lavorazione del ciclo. sempre se i valori non sono all'interno del range la lavorazione non ha avuto esito positivo.",
#                         "Controllo pressione dell'olio durante la lavorazione del ciclo. sempre se i valori non sono all'interno del range la lavorazione non ha avuto esito positivo.",
#                         "Per usi futuri"
#                         ]

measureDimensions = [
                "mm/sec",
                "g/1000",
                "g/1000",
                "mm/sec",
                "mm/sec",
                "g/1000",
                "g/1000",
                "g/1000",
                "g/1000",
                "bar",
                "bar",
                "bar",
                "N/A"
                ]

measureTypes = [
                "Speed",
                "Acceleration",
                "Acceleration",
                "Speed",
                "Speed",
                "Acceleration",
                "Acceleration",
                "Acceleration",
                "Acceleration",
                "Pressure",
                "Pressure",
                "Pressure",
                "N/A"
                ]

resourceNames = ["A1 Centralina idraulica punching", "A2 Centralina idraulica Seaming"]

with open('Drum Line Sensor _ data flow.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0

    with open("import_measures_encoded.sql", "a") as mmi:

        measure_id = 870534

        for row in csv_reader:
            if row:
                if line_count == 0 :
                    mmi.write("USE whr_mpfq_relational;\n")
                    line_count +=1
                    continue

                timestamp = row[0]
                if not timestamp:
                    continue

                for i in range(len(specificationTypes)):

                    if row[i+2] == "---":
                        continue

                   #adding Measure
                    value = row[i+2]
                    if(measureTypes[i] == "N/A" and measureDimensions[i] == "N/A"):
                        mmi.write("INSERT INTO Measure (description, measureDimension, measureType, dataDivisor, measure_prog_id, dateTime, dataSeriesValue, dataSeriesUSL, dataSeriesLSL, dataSingleValue, usl, lsl) VALUES (\"{0}\", {1}, {2}, {3}, {4}, \"{5}\", \"{6}\", {7}, {8}, {9}, {10}, {11} );\n".format(measureDescriptions[i], "NULL", 2, "NULL",  "NULL", timestamp, value, "NULL", "NULL", "NULL", "NULL", "NULL" ))
                    else:
                        mmi.write("INSERT INTO Measure (description, measureDimension, measureType, dataDivisor, measure_prog_id, dateTime, dataSeriesValue, dataSeriesUSL, dataSeriesLSL, dataSingleValue, usl, lsl) VALUES (\"{0}\", \"{1}\", {2}, {3}, {4}, \"{5}\", \"{6}\", {7}, {8}, {9}, {10}, {11} );\n".format(measureDescriptions[i], measureDimensions[i],  2, "NULL", "NULL", timestamp, value, "NULL", "NULL", "NULL", "NULL", "NULL" ))

                    measure_id += 1

                    line_count += 1
                    print(f'Processed {line_count} lines.')

                    if i<12:
                        mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351024, measure_id))
                        mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351016, measure_id))
                        mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351017, measure_id))
                        mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351018, measure_id))
                        mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351005, measure_id))
                        mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351008, measure_id))

                        mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351020, measure_id))
                        mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351019, measure_id))
                        mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351021, measure_id))

                        mmi.write("INSERT INTO Function_Measure (function_id, measure_id) VALUES ({0}, {1});\n".format(10351015, measure_id))

                        ##################################################################################################################

                        mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001035018, measure_id))

                        mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001035003, measure_id))

                        mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001070009, measure_id))
                        mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001070011, measure_id))
                        mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001070012, measure_id))
                        mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001070013, measure_id))

                        mmi.write("INSERT INTO Material_Measure (material_id, measure_id) VALUES ({0}, {1});\n".format(40001035010, measure_id))

                        ##################################################################################################################

                    if i==11:
                        resource_id = 308
                    elif i==12:
                        resource_id = 309
                    elif i<5:
                        resource_id = 246+i
                    else:
                        resource_id = 246+i+2

                    mmi.write("INSERT INTO Resource_Measure (resource_id, measure_id) VALUES ({0}, {1});\n".format(resource_id, measure_id))


        mmi.close()
    print(f'Processed {line_count} lines.')
