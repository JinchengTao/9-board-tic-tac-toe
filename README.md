# 9-board-tic-tac-toe
This program implements alpha-beta pruning search algorithm with default depth-limited of 5. A self-defined heuristic
function (describe below) is to evaluate the value when it reaches the depth limit. The AI player takes about 0.5 second to
calculate the move in the beginning but as the game develops it will be faster. The AI player is able to effectively
beat human and perform as well as "lookt" at the same depth. But in order to achieve better performance, it takes more
time to calculate the move with increasing search depth.

In this game, the state of the board is represented using a numpy arraylist of 9 9-sized boards. The value of an empty
position is 0, the position occupied by the AI player has value 1 and the position occupied by the opponent has value -1.
The function alphabeta() starts alpha-beta pruning searching and returns the best move. The function max_decision() represents
max decision, and the function min_decision() represents min decision respectively. The function win() and lose() check
whether this move checkmates. The function of value() returns the heuristic value. The judgement of draw is involved
in the function max_decision() and min_decision(). The method of getting available moves is involved in the function
max_decision() and min_decision() as well.

We define X_n as the number of rows, columns or diagonals with exactly n X's and no O's. Similarly, O_n is the number of rows,
columns or diagonals with just n O's. We define L_i as the number of the empty positions which can point to subboard_i.
C represents the weight of the line which exactly contains two X's or O's, C is set to 6 after the AI player plays against
itself thousands times. For the nonterminal situations, we use a linear evaluation function defined as:

`Equl(i) = (C * (X_2(i) - O_2(i)) + (X_1(i) - O_1(i))) * L_i`

In addition, in the early period, the difference between situations is relatively small because of limited moves, so we get
the value of each position by simulating 1,000,000 random games. Then, we combine them in the beginning, total value will
be the sum of all values of all 9 boards.
