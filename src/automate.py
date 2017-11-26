import subprocess

filePath = ["\map1\map1-0.txt","\map1\map1-1.txt","\map1\map1-2.txt","\map1\map1-3.txt","\map1\map1-4.txt","\map2\map2-0.txt","\map2\map2-1.txt"
			,"\map2\map2-2.txt","\map2\map2-3.txt","\map2\map2-4.txt","\map3\map3-0.txt","\map3\map3-1.txt","\map3\map3-2.txt","\map3\map3-3.txt"
			,"\map3\map3-4.txt","\map4\map4-0.txt","\map4\map4-1.txt","\map4\map4-2.txt","\map4\map4-3.txt","\map4\map4-4.txt","\map5\map5-0.txt"
			,"\map5\map5-1.txt","\map5\map5-2.txt","\map5\map5-3.txt","\map5\map5-4.txt","\map1\map1-5.txt","\map1\map1-6.txt","\map1\map1-7.txt"
			,"\map1\map1-8.txt","\map1\map1-9.txt","\map2\map2-5.txt","\map2\map2-6.txt"
			,"\map2\map2-7.txt","\map2\map2-8.txt","\map2\map2-9.txt","\map3\map3-5.txt","\map3\map3-6.txt","\map3\map3-7.txt","\map3\map3-8.txt"
			,"\map3\map3-9.txt","\map4\map4-5.txt","\map4\map4-6.txt","\map4\map4-7.txt","\map4\map4-8.txt","\map4\map4-9.txt","\map5\map5-5.txt"
			,"\map5\map5-6.txt","\map5\map5-7.txt","\map5\map5-8.txt","\map5\map5-9.txt"]

regcommands= [["py","search.py","map_benchmarks","u"],["py","search.py","map_benchmarks","a","1"]
			,["py","search.py","map_benchmarks","a","2"],["py","search.py","map_benchmarks","a","3"]
			,["py","search.py","map_benchmarks","a","4"],["py","search.py","map_benchmarks","a","5"]
			,["py","search.py","map_benchmarks","w","1","1.5"],["py","search.py","map_benchmarks","w","2","1.5"]
			,["py","search.py","map_benchmarks","w","3","1.5"],["py","search.py","map_benchmarks","w","4","1.5"]
			,["py","search.py","map_benchmarks","w","5","1.5"],["py","search.py","map_benchmarks","w","1","2.5"]
			,["py","search.py","map_benchmarks","w","2","2.5"],["py","search.py","map_benchmarks","w","3","2.5"]
			,["py","search.py","map_benchmarks","w","4","2.5"],["py","search.py","map_benchmarks","w","5","2.5"]]

commands= [["py","search.py","map_benchmarks","s","1.25","1.25"],["py","search.py","map_benchmarks","s","1.25","2"]
			,["py","search.py","map_benchmarks","s","2","1.25"],["py","search.py","map_benchmarks","s","2","2"]
			,["py","search.py","map_benchmarks","s","2.5","1.5"],["py","search.py","map_benchmarks","s","1.5","2.5"]
			,["py","search.py","map_benchmarks","s","1.5","1.5"],["py","search.py","map_benchmarks","s","2.5","2.5"]
		   	,["py","search.py","map_benchmarks","s","3","1.25"],["py","search.py","map_benchmarks","s","1.25","3"]
			,["py","search.py","map_benchmarks","s","1.5","3"],["py","search.py","map_benchmarks","s","3","1.5"]
			,["py", "search.py", "map_benchmarks", "s", "2.5", "3"], ["py", "search.py", "map_benchmarks", "s", "2.5", "10"]
			,["py", "search.py", "map_benchmarks", "s", "1.25", "10"]]

for file in filePath:
	for comand in commands:
		TempComand=[]
		for c in comand:
			TempComand.append(c)
		TempComand[2]=str(TempComand[2])+str(file)
		subprocess.call(TempComand)
	for comand in regcommands:
		TempComand=[]
		for c in comand:
			TempComand.append(c)
		TempComand[2]=str(TempComand[2])+str(file)
		subprocess.call(TempComand)
