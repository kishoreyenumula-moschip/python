#! /usr/bin/python3

# import sys

# n= len(sys.argv)
# print(n)

# class name:
#     n='kishore'

# obj=name()
# l=[f"name of the author is {obj.n}",2]
# print(l)

# l=['qw','ksf\n']
# l[-1]=l[-1].rstrip('\n')
# print(l)

# s='kishore !'
# k=' yenumula'
# print(s+k)


#staic and normal variables in python oops


# class fam():
#     #name='yenumula'
#     def __init__(self):
#         self.name='yenumula'
#         print("init is called")
    
# obj1=fam()
# obj1.name='YENUMULA'
# print(obj1.name)
# obj2=fam()
# print(obj2.name)

class fam():
    name='kishore'
    def __init__(self):
        self.myname='kissy'

def call():
    one=fam()
    print(one.name , one.myname)
one=fam()
print(one.name , one.myname)
fam.name='KISHORE'
one.myname='KISSY'
print(one.name , one.myname)
two=fam()
print(two.name,two.myname)
print(one.name , one.myname)
call()