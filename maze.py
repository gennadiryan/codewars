m1 = ((4, 2, 5, 4), (4, 15, 11, 1), ('B', 9, 6, 8), (12, 7, 7, 'X'))
m2 = ((6, 3, 10, 4, 11), (8, 10, 4, 8, 5), ('B', 14, 11, 3, 'X'), (15, 3, 4, 14, 15), (14, 7, 15, 5, 5))
m3 = ((9, 1, 9, 0, 13, 0), (14, 1, 11, 2, 11, 4), ('B', 2, 11, 0, 0, 15), (4, 3, 9, 6, 3, 'X'))
m4 = (('B', 6, 12, 15, 11), (8, 7, 15, 7, 10), (13, 7, 13, 15, 'X'), (11, 10, 8, 1, 3), (12, 6, 9, 14, 7))
m5 = ((6, 3, 0, 9, 14, 13, 14), ('B', 14, 9, 11, 15, 14, 15), (2, 15, 0, 12, 6, 15, 'X'), (4, 10, 7, 6, 15, 5, 3), (7, 3, 13, 13, 14, 7, 0))
m6 = ((0, 13, 13, 12, 9, 9), (4, 2, 9, 11, 3, 'X'), (0, 0, 4, 12, 10, 6), (15, 8, 3, 14, 0, 7), (9, 1, 15, 2, 10, 11), ('B', 10, 7, 2, 6, 13))
m7 = ((3, 7, 12, 6, 11, 9), ('B', 14, 4, 6, 6, 10), (9, 15, 14, 1, 14, 5), (0, 4, 15, 8, 4, 'X'), (10, 5, 3, 7, 3, 1), (14, 11, 10, 11, 15, 13))
m8 = (('B', 13, 1, 12, 5, 2, 12, 9), (7, 14, 7, 7, 10, 8, 9, 13), (12, 12, 12, 8, 1, 3, 9, 2), (1, 0, 8, 7, 9, 13, 15, 4), (15, 10, 5, 11, 7, 15, 12, 4), (6, 12, 4, 3, 2, 1, 14, 8), (15, 0, 6, 6, 8, 9, 11, 'X'), (0, 13, 7, 4, 3, 8, 11, 6))
m9 = ((9, 12, 7, 6, 9, 1, 1, 15, 5, 1), (13, 5, 4, 9, 11, 13, 2, 11, 4, 13), (14, 7, 5, 10, 15, 8, 5, 9, 7, 6), (5, 6, 5, 1, 13, 10, 9, 10, 7, 10), (10, 4, 1, 9, 13, 15, 0, 4, 11, 15), ('B', 5, 11, 5, 14, 7, 13, 8, 9, 12), (9, 10, 0, 13, 5, 3, 6, 9, 2, 3), (14, 4, 4, 2, 15, 9, 2, 11, 2, 'X'))
m10 = ((2, 3, 10, 1, 13, 7, 15, 0, 1, 9, 8, 9), (10, 15, 3, 9, 3, 10, 8, 1, 9, 5, 9, 4), (2, 12, 5, 3, 13, 15, 7, 4, 1, 14, 7, 1), (13, 4, 5, 11, 4, 6, 12, 13, 3, 14, 2, 11), (12, 3, 2, 15, 0, 5, 11, 5, 15, 6, 8, 2), ('B', 8, 11, 13, 11, 6, 8, 2, 14, 13, 1, 9), (12, 0, 2, 11, 5, 5, 6, 10, 9, 6, 0, 10), (3, 0, 1, 11, 0, 5, 14, 9, 4, 5, 13, 7), (11, 4, 15, 8, 15, 8, 3, 12, 1, 4, 9, 'X'), (9, 14, 4, 8, 8, 3, 4, 10, 10, 6, 3, 13), (15, 9, 14, 12, 10, 14, 8, 12, 11, 0, 4, 11), (12, 3, 13, 11, 8, 15, 6, 3, 2, 1, 8, 0))

dirs = (1, 1j, -1, -1j)
dirChrs = ('E', 'S', 'W', 'N') # for encoding directions

addInters = lambda l: list(map(lambda e: e + [''], l)) # break directions by intervals

# get wall parameters from tuple
access = lambda t, n: t[int(n.imag)][int(n.real)]

# wall measurement utilities
rotWalls = lambda n: ((n * 2) + (n // 8)) % 16
hasWall = lambda n, k: (n // (2 ** k)) % 2 == 1
hasWallC = lambda n, k: hasWall(n, dirs.index(k))

# find reachable adjacents
adj = lambda n: tuple(n + dir for dir in dirs)
inMap = lambda t, n: int(n.imag) in range(len(t)) and int(n.real) in range(len(t[int(n.imag)]))
reachable = lambda t, n: [c for c in adj(n) if inMap(t, c) and not hasWallC(access(t, n), c - n) and not hasWallC(access(t, c), n - c)]

def zeroChar(t, c):
	for i, l in enumerate(t):
		for j, e in enumerate(l):
			if e == c: return complex(j, i)

# remove chars and get their pos's
def cleaned(t):
	b = zeroChar(t, 'B')
	x = zeroChar(t, 'X')
	
	return tuple(tuple(e if complex(j, i) not in (b, x) else 0 for j, e in enumerate(l)) for i, l in enumerate(t)), b, x

# rotate all walls
def iter(t): return tuple(tuple(rotWalls(e) for j, e in enumerate(l)) for i, l in enumerate(t))

# expand one step at a time
def addReaches(t, paths, posits, targ):
	paths2 = []
	posits2 = []
	
	for i, pos in enumerate(posits):
		# catch target on second go-around
		if targ in posits2: break
		
		reaches = reachable(t, pos)
		for reach in reaches:
			if reach not in posits:
				posits2.append(reach)
				
				newPath = paths[i][:]
				newPath[-1] += dirChrs[dirs.index(reach - pos)]
				paths2.append(newPath)
				
				# get out when target found
				if reach == targ: break
	
	return (paths + paths2, posits + posits2)

# stops when nothing added
def expand(t, paths, posits, targ):
	l = -1
	while l < len(posits):
		l = len(posits)
		paths, posits = addReaches(t, paths, posits, targ)
	
	return (paths, posits)

def search(t, start, end):
	paths = [['']]
	posits = [start]
	
	lens = []
	
	while True:
		paths, posits = expand(t, paths, posits, end)
		lens.append(len(posits))
		
		if end in posits: return paths[posits.index(end)]
		
		# once all possible iters pass with no change means unsolvable
		if len(lens) >= 4 and lens[::-1][:4].count(lens[-1]) == 4: break
		
		paths = addInters(paths)
		t = iter(t)

def maze_solver(ar): return search(*cleaned(ar))

#print(maze_solver(m10))
