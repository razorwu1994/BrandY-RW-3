import subprocess


commands= [["py","search.py","map_benchmarks\map5\map5-1.txt","u"],["py","search.py","map_benchmarks\map5\map5-1.txt","a","1"]
			,["py","search.py","map_benchmarks\map5\map5-1.txt","a","2"],["py","search.py","map_benchmarks\map5\map5-1.txt","a","3"]
			,["py","search.py","map_benchmarks\map5\map5-1.txt","a","4"],["py","search.py","map_benchmarks\map5\map5-1.txt","a","5"]
			,["py","search.py","map_benchmarks\map5\map5-1.txt","w","1","1.25"],["py","search.py","map_benchmarks\map5\map5-1.txt","w","2","1.25"]
			,["py","search.py","map_benchmarks\map5\map5-1.txt","w","3","1.25"],["py","search.py","map_benchmarks\map5\map5-1.txt","w","4","1.25"]
			,["py","search.py","map_benchmarks\map5\map5-1.txt","w","5","1.25"],["py","search.py","map_benchmarks\map5\map5-1.txt","w","1","2"]
			,["py","search.py","map_benchmarks\map5\map5-1.txt","w","2","2"],["py","search.py","map_benchmarks\map5\map5-1.txt","w","3","2"]
			,["py","search.py","map_benchmarks\map5\map5-1.txt","w","4","2"],["py","search.py","map_benchmarks\map5\map5-1.txt","w","5","2"]]

for command in commands:
	subprocess.call(command)