#Python function to compute the principal directions and values 

def sprind(s,lstr,ndi,nshr): 
     import math 
     pi23=2.094395102393195 
     cons1=10000.0 
     precis=2.22e-16 
     preciz=precis*cons1 
     zero=0.0 
     half=0.5 
     one=1.e0 
     two=2.e0 
     third=one/3.e0 
     asmall=1.e0/1.e36 

     ps=[zero,zero,zero] 
     an=[[zero,zero,zero],[zero,zero,zero],[zero,zero,zero]] 




     # LSTR=1 - STRESS 
     # LSTR=2 - STRAIN 
     # 
     # THE EIGENVALUES OF S(*) ARE PUT IN PS(K1),K1=1,3 
     # 
     # DIRECTION COSINES OF PS(K1) ARE PUT IN AN(K1,K2),K2=1,2,3 
     # 

     ndip1=ndi 
     ndip2=ndi+1 
     ndip3=ndi+2 


     # 
     # NO SHEAR COMPONENTS 
     # 
     if nshr==0: 
         an[0][0]=one 
         an[1][1]=one 
         an[2][2]=one 
         for i in range(3): 
             ps[i]=s[i] 


     # 
     # ONE SHEAR COMPONENT: FIRST NORMALIZE WITHOUT DEVIATORIC PART 
     # 
     elif nshr==1: 

         if ndi==0: 
             sh=zero 
             s11=zero 
             s22=zero 
         elif ndi==1: 
             sh=half*s[0] 
             s11=sh 
             s22=-sh 
         else: 
             sh=half*(s[0]+s[1]) 
             s11=half*(s[0]-s[1]) 
             s22=-s11 
         if lstr==1: 
             s12=s[ndip1] 
         else: 
             s12=half*s[ndip1] 
         facd= math.fabs(s11) 
         facs= math.fabs(s12) 
         fact= max(facd,facs) 
         # 
         # ESSENTIALLY UNIT MATRIX 
         # 
         if fact<=math.fabs(preciz*sh) or facs<preciz*facd: 
             ps[0]=s[0] 
             ps[1]=s[1] 
             an[0][0]=one 
             an[1][1]=one 
         elif fact<asmall: 
             #     -- We've been given very small [zero] numbers 
             ps[0]=zero 
             ps[1]=zero 
             an[0][0]=one 
             an[1][1]=one 
         else: 
             # 
             # SCALE THE DEVIATORIC STRESS COMPONENTS 
             # 
             ofac=one/fact 
             s11=ofac*s11 
             s22=ofac*s22 
             s12=ofac*s12 
             # 
             # GET THE EIGENVALUES AND EIGENVECTORS 
             # 
             temp=s11**2+s12**2 
             d=math.sqrt(temp) 
             ps[0]=sh-fact*d 
             ps[1]=sh+fact*d 
             s11=s11+d 
             s22=s22+d 
             if math.fabs(s11)>=math.fabs(s22): 
                 ofac=one/math.sqrt(s11**2+s12**2) 
                 an[0][0]=ofac*s12 
                 an[1][0]=-ofac*s11 
             else: 
                 ofac=one/math.sqrt(s12**2+s22**2) 
                 an[0][0]=ofac*s22 
                 an[1][0]=-ofac*s12 

             an[0][1]=-an[1][0] 
             an[1][1]=an[0][0] 

         if ndi==3: 
             ps[2]=s[2] 
         an[2][2]=one 
     else: 

         # 
         # THREE SHEAR COMPONENTS, ALL DIRECTIONS UNKNOWN 
         # 
         # GET DEVIATORIC STRESSES 
         # 
         if ndi==0: 
             sh=zero 
             s11=zero 
             s22=zero 
             s33=zero 
         elif ndi==1: 
             sh=third*s[0] 
             s11=s[0]-sh 
             s22=-sh 
             s33=-sh 
         elif ndi==2: 
             sh=third*(s[0]+s[1]) 
             s11=s[0]-sh 
             s22=s[1]-sh 
             s33=-sh 
         else: 
             sh=third*(s[0]+s[1]+s[2]) 
             s11=s[0]-sh 
             s22=s[1]-sh 
             s33=s[2]-sh 
         if lstr==1: 
             s12=s[ndip1] 
             s13=s[ndip2] 
             if nshr>2: 
                 s23=s[ndip3] 
             else: 
                 s23=zero 
         else: 
             s12=half*s[ndip1] 
             s13=half*s[ndip2] 
             if  nshr>2: 
                 s23=half*s(ndip3) 
             else: 
                 s23=zero 
         facd=max(math.fabs(s11),math.fabs(s22),math.fabs(s33)) 
         facs=max(math.fabs(s12),math.fabs(s13),math.fabs(s23)) 
         fact=max(facd,facs) 
         if fact<=math.fabs(preciz*sh) or facs<preciz*facd: 
             # 
             # ESSENTIALLY UNIT MATRIX 
             # 
             for k1 in range(ndi): 
                 ps[k1]=s[k1] 
             an[0][0]=one 
             an[1][1]=one 
             an[2][2]=one 
         elif fact<asmall : 
             #     -- We've been given very small [zero] numbers 
             for k1 in range(ndi): 
                 ps[k1]=zero 
             an[0][0]=one 
             an[1][1]=one 
             an[2][2]=one 
         else: 
             # 
             # SCALE THE DEVIATORIC STRESS COMPONENTS 
             # 
             ofac=one/fact 
             s11=ofac*s11 
             s22=ofac*s22 
             s33=ofac*s33 
             s12=ofac*s12 
             s13=ofac*s13 
             s23=ofac*s23 
             # 
             # DO THE EIGENVALUE CALCULATION FOR THE SCALED STRESSES 
             # 
             q=math.sqrt(third*(s12**2+s13**2+s23**2+ 
                                half*(s11**2+s22**2+s33**2))) 
             r=(half*(s11*s22*s33-s11*s23**2-s22*s13**2-s33*s12**2) 
                +s12*s13*s23)/q**3 
             if(r>=one-precis) : 
                 cos1=-half 
                 cos2=-half 
                 cos3= one 
             elif(r<=precis-one) : 
                 cos1=-one 
                 cos2= half 
                 cos3= half 
             else: 
                 ang = third*math.acos(r) 
                 cos1= math.cos(ang) 
                 cos2= math.cos(ang+pi23) 
                 cos3=-cos1-cos2 
             ps[0]=two*q*cos1 
             ps[1]=two*q*cos2 
             ps[2]=two*q*cos3 
             # 
             # SPECIAL CASES: DOUBLE EIGENVALUES. SELECT THE UNIQUE ONE (K1) 
             # 
             if(ps[0]==ps[1]) : 
                 k1=2 
             elif(ps[1]==ps[2]) : 
                 k1=0 
             else: 
                 k1=1 
             # 
             # SUBTRACT SELECTED EIGENVALUE 
             # 
             s11=s11-ps[k1] 
             s22=s22-ps[k1] 
             s33=s33-ps[k1] 
             # 
             # FIND THE FIRST PRINCIPAL DIRECTION BY CROSS PRODUCT OF TWO ROWS 
             # TRY WHICH ROWS GIVE A NON-ZERO RESULT 
             # K0 INDICATES WHICH ROWS WERE USED 
             # 
             k0=1 
             an[0][k1]=s22*s33-s23*s23 
             an[1][k1]=s23*s13-s12*s33 
             an[2][k1]=s12*s23-s22*s13 
             anorm=an[0][k1]**2+an[1][k1]**2+an[2][k1]**2 
             a1=s12*s23-s13*s22 
             a2=s13*s12-s11*s23 
             a3=s11*s22-s12*s12 
             anormt=a1**2+a2**2+a3**2 
             if(math.fabs(anormt)>math.fabs(anorm)) : 
                 k0=3 
                 an[0][k1]=a1 
                 an[1][k1]=a2 
                 an[2][k1]=a3 
                 anorm=anormt 
             a1=s12*s33-s23*s13 
             a2=s13*s13-s33*s11 
             a3=s11*s23-s13*s12 
             anormt=a1**2+a2**2+a3**2 
             if(math.fabs(anormt)>math.fabs(anorm)) : 
                 k0=2 
                 an[0][k1]=a1 
                 an[1][k1]=a2 
                 an[2][k1]=a3 
                 anorm=anormt 
             if(anorm==zero) : 
                 k0=0 
                 an[0][k1]=one 
                 an[1][k1]=zero 
                 an[2][k1]=zero 
                 anorm=one 
             anorm=one/math.sqrt(anorm) 
             an[0][k1]=an[0][k1]*anorm 
             an[1][k1]=an[1][k1]*anorm 
             an[2][k1]=an[2][k1]*anorm 
             if(k1!=1 or ps[0]==ps[2]) : 
                 # 
                 # CASE OF DOUBLE EIGENVALUES: ONLY REQUIREMENT IS THEY ARE NORMAL TO THE 
                 # FIRST DIRECTION. FIRST SELECT SECOND AND THIRD EIGENVALUE (K2 AND K3) 
                 # 
                 if(k1!=1) : 
                     k2=2-k1 
                     k3=1 
                 else: 
                     k2=0 
                     k3=2 
                 # PICK UP ROW WHICH IS GUARANTEED NON-ZERO OR GENERATE UNIT X DIRECTION 
                 # 
                 if(k0==0) : 
                     an[0][k2]=zero 
                     an[1][k2]=one 
                     an[2][k2]=zero 
                     anorm=one 
                 elif(k0!=2) : 
                     an[0][k2]=s12 
                     an[1][k2]=s22 
                     an[2][k2]=s23 
                     anorm=s12**2+s22**2+s23**2 
                 else: 
                     an[0][k2]=s11 
                     an[1][k2]=s12 
                     an[2][k2]=s13 
                     anorm=s11**2+s12**2+s13**2 
             else: 
                     # 
                     # THREE SEPARATE EIGENVALUES: REPEAT THE PROCESS FOR THE FIRST ONE 
                     # 
                     k2=0 
                     k3=2 
                     s11=s11+ps[k1]-ps[k2] 
                     s22=s22+ps[k1]-ps[k2] 
                     s33=s33+ps[k1]-ps[k2] 
                     an[0][k2]=s22*s33-s23*s23 
                     an[1][k2]=s23*s13-s12*s33 
                     an[2][k2]=s12*s23-s22*s13 
                     anorm=an[0][k2]**2+an[1][k2]**2+an[2][k2]**2 
                     a1=s12*s23-s13*s22 
                     a2=s13*s12-s11*s23 
                     a3=s11*s22-s12*s12 
                     anormt=a1**2+a2**2+a3**2 
                     if(math.fabs(anormt)>math.fabs(anorm)) : 
                         an[0][k2]=a1 
                         an[1][k2]=a2 
                         an[2][k2]=a3 
                         anorm=anormt 
                     a1=s12*s33-s23*s13 
                     a2=s13*s13-s33*s11 
                     a3=s11*s23-s13*s12 
                     anormt=a1**2+a2**2+a3**2 
                     if(math.fabs(anormt)>math.fabs(anorm)) : 
                         an[0][k2]=a1 
                         an[1][k2]=a2 
                         an[2][k2]=a3 
                         anorm=anormt 
                     if(anorm==zero) : 
                         an[0][k2]=zero 
                         an[1][k2]=one 
                         an[2][k2]=zero 
                         anorm=one 
             anorm=one/math.sqrt(anorm) 
             an[0][k2]=an[0][k2]*anorm 
             an[1][k2]=an[1][k2]*anorm 
             an[2][k2]=an[2][k2]*anorm 
             # 
             # GET THE LAST ONE BY #ROSSING THE FIRST TWO 
             # 
             an[0][k3]=an[1][k1]*an[2][k2]-an[2][k1]*an[1][k2] 
             an[1][k3]=an[2][k1]*an[0][k2]-an[0][k1]*an[2][k2] 
             an[2][k3]=an[0][k1]*an[1][k2]-an[1][k1]*an[0][k2] 
             # 
             # SCALE UP EIGENVALUES AND ADD HYDROSTATIC PART 
             # 
             ps[0]=fact*ps[0]+sh 
             ps[1]=fact*ps[1]+sh 
             ps[2]=fact*ps[2]+sh 
     return ps,an 