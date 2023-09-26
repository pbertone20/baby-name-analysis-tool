#!/usr/bin/env python3

# Libraries
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
import getopt
import csv
import pandas as pd
import os.path
from ethnicolr import census_ln
import matplotlib.pyplot as plt
import numpy as np

#Function 1
def topName (inputFileName, year):
    #Declare lists
    names     = []
    ranks     = []
    frequency = []
    total     = 0

    #Traverse file and append data from year selected
    with open ( inputFileName ) as csvDataFile:
        next ( csvDataFile ) 
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:
            if int(row[0]) == year :
                tempName = row[1].strip().title()
                names.append(tempName)
                ranks.append(int(row[3]) - total)
                frequency.append(int(row[2]))
                total = total + 1

        #Test if entries were made in list(Ie input year was found)
        if total > 0 :
            print ( "There are ",total," names in ",year )

            #Assign list to dataframe
            people = {'Frequency':frequency,'Name':names,'Rank':ranks}
            people_df = pd.DataFrame(people)
        
            #Sort the list to new dataframe
            people_df.sort_values(["Frequency","Rank","Name"], axis = 0, ascending=[False,False,True],inplace=True)
            rankedPeople_df = people_df

            #Print out the top name of the assigned dataframe
            print("The top name in ", year, " is...")
            print (rankedPeople_df[:1].to_string(index=False, header=True, justify='Right', col_space=9))

        #Error check if year is not found
        else:
            print("Year not found...")

#Function 2
def nameSearch(inputFileName, name, year):
    #Declare lists variables
    names     = []
    rank      = []
    frequency = []
    total     = 0
    found = False

    #Traverse file, if input year is found, search names until input name is found and append to list
    with open ( inputFileName ) as csvDataFile:
        next ( csvDataFile ) 
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:
            if int(row[0]) == year:
                if row[1].strip().title() == name:
                    tempName = row[1].strip().title()
                    names.append(tempName)
                    rank.append((int(row[3])))
                    frequency.append(int(row[2]))
                    found = True;     
                total = total + 1
            
        #Check if name has been found
        if total > 0 and found == True:
            #Assign lists to a dataframe
            people = {'Frequency':frequency,'Name':names,'Rank':rank}
            people_df = pd.DataFrame(people)

            #Print out the top rank of the dataframe
            rankedPeople_df = people_df
            print("Name found!")
            print (rankedPeople_df[:1].to_string(index=False, header=True, justify='right', col_space=9))

        #Error case if name was not found
        else:
            print("Name does not exist in given year...")

#Function 3
def unisexNamesFunc(male_csv, female_csv, year): 

    province =(male_csv.split("_")[0]).title()
        
    #initialize arrays that will store what was read from the csv files
    namesFemale    = []
    namesMale    = []
    totalUnisexNames = 0 #initialize variable to calculate the total number of unisex names in that year

    yearFound = False

    with open ( female_csv ) as csvDataFile: #open female file for reading 
        next(csvDataFile) #skips header row
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:  
            if int(row[0]) == year : #reading all the rows of the file that are a part of the year given by the user 
                namesFemale.append(row[1]) #appends the name at row[1] to the array of female names 
                yearFound = True
    FNamesSet = set(namesFemale) #makes a set of the female names        

    with open ( male_csv ) as csvDataFile: #opens male file for reading 
        next(csvDataFile)
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader: #reads all the rows except for the header row if they are a part of the year given by the user 
            if int(row[0]) == year :
                namesMale.append(row[1]) #appends the name at row[1] to the array of male names 
                yearFound = True
    MNamesSet = set(namesMale) #makes a set of the male names 

    if(yearFound):
        unisexSet = set(FNamesSet.intersection(MNamesSet)) #finding the names that are in both gender sets and putting them in another set

        for i in unisexSet: #calculating the total number of unisex names
            totalUnisexNames = totalUnisexNames + 1
    
        #prints the total number of unisex names
        print("There are " + str(totalUnisexNames) + " names that are in both female and male name lists in the year " + str(year) + " in the province " + province)


        for i in unisexSet: #prints the names 
            print(i)

    else:
        print("Incorrect year! Please try again!")

