#!/usr/bin/env python3

import re, copy, sys
import AI
import os
import os.path
import time
import getopt 

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

    mov_cmd = re.compile('\d+')
    
    def __init__(self, ai = None, who = "Player", lvl = 5, istream = input, ostream = print, log=0, delay = 0):
        self.status = "Runing"
        self.who = who
        self.istream = istream
        self.ai = ai
        self.lvl = lvl
        self.log = log
        self.delay = delay
        self.count = 0
        arr = list(range(lvl+1))[1:]
        arr.reverse()
        self.pyramids = [
            stack_pyramid( copy.copy(arr) ),
            stack_pyramid(), 
            stack_pyramid()
        ]
        self.win_combination = arr
    

    def process(self):
        #(user_input[0] != "exit"  or user_input[0] != "e") and
        if (self.log==1):
            f= open('log.txt', 'w')
        while( self.status == "Runing"):
            if self.who == "Player":
                moves = self.istream().lower()
                moves = re.findall(Game.mov_cmd, moves)
                if len(moves) < 2: continue
                for i in range(len(moves)): moves[i] = int(moves[i])
            elif self.who == "AI":
                if self.count > 1000:
                    self.status = "Stopped"
                    print ("AI FAILED (TO MANY MOVES)")
                moves = self.ai(self)
            else: break
            if(  moves[0] > 0 and moves[0] < 4 ) and ( moves[1] > 0 and moves[1] < 4 ):
                self.count+=1
                from_ = moves[0]-1
                if (self.log==1):
                    f.write(str(from_))
                to_ = moves[1]-1
                if (self.log==1):
                    f.write(str(to_)+'\n')
            else:
                print("WRONG MOVE")
            try:
                self.pyramids[to_].push( self.pyramids[from_][-1] )
                self.pyramids[from_].pop()
            except:
                if self.who == "AI":
                    self.status = "Stopped"
                    print ("AI FAILED (FORBIDDEN MOVE)")
            self.situation()
            time.sleep(self.delay)

    def draw(self):
        os.system('cls')
        
        print ("COUNT: " + str(self.count) )
        print ("| "*3)
        for g in range(self.lvl):
            for pyramid in self.pyramids:
                try:
                    print( str(pyramid[self.lvl-g-1]), end=" " )
                except IndexError:
                    print("|", end=" ")
            print()
        

    def situation(self):
        #self.count+=1
        self.draw()
        for i in range(1,len(self.pyramids)):
            if self.pyramids[i] == self.win_combination:
                self.status = "Win"
                print ("YOU WIN")
            
def rules_text():
	lines = [
		u"\nПРАВИЛА:",
	    u"Подробнее тут - https://ru.wikipedia.org/wiki/Ханойская_башня",
	    u"Если вкратце, то нам даны 3 стержня, на первом из которых расположены N элементов",
	    u"(В оригинале эти элементы - кольца разного диаметра, в нашем случае это числа, в порядке убывания снизу вверх.",
	    u"Тоесть наменьшее кольцо расположено на вершине башни, а наибольшее лежит в основании, в самом низу.",
	    u"Цель - переместить башню с первого стержня на заданный (либо на второй, либо на третий, либо на любой из них,",
	    u"Причём можно снимать только один, верхний элемент с башни и класть его либо на пустой стержень,",
	    u"либо на элемент большего размера. Тоесть 1 на 2 положить можно, а вот 2 на 1 - нет.\n",
	    u"Основная информация:",
	    u"Используй флаг --ai для того, чтобы играл ваш ИИ (для игры используется файл AI.py,",
	    u"Чтобы ИИ сделал ход, верните в файле AI.py список из двух элементов - откуда куда соответсвенно",
	    u"ПРИМЕР:",
	    u"return [1, 2] - снять элемент из первой пирамиды и положить на вторую\n",
	    u"Используйте следующие методы:",
	    u"game.pyramids[N].get_top(, - вернуть верхний элемент N-ой пирамиды",
	    u"game.pyramids[N].get_all(, (или просто game.pyramids[N], - вернуть список всех элементов N-ой пирамиды",
	    u"game.pyramids[N].get_len(, - вернуть количество элементов в N-ой пирамиде\n",
	    u"ВНИМАНИЕ!\n",
	    u"N - номер пирамиды МИНУС один. Помните, что вы обращаетесь к списку :,",
	    u"Если вы хотите получить информацию о первой пирамиде, то N = 0\n",
	    u"УДАЧИ!\n"
	]
	return '\n'.join(lines)

def help_text():
	lines = [
		"Command arguments:",
		"-h, --help to display help",
		"-r, --rules to display rules",
		"-l, --log to log turns to file",
		"--ai to enable AI moves",
		"-d, --delay <MILISECONDS> to enable delay between moves in MS",
		"-w, --web to enable HTML/JS visualization at localhost:5000 (by default)"
	]

def main(argv):
	try:                                
        opts, args = getopt.getopt(argv, "hrlwd:", ["help","rules", "ai", "log","web", "delay="])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)   

    who="Player"
    ai=None
    log=0
    for opt, arg in opts:                                           
        if opt in ("-h", "--help"):
            print(help_text)
        	sys.exit(2)  
        elif opt in ("-r", "--rules"):
            print(rules_text)
        	sys.exit(2)
        elif opt in ("--ai"):
            who="AI"
        	ai=AI.AI
        elif opt in ("-l", "--log"):
            log=1
        elif opt in ("-w", "--web"):
            log=1
        elif opt in ("-d", "--delay"):
            delay = int(arg)

    game = Game(who = "AI", ai = AI.AI, log=log, delay=delay)
    game.draw()
    game.process()

if __name__ == "__main__":
    main(sys.argv[1:])