import random
from UI import *
from pygame import mixer
from sys import exit

pygame.init()
mixer.init()

# This class creates all cpus + the player as gameObjects along with a function to ascertain each player's "value".
class Poker:
    def __init__(self, name, risk, money, hand, hand_cards, hand_active_cards, hand_value, status, forward, coord, id):
        self.id = id
        self.uic = [object, object]
        self.coord = coord
        self.name = name
        self.risk = risk
        self.money = money
        self.hand = hand
        self.hand_cards = hand_cards
        self.hand_active_cards = hand_active_cards
        self.hand_value = hand_value
        self.status = status
        self.forward = forward

    # This definition will determine if the players have a particular hand or a potential hand do calculate risk and
    # card values eventually determining their decision (cpu only)
    def value_det(self):
        value_count = []
        hand_indices = []
        self.hand_active_cards = table_deck + self.hand_cards
        self.risk = 0.5
        player_deck_val = [0] * len(self.hand_active_cards)
        seq_int = 0
        flush_int = 0
        check = 0

        # Sorting logic
        while check < len(self.hand_active_cards) - 1:
            for i in range(0, (len(self.hand_active_cards) - 1)):
                cv = card_values[base_deck.index(self.hand_active_cards[i])]
                cv2 = card_values[base_deck.index(self.hand_active_cards[i + 1])]
                if cv > cv2:
                    x = self.hand_active_cards[i]
                    self.hand_active_cards[i] = self.hand_active_cards[i + 1]
                    self.hand_active_cards[i + 1] = x
                    check = 0
                else:
                    check += 1

        for i in range(0, len(self.hand_active_cards)):
            player_deck_val[i] = card_values[base_deck.index(self.hand_active_cards[i])]

        # Purpose is the count how many of each values there are in the player's hand which we need to det. hands.
        for i in range(1, 14):
            value_count.append(player_deck_val.count(i))

        # This block determines if the table cards + player cards are sequential
        gap = False
        for i in range(0, len(self.hand_active_cards) - 1):
            cv = card_values[base_deck.index(self.hand_active_cards[i])]
            cv2 = card_values[base_deck.index(self.hand_active_cards[i + 1])]
            if cv + 1 == cv2:
                seq_int += 1
            elif cv == cv2:
                continue
            elif cv + 2 == cv2 and not gap:
                seq_int = 0
                gap = True
            else:
                seq_int = 0
                gap = False
            if sequential >= 4:
                Break

        sequential = seq_int == 4

        C, D, H, S = 0, 0, 0, 0
        # This looks at the first letter of the cards which signifies the suit. If 5+ are equal, then player has flush.
        for i in range(0, len(self.hand_active_cards)):
            locals()[self.hand_active_cards[i][0]] += 1

        if C == 5 or D == 5 or H == 5 or S == 5:
            flush = True
        else:
            flush = False

        # When total cards<7, this calculates potential risk and current value for the incomplete set for each players.
        # If number of cards = 7, then all cards are there, determines each players' hand.
        # This risk is a value stemming from 0.5, higher the riskier. This value affects CPU decisions later.
        if len(self.hand_active_cards) < 7:
            if max(value_count) >= 2:
                p_val = ((value_count.index(max(value_count))) + 1) ** max(value_count)
                self.risk -= (p_val / 200 * max(value_count)) - 0.1 * max(value_count)
            else:
                p_val = min(card_values[base_deck.index(self.hand_cards[0])], card_values[base_deck.index(self.hand_cards[1])])
                self.risk += p_val/100

            if gap:
                p_val = max(card_values[base_deck.index(self.hand_cards[0])], card_values[base_deck.index(self.hand_cards[1])])
                self.risk -= (p_val / 100) * (1.03 ** (len(self.hand_active_cards) / 2))
            elif sequential:
                p_val = max(card_values[base_deck.index(self.hand_cards[0])], card_values[base_deck.index(self.hand_cards[1])])
                self.risk -= (p_val / 100) * (1.05 ** (len(self.hand_active_cards) / 2))
            elif flush_int >= 1:
                p_val = max(card_values[base_deck.index(self.hand_cards[0])], card_values[base_deck.index(self.hand_cards[1])])
                self.risk -= (p_val / 100) * (1.1 ** (len(self.hand_active_cards) / 2))
            elif sequential and flush_int >= 1:
                p_val = max(card_values[base_deck.index(self.hand_cards[0])], card_values[base_deck.index(self.hand_cards[1])])
                self.risk -= (p_val / 100) * (1.2 ** (len(self.hand_active_cards) / 2))
        else:
            if max(value_count) >= 2:
                if max(value_count) == 3:
                    if 2 in value_count:
                        hand_indices.append(hand_names.index("Full house"))
                        p_val = (value_count.index(3)) + 1
                        s_val = (value_count.index(2)) + 1
                        self.s_val = s_val
                        self.hand_value = p_val
                    else:
                        hand_indices.append(hand_names.index("Three of a kind"))
                        p_val = (value_count.index(3)) + 1
                        self.hand_value = p_val
                elif max(value_count) == 2:
                    if value_count.count(2) >= 2:
                        hand_indices.append(hand_names.index("Double pair"))
                        indices = []
                        for i in range(
                                len(value_count)):  # This loop is to determine the value of the highest pair.
                            if value_count[i] == 2:
                                indices.append(i)
                        p_val = max(indices) + 1
                        indices.remove(max(indices))    #Yeah, really lazy way of getting second highest value...
                        s_val = max(indices) + 1
                        self.hand_value = p_val
                        self.s_val = s_val
                    else:
                        p_val = (value_count.index(2)) + 1
                        hand_indices.append(hand_names.index("Single pair"))
                        self.hand_value = p_val
                elif max(value_count) == 4:
                    hand_indices.append(hand_names.index("Four of a kind"))
                    p_val = (value_count.index(4)) + 1
                    self.hand_value = p_val

            # This redundancy in determining the player's hand is necessary since it is possible to get overlapping
            # hands (ex: C4 D4 C5 H6 D7 D8 SA), we only want to consider the straight, not the pair.
            if sequential:
                hand_indices.append(hand_names.index("Straight"))
                p_val = max(card_values[base_deck.index(self.hand_cards[0])], card_values[base_deck.index(self.hand_cards[1])])
                self.hand_value = p_val
            elif flush:
                    hand_indices.append(hand_names.index("Flush"))
                    p_val = max(card_values[base_deck.index(self.hand_cards[0])], card_values[base_deck.index(self.hand_cards[1])])
                    self.hand_value = p_val
            elif sequential and flush:
                if player_deck_val[6] == 13 and player_deck_val[2] == 9:
                    hand_indices.append(hand_names.index("Royal flush"))
                else:
                    hand_indices.append(hand_names.index("Straight flush"))
                    p_val = max(card_values[base_deck.index(self.hand_cards[0])],
                                card_values[base_deck.index(self.hand_cards[1])])
                    self.hand_value = p_val
            else:
                hand_indices.append(hand_names.index("High card"))
                p_val = max(card_values[base_deck.index(self.hand_cards[0])], card_values[base_deck.index(self.hand_cards[1])])
                self.hand_value = p_val

            # Depending on the possible hands the player has, the highest is chosen. (ex: pair, straight), hand=straight
            if len(hand_indices) == 2:
                self.hand = hand_names[max(hand_indices[0], hand_indices[1])]
            else:
                self.hand = hand_names[hand_indices[0]]

        if self.risk < 0:
            self.risk = 0


