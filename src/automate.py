import subprocess

filePath = ["\map1\map1-0.txt","\map1\map1-1.txt","\map1\map1-2.txt","\map1\map1-3.txt","\map1\map1-4.txt","\map2\map2-0.txt","\map2\map2-1.txt"
			,"\map2\map2-2.txt","\map2\map2-3.txt","\map2\map2-4.txt","\map3\map3-0.txt","\map3\map3-1.txt","\map3\map3-2.txt","\map3\map3-3.txt"
			,"\map3\map3-4.txt","\map4\map4-0.txt","\map4\map4-1.txt","\map4\map4-2.txt","\map4\map4-3.txt","\map4\map4-4.txt","\map5\map5-0.txt"
			,"\map5\map5-1.txt","\map5\map5-2.txt","\map5\map5-3.txt","\map5\map5-4.txt"]

commands= [["py","search.py","map_benchmarks","u"],["py","search.py","map_benchmarks","a","1"]
			,["py","search.py","map_benchmarks","a","2"],["py","search.py","map_benchmarks","a","3"]
			,["py","search.py","map_benchmarks","a","4"],["py","search.py","map_benchmarks","a","5"]
			,["py","search.py","map_benchmarks","w","1","1.25"],["py","search.py","map_benchmarks","w","2","1.25"]
			,["py","search.py","map_benchmarks","w","3","1.25"],["py","search.py","map_benchmarks","w","4","1.25"]
			,["py","search.py","map_benchmarks","w","5","1.25"],["py","search.py","map_benchmarks","w","1","2"]
			,["py","search.py","map_benchmarks","w","2","2"],["py","search.py","map_benchmarks","w","3","2"]
			,["py","search.py","map_benchmarks","w","4","2"],["py","search.py","map_benchmarks","w","5","2"]]

for file in filePath:
	for comand in commands:
		TempComand=[]
		for c in comand:
			TempComand.append(c)
		TempComand[2]=str(TempComand[2])+str(file)
		subprocess.call(TempComand)