"""
Each futoshiki board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8

Empty values in the board are represented by 0

An * after the letter indicates the inequality between the row represented
by the letter and the next row.
e.g. my_board['A*1'] = '<' 
means the value at A1 must be less than the value
at B1

Similarly, an * after the number indicates the inequality between the
column represented by the number and the next column.
e.g. my_board['A1*'] = '>' 
means the value at A1 is greater than the value
at A2

Empty inequalities in the board are represented as '-'

"""
import sys

#======================================================================#
#*#*#*# Optional: Import any allowed libraries you may need here #*#*#*#
#======================================================================#
import numpy as np
import time
from collections import defaultdict
#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

ROW = "ABCDEFGHI"
COL = "123456789"

class Board:
    '''
    Class to represent a board, including its configuration, dimensions, and domains
    '''
    
    def get_board_dim(self, str_len):
        '''
        Returns the side length of the board given a particular input string length
        '''
        d = 4 + 12 * str_len
        n = (2+np.sqrt(4+12*str_len))/6
        if(int(n) != n):
            raise Exception("Invalid configuration string length")
        
        return int(n)
        
    def get_config_str(self):
        '''
        Returns the configuration string
        '''
        return self.config_str
        
    def get_config(self):
        '''
        Returns the configuration dictionary
        '''
        return self.config
        
    def get_variables(self):
        '''
        Returns a list containing the names of all variables in the futoshiki board
        '''
        variables = []
        for i in range(0, self.n):
            for j in range(0, self.n):
                variables.append(ROW[i] + COL[j])
        return variables
    
    def convert_string_to_dict(self, config_string):
        '''
        Parses an input configuration string, retuns a dictionary to represent the board configuration
        as described above
        '''
        config_dict = {}
        
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_string[0]
                config_string = config_string[1:]
                
                config_dict[ROW[i] + COL[j]] = int(cur)
                
                if(j != self.n - 1):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    config_dict[ROW[i] + COL[j] + '*'] = cur
                    
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    config_dict[ROW[i] + '*' + COL[j]] = cur
                    
        return config_dict
        
    def print_board(self):
        '''
        Prints the current board to stdout
        '''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    print('_', end=' ')
                else:
                    print(str(cur), end=' ')
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        print(' ', end=' ')
                    else:
                        print(cur, end=' ')
            print('')
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        print(' ', end='   ')
                    else:
                        print(cur, end='   ')
            print('')
    
    def __init__(self, config_string):
        '''
        Initialising the board
        '''
        self.config_str = config_string
        self.n = self.get_board_dim(len(config_string))
        if(self.n > 9):
            raise Exception("Board too big")
            
        self.config = self.convert_string_to_dict(config_string)
        self.domains = self.reset_domains()
        
        self.forward_checking(self.get_variables())


    def __str__(self):
        '''
        Returns a string displaying the board in a visual format. Same format as print_board()
        '''
        output = ''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    output += '_ '
                else:
                    output += str(cur)+ ' '
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        output += '  '
                    else:
                        output += cur + ' '
            output += '\n'
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        output += '    '
                    else:
                        output += cur + '   '
            output += '\n'
        return output
        
    def reset_domains(self):
        '''
        Resets the domains of the board assuming no enforcement of constraints
        '''
        domains = {}
        variables = self.get_variables()
        for var in variables:
            if(self.config[var] == 0):
                domains[var] = [i for i in range(1,self.n+1)]
            else:
                domains[var] = [self.config[var]]
                
        self.domains = domains
                
        return domains
        
    def forward_checking(self, reassigned_variables):
        '''
        Runs the forward checking algorithm to restrict the domains of variables based on the value
        of the assigned variable.
        ''' 
        for variable in reassigned_variables:
            value = self.config[variable]
            if value != 0:
                row_variable, col_variable = variable[0], variable[1]

                # Row constraint
                for col in COL[:self.n]:
                    neighbor = row_variable + col
                    if neighbor != variable and self.config[neighbor] == 0:
                        if value in self.domains[neighbor]:
                            self.domains[neighbor].remove(value)
                        if not self.domains[neighbor]:
                            return False
                
                # Column constraint
                for row in ROW[:self.n]:
                    neighbor = row + col_variable
                    if neighbor != variable and self.config[neighbor] == 0:
                        if value in self.domains[neighbor]:
                            self.domains[neighbor].remove(value)
                        if not self.domains[neighbor]:
                            return False

                # Inequality constraint
                for v1, inequality, v2 in get_inequalities(self.config):
                    if v1 == variable and self.config[v2] == 0:
                        new_domain = []
                        for val in self.domains[v2]:
                            if calculate_inequality(value, inequality, val):
                                new_domain.append(val)
                        
                        self.domains[v2] = new_domain

                        if not self.domains[v2]:
                            return False

                    if v2 == variable and self.config[v1] == 0:
                        new_domain = []
                        for val in self.domains[v1]:
                            if calculate_inequality(val, inequality, value):
                                new_domain.append(val)
                        
                        self.domains[v1] = new_domain

                        if not self.domains[v1]:
                            return False
                
        return True
        #=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#
        
    #=================================================================================#
	#*#*#*# Optional: Write any other functions you may need in the Board Class #*#*#*#
	#=================================================================================#
    def select_unassigned_variable(self):
        unassigned_variables = []
        for variable, domain in self.domains.items():
            if self.config[variable] == 0:
                unassigned_variables.append(variable)
        
        minimum_length = float("inf")
        minimum_domain = None
        for variable in unassigned_variables:
            if len(self.domains[variable]) < minimum_length:
                minimum_length = len(self.domains[variable])
                minimum_domain = variable
        
        return minimum_domain

    def update_config_str(self):
        updated_config_str = ""
        for i in range(self.n):
            for j in range(self.n):
                updated_config_str += str(self.config[ROW[i] + COL[j]])
                
                if j != self.n - 1:
                    updated_config_str += self.config.get(ROW[i] + COL[j] + '*', '-')
            
            if i != self.n - 1:
                for j in range(self.n):
                    updated_config_str += self.config.get(ROW[i] + '*' + COL[j], '-')

        self.config_str = updated_config_str
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

