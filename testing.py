from threading import Thread
from time import sleep


class first(Thread):
    def run(self):
        for i in range(1,20):
            print("hello")
class second(Thread):
    def run(self):
        for i in range(1,20):
            print("hiii")
        
ob1 = first()
ob2 = second()
ob1.start()
ob2.start()

ob1.join()
ob2.join(
)
print("vanakkam da mapla")