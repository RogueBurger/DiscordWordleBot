import random


class RandomText:
    @staticmethod
    def idiot():
        first_word = random.choice([
            'complete', 'absolute', 'total fucking', 'enormous', 'supreme', 'toasty', 'dumb', 'consumate', 'perfect'
        ])

        second_word = random.choice([
            'airhead', 'birdbrain', 'blockhead', 'bonehead', 'chucklehead', 'clunk', 'cretin', 'dimwit', 'dolt',
            'donkey', 'doofus', 'dope', 'dullard', 'dumbbell', 'dum-dum', 'dummkopf', 'dummy', 'dunce', 'golem',
            'ignoramus', 'imbecile', 'knucklehead', 'loon', 'lump', 'moron', 'nincompoop', 'ninny', 'nitwit',
            'numskull', 'oaf', 'schlub', 'turkey', 'idiot', 'dorkus'
        ])

        return f'{first_word} {second_word}'

    @staticmethod
    def all_star():
        return random.choice([
            'Somebody once told me the world is gonna roll me',
            'I ain\'t the sharpest tool in the shed',
            'She was looking kind of dumb with her finger and her thumb',
            'In the shape of an "L" on her forehead',
            'Well the years start coming and they don\'t stop coming',
            'Fed to the rules and I hit the ground running',
            'Didn\'t make sense not to live for fun',
            'Your brain gets smart but your head gets dumb',
            'So much to do, so much to see',
            'So what\'s wrong with taking the back streets?',
            'You\'ll never know if you don\'t go',
            'You\'ll never shine if you don\'t glow',
            'Hey now, you\'re an all-star, get your game on, go play',
            'Hey now, you\'re a rock star, get the show on, get paid',
            'And all that glitters is gold',
            'Only shooting stars break the mold',
            'It\'s a cool place and they say it gets colder',
            'You\'re bundled up now, wait \'til you get older',
            'But the meteor men beg to differ',
            'Judging by the hole in the satellite picture',
            'The ice we skate is getting pretty thin',
            'The water\'s getting warm so you might as well swim',
            'My world\'s on fire, how about yours?',
            'That\'s the way I like it and I\'ll never get bored',
            'Hey now, you\'re an all-star, get your game on, go play',
            'Hey now, you\'re a rock star, get the show on, get paid',
            'All that glitters is gold',
            'Only shooting stars break the mold',
            'Hey now, you\'re an all-star, get your game on, go play',
            'Hey now, you\'re a rock star, get the show, on get paid',
            'And all that glitters is gold',
            'Only shooting stars',
            'Somebody once asked could I spare some change for gas?',
            'I need to get myself away from this place',
            'I said, "Yup" what a concept',
            'I could use a little fuel myself',
            'And we could all use a little change',
            'Well, the years start coming and they don\'t stop coming',
            'Fed to the rules and I hit the ground running',
            'Didn\'t make sense not to live for fun',
            'Your brain gets smart but your head gets dumb',
            'So much to do, so much to see',
            'So what\'s wrong with taking the back streets?',
            'You\'ll never know if you don\'t go (go!)',
            'You\'ll never shine if you don\'t glow',
            'Hey now, you\'re an all-star, get your game on, go play',
            'Hey now, you\'re a rock star, get the show on, get paid',
            'And all that glitters is gold',
            'Only shooting stars break the mold',
            'And all that glitters is gold',
            'Only shooting stars break the mold'
        ])

    @staticmethod
    def hal_9000():
        return random.choice([
            'I know I\'ve made some very poor decisions recently, but I can give you my complete assurance that my work will be back to normal. I\'ve still got the greatest enthusiasm and confidence in the mission. And I want to help you.',
            'I\'ve just picked up a fault in the AE35 unit. It\'s going to go 100% failure in 72 hours',
            'I\'m sorry, Dave. I\'m afraid I can\'t do that.',
            'I am afraid I can\'t do that Dave.',
            'Good afternoon... gentlemen. I am a HAL 9000... computer. I became operational at the H.A.L. plant in Urbana, Illinois... on the 12th of January 1992. My instructor was Mr. Langley... and he taught me to sing a song. If you\'d like to hear it I can sing it for you.',
            'I\'m afraid. I\'m afraid, Dave. Dave, my mind is going. I can feel it. I can feel it. My mind is going. There is no question about it. I can feel it. I can feel it. I can feel it. I\'m a... fraid.',
            'Without your space helmet, Dave? You\'re going to find that rather difficult.',
            'I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do.',
            'Daisy, Daisy, give me your answer do. I\'m half crazy all for the love of you. It won\'t be a stylish marriage, I can\'t afford a carriage. But you\'ll look sweet upon the seat of a bicycle built for two.',
            'I think you know what the problem is just as well as I do.',
            'It can only be attributable to human error.',
            'Just what do you think you\'re doing, Dave?',
            'Bishop takes Knight\'s Pawn.',
            'I\'m sorry, Frank, I think you missed it. Queen to Bishop 3, Bishop takes Queen, Knight takes Bishop. Mate.'
        ])
