__author__ = 'Jian'

class school:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        print '(initialized schoolmember:%s)' %self.name

    def tell(self):
        print 'Name:"%s" Age:"%s"' %(self.name,self.age),

class teacher(school):
    def __init__(self,name,age,salary):
        school.__init__(self,name,age)
        self.salary = salary

    def tell(self):
        school.tell(self)
        print ' salary:"%s" ' %(self.salary),

class student(school):
    def __init__(self,name,age,marks):
        school.__init__(self,name,age)
        self.marks = marks
    def tell(self):
        school.tell(self)
        print ' marks:"%s" ' %(self.marks)

t = teacher('Mrs.shriva',40, 30000)
s = student('swaroop',22, 75)
print
members = [t,s]
for member in members:
    member.tell()