#Function 4
def topTenNamesFunc(alberta_csv,novaScotia_csv,choice,year): #choice of gender and year
    if choice == "1": 
        gender = "Male"

    if choice == "2": 
        gender = "Female"

    provinceOne = (alberta_csv.split("_")[0]).title()
    provinceTwo = (novaScotia_csv.split("_")[0]).title()

    #initializing arrays which will store what is going to be read from the csv files
    namesAlberta = []
    numbersAlberta = []  
    ranksAlberta = []
    totalAlberta = 0 
    namesNovaScotia = [] 
    numbersNovaScotia = []  
    ranksNovaScotia = []
    totalNovaScotia = 0

    yearFoundOne = False
    yearFoundTwo = False

    #getting the data from the csv files and storing them into arrays if they are during of the user chosen year 
    with open ( alberta_csv ) as csvDataFile:  
        next ( csvDataFile )
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:
            if int(row[0]) == year :
                temp = row[1].strip()
                namesAlberta.append(temp)
                numbersAlberta.append(int(row[2]))
                ranksAlberta.append(row[3])
                totalAlberta = totalAlberta + 1

                yearFoundOne = True
    
    with open ( novaScotia_csv ) as csvDataFile:
        next ( csvDataFile )
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:
            if int(row[0]) == year :
                temp = row[1].strip()
                namesNovaScotia.append(temp)
                numbersNovaScotia.append(int(row[2]))
                ranksNovaScotia.append(row[3])
                totalNovaScotia = totalNovaScotia + 1

                yearFoundTwo = True

    #Check if years were found in both files and then print results
    if(yearFoundOne and yearFoundTwo):
        #Print names for province one
        if totalAlberta > 0 :
            print("The top ten " + gender + " names in "+ provinceOne + " in the year " + str(year) + " are: ")
            
            provinceNamesAlberta = {'Name':namesAlberta,'Frequency':numbersAlberta} #setting the array namesAlberta under 'Name' in the data frame and numbersAlberta under 'Frequency'
            provinceNamesAlberta_df = pd.DataFrame(provinceNamesAlberta) #loading the data

            provinceNamesAlberta = {'Name':namesAlberta,'Frequency':numbersAlberta} #setting the array namesAlberta under 'Name' in the data frame and numbersAlberta under 'Frequency'
            provinceNamesAlberta_df = pd.DataFrame(provinceNamesAlberta) #loading the data

            provinceNamesAlberta_df.sort_values(["Frequency","Name"], axis = 0, ascending=[False,True], inplace=True) #sorting the data frame in order from greatest to least 
    
            rankedProvinceNamesAlberta_df = provinceNamesAlberta_df.assign(Rank=ranksAlberta) #assigns new column(array ranks under "Rank") to rankedProvinceNamesAlberta_df
            #in the first column, insert the rank 
            provinceNamesAlberta_df.insert(0,'Rank', '')
            provinceNamesAlberta_df['Rank'] = ranksAlberta
            rankedProvinceNamesAlberta_df = provinceNamesAlberta_df
                
                
            print ((rankedProvinceNamesAlberta_df[:10]).to_string(index=False)) #printing the top ten rows of the data frame

        print("\n")

        #Print names for province 2
        if totalNovaScotia > 0 :
            print("The top ten " + gender + " names in " + provinceTwo + " in the year " + str(year) + " are: ")
            
            provinceNamesNovaScotia = {'Name':namesNovaScotia,'Frequency':numbersNovaScotia} #setting the array namesNovaScotia under 'Name' in the data frame and numbersNovaScotia under 'Frequency'
            provinceNamesNovaScotia_df = pd.DataFrame(provinceNamesNovaScotia) #loading the data

            provinceNamesNovaScotia = {'Name':namesNovaScotia,'Frequency':numbersNovaScotia} #setting the array namesNovaScotia under 'Name' in the data frame and numbersNovaScotia under 'Frequency'
            provinceNamesNovaScotia_df = pd.DataFrame(provinceNamesNovaScotia) #loading the data
            

            provinceNamesNovaScotia_df.sort_values(["Frequency","Name"], axis = 0, ascending=[False,True], inplace=True) #sorting the data frame in order from greatest to least 
                
            rankedProvinceNamesNovaScotia_df = provinceNamesNovaScotia_df.assign(Rank=ranksNovaScotia) #assigns new column(array ranks under "Rank") to rankedProvinceNamesNovaScotia_df
            #in the first column, insert the rank 
            provinceNamesNovaScotia_df.insert(0,'Rank', '')
            provinceNamesNovaScotia_df['Rank'] = ranksNovaScotia
            rankedProvinceNamesNovaScotia_df = provinceNamesNovaScotia_df
                
                
                
            print ((rankedProvinceNamesNovaScotia_df[:10]).to_string(index=False)) #printing the top ten rows of the data frame

            NovaScotiaTop10 = provinceNamesNovaScotia_df.head(10) #getting the top 10 rows of the data frame
            AlbertaTop10 = provinceNamesAlberta_df.head(10) #getting the top 10 rows of the data frame

            merged_df = pd.merge(NovaScotiaTop10, AlbertaTop10, on='Name', how='inner')
            top10Common = merged_df['Name']
            listTop10Common = top10Common.tolist() #putting the common names between both data frames into a list 

            print("\n")

            print("The common names between the top 10 popular names of both provinces in that year are: ") 
            for i in listTop10Common: #printing the common names that are in the top 10 of both provinces
                print(i)

    #Error check if names were not found in either of the files for a given year
    else:
        print("Year not found! Please enter a year available in both files!")

