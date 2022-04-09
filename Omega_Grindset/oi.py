class Post:
    def __init__(self, user, text):
        self.user = user
        self.text = text
        self.comments = []

    def addComment(self, user, message):
        self.comments.append(message)

    def __repr__(self):
        return f"[{self.user.name}]:{self.text} "


class Wall:
    def __init__(self, user):
        self.user = user
        self.posts = []

    def add(self, post):
        self.posts.append(post)

    def __repr__(self):
        s = "Wall: " + self.user.name + "\n=========\n"
        for p in self.posts:
            s += s + str(p)
        return s


class User:
    def __init__(self, name):
        self.name = name
        self.friends = []
        self.wall = Wall(self)
        self.requests = []

    def addFriend(self, user):
        req = AddFriendRequest(self, user)
        user.requests.append(req)

    def postOnFriendsWall(self, user, message):
        req = PostRequest(self, user, message)
        user.requests.append(req)
        return req

    def post(self, message):
        p = Post(self, message)
        self.wall.add(p)
        for f in self.friends:
            f.notify(p)
        return p

    def approve(self, req):
        self.requests.append(req)
        req.approve()

    def __repr__(self):
        return self.name

    def notify(self, p):
        print(f"{p.user.name} just posted '{p.text}'")
        self.wall.posts.append(p)


class FBRequest:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

    def reject(self):
        self.receiver.requests.remove(self)


class AddFriendRequest(FBRequest):
    def __init__(self, sender, receiver):
        FBRequest.__init__(self, sender, receiver)

    def approve(self):
        self.sender.friends.append(self.receiver)
        self.receiver.friends.append(self.sender)
        self.receiver.requests.remove(self)

    def __repr__(self):
        return "Add friend request from " + self.sender.name


class PostRequest(FBRequest):
    def __init__(self, sender, receiver, message):
        FBRequest.__init__(self, sender, receiver)
        self.message = message

    def approve(self):
        self.receiver.wall.add(self.message)
        self.receiver.requests.remove(self)


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
