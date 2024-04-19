from otree.api import *
import data as dt
import random 
import reinforcement_learning as rl
import scripts as scripts
import itertools
import time 
from datetime import datetime

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    POINTS_PSYCH = 15
    CONV_FACTOR = 0.13
    #PAYOFF_ROUND = cu()
    

def custom_export(players):
    # header row
    yield [
        'session.code',
        'participant.code',
        'b1',
        'b2',
        'b3',
        'b4',
        'b5',
        'b6',
        'b7',
        'b8',
        'b9',
        'b10',
        'b11',
        'b12',
        'b13',
        'b14',
        'b15',
        'ba1',
        'ba2',
        'ba3',
        'ba4',
        'extraversion',
        'agreeableness',
        'conscientiousness',
        'neuroticism',
        'openness',
        'loc1',
        'loc2',
        'loc3',
        'loc4',
        'loc5',
        'loc6',
        'loc7',
        'loc8',
        'loc9',
        'loc10',
        'loc_general',
        't1',
        't3',
        't3',
        't4',
        't5',
        'trust',
        'start_timestamp',
        'start_timestamp_readable',
        'payoff_total_final',
        'payment_id_m',
        'payment_id_m',
        'earnings_t',
        'understanding_beginning',
        'instructions',
        'approach',
        'any_problems',
        'open_comments',
        #'participant.total_payoff',
        #'participant.payment_id'

    ]
    
    for p in players:
            participant = p.participant
            session = p.session
            group = p.group
            yield [
                session.code,
                participant.code,
                p.b1,
                p.b2,
                p.b3,
                p.b4,
                p.b5,
                p.b6,
                p.b7,
                p.b8,
                p.b9,
                p.b10,
                p.b11,
                p.b12,
                p.b13,
                p.b14,
                p.b15,
                p.ba1,
                p.ba2,
                p.ba3,
                p.ba4,
                p.extraversion,
                p.agreeableness,
                p.conscientiousness,
                p.neuroticism,
                p.openness,
                p.loc1,
                p.loc2,
                p.loc3,
                p.loc4,
                p.loc5,
                p.loc6,
                p.loc7,
                p.loc8,
                p.loc9,
                p.loc10,
                p.loc_general,
                p.t1,
                p.t3,
                p.t3,
                p.t4,
                p.t5,
                p.trust,
                p.start_timestamp,
                p.start_timestamp_readable,
                p.payoff_total_final,
                p.payment_id_m,
                p.payment_id_m,
                p.earnings_t,
                p.understanding_beginning,
                p.instructions,
                p.approach,
                p.any_problems,
                p.open_comments,
                #participant.total_payoff,
                #participant.payment_id
            ]
    


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


# make Big Five
def make_bf(label):
    return models.IntegerField(
        choices=[
            [1, "Strongly Disagree"],
            [2, "Disagree"],
            [3, "Somewhat Disagree"],
            [4, "Neither agree nor disagree"],
            [5, "Somewhat Agree"],
            [6, "Agree"],
            [7, "Strongly Agree"]],
        label=label,
        widget=widgets.RadioSelect,
    )


def make_bfrev(label):
    return models.IntegerField(
        choices=[
            [7, "Strongly Disagree"],
            [6, "Disagree"],
            [5, "Somewhat Disagree"],
            [4, "Neither agree nor disagree"],
            [3, "Somewhat Agree"],
            [2, "Agree"],
            [1, "Strongly Agree"]],
        label=label,
        widget=widgets.RadioSelect,
    )


