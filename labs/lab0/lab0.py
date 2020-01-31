########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab0: Getting Started with Python
# Goal: Learning the basics of Python
# Student Name: Kevin Huynh
# Student ID: 916307020
# Student Github Username: Kevin312x
# Instructions: Complete the TODO sections for each problem
# Guidelines: Read each problem carefully, and implement them correctly. Grade is based on lab correctness/completeness
#               No partial credit will be given. Labs #0 and #1 must be submitted by Monday Feb 3rd at 7:00 pm
#               No unit test are provided for lab #0
########################################################################################################################
import unittest # don't modify this line of code.
########################## Problem 0: Print  ###########################################################################
"""
Print your name, student id and Github username
Sample output:
Name: Jose
SID: 91744100
Github Username:
"""
name = "Kevin Huynh" # TODO: your name
SID = 916307020 # TODO: your student id
git_username = "Kevin312x" # TODO: your github username
print(name)
print(SID)
print(git_username)
print('\n')

########################## Problem 1: Processing user input ############################################################
"""
Accept two int values from the user, and print their product. If their product is greater than 500, then print their sum

Sample output:
Enter the first integer: 2
Enter the second integer: 4
Result is 8
Enter the first integer: 2
Enter the second integer: 1000
Result is 1002
"""
print("Problem 1 ********************") # problem header (don't modify)
# TODO: your code here

first_integer = input("Enter the first integer: ")
second_integer = input("Enter the second integer: ")
sum = int(first_integer) + int(second_integer)
print("Result is " + str(sum))

########################## Problem 2: String Processing ##############################################################
"""
Given a string print the number of times the string "Alice" appears anywhere in the given string

For example, given the string: "Alice and Bob go to the same school. They learned today in class how to treat a lice 
infestation, and Alice found the lecture really interesting", the sample output would be: 
Alice appeared 2 times. 
"""
print("Problem 2 ********************") # problem header (don't modify)
# the given string
myString = "Alice and Bob go to the same school. They learned today in class how to treat a lice" \
           "infestation, and Alice found the lecture really interesting"
# TODO: your code here

count = 0
arr = myString.split()

for word in arr:
    if word == 'Alice':
        count = count + 1
        
print("Alice appeared " + str(count) + " times.")

########################## Problem 3: Loops ############################################################################
"""
Given a list of numbers iterate over them and output the sum of the current number and previous one.

Given: [5, 10, 24, 32, 88, 90, 100] 
Outputs: 5, 15, 34, 56, 120, 178, 190.
"""
print("Problem 3 ********************") # problem header (don't modify)
numbers = [5, 10, 24, 32, 88, 90, 100]
# TODO: your code here

numbers = [0] + numbers
for x in range(len(numbers)-1):
    sum = numbers[x] + numbers[x+1]

    if x != len(numbers)-2:
        print(sum, end=", ")
    else:
        print(sum)

########################## Problem 4: Functions/Methods/Lists ##########################################################
"""
Create the method mergeOdds(l1, l2) which takes two unordered lists as parameters, and returns a new list with all the 
odd numbers from the first a second list sorted in ascending order. Function signature is provided for you below

For example: Given l1 = [2,1,5,7,9] and l2 = [32,33,13] the function will return odds = [1,5,7,9,13,33] 
"""
print("Problem 4 ********************") # problem header (don't modify)
# function skeleton
def merge_odds(l1, l2):
    odds = []
    # TODO: your code here
    for num in l1:
        if num%2 == 1:
            odds.append(num)

    for num in l2:
        if num%2 == 1:
            odds.append(num)

    odds.sort()
    return odds
l1 = [2,1,5,7,9]
l2 = [32,33,13]
odds = merge_odds(l1, l2)
print(odds)

########################## Problem 5: Functions/Methods/Dictionaries ###################################################
"""
Refactor problem #4 to return a python dictionary instead a list where the keys are the index of the odd numbers in l1,
and l2, and the values are the odd numbers. 

For example: Given l1 = [2,1,5,7,9] and l2 = [32,33,13] the function will return odds = {1: [1, 33], 2: [5,13], 3: [7], 4: [9]} 
"""
print("Problem 5 ********************") # problem header
# function skeleton
def merge_odds(l1, l2):
    odds = {}
    # TODO: your code here
    for num in l1:
        if num%2 == 0:
            l1.remove(num)

    for num in l2:
        if num%2 == 0:
            l2.remove(num)

    max_elem = max(len(l1), len(l2))

    for x in range(max_elem):
        if x < len(l1) and x < len(l2):
            odds.update({x+1 : [l1[x], l2[x]]})
        elif x >= len(l1):
            odds.update({x+1 : [l2[x]]})
        else:
            odds.update({x+1 : [l1[x]]})

    return odds
l1 = [2,1,5,7,9]
l2 = [32,33,13]
odds = merge_odds(l1, l2)
print(odds)
