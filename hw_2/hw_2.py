import sys


class Calculator:
    def __init__(self, formula):
        self.num = ''
        self.num_list = []
        self.op_list = []
        self.formula = formula
        self.operators = {
            '+': (1, lambda x, y: x + y),
            '-': (1, lambda x, y: x - y),
            '*': (2, lambda x, y: x * y),
            '/': (2, lambda x, y: x / y),
            '^': (3, lambda x, y: x ** y),
            '(': None,
            ')': None}

    def parse(self):
        for i in range(len(self.formula)):
            if self.formula[i] in self.operators.keys():
                if i == 0:
                    raise Exception
                elif self.formula[i - 1] in self.operators:
                    raise Exception
                if self.formula[i - 1] in '(':
                    raise Exception
                self.num_list.append(float(self.num))
                self.num = ''
                if self.formula[i] in ')':
                    while self.op_list[-1] != '(':
                        d = self.operators.get(self.op_list.pop())[1](self.num_list.pop(-2), self.num_list.pop(-1))
                        self.num_list.append(d)
                    continue
                if len(self.op_list) != 0 and self.operators.get(self.formula[i])[0] < \
                        self.operators.get(self.op_list[-1])[0]:
                    d = self.operators.get(self.op_list.pop())[1](self.num_list.pop(-2), self.num_list.pop(-1))
                    self.num_list.append(d)
                self.op_list.append(self.formula[i])
            elif self.formula[i] in '1234567890.':
                self.num += self.formula[i]
            if i == len(self.formula) - 1:
                self.num_list.append(float(self.num))

    def calculate(self):
        self.parse()
        while len(self.num_list) > 1:
            for i in self.op_list:
                d = self.operators.get(i)[1](self.num_list.pop(0), self.num_list.pop(0))
                self.num_list = [d] + self.num_list
        return self.num_list[0]


if __name__ == '__main__':
    try:
        print(Calculator(sys.argv[1]).calculate())
    except ZeroDivisionError:
        print('????????????, ???????????????? ?????????????????? ?????????????????????? ???????????? ?? ???????????????????? ????????????????????')
    except Exception:
        print('????????????, ???????????????? ?????????????????? ?????????????????????? ???????????? ?? ???????????????????? ????????????????????')
