#!/usr/bin/env python3


# Libraries
import os
import sys
import getopt
import csv  
  
inputFileName = "baby-names-frequency_1980_2020.csv"

rank = []
names = []
frequency = []
gender = []
year = []

#Input first portion of file
with open ( inputFileName ) as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:
            if(len(row) == 5):
                rank.append(row[0])
                names.append(row[1])
                frequency.append(row[2])
                gender.append(row[3])
                year.append(row[4])

#append the rest of the data to the lists
inputFileName = "baby-names-frequency_2021.csv"
with open ( inputFileName ) as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:
            if(len(row) == 5):
                rank.append(row[0])
                names.append(row[1])
                frequency.append(row[2])
                gender.append(row[3])
                year.append(row[4])

femaleFile = open("ALBERTA_1980_2021_FEMALE.csv", 'w')
maleFile = open("ALBERTA_1980_2021_MALE.csv", 'w')

femaleWriter = csv.writer(femaleFile)
maleWriter = csv.writer(maleFile)

row = ["Year", "Name", "Frequency", "Rank"]

femaleWriter.writerow(row)
maleWriter.writerow(row)

for i in range(len(rank)):
    row = [year[i], names[i].strip().title(), frequency[i], rank[i]]
    if(gender[i] == "Boy"):
        maleWriter.writerow(row)
    elif(gender[i] == "Girl"):
        femaleWriter.writerow(row)

femaleFile.close()
maleFile.close()


maleYear = []
maleName = []
maleFrequency = []
maleRank = []

femaleYear = []
femaleName = []
femaleFrequency = []
femaleRank = []



inputFileName = "NS_Top_Twenty_Baby_Names_-_1920-Current.csv"

maleRankCtr = 0
femaleRankCtr = 0

year = 1920

with open ( inputFileName ) as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:

            if(row[0] != "YEAR" and int(row[0]) != year):
                year = int(row[0])
                maleRankCtr = 0
                femaleRankCtr = 0


            if(row[1] == "F"):
                femaleRankCtr = femaleRankCtr + 1

                femaleYear.append(row[0])
                femaleName.append(row[2].title())
                femaleFrequency.append(row[3])

                femaleRank.append(femaleRankCtr)

            elif(row[1] == "M"):
                maleRankCtr = maleRankCtr + 1

                maleYear.append(row[0])
                maleName.append(row[2].title())
                maleFrequency.append(row[3])

                maleRank.append(maleRankCtr)


femaleFile = open("NOVASCOTIA_1920_2022_FEMALE.csv", 'w')
maleFile = open("NOVASCOTIA_1920_2022_MALE.csv", 'w')

femaleWriter = csv.writer(femaleFile)
maleWriter = csv.writer(maleFile)

row = ["Year", "Name", "Frequency", "Rank"]

femaleWriter.writerow(row)
maleWriter.writerow(row)


for i in range(len(femaleName)):

    if(i > 0 and femaleFrequency [i] == femaleFrequency [i-1]):
        femaleRank [i] = femaleRank[i-1]

    row = [femaleYear[i], femaleName[i].strip().title(), femaleFrequency[i], femaleRank[i]]

    femaleWriter.writerow(row)

for i in range(len(maleName)):

    if(i > 0 and maleFrequency [i] == maleFrequency [i-1]):
        maleRank [i] = maleRank[i-1]

    row = [maleYear[i], maleName[i].strip().title(), maleFrequency[i], maleRank[i]]

    maleWriter.writerow(row)




femaleFile.close()
maleFile.close()



