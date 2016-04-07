'''

'''
def AI(game):
    print (game.pyramids[0].get_top()) #Верхний элемент первой башни
    print (game.pyramids[0]) #Все элементы первой башни. Можно написать game.pyramids[0].get_all() - ничем не отличается
    print (game.pyramids[0].get_len())
    return [1, 2] #переместить из 1 башни во вторую
    
