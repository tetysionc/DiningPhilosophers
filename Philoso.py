import threading
import random
import time


class Philosopher(threading.Thread):
    running = True

    def __init__(self, name, forkOnLeft, forkOnRight):
        threading.Thread.__init__(self)
        self.name = name
        self.forkOnLeft = forkOnLeft
        self.forkOnRight = forkOnRight

    def run(self):
        while (self.running):
            time.sleep(random.uniform(1, 5))
            print("%s jest głodny. \n" % self.name)
            self.dine()

    def dine(self):
        fork1, fork2 = self.forkOnLeft, self.forkOnRight

        while (self.running):
            fork1.acquire(True)
            locked = fork2.acquire(False)
            if locked: break
            fork1.release()
            print("%s odkłada widelce. \n" % self.name)
            fork1, fork2 = fork2, fork1
        else:
            return

        self.dining()
        fork2.release()
        fork1.release()

    def dining(self):
        print("%s zaczyna jeść. \n" % self.name)
        time.sleep(random.uniform(1, 10))
        print("%s kończy jeść i zaczyna rozmyślać. \n" % self.name)
        self.running = False


def main():
    numPhilosophers = int(input("Dla ilu filozofów przygotować stół? Maksymalnie możemy obsłużyć 10 \n"))
    forks = [threading.Lock() for n in range(numPhilosophers)]
    philos = ["Arystoteles", "Kant", "Euler", "Russel", "Monteskiusz", "Hegel", "Hobbes", "Nietzsche", "Wittgenstein", "Shoppenhauer"]
    philosophers = [Philosopher(philos[i], forks[i % numPhilosophers], forks[(i - 1) % numPhilosophers]) \
                    for i in range(numPhilosophers)]

    Philosopher.running = True
    for p in philosophers: p.start()
    for p in philosophers: p.join()
    print("Wszyscy się najedli.")


main()