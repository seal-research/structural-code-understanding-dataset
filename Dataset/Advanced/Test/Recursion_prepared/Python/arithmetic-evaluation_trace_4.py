import operator

class AstNode(object):
   def __init__( self, opr, left, right ):
      self.opr = opr
      self.l = left
      self.r = right

   def eval(self):
      return self.opr(self.l.eval(), self.r.eval())

class LeafNode(object):
   def __init__( self, valStrg ):
      self.v = int(valStrg)

   def eval(self):
      return self.v

class Yaccer(object):
   def __init__(self):
      self.operstak = []
      self.nodestak =[]
      self.__dict__.update(self.state1)

   def v1( self, valStrg ):
      self.nodestak.append( LeafNode(valStrg))
      self.__dict__.update(self.state2)

   def o2( self, operchar ):
      def openParen(a,b):
         return 0

      opDict= { '+': ( operator.add, 2, 2 ),
         '-': (operator.sub, 2, 2 ),
         '*': (operator.mul, 3, 3 ),
         '/': (operator.truediv, 3, 3 ),
         '^': ( pow,         4, 5 ),
         '(': ( openParen,   0, 8 )
         }
      operPrecidence = opDict[operchar][2]
      self.redeuce(operPrecidence)

      self.operstak.append(opDict[operchar])
      self.__dict__.update(self.state1)

   def syntaxErr(self, char ):
      print(f'parse error - near operator {char}')

   def pc2( self,operchar ):
      self.redeuce( 1 )
      if len(self.operstak)>0:
         self.operstak.pop()
      else:
         print('Error - no open parenthesis matches close parens.')
      self.__dict__.update(self.state2)

   def end(self):
      self.redeuce(0)
      return self.nodestak.pop()

   def redeuce(self, precidence):
      while len(self.operstak)>0:
         tailOper = self.operstak[-1]
         if tailOper[1] < precidence: break

         tailOper = self.operstak.pop()
         vrgt = self.nodestak.pop()
         vlft= self.nodestak.pop()
         self.nodestak.append( AstNode(tailOper[0], vlft, vrgt))

   state1 = { 'v': v1, 'o':syntaxErr, 'po':o2, 'pc':syntaxErr }
   state2 = { 'v': syntaxErr, 'o':o2, 'po':syntaxErr, 'pc':pc2 }

def Lex( exprssn, p ):
   bgn = None
   cp = -1
   for c in exprssn:
      cp += 1
      if c in '+-/*^()':
         if bgn is not None:
            p.v(p, exprssn[bgn:cp])
            bgn = None
         if c=='(': p.po(p, c)
         elif c==')':p.pc(p, c)
         else: p.o(p, c)
      elif c in ' \t':
         if bgn is not None:
            p.v(p, exprssn[bgn:cp])
            bgn = None
      elif c in '0123456789':
         if bgn is None:
            bgn = cp
      else:
         print('Invalid character in expression')
         if bgn is not None:
            p.v(p, exprssn[bgn:cp])
            bgn = None

   if bgn is not None:
      p.v(p, exprssn[bgn:cp+1])
      bgn = None
   return p.end()

if __name__ == '__main__':
   expr = "8 / 2"
   astTree = Lex(expr, Yaccer())
   print(expr, '=', astTree.eval())