#Function 5
def rankOfNameGraph(inputFileName, name):
    x = []    #x is the year
    y = []    #y is the rank
    found = False

    #Title name
    name = name.strip().title()

    #Open file, and append data for name across each year
    with open ( inputFileName ) as csvDataFile:
        next ( csvDataFile ) 
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:
            if row[1].strip().title() == name:
                x.append(int(row[0]))
                y.append((int(row[3])))
                found = True;     

    #Check if name is found, then print results in graph function
    if(found):
        plotGraph(x,y, "Year", "Rank", "Rank of "+name+" from "+ str(x[0]) + " to " +str(x[len(x)-1]))

    #Error check if name is never found
    else:
        print("\nName not found in file!!\n")

#Graph Function
def plotGraph (x, y, xAxis, yAxis, Name):
    # Create the plot
    plt.plot(x, y)

    # Add labels to the plot
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.title(Name)

    # Display the plot
    plt.show()

#Graph for Function 6
def plotGraph2 (x, white, black, api, indigenous, mixed, hispanic, xAxis, yAxis, Name):
    # Create the plot
    plt.plot(x, white, label = "White")
    plt.plot(x, black, label = "Black")
    plt.plot(x, api, label = "Asian Pacific Islander")
    plt.plot(x, indigenous, label = "Indigenous")
    plt.plot(x, mixed, label = "Mixed")
    plt.plot(x, hispanic, label = "Hispanic")

    # Add labels to the plot
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.title(Name)

    # Display the plot
    plt.legend()
    plt.show()

