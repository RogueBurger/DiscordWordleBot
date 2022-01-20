import random


class RandomText:
    @staticmethod
    def idiot(author_id=None):
        if author_id == 685214248606892111:
            return 'Wordle Penetrations Master'

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
    def smarty():
        title = random.choice([
            'President', 'Admiral', 'Colonel', 'Commissioner', 'Count', 'Dr.', 'General', 'Governor', 'Grand Master', 
            'High Priest', 'Pope', 'Senator', 'Captain', 'Lieutenant', 'Professor', 'Chancellor', 'Mr.', 'Miss'
        ])
        
        modifier = random.choice([
            'Know-it-all', 'Taj Mowry', 'Wise Guy', 'Brainiac', 'Wisenheimer', 'Clever Clogs', 'Smarty-pants', 
            'Dictionary', 'Einstein', 'Genius', 'Witling', 'Mastermind', 'Whiz Kid', 'Thinker', 'Polymath', 'da Vinci',
            'Geekwad', 'Nerd', 'Intellectual', 'Crackerjack', 'Egghead', 'Academic', 'Wordlesmith', 'Does-NYT-Crosswords-In-Pen',
            'Bookworm', 'Pat Sajak', 'Encyclopedia', 'Expert', 'IQ', 'Hotshot', 'Poindexter', 'Prodigy', 'Will Shortz'
        ])

        return f'{title} {modifier}'

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
