prev_move = []
def check_can_move(pyr1, pyr2, i, j ):
    global prev_move
    if pyr1 == pyr2:
        raise(Exception("Trying to move to same pyramid dumbass"))
    try:
        pyr1_top = pyr1.get_top()
    except:
        pyr1_top = 0

    try:
        pyr2_top = pyr2.get_top()
    except:
        pyr2_top = 0


    #print("Attempting move", [i, j])

    if pyr1_top > pyr2_top and pyr2_top != 0:
        return False #can't move bigger to smaller

    if pyr1_top != 0 and pyr2_top != 0:
        if (pyr1_top % 2 == 0 and pyr2_top % 2 == 0) or (pyr1_top % 2 != 0 and pyr2_top % 2 != 0):
            return False #can't move even on even, odd on odd
    prv_reversed = list(prev_move)
    prv_reversed.reverse()
    if [x-1 for x in prv_reversed] == [i, j]:
        return False #can't undo previous move

    return True

def AI(game):
    global prev_move
    #iterative solution https://en.wikipedia.org/wiki/Tower_of_Hanoi#Simpler_statement_of_iterative_solution
    if game.count == 0:
        even_disks = game.pyramids[0].get_len()%2 == 0

        if even_disks:
            move = [1, 2]
            
        else:
            move = [1, 3]
        prev_move = list(move)
        return move


    possible_moves = []

    #if can move 1 2 add it
    for i in range(len(game.pyramids)):
        pyramid = game.pyramids[i]
        if pyramid.get_len() == 0:
            continue #pyramid is empty, we can't move

        for j in range(len(game.pyramids)):
            if i == j:
                continue
            if check_can_move(game.pyramids[i], game.pyramids[j], i, j):
                possible_moves.append([i+1, j+1])

    # for move in possible_moves:
    #     print(str(move))

    prev_move = list(possible_moves[0])
    return possible_moves[0]