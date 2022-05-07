# Title:        numerology.py
# Author:       Lennox Stampp
# Date:         4/22/2022
# Purpose:      This module contains a class that holds the data and functions
#               to run the Use_numerology.py GUI app

#               Here is an overview of Numerology: Numerology is the science of numbers.  It has been around
#               for over 2,500 years.  You take a birthday, which yields three numbers and a name, which provides
#               another three numbers.  With those six numbers you can insights on whom a person is and find out
#               ways to improve your life, or so the belief goes.
#               The output will be six numbers.  Since the art of numerology is based off the numbers derived from
#               a person’s birth date and name code needs to be written to compute these numbers.
#               •	The Birthday Number, Life Path Number and the Attitude Number are computed
#               from the inputted Birth Date.
#               •	The Soul Number, Personality Number and Power Name Number are derived from the Inputted name.

# Numerology class
class Numerology:
    # require parameters: name and dob, from interface
    def __init__(self):
        # private attributes
        # --Placeholder text. Will need to be updated in subclass
        self.__sName = "first last"
        # -- Will be used to hold cleaned str of sName
        self.__sNewName = ""
        # --Placeholder text. Will need to be updated in subclass
        self.__sDOB = "00/00/0000"
        # -- Will be used to extract the / or - string char
        self.__sKey = ""
        # -- Will be used to hold str of dob numbers
        self.__sNewDOB = ""
        # --dictionary to hold conversion of name letters to numbers
        self.__CNVRS_LETTERS2NUMS_DCT = {
            1: "AJS",
            2: "BKT",
            3: "CLU",
            4: "DMV",
            5: "ENW",
            6: "FOX",
            7: "GPY",
            8: "HQZ",
            9: "IR"
        }

    # set __sName value
    def setName(self, newName):
        # update values
        self.__sName = newName
        self.__sNewName = self.__sName.replace(" ", "")
        self.__sNewName = self.__sName.replace("-", "")

    # set __sDOB
    def setDOB(self, newDOB):
        # update values
        self.__sDOB = newDOB
        # get key char, either / or -
        self.__sKey = self.__sDOB[2]
        # --remove key from dob string
        self.__sNewDOB = self.__sDOB.replace(self.__sKey, "")

    # get __sName value
    def getName(self):
        return self.__sName

    # get __sDOB value
    def getDOB(self):
        return self.__sDOB

    # calculate and return an attitude number
    def getAttitude(self):
        iSum = 0
        for i in range(4):
            iSum += int(self.__sNewDOB[i])

        iSum = self.reduceDigits(iSum)

        return iSum

    # If num = 0, pass 0, otherwise return num
    def numCk(self, num):
        if num < 1:
            iSum = 0
            return iSum
        else:
            iSum = num
            return iSum

    # calculate and return a birthday number
    def getBirthDayNum(self):
        iSum = 0
        for i in range(2, 4):
            iSum += int(self.__sNewDOB[i])

        iSum = self.reduceDigits(iSum)

        return iSum

    # calculate and return a life path number
    def getLifePath(self):
        iSum = 0
        for i in self.__sNewDOB:
            iSum += int(i)

        iSum = self.reduceDigits(iSum)

        return iSum

    # calculate and return a personality number
    def getPersonality(self):
        sVowels = "AEIOU"
        sNmVwls = ""

        for letter in self.__sNewName:
            if letter not in sVowels:
                sNmVwls += letter

        iSum = 0
        for (key, val) in self.__CNVRS_LETTERS2NUMS_DCT.items():
            for letter in sNmVwls:
                if letter in val:
                    iSum += key

        iSum = self.reduceDigits(iSum)

        return iSum

    # calculate and return a power name number
    def getPowerName(self):
        iSoul = self.getSoul()
        iPersonality = self.getPersonality()
        iPowerName = iSoul + iPersonality
        ireducedPN = self.reduceDigits(iPowerName)
        return ireducedPN

    # calculate and return a soul number
    def getSoul(self):
        sVowels = "AEIOU"
        sNmVwls = ""
        for v in sVowels:
            if v in self.__sName.upper():
                sNmVwls += v
        iSum = 0
        for (key,val) in self.__CNVRS_LETTERS2NUMS_DCT.items():
            for v in sNmVwls:
                if v in val:
                    iSum += key

        iSum = self.reduceDigits(iSum)

        return iSum

    # reduce multi digit number to single digit - !! -- recursion -- !!
    def reduceDigits(self, num):
        if num > 9:
            sNum = str(num)
            inewNum = int(sNum[0]) + int(sNum[1])
            if inewNum > 9:
                return self.reduceDigits(inewNum)
            else:
                return inewNum
        else:
            return num

