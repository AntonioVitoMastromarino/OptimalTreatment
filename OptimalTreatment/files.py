from numpy import array, matrix, ndarray

def form( some ):
	if ( type( some ) == list ):
		TEMP = '['
		for temp in some:
			TEMP += form( temp )
		return TEMP + '],'
	if ( type( some ) == matrix ) or ( type( some ) == ndarray ):
		return form( list( array( some ) ) )
	if type( some ) == tuple:
		TEMP = '('
		for temp in some:
			TEMP += form( temp )
		return TEMP + '),'
	return str( some ) + ','

def save( some , path ):
	f = open( path , 'w' )
	f.write( form( some ) )
	f.close()

def load( path ):
	try: f = open( path , 'r' )
	except: return None
	TEMP = [[]]
	temp = ''
	while( True ):
		a = f.read( 1 )
		if ( a == '' ):
			f.close()
			if( len( TEMP ) == len( TEMP[ 0 ] ) == 1 ): return TEMP[0][0]
			else: raise Exception()
		elif ( a == '[' ): TEMP += [[]]
		elif ( a == '(' ): TEMP += [[]]
		elif ( a == ']' ): temp = [] + TEMP.pop( -1 )
		elif ( a == ')' ):
			temp = TEMP.pop( -1 )
			if len( temp ) == 2:
				temp = ( temp[ 0 ] , temp[ 1 ] )
			else:
				f.close()
				f = open( path , 'r' )
				print( f.read() )
				print( TEMP )
				f.close()
				raise Exception()
		elif ( a == ',' ):
			try:
				temp = float( temp )
				if ( temp == int( temp ) ): TEMP[ -1 ] += [ int( temp ) ]
				else: TEMP[ -1 ] += [ temp ]
			except:
				TEMP[ -1 ] += [ temp ]
			temp = ''
		else: temp += a