def reveal_cards():
    for i in range(0, len(active_players)):
        if active_players[i] == player or active_players[i].status == "Folded":
            pass
        else:
            for j in range(0, 2):
                flip_card(active_players[i].uic[j], uif)


def new_deck():
    globals()['table_deck'] = []
    globals()['removed_deck'] = []
    globals()['dealer_deck'] = ["C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK", "CA",
                         "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK", "SA",
                         "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK", "DA",
                         "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "HJ", "HQ", "HK", "HA"]


def next_card():
    card = dealer_deck[random.randint(0, 51 - len(removed_deck))]
    removed_deck.append(card)
    table_deck.append(card)
    dealer_deck.remove(card)

    card_sprite = Card((650, 450), card[1:], suit_name[suits.index(card[0])], True)
    table_UI.append(card_sprite)
    all_sprites.add(card_sprite)
    raise_sprites.add(card_sprite)
    card_sprites.add(card_sprite)

    move_card(card_sprite, (850-100*(5-len(table_deck)), 600), 20, uif)
    flip_card(card_sprite, uif)

    for i in range(0, len(active_players)):
        if active_players[i].status != "Busted":
            active_players[i].value_det()


# Gets the player id of the one having small and big blind and removes the appropriate amount of money.
def blinds_pot():
    globals()["blind_id"] -= 1
    if globals()["blind_id"] < 0:
        globals()["blind_id"] = len(active_players) - 1
    globals()["b_blind_id"] = blind_id + 1
    if globals()["b_blind_id"] > len(active_players)-1:
        globals()["b_blind_id"] = 0

    sp_blind = active_players[blind_id]
    bp_blind = active_players[b_blind_id]

    sp_blind.forward += blind
    bp_blind.forward += blind*2

    # Defunct logic to determine side pots (ran out of time to implement correctly).

    # if sp_blind.money >= blind:
    #     holder_s = blind
    # else:
    #     holder_s = sp_blind.money
    #
    # if bp_blind.money >= blind*2:
    #     holder_b = blind*2
    # else:
    #     holder_b = bp_blind.money

    # if sp_blind.money == 0 and bp_blind.money == 0:
    #     if holder_s <= holder_b:
    #         globals()["max_pot"] = holder_s * len(active_players)
    #     else:
    #         globals()["max_pot"] = holder_b * len(active_players)
    #     print_slow(sp_blind.name + "has now gone all-in!")
    #     print_slow(bp_blind.name + "has now gone all-in!")
    #     sp_blind.status = "Allin"
    #     bp_blind.status = "Allin"
    # elif sp_blind.money == 0:
    #     globals()["max_pot"] = holder_s * len(active_players)
    #     print_slow(sp_blind.name + "has now gone all-in!")
    #     sp_blind.status = "Allin"
    # elif bp_blind.money == 0:
    #     globals()["max_pot"] = holder_b * len(active_players)
    #     print_slow(bp_blind.name + "has now gone all-in!")
    #     bp_blind.status = "Allin"


def check_press():
    for i in range(0, 4):
        if buttons[i].rect.centerx - 150 <= mouse[0] <= buttons[i].rect.centerx + 150 and buttons[
            i].rect.centery - 50 <= mouse[1] <= buttons[i].rect.centery + 50:
            return i
    return 4


#Raise, Check, Fold, Call
def player_decision(call):
    txt_box.write("Now my reckless friend, what would you like to do?", uif)
    while True:
        decision = 4
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(0, 4):
                    if buttons[i].rect.centerx - 150 <= mouse[0] <= buttons[i].rect.centerx + 150 and buttons[
                        i].rect.centery - 50 <= mouse[1] <= buttons[i].rect.centery + 50:
                        decision = i
        if decision == 1:
            if call == player.forward:
                txt_box.write("The player passively checks.", uif)
                player.status = "Check"
            else:
                txt_box.write("You cannot check right now.", uif)
                txt_box.write("You have yet to cover either the blind or a raise.", uif)
                continue
            break
        elif decision == 2:
            player.status = "Folded"
            txt_box.write("The player has folded, a prudent choice.", uif)
            break
        elif decision == 3:
            if call == player.forward:
                txt_box.write("There is nothing to call right now...?", uif)
                txt_box.write("If you do not want to raise further please check.", uif)
                continue
            if player.money <= call:
                txt_box.write("The only way for you to call is to all-in yourself.", uif)
                if max_pot > player.money * len(active_players):
                    globals()["max_pot"] = player.money * len(active_players)
                player.forward = player.money
                player.status = "Allin"
            else:
                txt_box.write("The player calls and rises to the challenge!", uif)
                player.forward = call
                player.status = "Call"
            break
        elif decision == 0:
            if player.money <= call:
                txt_box.write("The call target is already higher than your entire savings...", uif)
                txt_box.write("You can't really raise right now...", uif)
                continue
            else:
                txt_box.write("How much would ya like to raise the stakes by?", uif)
                deciding = True
                while deciding:
                    slider.value_update(knob.prop, player.money)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if button_done.rect.centerx - 150 <= mouse[0] <= button_done.rect.centerx + 150 and \
                            button_done.rect.centery - 50 <= mouse[1] <= button_done.rect.centery + 50:
                                bet = slider.value
                                deciding = False
                    globals()["mouse"] = pygame.mouse.get_pos()
                    raise_sprites.update()
                    raise_sprites.draw(screen)
                    pygame.display.flip()

                globals()["call_target"] += int(bet)
                player.forward = int(bet)
                player.status = "Raise"
                for i in range(1, len(active_players)):
                    if active_players[i].status == "Folded" or active_players[i].status == "Busted" or \
                            active_players[i].status == "Allin":
                        continue
                    else:
                        active_players[i].status = ""
                if player.forward == player.money:
                    txt_box.write("The player has decided to go ALL-IN, was that the play?", uif)
                    player.status = "Allin"
                    player.all = True
                    for i in range(1, len(active_players)):
                        active_players[i].risk += 0.5
                txt_box.write("Let's see what the others have to think about this raise.", uif)
            break

        update_UI()


def card_eval():
    n = []
    j = []
    player_hand_values = [0, 0, 0, 0]
    player_card_values = []
    for i in range(0, len(active_players)):
        if active_players[i].status == "Folded":
            player_hand_values[i] = 0
            continue
        player_hand_values[i] = hand_values[hand_names.index(active_players[i].hand)]
    for i in range(0, len(active_players)):
        player_base = [0, 0]
        player_base[0] = card_values[base_deck.index(active_players[i].hand_cards[0])]
        player_base[1] = card_values[base_deck.index(active_players[i].hand_cards[1])]
        player_card_values.append(max(player_base))

    if player_hand_values.count(max(player_hand_values)) == 1:
        winner = active_players[player_hand_values.index(max(player_hand_values))]
    else:
        for i in range(0, len(active_players)):
            if player_hand_values[i] == max(player_hand_values):
                n.append(i)
        for i in range(0, len(n)):
            j.append(player_card_values[n[i]])
        if j.count(max(j)) == 1:
            winner = active_players[n[j.index(max(j))]]
        elif j.count(max(j)) > 1:
            for i in range(0, len(active_players)):
                if active_players[i].status == "Busted" or active_players[i].status == "Folded":
                    continue
                else:
                    winner = active_players[i]
                    return winner
    return winner


def cpu_decision(cpu, risk, money, bet):
    # Purely cosmetic
    txt_box.write(cpu.name + " is thinking about what to do next...", uif)
    wait(0.4)

    risk *= (1 - (status_list.count("Folded")/len(active_players)))
    if risk >= 0.15:
        risk += bet_incr / 10

    # Depending on the risk value previously determined and the wealth of the bot,
    # along with a small random factor,the cpu decides what to do.
    rand = (random.randint(-5, 5)) / 100
    if rand < 0:
        rand *= (money / 20000)
    rand += (bet / (money + 1)) * 0.5
    if random.randint(1, 15) == 1 and risk >= 0.4 and money > bet:
        cpu.status = "Raise"
        cpu_raise(cpu)
    elif risk >= 1 and call_target != 0:
        if random.randint(1, int(cpu.money/1500)+1) == 1:
            cpu_raise(cpu)
        else:
            cpu.status = "Folded"
            txt_box.write(str(cpu.name) + " has decided to fold. Scared are we?", uif)
    elif risk > 0.5 and call_target == 0:
        cpu.status = "Check"
        txt_box.write(str(cpu.name) + " has decided to check. A sound decision.", uif)
    elif risk >= 0.5 + rand:
        if active_players[b_blind_id] == cpu and len(table_deck) == 0:
            if call_target == cpu.forward:
                cpu.status = "Check"
                txt_box.write(str(cpu.name) + " has decided to check. A sound decision.", uif)
            else:
                cpu.status = "Call"
                cpu_call(cpu)
        elif active_players[blind_id] == cpu and random.randint(0, 10) >= 7 and len(table_deck) == 0:
            if call_target == cpu.forward:
                cpu.status = "Check"
                txt_box.write(str(cpu.name) + " has decided to check. A sound decision.", uif)
            else:
                cpu.status = "Call"
                cpu_call(cpu)
        elif call_target != 0:
            cpu.status = "Folded"
            txt_box.write(str(cpu.name) + " has decided to fold. Scared are we?", uif)
        else:
            cpu.status = "Check"
            txt_box.write(str(cpu.name) + " has decided to check. A sound decision.", uif)
    elif 0.1 + rand <= risk < 0.5 + rand and bet <= money:
        if random.randint(0, 10 + bet_incr) <= 2 and active_players[b_blind_id] != cpu:
            cpu.status = "Folded"
            txt_box.write(str(cpu.name) + " has decided to fold. Scared are we?", uif)
        elif cpu.forward == bet:
            cpu.status = "Check"
            txt_box.write(str(cpu.name) + " has decided to check. A sound decision.", uif)
        else:
            cpu.status = "Call"
            cpu_call(cpu)
    elif risk < 0.1 + rand and money > bet:
        if random.randint(0, 10) <= 2 + bet_incr:
            if cpu.forward == bet:
                cpu.status = "Check"
                txt_box.write(str(cpu.name) + " has decided to check. A sound decision.", uif)
            else:
                cpu.status = "Call"
                cpu_call(cpu)
        else:
            cpu.status = "Raise"
            cpu_raise(cpu)
    else:
        if call_target == 0:
            cpu.status = "Check"
            txt_box.write(str(cpu.name) + " has decided to check. A sound decision.", uif)
        else:
            cpu.status = "Call"
            cpu_call(cpu)


# Generates a random value for the increase, with a small chance of all-in. Also resets all player status'(Except self)
def cpu_raise(cpu):
    globals()["bet_incr"] += 1
    # TO REVIEW
    if random.randint(1, int(cpu.money/1000)+1) == 1 and round_counter >= 3:
        increase = cpu.money - call_target
        cpu.status = "Allin"
        txt_box.write(cpu.name + " has decided to go ALL-IN!", uif)
        txt_box.write("Reason for caution or baseless confidence.?", uif)
        for i in range(0, len(active_players)):
            if active_players[i] == cpu:
                continue
            else:
                x = (increase/cpu.money)
                if x >= 0.5:
                    x = 0.5
                active_players[i].risk += x
    else:
        increase = random.randint(100, int(cpu.money/5))
        txt_box.write(cpu.name + " has decided to throw in another " + str(increase) + "$ into the pot.", uif)

    globals()["call_target"] += increase

    for i in range(0, len(active_players)):
        if active_players[i] == cpu:
            cpu.risk += 0.08
            continue
        elif active_players[i].status == "Folded" or active_players[i].status == "Busted" or active_players[i].status == "Allin":
            continue
        else:
            active_players[i].status = ""
            active_players[i].risk *= 1.2

    cpu.forward = call_target


def cpu_call(cpu):
    if cpu.money <= call_target:
        cpu.forward = cpu.money
        if max_pot > cpu.money*len(active_players):
            globals()["max_pot"] = cpu.money*len(active_players)
        txt_box.write(str(cpu.name) + " has no choice but to go ALL-IN to follow!", uif)
        cpu.status = "Allin"
        globals()["bet_incr"] += 1
    else:
        cpu.forward = call_target
        txt_box.write(str(cpu.name) + " is calling, glowing with confidence.", uif)


def calculate_pot():
    total = 0
    for i in range(0, len(active_players)):
        total += active_players[i].forward
        active_players[i].money -= active_players[i].forward
        active_players[i].forward = 0

    return total


def update_status():
    status_list[0] = player.status
    status_list[1] = cpu1.status
    status_list[2] = cpu2.status
    status_list[3] = cpu3.status


def new_round(target):
    target.hand_value = 0
    target.risk = 0.5
    target.hand_cards = []
    target.hand_active_cards = []
    target.hand = ""
    target.status = ""

    for i in range(0, 2):
        if target.money > 0:
            target.hand_cards.append(dealer_deck[random.randint(0, 51 - len(removed_deck))])
            removed_deck.append(target.hand_cards[i])
            dealer_deck.remove(target.hand_cards[i])
            if target.name == "Player":
                target.uic[i] = Card((650, 450), target.hand_cards[i][1:],
                                     suit_name[suits.index(target.hand_cards[i][0])], False)
                all_sprites.add(target.uic[i])
                raise_sprites.add(target.uic[i])
                card_sprites.add(target.uic[i])
                move_card(target.uic[i], (target.coord[0]+i*90, target.coord[1]), 40, uif)
            else:
                target.uic[i] = Card((650, 450), target.hand_cards[i][1:], suit_name[suits.index(target.hand_cards[i][0])], True)
                all_sprites.add(target.uic[i])
                raise_sprites.add(target.uic[i])
                card_sprites.add(target.uic[i])
                move_card(target.uic[i], (target.coord[0]+i*90, target.coord[1]), 40, uif)


def redeck(card_sprites):
    for card in card_sprites:
        move_card(card, (640, 450), 50, uif)

    for card in card_sprites:
        all_sprites.remove(card)
        raise_sprites.remove(card)
        card_sprites.remove(card)

def wait(sec):
    frames = 0
    while frames <= sec*60:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        frames += 1
        update_UI()


def update_UI():
    globals()["mouse"] = pygame.mouse.get_pos()
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()


# General lists
dealer_deck = []
removed_deck = []
table_deck = []
status_list = ["", "", "", ""]
multi_winners = []
table_UI = []

# Quantitative variables
base_stake = 20000
main_pot = 0
side_pot = 0
max_pot = 0

# Ids, bool, increments
winner_id = 0
round_counter = 0
bet_incr = 0
no_cards = False
multi = False
intro = True

#UI
running = True
(width, height) = (1900, 1020)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kab's Amazing Poker")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
raise_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
card_sprites = pygame.sprite.Group()
card_list = []

winner = object

# Definition lists, cards are given numerical values from 1-13 with 2 being the lowest and Ace being the highest.
# Same principle for the different possible hands.
order = ["Player", "CPU1", "CPU2", "CPU3"]
card_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] * 4
base_deck = ["C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK", "CA",
             "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK", "SA",
             "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK", "DA",
             "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "HJ", "HQ", "HK", "HA"]
hand_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0]
hand_names = ["High card", "Single pair", "Double pair", "Three of a kind", "Straight", "Flush", "Full house",
              "Four of a kind", "Straight flush", "Royal flush", "Folded"]

