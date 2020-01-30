########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab1: Object Oriented Programming
# Goal: Learning Python OOP basics
# Student Name:
# Student ID:
# Student Github Username:
# Instructions: Read each problem carefully, and implement them correctly. Your grade in labs is based on passing
#               all the unit tests provided.
#               The following is an example of output for a program that pass all the unit tests.
#               Ran 3 tests in 0.000s
#               OK
#               No partial credit will be given. Labs are done in class and must be submitted by 9:45 pm on iLearn.
########################################################################################################################

import unittest # don't modify this line of code.

########################## Problem 0: Print  ###########################################################################
"""
Print your name, student id and Github username
Sample output:
Name: Jose
SID: 91744100
Github Username: joseortizcostadev
"""
name = "" # TODO: your name
SID = 000000000 # TODO: your student id
git_username = "" # TODO: your github username
print(name)
print(SID)
print(git_username)
print('\n')

########################## Problem 1: Classes I ########################################################################

class Employee (object):

    def __init__(self, name, department):
        """
        Class constructor
        :param name:
        :param department:
        """
        # TODO: create two local instance attributes and set them to the assigned parameters.


    def info(self):
        """
        TODO: Prints the info of this employee
        :return: "<employee name> works in the <department name> department"
                 i.e Sarah works in the Engineering department
        """
        return None 



########################## Problem 2: Classes II #######################################################################
"""
Department class is provided. Create three class methods as follows: 
1. set_name() to define the name of the department, 
2. add_employee() to add an employee to the department. 
3. employees() to return all the employees working in such department 
"""

class Department(object):

    def __init__(self, name=None):
        self.employees = [] # list of employees objects from problem 1.
        self.name = name

    def set_name(self, name):
        """
        Defines the department name
        :param name:
        :return: VOID
        """
        # TODO: implement your code here
        pass

    def add_employee(self, employee_name):
        """
        Adds an employee to this department
        :param employee_name:
        :return: VOID
        """
        # TODO: create a employee object
        # TODO: add the employee object to the self.employees list.
        pass

    def list_of_employees(self):
        """

        :return: the list of employees working in this department.
        """
        # TODO: return the self.employee list
        return None


print('\n')

########################## Problem 2: Inheritance #######################################################################
"""
Class Manager inherits data from class Employee. 
The manager class has a private method that provides a random id, and a public method that shows all the info about 
that employee and its manager id. 
"""

class Manager(Employee):

    def __init__(self, manager_id, name, department):
        Employee.__init__(self, name, department)
        self.managerID = manager_id

    def manager_info(self):
        """
        TODO: prints the manager info which name and department name is inhereted from the Employee class.
        :return: <info from employee> " with manager id: " <manager id>
                 i.e Sarah works in the Engineering department with manager id: 2345"
        """
        return None





######################### Unit Tests (Do not modify) ##################################################################

class TestCases(unittest.TestCase):
    def testP1(self):
        sarah = Employee("Sarah", "Engineering")
        john = Employee("John", "Marketing")
        self.assertEqual(sarah.info(), "Sarah works in the Engineering department")
        self.assertEqual(john.info(), "John works in the Marketing department")

    def testP2(self):
        eng = Department(name="Engineering")
        marketing = Department()
        marketing.set_name("Marketing")
        eng.add_employee("Alice")
        eng.add_employee("John")
        marketing.add_employee("Dana")
        marketing.add_employee("Bob")
        self.assertEqual(eng.name, "Engineering")
        self.assertEqual(marketing.name, "Marketing")
        engEmployees = eng.list_of_employees()
        markEmployees = marketing.list_of_employees()
        self.assertEqual(engEmployees[0].name, "Alice")
        self.assertEqual(engEmployees[1].name, "John")
        self.assertEqual(markEmployees[0].name, "Dana")
        self.assertEqual(markEmployees[1].name, "Bob")

    def testP3(self):
        manager_sarah = Manager(9167766, "Sarah", "Engineering")
        manager_john = Manager(2887766, "John", "Marketing")
        self.assertEqual(manager_sarah.manager_info(), "Sarah works in the Engineering department with manager id: " + str(9167766))
        self.assertEqual(manager_john.manager_info(), "John works in the Marketing department with manager id: " + str(2887766))


if __name__ == '__main__':
    unittest.main()

