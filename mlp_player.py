import numpy as np
import math
import sqlite3
import heapq  # find the n largest moves
from player import CheckersPlayer

database_name = "mlp_weights.db"
reset_db = False

class Sigmoid(object):
    # defines the sigmoid operation

    def __call__(self, x):
        return 1 / (1 + math.pow(math.e, -x))

    def derivative(self, x):
        y = self.__call__(x)
        return (1 - y) * y

class Layer(object):

    def __init__(self, nodes_in, nodes_out, name="", activation_function=Sigmoid(), reset=False):
        # (nodes_in + 1) x nodes_out sized matrix for dot product
        # one is added as an input for bias
        self.name = name
        self.weights = np.random.random((nodes_out, nodes_in + 1)) / nodes_in

        if not reset:
            self.load_params()

        self.activation_function = activation_function

    def load_params(self):
        # load the weights and bias from file
        conn = sqlite3.connect(database_name)
        c = conn.cursor()

        selectQuery = "SELECT * FROM %s" % (self.name)
        for row, column, weight in c.execute(selectQuery):
            self.weights[row, column] = weight

        conn.commit()

        conn.close()

    def save_params(self):
        # saves the state to a database
        conn = sqlite3.connect(database_name)
        c = conn.cursor()

        tableCreationQuery = "CREATE TABLE IF NOT EXISTS %s " \
            "(row integer, column integer, weight integer, PRIMARY KEY (row, column))" % \
            (self.name)
        c.execute(tableCreationQuery)
        conn.commit()

        shape = self.weights.shape
        for row in xrange(shape[0]):
            for column in xrange(shape[1]):
                insertionQuery = "INSERT OR REPLACE INTO  %s (row, column, weight) " \
                    "VALUES (%s, %s, %s)" % \
                    (self.name, row, column, self.weights[row, column])
                c.execute(insertionQuery)
        conn.commit()

        conn.close()

    def feed_forward(self, inputs):
        # assumes that inputs is of the correct dimension
        # store for future use
        self.raw_output = np.dot(self.weights, inputs)

        return np.array(map(self.activation_function, self.raw_output))

    def __del__(self):
        self.save_params()

class MLP(object):
    # performs the all the steps necessary for a single hidden layer

    def __init__(self, num_inputs, num_hidden, num_outputs, learning_rate=0.2, reset=False):
        self.hidden_layer = Layer(num_inputs, num_hidden, "hidden_nodes", reset=reset)
        self.output_layer = Layer(num_hidden, num_outputs, "output_nodes", reset=reset)
        self.eta = learning_rate

        # TODO: load in weights

    def run(self, training_data, moves_list, goodness, max_epochs=100, log=False):
        # runs the back-prop algorithm until all samples are correctly classified or
        # we reach the max number of epochs
        target_bonus = goodness * 0.2

        # assume training data is of the correct size (num_inputs)
        for epoch in xrange(max_epochs):
            for training_input, move in zip(training_data, moves_list):
                training_input = np.insert(training_input, 0, -1)  # add bias node

                # feed forward step
                hiddens = self.hidden_layer.feed_forward(training_input)

                hiddens = np.insert(hiddens, 0, -1)  # add bias node
                outputs = self.output_layer.feed_forward(hiddens)

                # back-propagation algorithm

                # for our purposes, we will set the target outputs to the outputs
                # with the exception of the move, which will be strengthened or weakened. 
                training_target = outputs
                training_target[move] = training_target[move] + target_bonus
                delta_o = (outputs - training_target) * \
                    map(self.output_layer.activation_function.derivative,
                        outputs)
                if log:
                    print "delta_o", delta_o

                delta_h = np.multiply(map(lambda x: x * (1 - x), hiddens),
                    np.dot(delta_o, self.output_layer.weights))
                if log:
                    print "delta_h", delta_h

                self.output_layer.weights -= self.eta * np.outer(delta_o, hiddens)
                self.hidden_layer.weights -= self.eta * np.outer(delta_h[1:], training_input)

                if log:
                    print "hidden weights", self.hidden_layer.weights
                    print "output_weights", self.output_layer.weights
            if log:
                print "--------"

        if log:
            print "hidden weights", self.hidden_layer.weights
            print "output_weights", self.output_layer.weights


    def feed_forward(self, input_data):
        # feed the input forward to test the output
        hiddens = self.hidden_layer.feed_forward(np.insert(input_data, 0, -1))
        outputs = self.output_layer.feed_forward(np.insert(hiddens, 0, -1))

        return outputs

    def __del__(self):
        # TODO: save weights
        pass

# training_data = np.array(
#     [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

# targets = np.array(
#     [[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#      ])

# m = MLP(32, 40, 49, reset=True)
# m.run(training_data, targets)

# print m.feed_forward([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