suits = ["C", "S", "D", "H"]
suit_name = ["clover", "spade", "diamond", "heart"]

player = Poker("Player", 0.5, 20000, "", [], [], 0, "", 0, (1050, 900), 0)
cpu1 = Poker("CPU1", 0.5, 20000, "", [], [], 0, "", 0, (100, 590), 1)
cpu2 = Poker("CPU2", 0.5, 20000, "", [], [], 0, "", 0, (600, 280), 2)
cpu3 = Poker("CPU3", 0.5, 20000, "", [], [], 0, "", 0, (1090, 580), 3)

active_players = [player, cpu1, cpu2, cpu3]
player_bank = active_players

blind_id = random.randint(0, 3)
b_blind_id = blind_id + 1
if b_blind_id >= 4:
    b_blind_id = 0

blind_pos = [(200, 900), (300, 450), (800, 150), (1000, 450)]

bg = Background((1920/2, 1080/2))
table = Board((650, 450))
stack = Stack((650, 450))

connor = Connor((1500, 700))
c1_sprite = CPU((150, 430), 1)
c2_sprite = CPU((650, 100), 2)
c3_sprite = CPU((1150, 400), 3)

kns_pos = (650, 830)
knob = Knob(kns_pos)
frame = Frame((1095, 900))
slider = Slider(kns_pos, knob.prop, player.money)

