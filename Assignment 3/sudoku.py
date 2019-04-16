import sys
import numpy as np
from random import shuffle, random, sample, randint
from copy import deepcopy
from math import exp

class SudokuPuzzle(object):
    def __init__(self, data=None, original_entries=None):
        
        if data is None:
            self.data = np.array([5,3,0,0,7,0,0,0,0,
                                  6,0,0,1,9,5,0,0,0,
                                  0,9,8,0,0,0,0,6,0,
                                  8,0,0,0,6,0,0,0,3,
                                  4,0,0,8,0,3,0,0,1,
                                  7,0,0,0,2,0,0,0,6,
                                  0,6,0,0,0,0,2,8,0,
                                  0,0,0,4,1,9,0,0,5,
                                  0,0,0,0,8,0,0,7,9])
        else:
            self.data = data
    
        if original_entries is None:
            self.original_entries = np.arange(81)[self.data > 0]
        else:
            self.original_entries = original_entries
            
    def randomize_on_zeroes(self):
        
        for num in range(9):
            block_indices = self.get_block_indices(num)
            block = self.data[block_indices]
            zero_indices = [ind for i,ind in enumerate(block_indices) if block[i] == 0]
            to_fill = [i for i in range(1,10) if i not in block]
            shuffle(to_fill)
            for ind, value in zip(zero_indices, to_fill):
                self.data[ind] = value
            
    def get_block_indices(self, k, ignore_originals=False):
        
        row_offset = (k // 3) * 3
        col_offset = (k % 3)  * 3
        indices = [col_offset + (j%3) + 9*(row_offset + (j//3)) for j in range(9)]
        if ignore_originals:
            indices = filter(lambda x:x not in self.original_entries, indices)
        return indices
        
    def get_column_indices(self, i, type="data index"):
        
        if type=="data index":
            column = i % 9
        elif type=="column index":
            column = i
        indices = [column + 9 * j for j in range(9)]
        return indices
        
    def get_row_indices(self, i, type="data index"):
        
        if type=="data index":
            row = i // 9
        elif type=="row index":
            row = i
        indices = [j + 9*row for j in range(9)]
        return indices
        
    def view_results(self):
        
        def notzero(s):
            if s <> 0: return str(s)
            if s == 0: return "'"
            
        results = np.array([self.data[self.get_row_indices(j, type="row index")] for j in range(9)])
        out_s = ""
        for i, row in enumerate(results):
            if i%3==0: 
                out_s += "="*25+'\n'
            out_s += "| " + " | ".join([" ".join(notzero(s) for s in list(row)[3*(k-1):3*k]) for k in range(1,4)]) + " |\n"
        out_s += "="*25+'\n'
        print out_s
        
    def score_board(self):
        
        score = 0
        for row in range(9):
            score -= len(set(self.data[self.get_row_indices(row, type="row index")]))
        for col in range(9):
            score -= len(set(self.data[self.get_column_indices(col,type="column index")]))
        return score
        
    def make_candidate_data(self):

        new_data = deepcopy(self.data)
        block = randint(0,8)
        num_in_block = len(self.get_block_indices(block, ignore_originals=True))
        random_squares = sample(range(num_in_block),2)
        square1, square2 = [self.get_block_indices(block, ignore_originals=True)[ind] for ind in random_squares]
        new_data[square1], new_data[square2] = new_data[square2], new_data[square1]
        return new_data

def sudoku_solver(input_data=None):

    SP = SudokuPuzzle(input_data)
    print "Original Puzzle:"
    SP.view_results()
    SP.randomize_on_zeroes()
    best_SP = deepcopy(SP)
    current_score = SP.score_board()
    best_score = current_score
    T = .5
    count = 0
    
    while (count < 400000):
        try:
            if (count % 1000 == 0): 
                print "Iteration %s,    \tT = %.5f, \tbest_score = %s, \tcurrent_score = %s"%(count, T, 
                                                               best_score, current_score)
            candidate_data = SP.make_candidate_data()
            SP_candidate = SudokuPuzzle(candidate_data, SP.original_entries)
            candidate_score = SP_candidate.score_board()
            delta_S = float(current_score - candidate_score)
            
            if (exp((delta_S/T)) - random() > 0):
                SP = SP_candidate
                current_score = candidate_score 
        
            if (current_score < best_score):
                best_SP = deepcopy(SP)
                best_score = best_SP.score_board()
        
            if candidate_score == -162:
                SP = SP_candidate
                break
    
            T = .99999*T
            count += 1
        except:
            print "Hit an inexplicable numerical error. It's a random algorithm-- try again."            
    if best_score == -162:
        print "\nSOLVED THE PUZZLE."
    else:
        print "\nDIDN'T SOLVE. (%s/%s points). It's a random algorithm-- try again."%(best_score,-162)
    print "\nFinal Puzzle:"
    SP.view_results()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            input_puzzle = np.array([int(s) for s in sys.argv[1]])
        except:
            print "Puzzle must be 81 consecutive integers, 0s for skipped entries."
        assert len(input_puzzle) == 81, "Puzzle must have 81 entries."
        sudoku_solver(input_data=input_puzzle)
    else:
        sudoku_solver()