class MLPPlayer(CheckersPlayer):

    def __init__(self, game, board, team):
        super(MLPPlayer, self).__init__(game, board, team)

        self.mlp = MLP(32, 40, 49, reset=reset_db)
        self.board_configs = []
        self.moves_list = []  # keep track of moves made
        self.repeated_moves = 0

    def choose_move(self):
        self.possible_moves = self.get_possible_moves()

        self.choose_move_from_nnet()

    def cost_func(self, index):
        if (self.moves_list and index == self.moves_list[-1]):
            # discount repeated moves
            return self.outputs.take(index) - (self.repeated_moves+1) * 0.1
        else:
            return self.outputs.take(index)

    def choose_move_from_nnet(self):
        # feed the game config forward through the neural network
        config = self.board.get_board_config(self.team)
        self.outputs = self.mlp.feed_forward(config.flatten())

        # outputs is now a 1 x 49 matrix that represents connections between
        # tiles you can move between

        # find the best move
        best_move_index = 0
        while(best_move_index < len(self.outputs)):
            # TODO: Add something that discounts repeated moves
            # if num pieces==1 and num_pieces < enemy_pieces then do not discount?
            nlargest = heapq.nlargest(best_move_index+1, range(len(self.outputs)),
                                      self.cost_func)
            best_move = nlargest[best_move_index]

            if (self.moves_list and self.moves_list[-1] == best_move):
                self.repeated_moves += 1
            else:
                self.repeated_moves = 0

            # check if the best move is in the set of possible moves
            is_possible, start_row, start_column, end_row, end_column = \
                self.check_possible(best_move)
            if (is_possible):
                # store for training
                self.board_configs.append(config)
                self.moves_list.append(best_move)

                self.game.select_move(start_row, start_column, end_row, end_column)
                return
            else:
                best_move_index += 1

        # if no best move is selected, the game is over?
        self.game.game_over()
        return

    def select_additional_jump(self, source_row, source_column):
        # do something very similar to choose move, except the possible_moves
        # are restricted
        _, moves = self.board.get_possible_moves(source_row, source_column)
        self.possible_moves = {}
        self.possible_moves[source_row, source_column] = moves
        self.choose_move_from_nnet()

    def check_possible(self, flattened_grid_index):
        # flattened grid index is a index into a 49x1 grid, needs conversion
        row, column = MoveConversion.num_to_7x7(flattened_grid_index)

        (first_row, first_column, second_row, second_column) = \
            MoveConversion.output_grid_to_move_board(row, column)

        # check if either the first row/column is in the list of possible moves
        if ((first_row, first_column) in self.possible_moves):
            # check if the second row/column is in the second list
            move_list = self.possible_moves[first_row, first_column]
            if ((second_row, second_column) in move_list):
                # take that move
                return (True, first_row, first_column, second_row, second_column)
            # check jumps in all downward directions
            elif ((second_row + 1, second_column + 1) in move_list):
                return (True, first_row, first_column, second_row+1, second_column+1)
            elif ((second_row + 1, second_column - 1) in move_list):
                return (True, first_row, first_column, second_row+1, second_column-1)
        elif ((second_row, second_column) in self.possible_moves):
            move_list = self.possible_moves[second_row, second_column]
            if ((first_row, first_column) in move_list):
                return (True, second_row, second_column, first_row, first_column)
            # check jumps in all upwards directions
            elif ((first_row - 1, first_column + 1) in move_list):
                return (True, second_row, second_column, first_row-1, first_column+1)
            elif ((first_row - 1, first_column - 1) in move_list):
                return (True, second_row, second_column, first_row-1, first_column-1)
        
        return (False, None, None, None, None)

    def train(self, goodness):
        # train the MLP
        self.mlp.run(self.board_configs, self.moves_list, goodness, max_epochs=1)


class MoveConversion(object):
    # converts between a 7x7 grid and the 8x8 checkers board

    # x o x o x o x o
    # o^x^o^x^o^x^o^x
    # x o x o x o x o
    # o x o x o x o x
    # x o x o x o x o
    # o x o x o x o x
    # x o x o x o x o
    # o x o x o x o x
    #
    # The 7x7 grid represents the spaces between the regular 8x8 grid
    # so (0,0) in the 7x7 would correspond to (0,1)-(1,0)
    # (0,1) would be (0,1)-(1,2)
    # (0,2) would be (0,3)-(1,2)
    # (1,6) would be (1,6)-(2,7)
    # 
    # first number is same row, column boosted up to even #
    # seconds is row+1, column boosted up to even #

    @staticmethod
    def output_grid_to_move_board(row, column):
        # returns two tuples, one for each of the tiles involved in the move
        first_row = row
        first_column = column if ((row % 2 == 0 and column % 2 == 1)
                                  or (row % 2 == 1 and column % 2 == 0)) \
                              else column + 1

        second_row = row + 1
        second_column = column if (((row+1) % 2 == 0 and column % 2 == 1)
                                   or ((row+1) % 2 == 1 and column % 2 == 0)) \
                               else column + 1
        
        return (first_row, first_column, second_row, second_column)

    @staticmethod
    def move_board_to_output_grid(row1, column1, row2, column2):
        # returns a single tuple, the row and column associated in the 7x7 grid

        # find the min row
        min_row = row1 if row1 < row2 else row2
        min_column = column1 if column1 < column2 else column2
        
        ret_row = min_row
        ret_column = min_column

        return (ret_row, ret_column)

    @staticmethod
    def num_to_7x7(number):
        row = number / 7
        column = number % 7

        return row, column
