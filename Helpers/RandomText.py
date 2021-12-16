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