#================================================================================#
#*#*#*# Optional: You may write helper functions in this space if required #*#*#*#
#================================================================================#        
def get_inequalities(board):
    inequalities = set()
    for key, value in board.items():
        if len(key) == 3 and '*' in key and value != "-":
            if key[1] == '*': 
                v1 = key[0] + key[2]
                v2 = ROW[ROW.index(key[0]) + 1] + key[2] 
                inequalities.add((v1, value, v2))

            if key[2] == '*':  
                v1 = key[0] + key[1]  
                v2 = key[0] + COL[COL.index(key[1]) + 1]
                inequalities.add((v1, value, v2))
    
    return inequalities

def calculate_inequality(v1, inequality, v2):
    if inequality == '<':
        return v1 < v2
    if inequality == '>':
        return v1 > v2
#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

def backtracking(board):
    '''
    Performs the backtracking algorithm to solve the board
    Returns only a solved board
    '''
    #==========================================================#
	#*#*#*# TODO: Write your backtracking algorithm here #*#*#*#
	#==========================================================#
    check = True
    for value in board.config.values():
        if value == 0:
            check = False
    if check:
        return board

    variable = board.select_unassigned_variable()
    for value in board.domains[variable]:
        board.config[variable] = value

        domains_copy = {}
        for var in board.domains:
            domains_copy[var] = board.domains[var].copy()
        
        board.domains[variable] = [value]

        if board.forward_checking([variable]):
            result = backtracking(board)
            if result:
                return result

        board.config[variable] = 0
        board.domains = domains_copy

    return None
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#
    
def solve_board(board):
    '''
    Runs the backtrack helper and times its performance.
    Returns the solved board and the runtime
    '''
    #================================================================#
	#*#*#*# TODO: Call your backtracking algorithm and time it #*#*#*#
	#================================================================#
    start_time = time.time()
    solved_board = backtracking(board)
    end_time = time.time()
    solved_board.update_config_str()

    return solved_board, end_time - start_time 
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

def print_stats(runtimes):
    '''
    Prints a statistical summary of the runtimes of all the boards
    '''
    min = 100000000000
    max = 0
    sum = 0
    n = len(runtimes)

    for runtime in runtimes:
        sum += runtime
        if(runtime < min):
            min = runtime
        if(runtime > max):
            max = runtime

    mean = sum/n

    sum_diff_squared = 0

    for runtime in runtimes:
        sum_diff_squared += (runtime-mean)*(runtime-mean)

    std_dev = np.sqrt(sum_diff_squared/n)

    print("\nRuntime Statistics:")
    print("Number of Boards = {:d}".format(n))
    print("Min Runtime = {:.8f}".format(min))
    print("Max Runtime = {:.8f}".format(max))
    print("Mean Runtime = {:.8f}".format(mean))
    print("Standard Deviation of Runtime = {:.8f}".format(std_dev))
    print("Total Runtime = {:.8f}".format(sum))


if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running futoshiki solver with one board $python3 futoshiki.py <input_string>.
        print("\nInput String:")
        print(sys.argv[1])
        
        print("\nFormatted Input Board:")
        board = Board(sys.argv[1])
        board.print_board()
        
        solved_board, runtime = solve_board(board)
        
        print("\nSolved String:")
        print(solved_board.get_config_str())
        
        print("\nFormatted Solved Board:")
        solved_board.print_board()
        
        print_stats([runtime])

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(solved_board.get_config_str())
        outfile.write('\n')
        outfile.close()

    else:
        # Running futoshiki solver for boards in futoshiki_start.txt $python3 futoshiki.py

        #  Read boards from source.
        src_filename = 'futoshiki_start.txt'
        try:
            srcfile = open(src_filename, "r")
            futoshiki_list = srcfile.read()
            srcfile.close()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        
        runtimes = []

        # Solve each board using backtracking
        for line in futoshiki_list.split("\n"):
            
            print("\nInput String:")
            print(line)
            
            print("\nFormatted Input Board:")
            board = Board(line)
            board.print_board()
            
            solved_board, runtime = solve_board(board)
            runtimes.append(runtime)
            
            print("\nSolved String:")
            print(solved_board.get_config_str())
            
            print("\nFormatted Solved Board:")
            solved_board.print_board()

            # Write board to file
            outfile.write(solved_board.get_config_str())
            outfile.write('\n')

        # Timing Runs
        print_stats(runtimes)
        
        outfile.close()
        print("\nFinished all boards in file.\n")
