import tokenize
import io
from collections import defaultdict



def make_corpus(code):
    tokens = []
    unique_tokens = set()
    count = defaultdict(int)  # Initialize count as a defaultdict with an int default value
    code = code.encode('utf-8')
    unwanted_tokens = {'ENCODING', 'NEWLINE', 'NL', 'COMMENT', 'INDENT', 'DEDENT', 'ENDMARKER'}

    tokens_generator = tokenize.tokenize(io.BytesIO(code).readline)

    for tok in tokens_generator:
        token_type = tokenize.tok_name[tok.type]
        token_value = tok.string

        if token_type not in unwanted_tokens:
            tokens.append(token_value)
            unique_tokens.add(token_value)
            count[token_value] += 1  # Increment the count for this token

    return tokens

# Example usage:
code_snippet = '''
# Add two Numbers
def add_two_numbers(a, b):
    result = a + b
'''
complex_code = '''
# This is a complex code snippet
def factorial_of_input_code(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

result = factorial(5)
print("Factorial of 5:", result)

# Let's add some more complexity
class MyClass:
    def __init__(self, x):
        self.x = x

    def squareOfValue(self):
        return self.x ** 2

obj1 = MyClass(5)
obj2 = MyClass(10)
sum_of_squares = obj1.square() + obj2.square()
print("Sum of squares:", sum_of_squares)
'''

input_code = """
def test depth first mro mixed ( ) :
class A : pass 
class B ( A , ) : pass 
class C ( A , ) : pass 
class D ( B , C , ) : pass 
class E ( D , object , ) : pass 
class G : pass class H ( G , ) : pass 
class I ( G , ) : pass 
class K ( H , I , object , ) : pass 
class L ( K , E , ) : pass  Are  Equal  ( L .   mro   , ( L , K , H , I , G , E , D , B , A , C , object ) )
def get svc alias ( ) : ret = { } for d in AVAIL SVR DIRS : for el in glob . glob ( os . path . join ( d , '*' ) ) : if ( not os . path . islink ( el ) ) : continue psvc = os . readlink ( el ) if ( not os . path . isabs ( psvc ) ) : psvc = os . path . join ( d , psvc ) nsvc = os . path . basename ( psvc ) if ( nsvc not in ret ) : ret [ nsvc ] = [ ] ret [ nsvc ] . append ( el ) return ret
def test html ( ) : dat = np . array ( [ 1.0 , 2.0 ] , dtype = np . float32 ) t =  Table  ( [ dat ] , names = [ 'a' ] ) lines = t . pformat ( html =  True  ) assert ( lines == [ '<table  id="table{id}">' . format ( id = id ( t ) ) , u'<thead><tr><th>a</th></tr></thead>' , u'<tr><td>1.0</td></tr>' , u'<tr><td>2.0</td></tr>' , u'</table>' ] ) lines = t . pformat ( html =  True  , tableclass = 'table-striped' ) assert ( lines == [ '<table  id="table{id}"  class="table-striped">' . format ( id = id ( t ) ) , u'<thead><tr><th>a</th></tr></thead>' , u'<tr><td>1.0</td></tr>' , u'<tr><td>2.0</td></tr>' , u'</table>' ] ) lines = t . pformat ( html =  True  , tableclass = [ 'table' , 'table-striped' ] ) assert ( lines == [ '<table  id="table{id}"  class="table  table-striped">' . format ( id = id ( t ) ) , u'<thead><tr><th>a</th></tr></thead>' , u'<tr><td>1.0</td></tr>' , u'<tr><td>2.0</td></tr>' , u'</table>' ] )
def test x y title (  Chart  ) : chart =  Chart  ( title = 'I   Am   A   Title ' , x title = 'I  am  a  x  title' , y title = 'I  am  a  y  title' ) chart . add ( '1' , [ 4 , ( - 5 ) , 123 , 59 , 38 ] ) chart . add ( '2' , [ 89 , 0 , 8 , 0.12 , 8 ] ) q = chart . render pyquery ( ) assert ( len ( q ( '.titles  .title' ) ) == 3 )
def run migrations online ( ) : engine manager =  Engine  Manager  ( config . get required ( 'DATABASE HOSTS' ) , config . get required ( 'DATABASE USERS' ) , include disabled =  True  ) engine = engine manager . engines [ shard id ] connection = engine . connect ( ) connection . execute ( 'SET  @@lock wait timeout=15' ) context . configure ( connection = connection , target metadata = target metadata ) try : with context . begin transaction ( ) : context . run migrations ( ) finally : connection . close ( )
def get Temp  Markdown  Preview  Path  ( view ) : settings = sublime . load settings ( ' Markdown  Preview .sublime-settings' ) tmp filename = ( '%s.html' % view . id ( ) ) tmp dir = tempfile . gettempdir ( ) if settings . get ( 'path tempfile' ) : if os . path . isabs ( settings . get ( 'path tempfile' ) ) : tmp dir = settings . get ( 'path tempfile' ) else : tmp dir = os . path . join ( os . path . dirname ( view . file name ( ) ) , settings . get ( 'path tempfile' ) ) if ( not os . path . isdir ( tmp dir ) ) : os . makedirs ( tmp dir ) tmp fullpath = os . path . join ( tmp dir , tmp filename ) return tmp fullpath
def  get default tempdir ( ) : namer =   Random  Name  Sequence  ( ) dirlist =  candidate tempdir list ( ) flags =  text openflags for dir in dirlist : if ( dir !=  os . curdir ) : dir =  os . path . normcase (  os . path . abspath ( dir ) ) for seq in xrange ( 100 ) : name = namer . next ( ) filename =  os . path . join ( dir , name ) try : fd =  os . open ( filename , flags , 384 ) try : try : with  io . open ( fd , 'wb' , closefd =  False  ) as fp : fp . write ( 'blat' ) finally :  os . close ( fd ) finally :  os . unlink ( filename ) return dir except ( OS Error  , IO Error  ) as e : if ( e . args [ 0 ] !=  errno . EEXIST ) : break pass raise IO Error  , (  errno . ENOENT , ( ' No   usable  temporary  directory  found  in  %s' % dirlist ) )
def all locale paths ( ) : globalpath = os . path . join ( os . path . dirname ( sys . modules [ settings .   module   ] .   file   ) , 'locale' ) return ( [ globalpath ] + list ( settings . LOCALE PATHS ) )
def output ( func , * args , ** kw ) : try : return func ( * args , ** kw ) except : log . msg ( ( ' Error   calling  %r:' % ( func , ) ) ) log . err ( ) return PRE ( ' An   error  occurred.' )
"""


token_counts = make_corpus(input_code)

print(token_counts)
for token in token_counts:
    print(token)
# Print the unique tokens and their counts
# for token, count in token_counts.items():
#     # print(f"{count} {token}")
#     print(f"{token}")
