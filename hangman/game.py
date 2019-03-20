from .exceptions import *
import random 

class GuessAttempt(object):
    def __init__(self,letter, hit=None,miss=None):
        self.letter = letter
        self.hit = hit
        self.miss = miss
        if  self.hit ==True and self.miss == True:
            raise  InvalidGuessAttempt()
    
        
    def is_hit(self):
        if self.hit == True:
            self.miss = False 
        return self.hit 
        
    def is_miss(self):
        
        if self.miss == True:
            self.hit = False
        return self.miss


class GuessWord(object):
    
    def __init__(self,answer,masked=None):
        if len(answer) == 0:
            raise InvalidWordException() 
        self.answer = answer
        self.masked =len(answer)*'*'
        


    def uncover_word(self,letter):
        s= ""
        
        for i in range(len(self.answer)):
            word_letter = self.answer[i]
            mask_letter = self.masked[i]
            
            if mask_letter != "*":
                s += mask_letter
            elif letter.lower()== word_letter.lower():
                s += word_letter.lower()
            else:
                s +="*"
        
        return s

    
    def perform_attempt(self,letter):
        
        if len(letter) > 1:
            raise InvalidGuessedLetterException()
        
        letter = letter.lower()
        if letter in self.answer.lower():
            attempt =  GuessAttempt(letter,hit=True)
            self.masked = self.uncover_word(letter)
        else:
            
            attempt = GuessAttempt(letter,miss=True) 
        
        
        return attempt
        
        


class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self,word_list=None,number_of_guesses=5,remaining_misses=None,previous_guesses=None):
            
                
            if word_list is None:
                word_list = self.WORD_LIST
                
            self.word_list = word_list
            self.number_of_guesses = number_of_guesses
            word_selected = self.select_random_word(word_list)
            self.word = GuessWord(word_selected)
            self.remaining_misses = number_of_guesses
            self.previous_guesses = []
            
    
    @classmethod 
    def select_random_word(cls,list_of_words):
        
            if not list_of_words:
                raise InvalidListOfWordsException()
            return random.choice(list_of_words)
    


    def guess(self,letter):
        
            if self.is_finished():
                raise GameFinishedException()
                
            letter_lower = letter.lower()
            self.previous_guesses.append(letter_lower)
            attempt = self.word.perform_attempt(letter)
            if attempt.is_miss():
                self.remaining_misses -=1
                if self.is_lost():
                    raise GameLostException()
                
            if self.is_won():
                raise GameWonException()
            
                
            return attempt
    
    
    
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses < 1:
            return True
        return False
    