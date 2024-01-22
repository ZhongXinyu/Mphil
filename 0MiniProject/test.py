class Myclass():
    def __init__(self, b):
        self.a = 'Hello'
        self.b = b

obj = Myclass('World')
Myclass.a = 'john'
obj.b = None
print(obj.a, obj.b)

a = [1,2,2]
b = [1,2,3]
print (a.concat(b))