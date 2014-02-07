#Made by J.T.B. Overvelde on 9 may 2011

listBack=['.com','.dat','.inp','.ipm','.lck','.log','.msg','.odb','.prt','.sta']
for i in listBack:
	if os.path.exists(tDr+'/'+jobName1+i)==True:
		os.remove(tDr+'/'+jobName1+i)
	if os.path.exists(tDr+'/'+jobName2+i)==True:
		os.remove(tDr+'/'+jobName2+i)

