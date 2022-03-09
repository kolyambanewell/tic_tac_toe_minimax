import math
import random


class Player:
    def __init__(self, token):
        self.token = token


class Human(Player):
    def __init__(self, token):
        super().__init__(token)

    def get_move(self, game):
        spot = False
        spot_fill = None
        while not spot:
            print(f"Очередь {self.token}. Введите число от 0 до 8")
            mark = input()
            try:
                spot_fill = int(mark)
                if spot_fill not in game.spaces():
                    raise ValueError
                spot = True
            except ValueError:
                print('Выберите поле еще раз')
        return spot_fill


class Smart(Player):
    def __init__(self, token):
        super().__init__(token)

    def get_move(self, game):
        if len(game.spaces()) == 9:
            spot = random.choice(game.spaces())
        else:
            spot = self.minimax(game, self.token)['spot']
        return spot

    def minimax(self, token, player):
        max = self.token
        min = 'O' if player == 'X' else 'X'

        if token.winner == min:
            return {'spot': None,
                    'points': 1 * (token.count_empty_spaces() + 1)
                    if min == max
                    else -1 * (token.count_empty_spaces() + 1)
                    }
        elif not token.empty_spaces():
            return {'spot': None, 'points': 0}

        if player == max:
            best_spot = {'spot': None, 'points': -math.inf}
        else:
            best_spot = {'spot': None, 'points': math.inf}
        for future_spot in token.spaces():
            token.filled_space(future_spot, min)
            predict = self.minimax(token, min)

            token.board[future_spot] = ' '
            token.winner = None
            predict['spot'] = future_spot

            if player == max:
                if predict['points'] > best_spot['points']:
                    best_spot = predict
            else:
                if predict['points'] < best_spot['points']:
                    best_spot = predict
        return best_spot


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.winner = None
        self.size = 3

    def filled_space(self, spot, token):
        if self.board[spot] == ' ':
            self.board[spot] = token
            if self.win_game(spot, token):
                self.winner = token
            return True
        return False

    def diagonal(self, spot, token):
        if spot % 2 == 0:
            diagonal_left = [self.board[i] for i in [0, 4, 8]]
            if all([sign == token for sign in diagonal_left]):
                return True
        elif spot % 2 != 0:
            diagonal_right = [self.board[i] for i in [2, 4, 6]]
            if all([sign == token for sign in diagonal_right]):
                return True
        else:
            return False

    def line_row(self, spot):
        index_row = math.floor(spot / 3)
        row = self.board[index_row * 3:(index_row + 1) * 3]
        return row

    def line_column(self, spot):
        index_column = spot % 3
        column = [self.board[index_column + i * 3] for i in range(3)]
        return column

    def win_game(self, spot, token):
        row_line = self.line_row(spot)
        if all([sign == token for sign in row_line]):
            return True
        column_line = self.line_column(spot)
        if all([sign == token for sign in column_line]):
            return True
        if spot % 2 == 0:
            diagonal_win = self.diagonal(spot, token)
            if diagonal_win:
                return True
            return False

    def print_board(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def empty_spaces(self):
        return ' ' in self.board

    def count_empty_spaces(self):
        return self.board.count(' ')

    def spaces(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']


def play(game, x, o, print_board=True):
    if print_board:
        game.print_board()

    turn = 'X'
    while game.empty_spaces():
        if turn == 'X':
            space = x.get_move(game)
        else:
            space = o.get_move(game)
        if game.filled_space(space, turn):

            if print_board:
                print(f"{turn} поставил метку на {space}")
                game.print_board()
                print(' ')

            if game.winner:
                if print_board:
                    print(f"{turn} победитель!")
                return turn
            turn = 'O' if turn == 'X' else 'X'

    if print_board:
        print('Спасибо за игру, ничья!')


if __name__ == '__main__':
    print("Это игра Крестики-Нолики\n"
          "Вы будете играть против компьютера\n"
          "Желаете ли вы ходить первым?\n"
          "Введите ответ y или n")
    choose = input().lower()

    if choose == 'y':
        first_player = Human('X')
        second_player = Smart('O')
    else:
        first_player = Smart('X')
        second_player = Human('O')

    start = TicTacToe()
    play(start, first_player, second_player)
