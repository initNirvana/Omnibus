# -*- coding: utf-8 -*-
"""
어니스트 네이글과 제임스 뉴먼이 쓴  괴델의 증명의 "괴델 수" 구현하기
"""
from re import Scanner
from itertools import groupby, takewhile

from util.number_theory import prime_smaller, factor
from util.bijection import Bijection 


UPPERBOUND_PRIME = 1000
PRIME = prime_smaller(UPPERBOUND_PRIME)


TICK = '`'

NUMERICAL_VAL = 'x', 'y', 'z' # 숫자 변항
SENTNTIAL_VAL = 'p', 'q', 'r' # 문장 변항
PREDICATE_VAL = 'P', 'Q', 'R' # 술어 변항
ALL_VAL = NUMERICAL_VAL + SENTNTIAL_VAL + PREDICATE_VAL

# 괴델의 증명 109 페이지
# 상항 기호와 각 기호에 부여된 괴델 수
CONSTANT_SIGNS = Bijection({
    '~' : 1,
    '∨' : 2,
    '⊃' : 3,
    '∃' : 4,
    '=' : 5,
    '0' : 6,
    's' : 7,
    '(' : 8,
    ')' : 9,
    ',' : 10,
    '+' : 11,
    '×' : 12
})

MAX = max(CONSTANT_SIGNS.mapping.values())
PRIME_OFFSET = len(list(takewhile(lambda x:x < MAX, PRIME)))

def prod(iterable):
    product = 1
    for n in iterable:
        product *= n
    return product

class LexicalException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Lexer:

    constant_type = "C"
    numerical_type = "N"
    sentntial_type = "S"
    predicate_type = "P"

    def __init__(self):
        self.constant_signs = self.match_any(CONSTANT_SIGNS.mapping.keys())
        self.numerical_variables = self.match_any_with_ticks(NUMERICAL_VAL)
        self.sentntial_variables = self.match_any_with_ticks(SENTNTIAL_VAL)
        self.predicate_variables = self.match_any_with_ticks(PREDICATE_VAL)

    def match_any(self, iterable):
        return "[%s]" % ''.join(iterable)

    def match_any_with_ticks(self, iterable):
        return "{0}{1}*".format(self.match_any(iterable), TICK)

    def scan(self, string):
        scanner = Scanner([
            (self.constant_signs, lambda _, tok: (self.constant_type, tok)),
            (self.numerical_variables, lambda _, tok: (self.numerical_type, tok)),
            (self.sentntial_variables, lambda _, tok: (self.sentntial_type, tok)),
            (self.predicate_variables, lambda _, tok: (self.predicate_type, tok))])

        tokens, remainder = scanner.scan(string)
        if remainder:
            if len(remainder) > 10:
                remainder = remainder[:10]
            raise LexicalException("error lexing {0} ..".format(remainder))
        return tokens

class State:

    def __init__(self):
        self.encoding = []
        self.numerical_variables = {}
        self.sentntial_variables = {}
        self.predicate_variables = {}

    def next_var_name(self, assigned, pool):
        poollen = len(pool)
        count = len(assigned)
        ticks = count // poollen
        name = pool[count % poollen] + TICK * ticks
        return name

    def encode_constant_sign(self, symbol):
        return CONSTANT_SIGNS.mapping.get(symbol)

    def encode_numerical_variable(self, symbol):
        gnum = self.numerical_variables.get(symbol)
        if gnum:
            return gnum
        else:
            gnum = PRIME[PRIME_OFFSET + len(self.numerical_variables)]
            self.numerical_variables[symbol] = gnum
            return gnum
    
    def encode_sentntial_variable(self, symbol):
        gnum = self.sentntial_variables.get(symbol)
        if gnum:
            return gnum
        else:
            gnum = PRIME[PRIME_OFFSET + len(self.sentntial_variables)] ** 2
            self.sentntial_variables[symbol] = gnum
            return gnum
    
    def encode_predicate_variable(self, symbol):
        gnum = self.sentntial_variables.get(symbol)
        if gnum:
            return gnum
        else:
            gnum = PRIME[PRIME_OFFSET + len(self.sentntial_variables)] ** 3
            self.sentntial_variables[symbol] = gnum
            return gnum
    
    def decode_numerical_variable(self, gnum):
        symbol = self.numerical_variables.get(gnum)
        if symbol:
          return symbol
        symbol = self.next_var_name(self.numerical_variables, NUMERICAL_VARIABLES)
        self.numerical_variables[gnum] = symbol
        return symbol

    def decode_sentential_variable(self, gnum):
        symbol = self.sentntial_variables.get(gnum)
        if symbol:
          return symbol
        symbol = self.next_var_name(self.sentntial_variables, SENTNTIAL_VARIABLES)
        self.sentntial_variables[gnum] = symbol
        return symbol

    def decode_predicate_variable(self, gnum):
        symbol = self.predicate_variables.get(gnum)
        if symbol:
          return symbol
        symbol = self.next_var_name(self.predicate_variables, PREDICATE_VARIABLES)
        self.predicate_variables[gnum] = symbol
        return symbol

def encode(string):
    """
    PM encode
    
    ~ ∨ ⊃ ∃ = 0 s () , + ×

    x, y, z, p, r, q, P, R, Q, x`, x``, ...
    """
    if not string: return 0

    state = State()
    lexer = Lexer()
    tokens = lexer.scan(string)

    lexmap = {
        lexer.constant_type  : state.encode_constant_sign,
        lexer.numerical_type : state.encode_numerical_variable,
        lexer.sentntial_type : state.encode_sentntial_variable,
        lexer.predicate_type : state.encode_predicate_variable
    }

    for token_type, lexeme in tokens:
        lookup = lexmap[token_type]
        gnum = lookup(lexeme)
        state.encoding.append(gnum)
    retval = prod(PRIME[idx]**gnum for idx, gnum in enumerate(state.encoding))
    return retval

def decode(number):
    if not number: return ""

    state = State()
    symbols = []
    factors = ((k, len(list(v))) for k, v in groupby(factor(number)))
    for i, (f, gnum) in enumerate(factors):
        if PRIME[i] != f:
            err = "not a Gödel number: prime at index {0} is {1} but should be {2}."
            err = err.format(i, f, PRIME[i])
            raise ValueError(err)

    symbol = CONSTANT_SIGNS.inverse.get(gnum)
    if not symbol:
        if gnum in PRIME:
            symbol = state.decode_numerical_variable(gnum)
        else:
            factors = factor(gnum)
            if len(set(factors)) != 1:
                err = '{0} is not prime, a prime squared, or a prime cubed.'
                err = err.format(gnum)
                raise ValueError(err)

            if len(factors) == 2 and factors[0] in PRIME:
                symbol = state.decode_sentential_variable(gnum)
            elif len(factors) == 3 and factors[0] in PRIME:
                symbol = state.decode_predicate_variable(gnum)
            else:
                err = '{0} is not prime, a prime squared, or a prime cubed.'
                err = err.format(gnum)
                raise ValueError(err)
                
        symbols.append(symbol)
    return ''.join(symbols)  
  
  
if __name__ == '__main__':
  test_string1 = '0=0'
  test_string2 = '(∃pPx)(x=sy)'

  encoded_test_string1 = encode(test_string1)
  encoded_test_string2 = encode(test_string2)

  print(encoded_test_string1)
  print(encoded_test_string2)

  decoded_test_string1 = decode(encoded_test_string1)
  decoded_test_string2 = decode(encoded_test_string2)

  print((test_string1, encoded_test_string1, decoded_test_string1))
  print((test_string2, encoded_test_string2, decoded_test_string2))

