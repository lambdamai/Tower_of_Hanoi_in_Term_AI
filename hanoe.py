#!/usr/bin/env python3

import re, copy, sys, curses
import AI

#Вместо len лучше было бы вставить hoops_number

class stack_pyramid(list):
    def __init__(self, arr = []):
        self.hoops_number = len(arr)
        list.__init__(self)
        for i in arr:
            self.append(i)
    def push(self, value):
        if not(self.hoops_number) or value <= self[-1]:
            self.hoops_number+=1
            self.append(value)
        else:
            raise Exception("ERROR: YOUR PYRAMID LIKE LEANING TOWER OF PISA")
    def pop(self):
        try:
            elem = self[-1]
            del self[-1]
            self.hoops_number-=1
            return elem
        except:
            raise Exception("ERROR: EMPTY PYRAMID.")
    def get_top(self):
        try:
            return self[-1]
        except:
            raise Exception("ERROR: EMPTY PYRAMID.")
    def get_all(self):
        return self
    def get_len(self):
        return self.hoops_number
        
class Game:

    #high_cmd = re.compile('\d+')
    
    def __init__(self, ai = None, who = "Player", lvl = 5, istream = input, ostream = print):
        self.status = "Running"
        self.who = who
        self.istream = istream
        self.ai = ai
        self.lvl = lvl
        self.count = 0
        arr = list(range(lvl+1))[1:]
        arr.reverse()
        self.pyramids = [
            stack_pyramid( copy.copy(arr) ),
            stack_pyramid(), 
            stack_pyramid()
        ]
        self.win_combination = arr
        if self.who != "AI":
            self.screen = curses.initscr()
        self.highlighted = -1;
    
    def init(self):
        if self.who != "AI":
            curses.noecho()
            curses.cbreak()
            self.screen.keypad(True)
            self.draw()
        try:
            self.process()
        except (Exception, KeyboardInterrupt) as e:
            if self.who != "AI":
                self.screen.clear()
                curses.nocbreak()
                self.screen.keypad(False)
                curses.echo()
                curses.endwin()
            raise e
    
    def process(self):
        #(user_input[0] != "exit"  or user_input[0] != "e") and
        while( self.status == "Running"):
            pyr_num = 0
            if self.who == "Player":
                pyr_num = self.screen.getch() - 48
                #try: pyr_num = int(pyr_num)
                #except: continue
                if pyr_num < 1 or pyr_num > 3: continue
                if self.highlighted == -1:
                    self.highlighted = pyr_num
                    continue
            elif self.who == "AI":
                if self.count > 1000:
                    self.status = "Stopped"
                    print ("AI FAILED (TO MANY MOVES)")
                move = self.ai(copy.deepcopy(self.pyramids))
                if(  move[0] >= 1 and move[0] <= 3 ) and ( move[1] >= 1 and move[1] <= 3 ):
                    self.highlighted = move[0]
                    pyr_num = move[1]
                else:
                    self.status = "Stopped"
                    self.situation()
                    raise Exception("AI FAILED (FORBIDDEN MOVE)")
            else:
                self.status = "Stopped"
                raise Exception("WRONG PLAYER TYPE")
            from_ = self.highlighted-1
            to_ = pyr_num-1
            self.highlighted = -1
            try:
                self.pyramids[to_].push( self.pyramids[from_][-1] )
                self.pyramids[from_].pop()
                self.count+=1
            except:
                if self.who == "AI":
                    self.status = "Stopped"
                    self.situation()
                    raise Exception("AI FAILED (FORBIDDEN MOVE)")
            self.situation()
            '''else: break
            if(  moves[0] > 0 and moves[0] < 4 ) and ( moves[1] > 0 and moves[1] < 4 ):
                self.count+=1
                from_ = moves[0]-1
                to_ = moves[1]-1
            else:
                print("WRONG MOVE")'''
    def draw(self, highlighted = -1):
        if self.who != "AI":
            self.screen.clear()
            self.screen.border(0)
        if self.status == "Running":
            if self.who != "AI": 
                self.screen.addstr(3,3,"COUNT: " + str(self.count))
                self.screen.addstr(4,3,"| "*3)
            else: 
                print("COUNT: " + str(self.count))
                print("| "*3)
            for g in range(self.lvl):
                st = ""
                for pyramid in self.pyramids:
                    try:
                        st += str(pyramid[self.lvl-g-1]) + " "
                    except IndexError:
                        st += "| "
                if self.who != "AI": 
                    self.screen.addstr(5+g,3, st)
                else:
                    print(st)
        elif self.status == "Stopped":
            if self.who != "AI": self.screen.addstr(3,3,self.status)
            else: print(self.status)
        elif self.status == "Win":
            if self.who != "AI": self.screen.addstr(3,3,"YOU WIN!")
            else: print("YOU WIN")
        else: 
            if self.who != "AI": self.screen.addstr(3,3,"UNKNOWN STATUS")
            else: print("UNKNOWN STATUS")
        if self.who != "AI": self.screen.refresh()
    def situation(self):
        #self.count+=1
        if self.pyramids[2] == self.win_combination:
            self.status = "Win"
            #print("YOU WIN")
        self.draw()
  
def main():
    game = Game()
    game.init()
    #game.draw()
    #game.process()
    
def ai_mode():
    game = Game(who = "AI", ai = AI.AI)
    game.init()
    
def help():
        print(u"\nПРАВИЛА:")
        print(u"Подробнее тут - https://ru.wikipedia.org/wiki/Ханойская_башня")
        print(u"Если вкратце, то нам даны 3 стержня, на первом из которых расположены N элементов")
        print(u"(В оригинале эти элементы - кольца разного диаметра, в нашем случае это числа) в порядке убывания снизу вверх.")
        print(u"Тоесть наменьшее кольцо расположено на вершине башни, а наибольшее лежит в основании, в самом низу.")
        print(u"Цель - переместить башню с первого стержня на заданный (либо на второй, либо на третий, либо на любой из них)")
        print(u"Причём можно снимать только один, верхний элемент с башни и класть его либо на пустой стержень,")
        print(u"либо на элемент большего размера. Тоесть 1 на 2 положить можно, а вот 2 на 1 - нет.\n")
        print(u"Основная информация:")
        print(u"Используй флаг --ai для того, чтобы играл ваш ИИ (для игры используется файл AI.py)")
        print(u"Чтобы ИИ сделал ход, верните в файле AI.py список из двух элементов - откуда куда соответсвенно")
        print(u"ПРИМЕР:")
        print(u"return [1, 2] - снять элемент из первой пирамиды и положить на вторую\n")
        print(u"Используйте следующие методы:")
        print(u"pyramids[N].get_top() - вернуть верхний элемент N-ой пирамиды")
        print(u"pyramids[N].get_all() (или просто game.pyramids[N]) - вернуть список всех элементов N-ой пирамиды")
        print(u"pyramids[N].get_len() - вернуть количество элементов в N-ой пирамиде\n")
        print(u"ВНИМАНИЕ!\n")
        print(u"N - номер пирамиды МИНУС один. Помните, что вы обращаетесь к списку :)")
        print(u"Если вы хотите получить информацию о первой пирамиде, то N = 0\n")
        print(u"УДАЧИ!\n")
    
    
if __name__ == "__main__":
    if '--help' in sys.argv:
        help()
    elif '--ai' in sys.argv:
        ai_mode()
    else: main()