#Function 6
def ethnicity(inputFile):
    #Initialize lists
    names = []
    years = []

    white = []
    black = []
    api = []
    indigenous = []
    mixed = []
    hispanic = []

    #Traverse file and append list of years
    with open ( inputFile ) as csvDataFile:
        next ( csvDataFile ) 
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:
            if(row[0].isdigit()):
                years.append(int(row[0]))
    years = list(dict.fromkeys(years))

    #Initialize start year of file
    year = years[0]

    #Open file again and traverse it by year
    with open ( inputFile ) as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:
            if(row[0].isdigit()):
                #While traversing the start year
                if(int(row[0]) == year):
                    names.append(row[1])

                #When next year is found
                else:
                    #Assign lists to dataframe
                    df = pd.DataFrame({'names':names})
                    newDf = census_ln(df, 'names')
                    
                    #Convert dataframes to float, and replace non integer values
                    newDf['pctwhite'] = newDf['pctwhite'].fillna(0).replace('(S)', 0).astype(float)
                    newDf['pctblack'] = newDf['pctblack'].fillna(0).replace('(S)', 0).astype(float)
                    newDf['pctapi'] = newDf['pctapi'].fillna(0).replace('(S)', 0).astype(float)
                    newDf['pctaian'] = newDf['pctaian'].fillna(0).replace('(S)', 0).astype(float)
                    newDf['pct2prace'] = newDf['pct2prace'].fillna(0).replace('(S)', 0).astype(float)
                    newDf['pcthispanic'] = newDf['pcthispanic'].fillna(0).replace('(S)', 0).astype(float)

                    #Append average of dataframes to list
                    white.append(newDf['pctwhite'].mean())
                    black.append(newDf['pctblack'].mean())
                    api.append(newDf['pctapi'].mean())
                    indigenous.append(newDf['pctaian'].mean())
                    mixed.append(newDf['pct2prace'].mean())
                    hispanic.append(newDf['pcthispanic'].mean())

                    #Reset names list for next year
                    names = []
                    year = year + 1

                    #Fetch data from current row into year list
                    if(int(row[0] == year)):
                        names.append(row[1])


    #Final pass of converting list names to a dataframe (for final year)
    df = pd.DataFrame({'names':names})
    newDf = census_ln(df, 'names')
    
    #Convert dataframes to float, and replace non integer values
    newDf['pctwhite'] = newDf['pctwhite'].fillna(0).replace('(S)', 0).astype(float)
    newDf['pctblack'] = newDf['pctblack'].fillna(0).replace('(S)', 0).astype(float)
    newDf['pctapi'] = newDf['pctapi'].fillna(0).replace('(S)', 0).astype(float)
    newDf['pctaian'] = newDf['pctaian'].fillna(0).replace('(S)', 0).astype(float)
    newDf['pct2prace'] = newDf['pct2prace'].fillna(0).replace('(S)', 0).astype(float)
    newDf['pcthispanic'] = newDf['pcthispanic'].fillna(0).replace('(S)', 0).astype(float)

    #Append average of dataframes to list
    white.append(newDf['pctwhite'].mean())
    black.append(newDf['pctblack'].mean())
    api.append(newDf['pctapi'].mean())
    indigenous.append(newDf['pctaian'].mean())
    mixed.append(newDf['pct2prace'].mean())
    hispanic.append(newDf['pcthispanic'].mean())
    
    #Call graph function to print results
    plotGraph2(years, white, black, api, indigenous, mixed, hispanic, "Years", "Percentages", "Average Percentage of Ethnicities")

