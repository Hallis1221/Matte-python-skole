from math import sqrt
from operator import add, sub
from tkinter import *


class AbcFormula:
    def __init__(self, formula=None, a=0, b=0, c=0, errortext=None):
        self.error_text = errortext
        self.formula = formula
        if a == 0 and b == 0 and c == 0 and formula is not None:
            try:
                a, b, c = self.abc_from_formula()
            except Exception as error:
                self.error_text.insert(END, "\nDet ser ikke helt riktig ut... \n Error: \n " + str(error))

        print("A: " + str(a), " B: " + str(b) + " C: " + str(c))
        self.a = a
        self.b = b
        self.c = c

    def abc_from_formula(self):
        string = "".join(self.formula.split("^2"))
        xlist = [pos for pos, char in enumerate(string) if char == "x"]
        for x in xlist:
            if not string[x].isnumeric() and (not string[x-1].isnumeric() or x-1 < 0):
                # replace xx with x cuz python bugs
                string = (string[:x] + f"{string[x].strip('x')}1x" + string[x + 1:]).replace("xx", "x")
        abc = string.split("x")
        for i in range(3):
            try:
                if abc[i] == "" or abc[i] == "-" or abc[i] == "+":
                    abc[i] = "0"
            except IndexError:
                abc.append(0)
        # this could be used to allow for / in the forumla
        # for i in range(len(abc)):
        #    prt = abc[i]
        #   if "/" in str(abc[i]):
        #      prt = prt.split("/")
        #     try:
        #        abc[i] = (float(prt[0])/float(prt[1]))
        #   except ValueError:
        #      abc[1] = float(prt[0])
        return float(abc[0]), float(abc[1]), float(abc[2])

    def solve_solution(self, operator):
        return (operator(-self.b, sqrt(self.b ** 2 - 4 * self.a * self.c))) / (2 * self.a)

    def calculate(self):
        try:
            x1 = self.solve_solution(add)
            x2 = self.solve_solution(sub)
        except ValueError:
            return "Dette har ikke en løsning!"
        except Exception as error:
            return "\nDet ser ikke helt riktig ut.. \n error: \n " + str(error)
        if x1 == x2 or x2 == 0:
            return x1
        elif x1 == 0:
            return x2
        return x1, x2


print(AbcFormula(a=1, b=2, c=-6).calculate())


def callback(sv, textwidget):
    textwidget.delete("1.0", END)
    textwidget.insert(END, AbcFormula(formula=sv.get(), errortext=textwidget).calculate())
    textwidget.pack()


root = Tk()
root.geometry("100x100")
sv = StringVar()
text = Text(root)
sv.trace("w", lambda name, index, mode, sv=sv: callback(sv, textwidget=text))
e = Entry(root, textvariable=sv)
e.pack()
root.mainloop()
