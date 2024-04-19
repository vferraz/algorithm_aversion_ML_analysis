from otree.api import *
import data as dt
import random 
import reinforcement_learning as rl
import scripts as sc
import itertools
import time 
from datetime import datetime

doc = """
Your app description
"""
#PARTICIPANT_FIELDS = ['total_payoff', 'treatment', 'p1', 'p2', 'p3', 'automation', 'delegation_p','payment_id', 'earnings']
#test commitasdasdasdasdas
class C(BaseConstants):
    NAME_IN_URL = 'experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 4
    #PAYOFF_ROUND = cu()
    
    #Regular probs
    PROB_1 = 0.5
    PROB_2 = 0.7
    PROB_3 = 0.9
    
    #Higher probs (treatment 1b)
    PROB_1_2 = 0.7
    PROB_2_2 = 0.8
    PROB_3_2 = 0.9
    
    #RL Parameters
    PHI = 0.47 # recency parameter
    LAM = 4.5 # sensitivity to attractions
    A0_P1 = 0 # initial attraction product 1
    A0_P2 = 0 # initial attraction product 2
    A0_P3 = 0 # initial attraction product 3
    
    ALGO_COST = 0.1 # cost to pay for algorithm decision
    BASE_PAYOFF = 1 # points earned for correct answer (if probability realized)
    ENDOWMENT = 1 # initial endowment for treatments where payment is available
    CONV_FACTOR = 0.13
    POINTS_PSYCH = 15
    
    AUTO_TIMER = 5 # seconds
 
    CAT_ROUND = 3
    
    ALGO_DESC = 'the algorithm calculates probabilities and chooses an alternative based on the success of choices in previous rounds.'
    #the algorithm learns from past decisions - give an example if box 1 is retuning a payoff, the probability for this selectioin will increase. 
    #explain the process how it adjusts
    

def custom_export(players):
    # header row
    yield [
        'session_code',
        'participant_code',
        'treatment',
        'round_number',
        'selection',
        'delegation',
        'automation',
        'stop_click',
        'prob_1',
        'prob_2',
        'prob_3',
        'prob_selected',
        'payoff_round',
        'payoff_total',
        'attraction_p1',
        'attraction_p2',
        'attraction_p3',
        'choice_prob_p1',
        'choice_prob_p2',
        'choice_prob_p3',
        'payoff_p1',
        'payoff_p2',
        'payoff_p3',
        'perception',
        'payment_id_m',
        'earnings_t',
        'active_time_sel',
        'active_time_fb',
        'active_time_ss',
        'animal_answer',
        'attention_answer',
        'start_timestamp',
        'start_timestamp_readable',
        'age',
        'gender',
        'nationality',
        'university',
        'field_of_study',
        'income_level',
        #'participant_total_payoff',
        #'participant_treatment',
        #'participant_p1',
        #'participant_p2',
        #'participant_p3',
        #'participant_automation',
        #'participant_delegation_p',
        #'participant_payment_id',
        #'participant_earnings',

    ]
    
    for p in players:
            participant = p.participant
            session = p.session
            group = p.group
            yield [
                session.code,
                participant.code,
                p.treatment,
                p.round_number,
                p.selection,
                p.delegation,
                p.automation,
                p.stop_click,
                p.prob_1,
                p.prob_2,
                p.prob_3,
                p.prob_selected,
                p.payoff_round,
                p.payoff_total,
                p.attraction_p1,
                p.attraction_p2,
                p.attraction_p3,
                p.choice_prob_p1,
                p.choice_prob_p2,
                p.choice_prob_p3,
                p.payoff_p1,
                p.payoff_p2,
                p.payoff_p3,
                p.perception,
                p.payment_id_m,
                p.earnings_t,
                p.active_time_sel,
                p.active_time_fb,
                p.active_time_ss,
                p.animal_answer,
                p.attention_answer,
                p.start_timestamp,
                p.start_timestamp_readable,
                p.age,
                p.gender,
                p.nationality,
                p.university,
                p.field_of_study,
                p.income_level,
                #participant.total_payoff,
                #participant.treatment,
                #participant.p1,
                #participant.p2,
                #participant.p3,
                #participant.automation,
                #participant.delegation_p,
                #participant.payment_id,
                #participant.earnings,
            ]

    
# make attention / comprehension check, so that they know what proportional means
    
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    # Subject decision 
    selection = models.IntegerField(widget=widgets.RadioSelect, choices = dt.alternatives)
    
    delegation = models.IntegerField(widget=widgets.RadioSelect, choices = dt.delegate, label='')
    automation = models.IntegerField()
    stop_click = models.IntegerField()
    
    prob_1 = models.FloatField()
    prob_2 = models.FloatField()
    prob_3 = models.FloatField()
    
    image_p1 = models.StringField()
    image_p2 = models.StringField()
    image_p3 = models.StringField()
    
    prob_selected = models.FloatField()
    
    payoff_round = models.FloatField()
    payoff_total = models.FloatField()
    
    #RL variables
    attraction_p1 = models.FloatField()
    attraction_p2 = models.FloatField()
    attraction_p3 = models.FloatField() 
    
    choice_prob_p1 = models.FloatField()
    choice_prob_p2 = models.FloatField()
    choice_prob_p3 = models.FloatField()
    
    payoff_p1 = models.FloatField()
    payoff_p2 = models.FloatField()
    payoff_p3 = models.FloatField()
    
    perception = models.IntegerField(widget=widgets.RadioSelect, choices = dt.perception, label = dt.label_perception)
    
    treatment = models.IntegerField()
    
    selection_algo = models.IntegerField()
    
    payment_id_m = models.StringField()
    
    earnings_t = models.FloatField()
    
    # Attention tracking
    active_time_sel = models.IntegerField()
    active_time_fb = models.IntegerField()
    active_time_ss = models.IntegerField()
    
    animal_answer = models.IntegerField(widget=widgets.RadioSelect, choices = dt.animals, label = dt.label_animal)
    attention_answer = models.IntegerField(widget=widgets.RadioSelect, choices = dt.attention, label = dt.label_attention)
    
    # Time stamps
    start_timestamp = models.IntegerField()
    start_timestamp_readable = models.StringField()
    
    # Demographics
    
    #first_name = models.StringField(label = 'First Name')
    #last_name = models.StringField(label = 'Last Name')
    age = models.IntegerField(max = 100, min = 18)
    gender = models.StringField(choices = dt.genders, label = 'Gender', widget = widgets.RadioSelect)
    nationality = models.StringField(choices = dt.list_of_countries, label = 'Nationality')
    university = models.StringField(choices = dt.universities, label = 'From which university you are taking part in this experiment?')
    field_of_study = models.StringField(choices = dt.study_fields, label = 'What is your field of study?')
    income_level = models.IntegerField(choices = dt.income, label = 'How much money do you have available per month after rent?', widget = widgets.RadioSelect)
   
    