#Function 7
def averageConsistentNames(inputFileName):
    #Declaration of lists, variables, and start year
    names    = []
    ranks    = []

    uniqueNames = []
    everyName = []
    years = []

    #Open file and create list of every name
    with open ( inputFileName ) as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:
            if(row[0].isdigit()):
                years.append(row[0])
                everyName.append(row[1])

    #Assign start year to first element of year list
    year = int(years[0])

    #Open unique file and create list of every unique names
    with open ( inputFileName ) as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',')
        for row in csvReader:
            if(row[0].isdigit() and int(row[0]) == year):
                uniqueNames.append(row[1])


    #Remove instances of unique name that do not occur in every year
    with open ( inputFileName ) as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',')
        #Traverse file rows
        for row in csvReader:
            if(row[0].isdigit()):
                #Append to names list for current year
                if int(row[0]) == year :
                    names.append(row[1])

                #When a new year is found, remove names from uniqueNames that did not occur in current year
                else:
                    #Remove names in list that did not occur in current year
                    for i in range(0,len(uniqueNames)):
                        if(uniqueNames[i] not in names):
                            uniqueNames[i] = ""

                    #Shrink list by removing null values
                    while(uniqueNames.count("")):
                        uniqueNames.remove("")

                    #Reset lists and count year for next pass
                    names    = []
                    ranks    = []
                    year = year + 1
                    
                    #Append current row to names list
                    if int(row[0]) == year :
                        names.append(row[1])

    #Pass for Final Year
    for i in range(0,len(uniqueNames)):
        if(uniqueNames[i] not in names):
            uniqueNames[i] = ""

    #Remove the empty name from list
    while(uniqueNames.count("")):
        uniqueNames.remove("")

    #Reset names and reinitialize start year
    names = []
    year = int(years[0])

    #Initialize rank list, and sort list of names
    uniqueNamesRank = [0] * len(uniqueNames)
    uniqueNames.sort()

    #Open file
    with open ( inputFileName ) as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',')

        #Traverse file rows
        for row in csvReader:
            if(row[0].isdigit()):
                #For current year, append list of names and rank
                if int(row[0]) == year :
                    names.append(row[1])
                    ranks.append(row[3])

                #When a new year is found, find rank for each unique name and assign them to list
                else:
                    #Find the rank for each unique name for the current pass in the year
                    for i in range(0,len(uniqueNames)):
                        uniqueNamesRank[i] = int(uniqueNamesRank[i]) + int(ranks[names.index(uniqueNames[i])]) 

                    #Reset lists and traverse to next year
                    names    = []
                    ranks    = []
                    year = year + 1
                    
                    #Append current row to the lists
                    if int(row[0]) == year :
                        names.append(row[1])
                        ranks.append(row[3])

        #Pass for final year
        for i in range(0,len(uniqueNames)):
                        uniqueNamesRank[i] = int(uniqueNamesRank[i]) + int(ranks[names.index(uniqueNames[i])]) 
        
        #traverse unique names list, find index in total names and add its rank to its respective rank index     
        for i in range(len(uniqueNames)):
            uniqueNamesRank[i] = int(uniqueNamesRank[i]) + int(ranks[names.index(uniqueNames[i])])
        
        #Traverse ranks, divide by total years and round the result
        for i in range(len(uniqueNamesRank)):
            uniqueNamesRank[i] = round(int(uniqueNamesRank[i]) / (int(years[len(years)-1]) - int(years[0])))
        
        #Traverse unique names, and print name with respective rank
        for i in range(len(uniqueNames)):
                print(str(uniqueNames[i]) + "," + str(uniqueNamesRank[i]))

        #find index of minimum rank in the list, and print the respective name in the index along with the value of the minium rank
        if(len(uniqueNamesRank) > 0):
            print("And the winner is " + str(uniqueNames[uniqueNamesRank.index(min(uniqueNamesRank))]) + " with an average rank of " + str(min(uniqueNamesRank)))

        #Error check if No uniqueNames were found across the entire dataset
        else:
            print("\nDataset too small for function. No names exist that are consistent across all years!")

 
