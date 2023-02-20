'''
The purpose of this project to utlize the tools of Multiprocessing that is teached in this course and
implement modular cellular life simulator by running first 100 steps. For multiprocessing I used the Multiprocessing
library in that I used Pool classes and argparse to parse CMD commands
Created by: Suchith Chandan Reddy Pinreddy
Created and Tested in HPCC: 12/01/2022
'''
from multiprocessing import Pool
import argparse
'''
The purpose of the function is to collect the neighbors of each cell and keep track all the '+' characters and determine whether cell is going
to be alive or dead in next cycle.
Arguments: Integer and 2D array
Retrun: Array
'''
def collectingNeighborInfo(r,matrix):
  matrixCopy = matrix
  lenth = len(matrix[0]) #access the length of the columns in matrix
  lenth1 = len(matrix) #access the length of the rows in matrix
  x = r+1 #access the row below
  y = r-1 #access the row above
  colMatrix = ['']*len(matrixCopy[0]) #creation empty list of characters to the length of the columns in the matrix
  for col in range(lenth):
    z = col - 1 #access the left side of the column
    w = col +1  #access the right side of the column
    counter = 0 #counter
    if(matrixCopy[r][w%lenth]=='+'):
      counter+=1
    if(matrixCopy[r][z%lenth]=='+'):
      counter+=1
    if(matrixCopy[x % lenth1][col]=='+'):
      counter+=1
    if(matrixCopy[x % lenth1][w % lenth]=='+'):
      counter+=1
    if(matrixCopy[x % lenth1][(z % lenth)]=='+'):
      counter+=1
    if(matrixCopy[y%lenth1][col] =='+'):
      counter+=1
    if(matrixCopy[y % lenth1][w % lenth] =='+'):
      counter+=1
    if(matrixCopy[y % lenth1][z % lenth] =='+'):
      counter+=1
    if(matrixCopy[r][col] == '-'):
      if(counter ==2 or counter ==3 or counter ==5 or counter ==7 or counter ==11): #checks if the total cells that are + in neighbors are prime or not when the cell that is -
        colMatrix[col] = '+'
      else:
        colMatrix[col] = '-'
    elif (matrix[r][col] == '+'):
      if(counter ==2 or counter ==4 or counter ==6): #checks if the total cells that are + in neighbors either two or four or six when the cell that is +
        colMatrix[col] = '+'
      else:
        colMatrix[col] = '-'

  return colMatrix
'''
The purpose of this function is that it acts like a main functions and in this function it parses command prompt arguments and
runs multiprocesssing and writes it in the binary files.
Arguments: N/A
Return: N/A
'''
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i','--input',action = 'store', help="Provide Input file location", type = str, required=True) #usage of argparser library parse CMD commands
  parser.add_argument('-t','--threads', help='Provide Threads in integer > 0', type=int, default = 1)
  parser.add_argument('-o','--output', help="Provide Output file location", type = str, required=True)
  arguments=parser.parse_args()
  if(arguments.threads<=0):
    exit()
  multidimArray = []
  filePointer = open(arguments.input) #opens the binary file and converts into the matrix
  for i in filePointer:
    if i != "\n": #ignores the new line character in between rows
        multidimArray.append(i.strip()) #removes the new line character after each string
  filePointer.close()
  print("Project :: R11704958")
  rows = len(multidimArray)
  columns = len(multidimArray[0])
  iterator =[]
  for i in range(rows):
    tuple1 = (i,multidimArray) #binds the row numbers with the matrix
    iterator.append(tuple1) #appended the tuple data set in the list
  updatedMatrix = None
  p = Pool(processes=arguments.threads) #divides the task automatically based on the thread arguments
  for i in range(100): #running the 100 time steps
    updatedMatrix = p.starmap(collectingNeighborInfo,iterator) #does the multiprocessing by using starmap function in which it takes the function that you want to do multiprocessing and the iterable which in this case is a list consisting with tuples
    iterator = []
    for j in range(rows):
      tuple1 = (j,updatedMatrix) #updates to the next time step matrix
      iterator.append(tuple1)
  fp_Write = open(arguments.output,'w')
  for row in range(rows):
    conv_string = ''
    for column in range(columns):
        conv_string+= updatedMatrix[row][column]
    if row!=rows-1:
        conv_string+='\n'
    fp_Write.write(conv_string)
  fp_Write.close()
'''
The purpose of this function is to run the driver function
Arguments: N/A
Return: N/A
'''
if __name__ == '__main__':
  main()