class Player(BasePlayer):
    #   big five
    b1 = make_bf("worries a lot")
    b2 = make_bf("gets nervous easily")
    b3 = make_bfrev("remains calm in tense situations")
    b4 = make_bf("is talkative")
    b5 = make_bf("is outgoing, sociable")
    b6 = make_bfrev("is reserved")
    b7 = make_bf("is original, comes up with new ideas")
    b8 = make_bf("values artistic, aesthetic experiences")
    b9 = make_bf("has an active  imagination")
    b10 = make_bfrev("is sometimes rude to others")
    b11 = make_bf("has a forgiving nature")
    b12 = make_bf("is considerate and kind to almost everyone")
    b13 = make_bf("does a thorough job")
    b14 = make_bfrev("tends to be lazy")
    b15 = make_bf("does things efficiently")
    
    #control questions
    ba1 = make_bf("control question, please select somewhat agree") #5
    ba2 = make_bf("please select disagree") #2
    ba3 = make_bf("please select strongly agree") #7
    ba4 = make_bf("please select neither agree nor disagree") #4
    
    # Big Five Score
    extraversion = models.FloatField()
    agreeableness = models.FloatField()
    conscientiousness = models.FloatField()
    neuroticism = models.FloatField()
    openness = models.FloatField()


    # locus of control
    loc1 = make_bf("How my life goes depends on me.")
    loc2 = make_bfrev("Compared to other people, I have not achieved what I deserve.")
    loc3 = make_bfrev("What a person achieves in life is above all a question of fate or luck.")
    loc4 = make_bf("If a person is socially or politically active, he/she can have an effect on social conditions.")
    loc5 = make_bfrev("I frequently have the experience that other people have a controlling influence over my life.")
    loc6 = make_bf("One has to work hard in order to succeed.")
    loc7 = make_bfrev("If I run up against difficulties in life, I often doubt my own abilities.")
    loc8 = make_bfrev("The opportunities that I have in life are determined by the social conditions.")
    loc9 = make_bfrev("Innate abilities are more important than any efforts one can make.")
    loc10 = make_bfrev("I have little control over the things that happen in my life.")
    

    loc_general = models.FloatField()

    # generalized trust
    t1 = make_bf("On the whole, one can trust people.")
    t2 = make_bfrev("Nowadays one can’t depend on anyone.")
    t3 = make_bfrev("When dealing with strangers, it is better to be cautious before trusting them.")
    t4 = make_bfrev("... would exploit you if they had the opportunity.")
    t5 = make_bf("... attempt to be helpful?")

    trust = models.FloatField()
    
    # Time stamps
    start_timestamp = models.IntegerField()
    start_timestamp_readable = models.StringField()
    
    payoff_total_final = models.FloatField()
    payment_id_m = models.StringField()
    
    earnings_t = models.FloatField()
    
    # open questions
    understanding_beginning = models.IntegerField(label = 'On a scale from 1-10, how well did you understand the instructions?', choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], widget=widgets.RadioSelectHorizontal, blank=True)
    instructions = models.LongStringField(label = 'Do you have suggestions for the instructions?', blank=True)
    approach = models.LongStringField(label = 'How did you approach the tasks?', blank=True)
    any_problems = models.LongStringField(label = 'Did you experience any problems?', blank=True)
    open_comments = models.LongStringField(label = 'Do you have any other comments, thoughts or feedback?', blank=True)
    
   



    # calculating scores
    @staticmethod
    def calc_bigfive(player):
        player.extraversion = float(player.b4 + player.b5 + player.b6) / 3.0
        player.agreeableness = float(player.b10 + player.b11 + player.b12) / 3.0
        player.conscientiousness = float(player.b13 + player.b14 + player.b15) / 3.0
        player.neuroticism = float(player.b1 + player.b2 + player.b3) / 3.0
        player.openness = float(player.b7 + player.b8 + player.b9) / 3.0

    @staticmethod
    def calc_LoC(player):
        player.loc_general = float(player.loc1 + player.loc2 + player.loc3 + player.loc5 + player.loc7 + player.loc8 + player.loc10)/ 7

    @staticmethod
    def calc_trust(player):
        player.trust = float(player.t1 + player.t2 + player.t3) / 3
    

def creating_session(subsession):
    pass
        
# PAGES

class Intro_Psych(Page):
    pass

class BigFive(Page):
    form_model = 'player'
    form_fields = ['b1', 'b2', 'b3', 'b4','ba1' ,'b5', 'b6', 'b7']        
        


class BigFive2(Page):
    form_model = 'player'
    form_fields = ['b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'b14','ba2' ,'b15']
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.calc_bigfive(player)


class LoC(Page):
    form_model = 'player'
    form_fields = ['loc1', 'loc2','ba3' ,'loc3', 'loc4', 'loc5', 'loc6', 'loc7', 'loc8', 'loc9', 'loc10']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.calc_LoC(player)


class Trust(Page):
    form_model = 'player'
    form_fields = ['t1','ba4' ,'t2', 't3']
    
class Trust2(Page):
    
    form_model = 'player'
    form_fields = ['t4']


class Trust3(Page):
    form_model = 'player'
    form_fields = ['t5']
    
    

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.calc_trust(player)

        timestamp = int(time.time())
        player.start_timestamp = timestamp
        player.start_timestamp_readable = datetime.utcfromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        participant = player.participant
        if player.ba1 == 5 and player.ba2 == 2 and player.ba3 == 7 and player.ba4 == 4:
            participant.total_payoff += C.POINTS_PSYCH
            player.payoff_total_final = participant.total_payoff
        else:
            player.payoff_total_final = participant.total_payoff
            


class Questions_trial(Page):
    form_model = 'player'
    form_fields = ['understanding_beginning', 'instructions', 'approach', 'any_problems', 'open_comments']


class Final_page(Page):
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    def vars_for_template(player):
     participant = player.participant
     player.payment_id_m = participant.payment_id
     
     if player.ba1 == 5 and player.ba2 == 2 and player.ba3 == 7 and player.ba4 == 4:
         questions_correct = 1
         
     else:
         questions_correct = 0
    
     participant.earnings = participant.total_payoff * C.CONV_FACTOR
     player.earnings_t = participant.earnings 
     
     return{
         'questions_correct':questions_correct}
 


page_sequence = [Intro_Psych,BigFive, BigFive2, LoC, Trust, Trust2, Trust3, Questions_trial,Final_page]
