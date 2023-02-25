import pydealer as p
import random as r
import matplotlib.pyplot as plt
import numpy as np

TOTAL_PLAYERS = 4
TOTAL_TEAM = 2
TOTAL_CARDS_PER_PLAYER = 13
WINNING_SCORE = 500
LOSING_SCORE = -200
TOTAL_GAMES = 5000
TOTAL_RUNS = 10

win_probability = np.zeros(TOTAL_RUNS)
# array with size of total runs
# win_probability = np.zeros((TOTAL_RUNS, TOTAL_GAMES))
# matrix with shape TOTAL_RUN * TOTAL_GAMES
for current_run in range(TOTAL_RUNS):
    win = 0
    # total winning times
    for current_game_count in range(1, TOTAL_GAMES + 1):

        team_score = [0] * TOTAL_TEAM
        # team index 0 -> player 0 and player 2
        # team index 1 -> player 1 and player 3
        team_bag = [0] * TOTAL_TEAM
        rounds_count = 1
        dealer = r.randint(0, 3)
        while min(team_score) > LOSING_SCORE and max(team_score) < WINNING_SCORE:
        #     win if team with score higher than winning score or lost if team with score lower than losing score
        #     print()
        #     print(f'Round {rounds_count}')
            player_deck = []
            whole_deck = p.Deck()
            whole_deck.shuffle(1)
            
            for i in range(TOTAL_PLAYERS):
                player_deck.append(whole_deck.deal(TOTAL_CARDS_PER_PLAYER))
                player_deck[i].sort()
            player_bid = []

            for i in range(TOTAL_PLAYERS):
        #         print()
        #         print(f'Player {i + 1}:')
        #         is_blind_nil = bool(int(input('Blind Nil (Enter 1 for yes, 0 for no)?')))
        #         if is_blind_nil:
        #     #         -1 means blind nil
        #             player_bid.append(-1)
        #         else:
        # ignore this part that needs manually input
                    
        #         if choose not to blind nil then show cards
        #         print(f'Player {i + 1} has cards: ')
        #         print(player_deck[i])
                
                bid = len(player_deck[i].find_list(['King', 'Ace'])) + int(len(player_deck[i].find_list(['Queen', 'Jack'])) / 2)
        #         strategy of bidding numbers of king and ace + number of queen and jack divided by 2
                
        #         print(bid)
                
        #         bid = int(input(f'Player {i + 1} Bid (0 minimum, 13 maximum inclusive): '))
        #         while bid < 0 or bid > 13:
        # #             bid should be between 0 to 13
        #             print('Wrong Bid. Please Retry!')
        #             bid = int(input(f'Player {i + 1} Bid (0 minimum, 13 maximum inclusive): '))
        # manual input bid

                player_bid.append(bid)

            player_turn = dealer + 1
            # game starts with player on the left of dealer
            if player_turn == 4:
        #         prevent out of bound
                player_turn = 0
            is_last_round = False
            # variable to record whether this is the last round
            is_broke_spades = False
            # boolean of whether the spade has been broken
            player_made = [0] * TOTAL_PLAYERS
            # list recording each player's made
            
            while not is_last_round:
                lead_suit = None
                card_played = [None] * TOTAL_PLAYERS
            #     a list of the card played this round
                for count in range(TOTAL_PLAYERS):
        #             print()
        #             print(f'Player {player_turn + 1} cards:')
                    current_deck = player_deck[player_turn]
        #             print(current_deck)
            #         showing all cards
        #             print()
        #             print('Picking options:')
                    
                    valid_list = None
                    
                    if count == 0 and is_broke_spades:
                        valid_list = current_deck.find_list(['Diamonds', 'Hearts', 'Clubs', 'Spades'])
                    elif count == 0:
            #             when not broken spades, we can only choose non spade for the first card
                        valid_list = current_deck.find_list(['Diamonds', 'Hearts', 'Clubs'])
                        if len(valid_list) == 0:
    #                         must play spades, and spade broke in this case
                            valid_list = current_deck.find_list(['Diamonds', 'Hearts', 'Clubs', 'Spades'])
                            is_broke_spades = True
                    else:
                        valid_list = current_deck.find(lead_suit)
                        if len(valid_list) == 0:
                            valid_list = current_deck.find_list(['Diamonds', 'Hearts', 'Clubs', 'Spades'])
        #             for i in sorted(valid_list):
        #                 print(current_deck.cards[i])
                    
                    if player_turn == 0:
#                         my turn, so apply different strategy
                        if current_deck.size >= 9:
                            pick = 0
                        else:
                            pick = len(valid_list) - 1