#nt = 10
def creating_session(subsession):
    #treatments = itertools.cycle(list(range(1, nt + 1)))
    treatments = itertools.cycle([3,4,5,7])
                                 
    for player in subsession.get_players():
        
        player.treatment = next(treatments)
        
        if player.treatment == 1 or player.treatment == 2:
            player.delegation = 2
        else:
            pass
        if player.treatment > 6:
            player.automation = 0
        else:
            pass

# selected treatments: 
#    1 - treatment 3 (delegation, black box) - baseline
#    2 - treatment 4 (delegation, white box) - baseline + info
#    3 - treatment 5 (delegation, black box, payment) - baseline + payment
#    4 - treatment 7 (delegation, black box, automation) - baseline + automation


# PAGES
class Demographics(Page):
    def is_displayed(player: Player):
        return player.round_number == 1
    form_model = 'player'
    form_fields = ['age', 'gender', 'nationality', 'university', 'field_of_study', 'income_level']
    
    # def before_next_page(player, timeout_happened):
    #    participant = player.participant
       
    #    participant.treatment = 0
    #    participant.p1 = 0
    #    participant.p2 = 0
    #    participant.p3 = 0
    #    participant.automation = 0
    #    participant.automation = 0
    #    participant.delegation_p = 0
    #    participant.payment_id = 'not_yet_assigned'
    #    participant.earnings = 0
        

class Introduction(Page):
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def vars_for_template(player):
        total_points_possible = (C.NUM_ROUNDS + C.ENDOWMENT + C.POINTS_PSYCH) * C.CONV_FACTOR
        
        return {
            'total_points_possible':total_points_possible}
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        
        participant.total_payoff = C.ENDOWMENT
        player.payoff_total = participant.total_payoff 

        selection_list_1 = [C.PROB_1, C.PROB_2, C.PROB_3]
        selection_list_2 = [C.PROB_1_2, C.PROB_2_2, C.PROB_3_2]

        if player.treatment == 2:
            participant.p1 = selection_list_2.pop(random.randrange(len(selection_list_2)))
            participant.p2 = selection_list_2.pop(random.randrange(len(selection_list_2)))
            participant.p3 = selection_list_2.pop(random.randrange(len(selection_list_2)))
            
        else:
            participant.p1 = selection_list_1.pop(random.randrange(len(selection_list_1)))
            participant.p2 = selection_list_1.pop(random.randrange(len(selection_list_1)))
            participant.p3 = selection_list_1.pop(random.randrange(len(selection_list_1)))
        
            
 #       if player.treatment > 6: 
        participant.automation = 0
#        else:
 #           pass
        participant.payment_id = sc.name_gen_LC(8)
        player.payment_id_m = participant.payment_id
        
        
            

# PAGES
class Instructions_a(Page): # selection only
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.treatment == 1
    
# PAGES
class Instructions_b(Page): # selection only
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.treatment == 2
    
class Instructions_2(Page): # alogorithm, no payment 
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.treatment == 3 or player.round_number == 1 and player.treatment == 4
    
class Instructions_3(Page): # alogorithm, with payment 
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.treatment == 5 or player.round_number == 1 and player.treatment == 6
    
class Instructions_4(Page): # alogorithm, no payment 
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.treatment == 7 or player.round_number == 1 and player.treatment == 8
    