def main ( argv ):

    if len(argv) < 8:
        print ( "Usage: ./main.py -a <input file one male> -b <input file one female> -c <input file two male> -d <input file two female>" )
        sys.exit(2)
    try:
        (opts, args) = getopt.getopt ( argv,"a:b:c:d:",["input=","input=","input=","input="] )

    except getopt.GetoptError:
        print ( "Usage: ./main.py -a <input file one male> -b <input file one female> -c <input file two male> -d <input file two female>" )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ( "Usage: ./main.py -a <input file one male> -b <input file one female> -c <input file two male> -d <input file two female>" )
            sys.exit()
        elif opt in ( "-a", "--input"):
            fileOneMale = arg

        elif opt in ( "-b", "--input"):
            fileOneFemale = arg

        elif opt in ( "-c", "--input"):
            fileTwoMale = arg

        elif opt in ( "-d", "--input"):
            fileTwoFemale = arg

    if(not(os.path.isfile(fileOneMale) and os.path.isfile(fileOneFemale) and os.path.isfile(fileTwoMale) and os.path.isfile(fileTwoFemale))):
        print("\nError with files!! Please ensure each file in command line argument corresponds to an existing file!!\n")
        sys.exit(2)
    
    if("FEMALE" in fileOneMale or "FEMALE" not in fileOneFemale or "FEMALE" in fileTwoMale or "FEMALE" not in fileTwoFemale):
        print("\nError!! Gender files in command line arguement not matched with arguement order!\n")
        print ( "Usage: ./main.py -a <input file one male> -b <input file one female> -c <input file two male> -d <input file two female>" )
        sys.exit(2)

    fileOneName = fileOneMale.split("_")[0]
    fileTwoName = fileTwoMale.split("_")[0]


    userInput = 0
    functionInput = 0
    functionGender = 0
    functionInputYear = 0

    while(userInput != "8"):
        print ("\n          ----- MAIN MENU -----          \n")
        print ("1. Most popular name in a year?")
        print ("2. Search for data on name in a given year")
        print ("3. Unisex names for a given year")
        print ("4. Top 10 Common for a Gender")
        print ("5. Graph the rank of name across all years")
        print ("6. Graph the average percentage of ethnicities of names across all years")
        print ("7  Finds the average rank of names across all years")
        print ("8. Exit program\n")
        print ("          ----- MENU END -----          \n")


        
        userInput = input("Choose a menu option: ")

        #Function 1
        if(userInput == "1"):
            print("\n")
            print("Select a province: [1] " + fileOneName.title() + " or [2] " + fileTwoName.title())
            functionInput = input("Enter a choice: ")

            print("Select a gender: [1] Male or [2] Female")
            functionGender = input("Enter a choice: ")

            functionInputYear = input("Enter a year: ")
            print("\n")

            if(functionInputYear.isdigit() and (functionInput == "1" or functionInput == "2") and (functionGender == "1" or functionGender == "2")):
                functionInputYear = int(functionInputYear)

                if(functionInput == "1" and functionGender == "1"):
                    topName(fileOneMale, functionInputYear)
                
                elif(functionInput == "1" and functionGender == "2"):
                    topName(fileOneFemale, functionInputYear)

                elif(functionInput == "2" and functionGender == "1"):
                    topName(fileTwoMale, functionInputYear)

                elif(functionInput == "2" and functionGender == "2"):
                    topName(fileTwoFemale, functionInputYear)

                else:
                    print("\n Incorrect input!!")
            else:
                print("\nIncorrect input!!")


        #Function 2
        elif(userInput == "2"):
            print("\n")
            print("Select a province: [1] " + fileOneName.title() + " or [2] " + fileTwoName.title())
            functionInput = input("Enter a choice: ")

            print("Select a gender: [1] Male or [2] Female")
            functionGender = input("Enter a choice: ")

            functionInputYear = input("Enter a year: ")
            functionInputName = input("Enter a name: ")
            functionInputName = functionInputName.title()
            print("\n")

            if(functionInputYear.isdigit() and (functionInput == "1" or functionInput == "2") and (functionGender == "1" or functionGender == "2")):
                functionInputYear = int(functionInputYear)

                if(functionInput == "1" and functionGender == "1"):
                    nameSearch(fileOneMale, functionInputName, functionInputYear)
                
                elif(functionInput == "1" and functionGender == "2"):
                    nameSearch(fileOneFemale, functionInputName, functionInputYear)

                elif(functionInput == "2" and functionGender == "1"):
                    nameSearch(fileTwoMale, functionInputName, functionInputYear)

                elif(functionInput == "2" and functionGender == "2"):
                    nameSearch(fileTwoFemale, functionInputName, functionInputYear)

                else:
                    print("\n Incorrect input!!")
            else:
                print("\nIncorrect input!!")


        #Function 3
        elif(userInput == "3"):
            print("\n")
            print("Select a province: [1] " + fileOneName.title() + " or [2] " + fileTwoName.title())
            functionInput = input("Enter a choice: ")

            functionInputYear = input("Enter a year: ")
            print("\n")

            if(functionInputYear.isdigit() and (functionInput == "1" or functionInput == "2")):
                if(functionInput == "1"):
                    unisexNamesFunc(fileOneMale, fileOneFemale, int(functionInputYear))

                else:
                    unisexNamesFunc(fileTwoMale, fileTwoFemale, int(functionInputYear))

            else:
                print("\nIncorrect input!!")


        #Function 4
        elif(userInput == "4"):
            print("Select a gender: [1] Male or [2] Female")
            functionGender = input("Enter a choice: ")

            functionInputYear = input("Enter a year: ")


            if(functionInputYear.isdigit() and (functionGender == "1" or functionGender == "2")):
                functionInputYear = int(functionInputYear)
                print("\n")

                if(functionGender == "1"):
                    topTenNamesFunc(fileOneMale, fileTwoMale, functionGender, functionInputYear)

                else:
                    topTenNamesFunc(fileOneFemale, fileTwoFemale, functionGender, functionInputYear)

            else:
                print("\nIncorrect input!!")



        #Function 5
        elif(userInput == "5"):
            print("\n")
            print("Select a province: [1] " + fileOneName.title() + " or [2] " + fileTwoName.title())
            functionInput = input("Enter a choice: ")

            print("Select a gender: [1] Male or [2] Female")
            functionGender = input("Enter a choice: ")

            if((functionInput == "1" or functionInput == "2") and (functionGender == "1" or functionGender == "2")):
                functionInputName = input("Enter a name: ")
                
                if(functionInput == "1" and functionGender == "1"):
                    rankOfNameGraph(fileOneMale, functionInputName)
                
                elif(functionInput == "1" and functionGender == "2"):
                    rankOfNameGraph(fileOneFemale, functionInputName)

                elif(functionInput == "2" and functionGender == "1"):
                    rankOfNameGraph(fileTwoMale, functionInputName)

                elif(functionInput == "2" and functionGender == "2"):
                    rankOfNameGraph(fileTwoFemale, functionInputName)

            else:
                print("\nIncorrect input!!")


        #Function 6
        elif(userInput == "6"):
            print("\n")
            print("Select a province: [1] " + fileOneName.title() + " or [2] " + fileTwoName.title())
            functionInput = input("Enter a choice: ")

            print("Select a gender: [1] Male or [2] Female")
            functionGender = input("Enter a choice: ")

            if((functionInput == "1" or functionInput == "2") and (functionGender == "1" or functionGender == "2")):
                
                if(functionInput == "1" and functionGender == "1"):
                    ethnicity(fileOneMale)
                
                elif(functionInput == "1" and functionGender == "2"):
                    ethnicity(fileOneFemale)

                elif(functionInput == "2" and functionGender == "1"):
                    ethnicity(fileTwoMale)

                elif(functionInput == "2" and functionGender == "2"):
                    ethnicity(fileTwoFemale)
                else:
                    print("Incorrect Input!")

            else:
                print("Incorrect Input!")
        
        elif(userInput == "7"):
            print('\n')
            print("Select a province: [1] " + fileOneName.title() + " or [2] " + fileTwoName.title())
            functionInput = input("Enter a choice: ")

            print("Select a gender: [1] Male or [2] Female")
            functionGender = input("Enter a choice: ")

            if((functionInput == "1" or functionInput == "2") and (functionGender == "1" or functionGender == "2")):
                
                if(functionInput == "1" and functionGender == "1"):
                    averageConsistentNames(fileOneMale)
                
                elif(functionInput == "1" and functionGender == "2"):
                    averageConsistentNames(fileOneFemale)

                elif(functionInput == "2" and functionGender == "1"):
                    averageConsistentNames(fileTwoMale)

                elif(functionInput == "2" and functionGender == "2"):
                    averageConsistentNames(fileTwoFemale)
                else:
                    print("Incorrect Input!")

            else:
                print("Incorrect Input!")


        #Exit choice
        elif(userInput == "8"):
            print("Exiting Program")

        #add more here if needed.

        #Error Check
        else:
            print("Incorrect Input! Please try again!")

if __name__ == "__main__":
    main ( sys.argv[1:] )

#
#   End of main.py
#