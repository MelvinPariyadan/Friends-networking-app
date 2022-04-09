from oi import *
def test_addFriend():
    u1 = User ("Joe")
    u2 = User ("Jill")
    u1.addFriend(u2)
    assert u1 not in u2.friends
    u2.approve (u2.requests[0])
    assert u1 in u2.friends
def test_postMessage():
    u1 = User ("Joe")
    u2 = User ("Jill")
    u1.addFriend(u2)
    u2.approve (u2.requests[0])