button_call = Button((500, 850), "Call")
button_check = Button((800, 850), "Check")
button_raise = Button((500, 950), "Raise")
button_fold = Button((800, 950), "Fold")
button_done = Button((kns_pos[0], kns_pos[1]+120), "Done")
buttons = [button_raise, button_check, button_fold, button_call]

stats = Status((1575, 250))

uif = [connor, all_sprites, screen]
txt_box = TextBox((1600, 500))
all_sprites.add(bg, table, connor, txt_box, c1_sprite, c2_sprite, c3_sprite, button_call, button_fold, button_check, button_raise, stats, stack, frame)
raise_sprites.add(bg, table, connor, txt_box, c1_sprite, c2_sprite, c3_sprite, slider, knob, button_done, stats, stack, frame)

mixer.music.load('Sounds/Endless Summer (Extended).mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1, 0, 10000)

while running:
    clock.tick(60)
    pygame.event.get()
    mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if intro:
        wait(3)
        txt_box.write("Welcome to the poker table, most esteemed guest.", uif)
        txt_box.write("My name is Connor and I will be your host for tonight.", uif)
        wait(0.5)
        txt_box.write("If you think I talk too much,", uif)
        txt_box.write("you can (rudely) press mouse1 to skip my dialogue...", uif)
        wait(0.5)
        txt_box.write("Tonight's buy-in is 20,000$.", uif)
        wait(0.5)
        txt_box.write("Let's get started shall we?", uif)
        wait(1)


    # Resets status
    for i in range(0, len(active_players)):
        if active_players[i].status != "Busted":
            active_players[i].status = ""
    update_status()

    # Bust check
    if player.money <= 0:
        txt_box.write("The player has busted.", uif)
        txt_box.write("It was a good show of ill-advised decisions.", uif)
        txt_box.write(" Better luck next time.", uif)
        wait(3)
        exit()
    if cpu1.money <= 0 and cpu1 in active_players:
        cpu1.money = 0
        cpu1.status = "Busted"
        c1_sprite.bust()
        txt_box.write("CPU1 has busted. Somebody should've coded him better.", uif)
        active_players.remove(cpu1)
    if cpu2.money <= 0 and cpu2 in active_players:
        cpu2.money = 0
        cpu2.status = "Busted"
        c2_sprite.bust()
        txt_box.write("CPU2 has busted. Quite the unfortunate turn of events.", uif)
        active_players.remove(cpu2)
    if cpu3.money <= 0 and cpu3 in active_players:
        cpu3.money = 0
        cpu3.status = "Busted"
        c3_sprite.bust()
        txt_box.write("CPU3 has busted. Should've been more careful.", uif)
        active_players.remove(cpu3)
    update_status()

    round_counter += 1
    pot = 0
    new_deck()

    # Renders a blind of 500, 1000, 2000 depending on how many players are left.
    blind = 500*(2**(4-len(active_players)))
    call_target = blind*2

    # Win condition
    if cpu1.status == "Busted" and cpu2.status == "Busted" and cpu3.status == "Busted":
        txt_box.write("Everyone has busted except the player! Congratulations!", uif)
        wait(0.5)
        txt_box.write(" You have won $60000 during this frugal event.", uif)
        txt_box.write("See you next time!", uif)
        cards = []
        val = 0
        word = "CONGRATULATIONS!"
        for i in range(0, 16):
            card = Card((350 + (i * 80), 0), word[i], "heart", False)
            cards.append(card)
            all_sprites.add(card)
        while True:
            val += 0.005
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            sin_card(cards, val, 400)

            all_sprites.draw(screen)
            pygame.display.update()
            pygame.display.flip()

    for i in range(0, len(active_players)):
        new_round(active_players[i])
        active_players[i].value_det()

    stats.text_update(player.money, cpu1.money, cpu2.money, cpu3.money, round_counter)

    blinds_pot()

    txt_box.write("Cards have been distributed.", uif)
    txt_box.write(
        "The small and big blind are given to " + active_players[blind_id].name + " and " +
        active_players[b_blind_id].name + ".", uif)

    if intro:
        sblind = Blind(blind_pos[active_players[blind_id].id], "any")
        bblind = Blind(blind_pos[active_players[b_blind_id].id], "big")
        intro = False
    else:
        move_card(sblind, blind_pos[active_players[blind_id].id], 50, uif)
        move_card(bblind, blind_pos[active_players[b_blind_id].id], 50, uif)

    all_sprites.add(bblind, sblind)
    raise_sprites.add(bblind, sblind)
    wait(1)

    while True:
        Board.board_update(table, call_target, pot)
        stats.text_update(player.money, cpu1.money, cpu2.money, cpu3.money, round_counter)

        if len(table_deck) == 5:
            winner = card_eval()
            winner.money += pot
            txt_box.write("Let's see those cards!", uif)
            reveal_cards()
            wait(0.5)
            txt_box.write(winner.name + " wins the pot with a " + winner.hand + " !", uif)
            wait(1)
            redeck(card_sprites)
            break

        i = b_blind_id + 1
        while "" in status_list:
            Board.board_update(table, call_target, pot)
            if i >= len(active_players):
                i = 0
            if status_list.count("Folded") == len(active_players) - 1:
                break
            if "" not in status_list:
                break
            if status_list.count("Folded") == len(active_players) - 1:
                break
            if active_players[i].status == "Allin":
                i += 1
                continue
            if active_players[i].status == "Folded":
                i += 1
                continue
            if i == 0 or i == len(active_players):
                player_decision(call_target)
            else:
                cpu_decision(active_players[i], active_players[i].risk, active_players[i].money, call_target)
            update_status()
            i += 1

        pot += calculate_pot()
        Board.board_update(table, call_target, pot)

        # Checking if one player is left with everyone folded
        if status_list.count("Folded") == len(active_players) - 1:
            for i in range(0, len(active_players)):
                if active_players[i].status != "Folded":
                    winner = active_players[i]
                    break
            txt_box.write("Everyone but " + winner.name + " has folded. " + winner.name + " wins the pot!", uif)
            winner.money += pot
            wait(0.5)
            Board.board_update(table, call_target, pot)
            redeck(card_sprites)
            break

        # Determines if a side pot is needed and creates it if so. (Defunct)
        # if "Allin" in status_list and max_pot < pot:
        #     side_pot += (pot - max_pot)
        #     pot -= max_pot

        if len(table_deck) == 4:
            txt_box.write("All players have either folded or checked. Let's see the river.", uif)
            next_card()
        elif len(table_deck) == 3:
            txt_box.write("All players have either folded or checked. Let's see the turn.", uif)
            next_card()
        elif len(table_deck) < 3:
            txt_box.write("All players have either folded or checked. Let's see the flop.", uif)
            next_card()
            next_card()
            next_card()

        for i in range(0, len(active_players)):
            if active_players[i].status == "Folded" or active_players[i].status == "Busted" or active_players[i].status == "Allin":
                continue
            else:
                active_players[i].status = ""

        call_target = 0
        bet_incr = 0

        update_status()
        update_UI()

    all_sprites.update()

    # Clear and draw
    all_sprites.draw(screen)
    pygame.display.update()
    pygame.display.flip()