#                         card left -> rounds
#                         13 -> 1
#                         12 -> 2
#                         11 -> 3
#                         10 -> 4
#                         9 -> 5
#                         8 -> 6
#                         7 -> 7
#                         6 -> 8
#                         5 -> 9
#                         4 -> 10
#                         3 -> 11
#                         2 -> 12
#                         1 -> 13
                    else:
                        pick = len(valid_list) - 1
        #             lowest card strategy: 0
        #             highest card strategy: len(valid_list) - 1
        #             mid card strategy: int(len(valid_list) / 2)
        #             random strategy: r.randint(0, len(valid_list) - 1)
        
        #             print()
        #             print(sorted(valid_list))
        #             print(pick)
                    
                    card_choose = (sorted(valid_list))[pick]
                    
        #             card_choose = input('Enter the card to play:')
    #                 while len(current_deck.find(card_choose)) != 1 or current_deck.find(card_choose)[0] not in valid_list:
    #              #         entered card choose invalid
    #                     print('Invalid input. Please Retry!')
    #                     card_choose = input('Enter the card to play:')
        # manual input

                    card_get = current_deck.get(card_choose)
                    
        #             print(card_get)
                    
                    card_played[player_turn] = card_get[0]
            #         store the player's move

                    if lead_suit is None:
            #             set leading suit if haven't defined earlier
                        lead_suit = card_get[0].suit
                        

                    if not is_broke_spades and card_get[0].suit == 'Spades':
            #             set broken spades to true if previously it was false and the chosen card has suit spades
                        is_broke_spades = True
        #                 print('Broke Spades!!')
                    
                    player_turn += 1
            #         next player's turn
                    
                    if player_turn == 4:
            #             reset if index out of bound
                        player_turn = 0
                    
                    if current_deck.size == 0:
                        is_last_round = True
                
                played_card_stack = p.stack.Stack(cards=card_played)
            #     save the original index
                sorted_played_card = p.stack.Stack(cards=card_played, sort=True)

                index_made = None
                if len(sorted_played_card.find('Spades')) == 0:
                    index_largest = max(sorted_played_card.find(lead_suit))
            #         this gives us the largest cards that's the lead suit
                    index_made = played_card_stack.find(str(sorted_played_card.cards[index_largest]))[0]
                else:
                    index_largest = max(sorted_played_card.find('Spades'))
            #         gives us largest rank with suit Spades
                    index_made = played_card_stack.find(str(sorted_played_card.cards[index_largest]))[0]
                player_turn = index_made
                player_made[index_made] += 1

        #         print()
        #         print('Current made:', player_made)
        #         print('Player bid:', player_bid)
            
            for i in range(TOTAL_TEAM):
                if 0 in player_bid[i::2] or -1 in player_bid[i::2]:
        #             since someone bid nil, we need to count individually
                    for j in range(2):
                        if player_made[i + 2 * j] > 0 and player_bid[i + 2 * j] == 0:
        #                     bid nil but does not satisfy
                            team_score[i] -= 100
                        elif player_made[i + 2 * j] > 0 and player_bid[i + 2 * j] == -1:
        #                     bid blind nil but does not satisfy
                            team_score[i] -= 200
                        elif player_made[i + 2 * j] < player_bid[i + 2 * j]:
        #                     bid non-nil but does not satisfy
                            team_score[i] -= player_bid[i]
                        elif player_bid[i + 2 * j] == -1:
        #                     blind nil satify
                            team_score[i] += 200
                        elif player_bid[i + 2 * j] == 0:
        #                     nil satisfy
                            team_score[i] += 100
                        else:
        #                     bid non-nil and satisfy
                            bag = player_made[i + 2 * j] - player_bid[i + 2 * j]
                            team_bag[i] += bag
                            team_score[i] += (player_bid[i + 2 * j] * 10 + bag)
        #                     10 points for non bag and 1 points for bag
                else:
                    team_made = [0] * TOTAL_TEAM
                    team_bid = [0] * TOTAL_TEAM
                    for j in range(2):
                        team_made[i] += player_made[i + 2 * j]
                        team_bid[i] += player_bid[i + 2 * j]
        #                 summing all team players' made and bid

                    if team_made[i] < team_bid[i]:
                        team_score[i] -= team_bid[i]
                    else:
        #                 bid non-nil and satisfy
                        bag = team_made[i] - team_bid[i]
                        team_bag[i] += bag
                        team_score[i] += (team_bid[i] * 10 + bag)
        #                 10 points for non bag and 1 points for bag

            dealer += 1
        #     dealer rotating clockwise
            if dealer == 4:
                dealer = 0
            
            for i in range(TOTAL_TEAM):
                if team_bag[i] >= 10:
                    team_score[i] -= 100
        #             minus 100 points if bag higher or equal to 10
                    team_bag[i] -= 10
            
            rounds_count += 1
        #     print()
        #     print('Score', team_score)
        #     print('Bag', team_bag)

    #     print()
    #     if team_score[0] == team_score[1]:
    #         print('Tie!')
    #     else:
    #         winning_team_index = team_score.index(max(team_score)) + 1
    #         print('Winning Team:', winning_team_index)
    #         print('Winning Player:', winning_team_index, 2 + winning_team_index)
        if team_score[0] > team_score[1]:
    #         i am player 0 in team 0 so if team 0 win I win
            win += 1
#         win_probability[current_run, current_game_count - 1] = (win / current_game_count)
    win_probability[current_run] = (win / current_game_count)

# fig, ax = plt.subplots()
# x = np.arange(1, TOTAL_GAMES + 1, 1)
# ax.plot(x, win_probability[0, :], label='Run 1')
# ax.plot(x, win_probability[1, :], label='Run 2')
# ax.plot(x, win_probability[2, :], label='Run 3')
# ax.plot(x, win_probability[3, :], label='Run 4')
# ax.plot(x, win_probability[4, :], label='Run 5')
# ax.plot(x, win_probability[5, :], label='Run 6')
# ax.plot(x, win_probability[6, :], label='Run 7')
# ax.plot(x, win_probability[7, :], label='Run 8')
# ax.plot(x, win_probability[8, :], label='Run 9')
# ax.plot(x, win_probability[9, :], label='Run 10')
# ax.set_xlabel('Number of Games')
# ax.set_ylabel('Winning Probability')
# ax.legend(bbox_to_anchor=(1.5,1))
# fig.savefig('hi_vs_rand.png', bbox_inches='tight')
# for converge graph

# ax.hist(win_probability)
# fig.savefig('normal.png')
print(min(win_probability), max(win_probability))