import multiprocessing

INT_VAL = 100000000

def func1():
    for i in range(INT_VAL):
        print(i)
        
def func2():
    i = INT_VAL
    while i >= 0:
        print(i)
        i -= 1

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=func1)
    p2 = multiprocessing.Process(target=func2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    """
    func1()
    func2()
    """
