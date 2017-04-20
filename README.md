This is an automated sudoku solver developed when I was taking the Udacity AI course. It uses some simple constraint propagation techniques before resorting to a depth search.
The input is a string of the sudoku board with the cells listed from top right going across and downward to bottom left with periods to signify empty cells. 
If you want to also line up digits 1-9 on the diagonal you can type yes/y in the second prompt. However, a regular sudoku board may not have a solution with the diagonal constraint and would throw an error. In general, I did not dress up any error handling so if the input is wrong ugly python errors will pop up. 

Example of the program (output looks prettier in the terminal than in the .md file):

Googling the words "hardest sudoku", I find this link with the below board

http://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html

>>>$ python sudoku.py


WELCOME TO THE SUDOKU SOLVER!


Input the sudoku board as a string. It should be 81 characters long and have periods in the place of the empty cells:
>>>$ 8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..


Is this a diagonal sudoku? Enter y/n
>>>$ n

 Starting board:

 
   
8 . . |. . . |. . . 

. . 3 |6 . . |. . . 

. 7 . |. 9 . |2 . . 

------+------+------

. 5 . |. . 7 |. . . 

. . . |. 4 5 |7 . . 

. . . |1 . . |. 3 .

------+------+------

. . 1 |. . . |. 6 8 

. . 8 |5 . . |. 1 . 

. 9 . |. . . |4 . .


 Solved board:


8 1 2 |7 5 3 |6 4 9 

9 4 3 |6 8 2 |1 7 5 

6 7 5 |4 9 1 |2 8 3 

------+------+------

1 5 4 |2 3 7 |8 9 6 

3 6 9 |8 4 5 |7 2 1 

2 8 7 |1 6 9 |5 3 4 

------+------+------

5 2 1 |9 7 4 |3 6 8 

4 3 8 |5 2 6 |9 1 7 

7 9 6 |3 1 8 |4 5 2
