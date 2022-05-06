import pytest

class NotInRange(Exception):
    def __init__(self, message='Value is not in range'):
        #self.input_ = input_
        self.message = message
        super().__init__(self.message)



def test_generic():
    a = 5
    with pytest.raises(NotInRange):
        if a not in range(10, 20):
           raise NotInRange

''' 
#if we want to have more tests that our algorithm have to go through we have to define it as test_something() 
#if we just write def something like below, nothing will happen, it will ignore it in execution:
def something():
    a=2
    b=2
    assert True
'''

def test_something():
    a=2
    b=2
    assert True