class Instructions_5(Page): # alogorithm, with payment 
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.treatment > 8
    
    
class Perception(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    form_model = 'player'
    form_fields = ['perception']

        
class Subject_selection(Page):
    
    @staticmethod
    def is_displayed(player: Player):
        delegation = player.field_maybe_none('delegation')
        if delegation is None:
            player.delegation = 1
        else:
            pass
        return player.delegation == 2 and player.participant.automation != 1
    # simple choice, information about 3 products of different qualities
    form_model = 'player'
    form_fields = ['selection']

    @staticmethod
    def vars_for_template(player):
        if player.round_number == 1:
            previous_choice = "not yet recorded"
        else:
            prev_round = player.in_round(player.round_number - 1)
            previous_choice = 'Product ' + str(prev_round.selection)
            
        return {
            'previous_choice':previous_choice
            }

    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group
        t = data["information_type"]
        value = data["value"]
        if t == "active_time":
            player.active_time_ss = int(value)

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        
        player.prob_1  = participant.p1
        player.prob_2  = participant.p2
        player.prob_3  = participant.p3


        if player.round_number == 1:
            player.attraction_p1 = C.A0_P1
            player.attraction_p2 = C.A0_P2
            player.attraction_p3 = C.A0_P3
        else:
            prev_round = player.in_round(player.round_number - 1)
            player.attraction_p1 = prev_round.attraction_p1
            player.attraction_p2 = prev_round.attraction_p2
            player.attraction_p3 = prev_round.attraction_p3
            
        
        if player.selection == 1:
           player.prob_selected = player.prob_1
        elif player.selection == 2:
            player.prob_selected = player.prob_2 
        else:
            player.prob_selected = player.prob_3
         
        rand_u = random.uniform(0, 1)
        
        if rand_u <= player.prob_selected:
            player.payoff_round = C.BASE_PAYOFF
        else:
            player.payoff_round = 0
            
        participant.total_payoff += player.payoff_round
        player.payoff_total = participant.total_payoff

        if player.selection == 1:
            player.payoff_p1 = player.payoff_round
            player.payoff_p2 = 0
            player.payoff_p3 = 0
        elif player.selection == 2:
            player.payoff_p1 = 0
            player.payoff_p2 = player.payoff_round
            player.payoff_p3 = 0
        else:
            player.payoff_p1 = 0
            player.payoff_p2 = 0
            player.payoff_p3 = player.payoff_round
        
        (
        player.attraction_p1,  
        player.attraction_p2, 
        player.attraction_p3
        ) = rl.reinforcement_learning_update(
            C.PHI,  
            player.payoff_p1, 
            player.payoff_p2,
            player.payoff_p3, 
            player.attraction_p1, 
            player.attraction_p2, 
            player.attraction_p3)
            
        timestamp = int(time.time())
        player.start_timestamp = timestamp
        player.start_timestamp_readable = datetime.utcfromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        

class Treatment_1b(Page): #Treatment 3
    # player can choose to delegate decision to RL, no information about the algorithm
    form_model = 'player'
    form_fields = ['delegation']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 3
    
    @staticmethod
    def vars_for_template(player):
        if player.round_number == 1:
            previous_choice = "not yet recorded"
        else:
            prev_round = player.in_round(player.round_number - 1)
            previous_choice = 'Product ' + str(prev_round.selection)
            
        return {
            'previous_choice':previous_choice
            }

    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group
        t = data["information_type"]
        value = data["value"]
        if t == "active_time":
            player.active_time_sel = int(value)

    @staticmethod
    def before_next_page(player, timeout_happened):
        
        participant = player.participant
        
        player.prob_1  = participant.p1
        player.prob_2  = participant.p2
        player.prob_3  = participant.p3

        
        if player.round_number == 1:
            player.attraction_p1 = C.A0_P1
            player.attraction_p2 = C.A0_P2
            player.attraction_p3 = C.A0_P3
        else:
            prev_round = player.in_round(player.round_number - 1)
            player.attraction_p1 = prev_round.attraction_p1
            player.attraction_p2 = prev_round.attraction_p2
            player.attraction_p3 = prev_round.attraction_p3
        
        if player.delegation == 1:
        
            (player.choice_prob_p1,
             player.choice_prob_p2,
             player.choice_prob_p3
             ) = rl.prob_gen(C.LAM, 
                             player.attraction_p1, 
                             player.attraction_p2, 
                             player.attraction_p3)
    
            player.selection = rl.product_selection(player.choice_prob_p1, 
                                                    player.choice_prob_p2, 
                                                    player.choice_prob_p3)

    
            if player.selection == 1:
               player.prob_selected = player.prob_1
            elif player.selection == 2:
                player.prob_selected = player.prob_2
            else:
                player.prob_selected = player.prob_3
             
            rand_u = random.uniform(0, 1)
            
            if rand_u <= player.prob_selected:
                player.payoff_round = C.BASE_PAYOFF
            else:
                player.payoff_round = 0

            participant.total_payoff += player.payoff_round
            player.payoff_total = participant.total_payoff
    
            if player.selection == 1:
                player.payoff_p1 = player.payoff_round
                player.payoff_p2 = 0
                player.payoff_p3 = 0
            elif player.selection == 2:
                player.payoff_p1 = 0
                player.payoff_p2 = player.payoff_round
                player.payoff_p3 = 0
            else:
                player.payoff_p1 = 0
                player.payoff_p2 = 0
                player.payoff_p3 = player.payoff_round
            
            (
            player.attraction_p1,  
            player.attraction_p2, 
            player.attraction_p3
            ) = rl.reinforcement_learning_update(
                C.PHI,  
                player.payoff_p1, 
                player.payoff_p2,
                player.payoff_p3, 
                player.attraction_p1, 
                player.attraction_p2, 
                player.attraction_p3)
                    
        else:
            pass
        
        timestamp = int(time.time())
        player.start_timestamp = timestamp
        player.start_timestamp_readable = datetime.utcfromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

#############################################
class Treatment_1c(Page): #Treatment 4
    # player can choose to delegate decision to RL, no information about the algorithm
    form_model = 'player'
    form_fields = ['delegation']

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 4

    @staticmethod
    def vars_for_template(player):
        if player.round_number == 1:
            previous_choice = "not yet recorded"
        else:
            prev_round = player.in_round(player.round_number - 1)
            previous_choice = 'Product ' + str(prev_round.selection)
            
        return {
            'previous_choice':previous_choice
            }
    
    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group
        t = data["information_type"]
        value = data["value"]
        if t == "active_time":
            player.active_time_sel = int(value)

    @staticmethod
    def before_next_page(player, timeout_happened):

        participant = player.participant
        
        player.prob_1  = participant.p1
        player.prob_2  = participant.p2
        player.prob_3  = participant.p3

        
        if player.round_number == 1:
            player.attraction_p1 = C.A0_P1
            player.attraction_p2 = C.A0_P2
            player.attraction_p3 = C.A0_P3
        else:
            prev_round = player.in_round(player.round_number - 1)
            player.attraction_p1 = prev_round.attraction_p1
            player.attraction_p2 = prev_round.attraction_p2
            player.attraction_p3 = prev_round.attraction_p3
        
        if player.delegation == 1:
             
            (player.choice_prob_p1,
             player.choice_prob_p2,
             player.choice_prob_p3
             ) = rl.prob_gen(C.LAM, 
                             player.attraction_p1, 
                             player.attraction_p2, 
                             player.attraction_p3)
    
            player.selection = rl.product_selection(player.choice_prob_p1, 
                                                    player.choice_prob_p2, 
                                                    player.choice_prob_p3)
    
            if player.selection == 1:
               player.prob_selected = player.prob_1
            elif player.selection == 2:
                player.prob_selected = player.prob_2
            else:
                player.prob_selected = player.prob_3
             
            rand_u = random.uniform(0, 1)
            
            if rand_u <= player.prob_selected:
                player.payoff_round = C.BASE_PAYOFF
            else:
                player.payoff_round = 0              
            
            participant.total_payoff += player.payoff_round
            player.payoff_total = participant.total_payoff
    
            if player.selection == 1:
                player.payoff_p1 = player.payoff_round
                player.payoff_p2 = 0
                player.payoff_p3 = 0
            elif player.selection == 2:
                player.payoff_p1 = 0
                player.payoff_p2 = player.payoff_round
                player.payoff_p3 = 0
            else:
                player.payoff_p1 = 0
                player.payoff_p2 = 0
                player.payoff_p3 = player.payoff_round
            
            (
            player.attraction_p1,  
            player.attraction_p2, 
            player.attraction_p3
            ) = rl.reinforcement_learning_update(
                C.PHI,  
                player.payoff_p1, 
                player.payoff_p2,
                player.payoff_p3, 
                player.attraction_p1, 
                player.attraction_p2, 
                player.attraction_p3)
                    
        else:
            pass

        timestamp = int(time.time())
        player.start_timestamp = timestamp
        player.start_timestamp_readable = datetime.utcfromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

#############################################
class Treatment_1d(Page): #Treatment 5
    form_model = 'player'
    form_fields = ['delegation']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 5

    def error_message(player, values):
        participant = player.participant
        if values['delegation'] == 1 and participant.total_payoff < C.ALGO_COST:
            return 'You dont have enough budget. Please accumulate points before you can pay for the decision'
        
    @staticmethod
    def vars_for_template(player):
        if player.round_number == 1:
            previous_choice = "not yet recorded"
        else:
            prev_round = player.in_round(player.round_number - 1)
            previous_choice = 'Product ' + str(prev_round.selection)
            
        return {
            'previous_choice':previous_choice
            }

    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group
        t = data["information_type"]
        value = data["value"]
        if t == "active_time":
            player.active_time_sel = int(value)

    @staticmethod
    def before_next_page(player, timeout_happened):
        
        participant = player.participant

        player.prob_1  = participant.p1
        player.prob_2  = participant.p2
        player.prob_3  = participant.p3
        
        
        if player.round_number == 1:
            player.attraction_p1 = C.A0_P1
            player.attraction_p2 = C.A0_P2
            player.attraction_p3 = C.A0_P3
        else:
            prev_round = player.in_round(player.round_number - 1)
            player.attraction_p1 = prev_round.attraction_p1
            player.attraction_p2 = prev_round.attraction_p2
            player.attraction_p3 = prev_round.attraction_p3
        
        if player.delegation == 1:
            
            participant.total_payoff -= C.ALGO_COST
             
            (player.choice_prob_p1,
            player.choice_prob_p2,
            player.choice_prob_p3
            ) = rl.prob_gen(C.LAM, 
                            player.attraction_p1, 
                            player.attraction_p2, 
                            player.attraction_p3)
    
            player.selection = rl.product_selection(player.choice_prob_p1, 
                                                    player.choice_prob_p2, 
                                                    player.choice_prob_p3)
            if player.selection == 1:
               player.prob_selected = player.prob_1
            elif player.selection == 2:
                player.prob_selected = player.prob_2
            else:
                player.prob_selected = player.prob_3
             
            rand_u = random.uniform(0, 1)
            
            if rand_u <= player.prob_selected:
                player.payoff_round = C.BASE_PAYOFF
            else:
                player.payoff_round = 0

            participant.total_payoff += player.payoff_round
            player.payoff_total = participant.total_payoff
    
            if player.selection == 1:
                player.payoff_p1 = player.payoff_round
                player.payoff_p2 = 0
                player.payoff_p3 = 0
            elif player.selection == 2:
                player.payoff_p1 = 0
                player.payoff_p2 = player.payoff_round
                player.payoff_p3 = 0
            else:
                player.payoff_p1 = 0
                player.payoff_p2 = 0
                player.payoff_p3 = player.payoff_round
            
            (
            player.attraction_p1,  
            player.attraction_p2, 
            player.attraction_p3
            ) = rl.reinforcement_learning_update(
                C.PHI,  
                player.payoff_p1, 
                player.payoff_p2,
                player.payoff_p3, 
                player.attraction_p1, 
                player.attraction_p2, 
                player.attraction_p3)
                    
        else:
            pass
        
        timestamp = int(time.time())
        player.start_timestamp = timestamp
        player.start_timestamp_readable = datetime.utcfromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        
#############################################
class Treatment_1e(Page): #Treatment 6
    form_model = 'player'
    form_fields = ['delegation']

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 6

    def error_message(player, values):
        participant = player.participant
        if values['delegation'] == 1 and participant.total_payoff < C.ALGO_COST:
            return 'You dont have enough budget. Please accumulate points before you can pay for the decision'
        
    @staticmethod
    def vars_for_template(player):
        if player.round_number == 1:
            previous_choice = "not yet recorded"
        else:
            prev_round = player.in_round(player.round_number - 1)
            previous_choice = 'Product ' + str(prev_round.selection)
            
        return {
            'previous_choice':previous_choice
            }

    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group
        t = data["information_type"]
        value = data["value"]
        if t == "active_time":
            player.active_time_sel = int(value)
                
    @staticmethod
    def before_next_page(player, timeout_happened):
        
        participant = player.participant
        
        player.prob_1  = participant.p1
        player.prob_2  = participant.p2
        player.prob_3  = participant.p3
        
        if player.round_number == 1:
            player.attraction_p1 = C.A0_P1
            player.attraction_p2 = C.A0_P2
            player.attraction_p3 = C.A0_P3
        else:
            prev_round = player.in_round(player.round_number - 1)
            player.attraction_p1 = prev_round.attraction_p1
            player.attraction_p2 = prev_round.attraction_p2
            player.attraction_p3 = prev_round.attraction_p3
        
        if player.delegation == 1:
            
            participant.total_payoff -= C.ALGO_COST

             
            (player.choice_prob_p1,
             player.choice_prob_p2,
             player.choice_prob_p3
             ) = rl.prob_gen(C.LAM, 
                             player.attraction_p1, 
                             player.attraction_p2, 
                             player.attraction_p3)
    
            player.selection = rl.product_selection(player.choice_prob_p1, 
                                                    player.choice_prob_p2, 
                                                    player.choice_prob_p3)
            
            if player.selection == 1:
               player.prob_selected = player.prob_1
            elif player.selection == 2:
                player.prob_selected = player.prob_2
            else:
                player.prob_selected = player.prob_3
             
            rand_u = random.uniform(0, 1)
            
            if rand_u <= player.prob_selected:
                player.payoff_round = C.BASE_PAYOFF
            else:
                player.payoff_round = 0

            participant.total_payoff += player.payoff_round
            player.payoff_total = participant.total_payoff
    
            if player.selection == 1:
                player.payoff_p1 = player.payoff_round
                player.payoff_p2 = 0
                player.payoff_p3 = 0
            elif player.selection == 2:
                player.payoff_p1 = 0
                player.payoff_p2 = player.payoff_round
                player.payoff_p3 = 0
            else:
                player.payoff_p1 = 0
                player.payoff_p2 = 0
                player.payoff_p3 = player.payoff_round
            
            (
            player.attraction_p1,  
            player.attraction_p2, 
            player.attraction_p3
            ) = rl.reinforcement_learning_update(
                C.PHI,  
                player.payoff_p1, 
                player.payoff_p2,
                player.payoff_p3, 
                player.attraction_p1, 
                player.attraction_p2, 
                player.attraction_p3)
                
        timestamp = int(time.time())
        player.start_timestamp = timestamp
        player.start_timestamp_readable = datetime.utcfromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
                

#############################################
class Treatment_1f(Page): #Treatment 7
    # automated, black box, no payment
    form_model = 'player'
    form_fields = ['delegation']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 7 and player.participant.automation != 1
    
    @staticmethod
    def vars_for_template(player):
        if player.round_number == 1:
            previous_choice = "not yet recorded"
        else:
            prev_round = player.in_round(player.round_number - 1)
            previous_choice = 'Product ' + str(prev_round.selection)
            
        return {
            'previous_choice':previous_choice
            }

    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group
        t = data["information_type"]
        value = data["value"]
        if t == "active_time":
            player.active_time_sel = int(value)

    @staticmethod
    def before_next_page(player, timeout_happened):
        
        participant = player.participant
        
        player.prob_1  = participant.p1
        player.prob_2  = participant.p2
        player.prob_3  = participant.p3

        
        if player.round_number == 1:
            player.attraction_p1 = C.A0_P1
            player.attraction_p2 = C.A0_P2
            player.attraction_p3 = C.A0_P3
        else:
            prev_round = player.in_round(player.round_number - 1)
            player.attraction_p1 = prev_round.attraction_p1
            player.attraction_p2 = prev_round.attraction_p2
            player.attraction_p3 = prev_round.attraction_p3
        
        if player.delegation == 1:
            
            participant.automation = 1
        
            (player.choice_prob_p1,
             player.choice_prob_p2,
             player.choice_prob_p3
             ) = rl.prob_gen(C.LAM, 
                             player.attraction_p1, 
                             player.attraction_p2, 
                             player.attraction_p3)
    
            player.selection = rl.product_selection(player.choice_prob_p1, 
                                                    player.choice_prob_p2, 
                                                    player.choice_prob_p3)

    
            if player.selection == 1:
                player.prob_selected = player.prob_1
                player.image_p1 = 'product1_s.png'
                player.image_p2 = 'product2.png'
                player.image_p3 = 'product3.png'
               
            elif player.selection == 2:
                player.prob_selected = player.prob_2
                player.image_p1 = 'product1.png'
                player.image_p2 = 'product2_s.png'
                player.image_p3 = 'product3.png'
            else:
                player.prob_selected = player.prob_3
                player.image_p1 = 'product1.png'
                player.image_p2 = 'product2.png'
                player.image_p3 = 'product3_s.png'
                
            rand_u = random.uniform(0, 1)
            
            if rand_u <= player.prob_selected:
                player.payoff_round = C.BASE_PAYOFF
            else:
                player.payoff_round = 0

            participant.total_payoff += player.payoff_round
            player.payoff_total = participant.total_payoff
    
            if player.selection == 1:
                player.payoff_p1 = player.payoff_round
                player.payoff_p2 = 0
                player.payoff_p3 = 0
            elif player.selection == 2:
                player.payoff_p1 = 0
                player.payoff_p2 = player.payoff_round
                player.payoff_p3 = 0
            else:
                player.payoff_p1 = 0
                player.payoff_p2 = 0
                player.payoff_p3 = player.payoff_round
            
            (
            player.attraction_p1,  
            player.attraction_p2, 
            player.attraction_p3
            ) = rl.reinforcement_learning_update(
                C.PHI,  
                player.payoff_p1, 
                player.payoff_p2,
                player.payoff_p3, 
                player.attraction_p1, 
                player.attraction_p2, 
                player.attraction_p3)
                    
        else:
            participant.automation = 0
            
        player.automation = participant.automation
        timestamp = int(time.time())
        player.start_timestamp = timestamp
        player.start_timestamp_readable = datetime.utcfromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

#############################################
class Treatment_1g(Page): #Treatment 8
    # automated, white box, no payment
    form_model = 'player'
    form_fields = ['delegation']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 8 and player.participant.automation != 1

    @staticmethod
    def vars_for_template(player):
        if player.round_number == 1:
            previous_choice = "not yet recorded"
        else:
            prev_round = player.in_round(player.round_number - 1)
            previous_choice = 'Product ' + str(prev_round.selection)
            
        return {
            'previous_choice':previous_choice
            }

    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group
        t = data["information_type"]
        value = data["value"]
        if t == "active_time":
            player.active_time_sel = int(value)
            
    @staticmethod
    def before_next_page(player, timeout_happened):
        
        participant = player.participant
        
        player.prob_1  = participant.p1
        player.prob_2  = participant.p2
        player.prob_3  = participant.p3

        
        if player.round_number == 1:
            player.attraction_p1 = C.A0_P1
            player.attraction_p2 = C.A0_P2
            player.attraction_p3 = C.A0_P3
        else:
            prev_round = player.in_round(player.round_number - 1)
            player.attraction_p1 = prev_round.attraction_p1
            player.attraction_p2 = prev_round.attraction_p2
            player.attraction_p3 = prev_round.attraction_p3
        
        if player.delegation == 1:
            
            participant.automation = 1
        
            (player.choice_prob_p1,
             player.choice_prob_p2,
             player.choice_prob_p3
             ) = rl.prob_gen(C.LAM, 
                             player.attraction_p1, 
                             player.attraction_p2, 
                             player.attraction_p3)
    
            player.selection = rl.product_selection(player.choice_prob_p1, 
                                                    player.choice_prob_p2, 
                                                    player.choice_prob_p3)

    
            if player.selection == 1:
                player.prob_selected = player.prob_1
                player.image_p1 = 'product1_s.png'
                player.image_p2 = 'product2.png'
                player.image_p3 = 'product3.png'
               
            elif player.selection == 2:
                player.prob_selected = player.prob_2
                player.image_p1 = 'product1.png'
                player.image_p2 = 'product2_s.png'
                player.image_p3 = 'product3.png'
            else:
                player.prob_selected = player.prob_3
                player.image_p1 = 'product1.png'
                player.image_p2 = 'product2.png'
                player.image_p3 = 'product3_s.png'
                
            rand_u = random.uniform(0, 1)
            
            if rand_u <= player.prob_selected:
                player.payoff_round = C.BASE_PAYOFF
            else:
                player.payoff_round = 0

            participant.total_payoff += player.payoff_round
            player.payoff_total = participant.total_payoff
    
            if player.selection == 1:
                player.payoff_p1 = player.payoff_round
                player.payoff_p2 = 0
                player.payoff_p3 = 0
            elif player.selection == 2:
                player.payoff_p1 = 0
                player.payoff_p2 = player.payoff_round
                player.payoff_p3 = 0
            else:
                player.payoff_p1 = 0
                player.payoff_p2 = 0
                player.payoff_p3 = player.payoff_round
            
            (
            player.attraction_p1,  
            player.attraction_p2, 
            player.attraction_p3
            ) = rl.reinforcement_learning_update(
                C.PHI,  
                player.payoff_p1, 
                player.payoff_p2,
                player.payoff_p3, 
                player.attraction_p1, 
                player.attraction_p2, 
                player.attraction_p3)
                    
        else:
            pass

        timestamp = int(time.time())
        player.start_timestamp = timestamp
        player.start_timestamp_readable = datetime.utcfromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

#############################################
class Treatment_1h(Page): #Treatment 9
    # automated, black box, with payment
    form_model = 'player'
    form_fields = ['delegation']
    
    @staticmethod
    def is_displayed(player: Player):
        
        return player.treatment == 9 and player.participant.automation != 1
    
    def error_message(player, values):
        participant = player.participant
        if values['delegation'] == 1 and participant.total_payoff < C.ALGO_COST:
            return "You dont have enough budget. Please accumulate points before you can pay for the algorithm's support"
        
    @staticmethod
    def vars_for_template(player):
        if player.round_number == 1:
            previous_choice = "not yet recorded"
        else:
            prev_round = player.in_round(player.round_number - 1)
            previous_choice = 'Product ' + str(prev_round.selection)
            
        return {
            'previous_choice':previous_choice
            }

    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group
        t = data["information_type"]
        value = data["value"]
        if t == "active_time":
            player.active_time_sel = int(value)
                
    @staticmethod
    def before_next_page(player, timeout_happened):
        
        participant = player.participant
        
        player.prob_1  = participant.p1
        player.prob_2  = participant.p2
        player.prob_3  = participant.p3

        
        if player.round_number == 1:
            player.attraction_p1 = C.A0_P1
            player.attraction_p2 = C.A0_P2
            player.attraction_p3 = C.A0_P3
        else:
            prev_round = player.in_round(player.round_number - 1)
            player.attraction_p1 = prev_round.attraction_p1
            player.attraction_p2 = prev_round.attraction_p2
            player.attraction_p3 = prev_round.attraction_p3
        
        if player.delegation == 1:
            
            participant.total_payoff -= C.ALGO_COST
            
            participant.automation = 1
        
            (player.choice_prob_p1,
             player.choice_prob_p2,
             player.choice_prob_p3
             ) = rl.prob_gen(C.LAM, 
                             player.attraction_p1, 
                             player.attraction_p2, 
                             player.attraction_p3)
    
            player.selection = rl.product_selection(player.choice_prob_p1, 
                                                    player.choice_prob_p2, 
                                                    player.choice_prob_p3)

            if player.selection == 1:
                player.prob_selected = player.prob_1
                player.image_p1 = 'product1_s.png'
                player.image_p2 = 'product2.png'
                player.image_p3 = 'product3.png'
               
            elif player.selection == 2:
                player.prob_selected = player.prob_2
                player.image_p1 = 'product1.png'
                player.image_p2 = 'product2_s.png'
                player.image_p3 = 'product3.png'
            else:
                player.prob_selected = player.prob_3
                player.image_p1 = 'product1.png'
                player.image_p2 = 'product2.png'
                player.image_p3 = 'product3_s.png'
                
            rand_u = random.uniform(0, 1)
            
            if rand_u <= player.prob_selected:
                player.payoff_round = C.BASE_PAYOFF
            else:
                player.payoff_round = 0

            participant.total_payoff += player.payoff_round
            player.payoff_total = participant.total_payoff
    
            if player.selection == 1:
                player.payoff_p1 = player.payoff_round
                player.payoff_p2 = 0
                player.payoff_p3 = 0
            elif player.selection == 2:
                player.payoff_p1 = 0
                player.payoff_p2 = player.payoff_round
                player.payoff_p3 = 0
            else:
                player.payoff_p1 = 0
                player.payoff_p2 = 0
                player.payoff_p3 = player.payoff_round
            
            (
            player.attraction_p1,  
            player.attraction_p2, 
            player.attraction_p3
            ) = rl.reinforcement_learning_update(
                C.PHI,  
                player.payoff_p1, 
                player.payoff_p2,
                player.payoff_p3, 
                player.attraction_p1, 
                player.attraction_p2, 
                player.attraction_p3)
                    
        else:
            pass
        
        timestamp = int(time.time())
        player.start_timestamp = timestamp
        player.start_timestamp_readable = datetime.utcfromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

#############################################
class Treatment_1i(Page): #Treatment 10
    # automated, black box, with payment
    form_model = 'player'
    form_fields = ['delegation']
    
    @staticmethod
    def is_displayed(player: Player):
        
        return player.treatment == 10 and player.participant.automation != 1
    
    def error_message(player, values):
        participant = player.participant
        if values['delegation'] == 1 and participant.total_payoff < C.ALGO_COST:
            return "You dont have enough budget. Please accumulate points before you can pay for the algorithm's support"
        
    @staticmethod
    def vars_for_template(player):
        if player.round_number == 1:
            previous_choice = "not yet recorded"
        else:
            prev_round = player.in_round(player.round_number - 1)
            previous_choice = 'Product ' + str(prev_round.selection)
            
        return {
            'previous_choice':previous_choice
            }
                
    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group
        t = data["information_type"]
        value = data["value"]
        if t == "active_time":
            player.active_time_sel = int(value)

    @staticmethod
    def before_next_page(player, timeout_happened):
        
        participant = player.participant
        
        player.prob_1  = participant.p1
        player.prob_2  = participant.p2
        player.prob_3  = participant.p3

        
        if player.round_number == 1:
            player.attraction_p1 = C.A0_P1
            player.attraction_p2 = C.A0_P2
            player.attraction_p3 = C.A0_P3
        else:
            prev_round = player.in_round(player.round_number - 1)
            player.attraction_p1 = prev_round.attraction_p1
            player.attraction_p2 = prev_round.attraction_p2
            player.attraction_p3 = prev_round.attraction_p3
        
        if player.delegation == 1:
            
            participant.total_payoff -= C.ALGO_COST
            
            participant.automation = 1
        
            (player.choice_prob_p1,
             player.choice_prob_p2,
             player.choice_prob_p3
             ) = rl.prob_gen(C.LAM, 
                             player.attraction_p1, 
                             player.attraction_p2, 
                             player.attraction_p3)
    
            player.selection = rl.product_selection(player.choice_prob_p1, 
                                                    player.choice_prob_p2, 
                                                    player.choice_prob_p3)

            if player.selection == 1:
                player.prob_selected = player.prob_1
                player.image_p1 = 'product1_s.png'
                player.image_p2 = 'product2.png'
                player.image_p3 = 'product3.png'
               
            elif player.selection == 2:
                player.prob_selected = player.prob_2
                player.image_p1 = 'product1.png'
                player.image_p2 = 'product2_s.png'
                player.image_p3 = 'product3.png'
            else:
                player.prob_selected = player.prob_3
                player.image_p1 = 'product1.png'
                player.image_p2 = 'product2.png'
                player.image_p3 = 'product3_s.png'
                
            rand_u = random.uniform(0, 1)
            
            if rand_u <= player.prob_selected:
                player.payoff_round = C.BASE_PAYOFF
            else:
                player.payoff_round = 0

            participant.total_payoff += player.payoff_round
            player.payoff_total = participant.total_payoff
    
            if player.selection == 1:
                player.payoff_p1 = player.payoff_round
                player.payoff_p2 = 0
                player.payoff_p3 = 0
            elif player.selection == 2:
                player.payoff_p1 = 0
                player.payoff_p2 = player.payoff_round
                player.payoff_p3 = 0
            else:
                player.payoff_p1 = 0
                player.payoff_p2 = 0
                player.payoff_p3 = player.payoff_round
            
            (
            player.attraction_p1,  
            player.attraction_p2, 
            player.attraction_p3
            ) = rl.reinforcement_learning_update(
                C.PHI,  
                player.payoff_p1, 
                player.payoff_p2,
                player.payoff_p3, 
                player.attraction_p1, 
                player.attraction_p2, 
                player.attraction_p3)
                    
        else:
            pass
                
        
class Feedback(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.automation != 1
    
    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group
        t = data["information_type"]
        value = data["value"]
        if t == "active_time":
            player.active_time_fb = int(value)

class Feedback_auto(Page):
    
    timeout_seconds = C.AUTO_TIMER
    timer_text = 'Time left to take back control before the algorithm decides for the round:'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 7 and player.participant.automation == 1
        #return player.treatment == 7 or player.treatment == 8 and player.automation == 1
    
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        
        participant = player.participant
        
        player.prob_1  = participant.p1
        player.prob_2  = participant.p2
        player.prob_3  = participant.p3
        
        if player.round_number == 1:
            pass
        
        elif player.in_round(player.round_number - 1).delegation == 2:
            pass
        
        else:
            
            #player.in_round(player.round_number - 1).selection
            
            prev_round = player.in_round(player.round_number - 1)
            player.attraction_p1 = prev_round.attraction_p1
            player.attraction_p2 = prev_round.attraction_p2
            player.attraction_p3 = prev_round.attraction_p3
        
            (player.choice_prob_p1,
             player.choice_prob_p2,
             player.choice_prob_p3
             ) = rl.prob_gen(C.LAM, 
                             player.attraction_p1, 
                             player.attraction_p2, 
                             player.attraction_p3)
    
            player.selection = rl.product_selection(player.choice_prob_p1, 
                                                    player.choice_prob_p2, 
                                                    player.choice_prob_p3)
    
            if player.selection == 1:
                player.prob_selected = player.prob_1
                player.image_p1 = 'product1_s.png'
                player.image_p2 = 'product2.png'
                player.image_p3 = 'product3.png'
               
            elif player.selection == 2:
                player.prob_selected = player.prob_2
                player.image_p1 = 'product1.png'
                player.image_p2 = 'product2_s.png'
                player.image_p3 = 'product3.png'
            else:
                player.prob_selected = player.prob_3
                player.image_p1 = 'product1.png'
                player.image_p2 = 'product2.png'
                player.image_p3 = 'product3_s.png'
             
            rand_u = random.uniform(0, 1)
            if rand_u <= player.prob_selected:
                player.payoff_round = C.BASE_PAYOFF
            else:
                player.payoff_round = 0
    
            participant.total_payoff += player.payoff_round
            player.payoff_total = participant.total_payoff
    
            if player.selection == 1:
                player.payoff_p1 = player.payoff_round
                player.payoff_p2 = 0
                player.payoff_p3 = 0
            elif player.selection == 2:
                player.payoff_p1 = 0
                player.payoff_p2 = player.payoff_round
                player.payoff_p3 = 0
            else:
                player.payoff_p1 = 0
                player.payoff_p2 = 0
                player.payoff_p3 = player.payoff_round
            
            (
            player.attraction_p1,  
            player.attraction_p2, 
            player.attraction_p3
            ) = rl.reinforcement_learning_update(
                C.PHI,  
                player.payoff_p1, 
                player.payoff_p2,
                player.payoff_p3, 
                player.attraction_p1, 
                player.attraction_p2, 
                player.attraction_p3)
                
            player.automation = participant.automation
                
    @staticmethod
    def live_method(player: Player, data):
        participant = player.participant
        my_id = player.id_in_group
        t = data["information_type"]
        value = data["value"]
        if t == "stop":
            participant.automation = int(value)
        if t == "button_click":
            player.stop_click = int(value)
        if t == "active_time":
            player.active_time_fb = int(value)
            
    @staticmethod
    def vars_for_template(player):
        
        selection = player.field_maybe_none('selection')
        
        if selection is None:
            selection_show = player.in_round(player.round_number - 1).selection
            payoff_show = player.in_round(player.round_number - 1).payoff_round
            total_payoff_show = player.in_round(player.round_number - 1).payoff_total
            img_p1 = player.in_round(player.round_number - 1).image_p1
            img_p2 = player.in_round(player.round_number - 1).image_p2
            img_p3 = player.in_round(player.round_number - 1).image_p3
        else:
            selection_show = player.selection
            payoff_show = player.payoff_round
            total_payoff_show = player.payoff_total
            img_p1 = player.image_p1
            img_p2 = player.image_p2
            img_p3 = player.image_p3
            
        return {
            'selection_show': selection_show,
            'payoff_show': payoff_show,
            'total_payoff_show': total_payoff_show,
            'img_p1': img_p1,
            'img_p2': img_p2,
            'img_p3': img_p3 
            }

class Feedback_auto2(Page):
    
    timeout_seconds = C.AUTO_TIMER
    timer_text = 'Time left to take back control before the algorithm decides for the round:'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment > 8 and player.participant.automation == 1
    
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        
        participant = player.participant
        
        player.prob_1  = participant.p1
        player.prob_2  = participant.p2
        player.prob_3  = participant.p3
        
        if participant.total_payoff >= C.ALGO_COST:  
            

            if player.round_number == 1:
                pass
            
            elif player.in_round(player.round_number - 1).delegation == 2:
                pass
            
            else:
                
                #player.in_round(player.round_number - 1).selection
                
                prev_round = player.in_round(player.round_number - 1)
                player.attraction_p1 = prev_round.attraction_p1
                player.attraction_p2 = prev_round.attraction_p2
                player.attraction_p3 = prev_round.attraction_p3
            
                (player.choice_prob_p1,
                 player.choice_prob_p2,
                 player.choice_prob_p3
                 ) = rl.prob_gen(C.LAM, 
                                 player.attraction_p1, 
                                 player.attraction_p2, 
                                 player.attraction_p3)
        
                player.selection = rl.product_selection(player.choice_prob_p1, 
                                                        player.choice_prob_p2, 
                                                        player.choice_prob_p3)
        
                if player.selection == 1:
                    player.prob_selected = player.prob_1
                    player.image_p1 = 'product1_s.png'
                    player.image_p2 = 'product2.png'
                    player.image_p3 = 'product3.png'
                   
                elif player.selection == 2:
                    player.prob_selected = player.prob_2
                    player.image_p1 = 'product1.png'
                    player.image_p2 = 'product2_s.png'
                    player.image_p3 = 'product3.png'
                else:
                    player.prob_selected = player.prob_3
                    player.image_p1 = 'product1.png'
                    player.image_p2 = 'product2.png'
                    player.image_p3 = 'product3_s.png'
                 
                rand_u = random.uniform(0, 1)
                if rand_u <= player.prob_selected:
                    player.payoff_round = C.BASE_PAYOFF
                else:
                    player.payoff_round = 0
                
                participant.total_payoff -= C.ALGO_COST
                
                participant.total_payoff += player.payoff_round
                
                player.payoff_total = participant.total_payoff
        
                if player.selection == 1:
                    player.payoff_p1 = player.payoff_round
                    player.payoff_p2 = 0
                    player.payoff_p3 = 0
                elif player.selection == 2:
                    player.payoff_p1 = 0
                    player.payoff_p2 = player.payoff_round
                    player.payoff_p3 = 0
                else:
                    player.payoff_p1 = 0
                    player.payoff_p2 = 0
                    player.payoff_p3 = player.payoff_round
                
                (
                player.attraction_p1,  
                player.attraction_p2, 
                player.attraction_p3
                ) = rl.reinforcement_learning_update(
                    C.PHI,  
                    player.payoff_p1, 
                    player.payoff_p2,
                    player.payoff_p3, 
                    player.attraction_p1, 
                    player.attraction_p2, 
                    player.attraction_p3)    
                
        else:
            participant.automation = 0
                    
    @staticmethod
    def live_method(player: Player, data):
        participant = player.participant
        my_id = player.id_in_group
        t = data["information_type"]
        value = data["value"]
        if t == "stop":
            participant.automation = int(value)
        if t == "button_click":
            player.stop_click = int(value)
        if t == "active_time":
            player.active_time_fb = int(value)
            

    @staticmethod
    def vars_for_template(player):
        
        selection = player.field_maybe_none('selection')
        
        if selection is None:
            selection_show = player.in_round(player.round_number - 1).selection
            payoff_show = player.in_round(player.round_number - 1).payoff_round
            total_payoff_show = player.in_round(player.round_number - 1).payoff_total
            img_p1 = player.in_round(player.round_number - 1).image_p1
            img_p2 = player.in_round(player.round_number - 1).image_p2
            img_p3 = player.in_round(player.round_number - 1).image_p3
        else:
            selection_show = player.selection
            payoff_show = player.payoff_round
            total_payoff_show = player.payoff_total
            img_p1 = player.image_p1
            img_p2 = player.image_p2
            img_p3 = player.image_p3
            
        return {
            'selection_show': selection_show,
            'payoff_show': payoff_show,
            'total_payoff_show': total_payoff_show,
            'img_p1': img_p1,
            'img_p2': img_p2,
            'img_p3': img_p3 
            }

class Results(Page):
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        player.payment_id_m = participant.payment_id
        
class Attention_regular(Page):
    def is_displayed(player: Player):
        return player.treatment < 7 and player.round_number == C.NUM_ROUNDS
    
    form_model = 'player'
    form_fields = ['animal_answer']

class Attention_auto(Page):
    def is_displayed(player: Player):
        return player.treatment > 6 and player.round_number == C.NUM_ROUNDS
    
    form_model = 'player'
    form_fields = ['attention_answer', 'animal_answer']



page_sequence = [Introduction,
                 Demographics,
                 Instructions_a,
                 Instructions_b,
                 Instructions_2,
                 Instructions_3,
                 Instructions_4,
                 Instructions_5,
                 Perception,
                 Treatment_1b,
                 Treatment_1c,
                 Treatment_1d,
                 Treatment_1e, 
                 Treatment_1f,
                 Treatment_1g,
                 Treatment_1h,
                 Treatment_1i,
                 Subject_selection, 
                 Feedback,
                 Feedback_auto,
                 Feedback_auto2,
                 Results,
                 Attention_regular,
                 Attention_auto]
