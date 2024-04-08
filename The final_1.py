class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы стреляете за пределы игрового поля"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass

class Dot:
    def __init__(self, x , y, ):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'Dot: {self.x, self.y}'

class Ship:
    def __init__(self, bow,  len, orient, hp):
        self.bow = bow
        self.len = len
        self.orient = orient
        self.hp = hp

    def dots(self):
        ship_dots = []
        for i in range (self.len):
            x = self.bow.x
            y = self.bow.y
            if self.orient == 0:
                x += i
            elif self.orient == 1:
                y += i
            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots



class Board:
    def __init__(self, hide=False, size=6,):
        self.size = size
        self.hide = hide
        self.count = 0
        self.field = [["0"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def __str__(self):
        cell = ""
        cell += "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            cell += f"\n{i + 1}  | " + " | ".join(row) + " |"

        if self.hide:
            cell = cell.replace("■", "0")
        return cell

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = ""
                    self.busy.append(cur)
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)
        for ship in self.ships:
            if ship.shooten(d):
                ship.hp -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль повреждён!")
                    return True
        self.field[d.x][d.y] = "✸"
        print("Промах!")
        return False

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print("Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hide = True
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("------------------------")
        print("    Здравствуйте, вы вошли в игру    ")
        print("            морской бой        ")
        print("------------------------")
        print("    формат ввода: x y   ")
        print("    x - номер строки    ")
        print("    y - номер столбца   ")
    def loop(self):
        num = 0
        while True:
            self.print_boards()
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("✅ Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("✅ Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.print_boards()
                print("-" * 20)
                print("✸✸✸Пользователь выиграл!✸✸✸")
                break

            if self.us.board.defeat():
                self.print_boards()
                print("-" * 20)
                print("✸✸✸Компьютер выиграл!✸✸✸")
                break
            num += 1
    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()