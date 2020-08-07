# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 21:47:04 2018

@author: Josué Luiz Caprini Liaber
"""

fcd = 3/1.4        #[kN/cm^2] Resitência à tração no concreto de cálculo
fyd = 50/1.15       #[kN/cm^2] Resitência à tração no aço de cálculo
L = 6               #[m] Tamanho do vão
q = 80          #[kN/m] Carregamento
c = 3               #[cm] Cobrimento
H = 3               #[m] Pe direito
h = 50              #[cm] Altura da viga
b = 20              #[cm] Largura da viga
d = h-c             #[cm] Altura útil
Cc = 244            #custo do volume do concreto
Cforma = 26.04      #custo da area da forma
Caco = 3.99         #custo do kg do aço
# Valores de inicializaçao
Xpotimo=0
Ypotimo=0
customin=10000000000 

for xp in range(20,60,1):
    for yp in range (20,60,1):
        fatorxh=2*10**(-5)*xp**3-0.0026*xp**2+0.088*xp+1.2019
        fatoryh=0.0005*yp**2-0.0668*yp+3.2116
        fatorxv=2*10**(-5)*yp**3-0.0026*yp**2+0.088*yp+1.2019
        fatoryv=0.0005*xp**2-0.0668*xp+3.2116
        if fatorxh > fatoryh:
            Mdh = 1.4*q*(L^2)/8*fatorxh
        else:
            Mdh = 1.4*q*(L^2)/8*fatoryh
        if fatorxv > fatoryv:
            Mdv = 1.4*q*(L^2)/8*fatorxv
        else:
            Mdv = 1.4*q*(L^2)/8*fatoryv
        Mdlim = 0.251*(b/100)*(d**2)*fcd
        dlimite = 2*(Mdv/((b/100)*fcd))**(0.5) #Cálculo da altura mínima da viga
        xlinhah = 1.25*d*(1-(1-Mdh/(0.425*(b/100)*(d**2)*fcd))**(0.5)) #valor do x para as vigas carregadas por 1/4 da lage
        xlinhav1 = 1.25*d*(1-(1-Mdv/(0.425*(b/100)*(d**2)*fcd))**(0.5)) #valor do x para as vigas carregadas por 1/4 da lage
        xlinhav2 = 1.25*d*(1-(1-Mdv*2/(0.425*(b/100)*(d**2)*fcd))**(0.5)) #valor do x para a viga carregada por 1/4 de duas lages
        xlimite = d*0.45        # a partir dai ruptura ductil
        if Mdh <Mdlim:
            Ash = 0.68*b*xlinhah*fcd/fyd
        else:
            Ash = 0.306*(b/100)*h*fcd/fyd+(Mdh-Mdlim)/(fyd*d)*2
        if Mdv<Mdlim:
            Asv1 = 0.68*b*xlinhav1*fcd/fyd
        else:
            Asv1 = 0.306*(b/100)*h*fcd/fyd+(Mdv-Mdlim)/(fyd*d)*2
        if (Mdv*2)<Mdlim:
            Asv2 = 0.68*b*xlinhav2*fcd/fyd
        else:
            Asv2 = 0.306*(b/100)*h*fcd/fyd+(Mdv*2-Mdlim)/(fyd*d)*2
        fck=fcd*1.4*10
        delt=0.6*(1-fck/250)
        Vdr2=0.45*b*h*fcd*delt
        Vsd=(1.4*q*4*L/2)
        Vc=0.009*b*h*fck**(2/3)
        Asw=(Vsd-Vc)*100/(0.9*h*fyd)
        Aswmin=0.009*b*100*fck**(2/3)
        if Asw>Aswmin:
            Asw=Aswmin
        Tp=Vsd/(xp*yp)
        PAs = (((Ash*4+Asv1*2+Asv2+7*Asw)*L)+0.4*xp*yp*6)*7800/10000               #Massa de aco
        Vc = L*(h/100)*(b/100)*7 + 6*yp*xp*H/10000 #volume concreto
        Aforma = 2*7*(L*(h/100)+L*(b/100))+ 2*6*(H*(xp/100)+H*(yp/100))
        if xlinhav2>xlimite or dlimite>d or Tp>fcd:
            custo_avaliacao=10000000       #Coloca-se valor exorbitante para ser desconsiderado no rankiamento
        else:
            custo_avaliacao= Vc*Cc+Aforma*Cforma+Caco*PAs
        if custo_avaliacao<customin:
            customin=custo_avaliacao
            Xpotimo=xp
            Ypotimo=yp
print('\n Melhor Valor -> Custo:%s Xp:%s Yp:%s'%(customin,Xpotimo,Ypotimo))