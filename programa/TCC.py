"""
@author: Josué Luiz Caprini Laiber
"""
from random import random
import matplotlib.pyplot as plt
class Individuo():
    def __init__(self, geracao=0):
        self.yp = 0                     #tamanho em y do pilar
        self.xp = 0                     #tamanho em x do pilar
        self.custo_avaliacao = 0
        self.geracao = geracao
        self.cromossomo = []
        
        for i in range(10):
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")   

        self.xp = 20+ 1*int(self.cromossomo[0])+2*int(self.cromossomo[1])+4*int(self.cromossomo[2])+8*int(self.cromossomo[3])+16*int(self.cromossomo[4])
        self.yp = 20+ 1*int(self.cromossomo[5])+2*int(self.cromossomo[6])+4* int(self.cromossomo[7])+8*int(self.cromossomo[8])+16*int(self.cromossomo[9])
        #Fatores de correção do momento seguindo o trabalho do trento
        self.fatorxh=2*10**(-5)*self.xp**3-0.0026*self.xp**2+0.088*self.xp+1.2019
        self.fatoryh=0.0005*self.yp**2-0.0668*self.yp+3.2116
        self.fatorxv=2*10**(-5)*self.yp**3-0.0026*self.yp**2+0.088*self.yp+1.2019
        self.fatoryv=0.0005*self.xp**2-0.0668*self.xp+3.2116
        
        
    def avaliacao(self, fyd, fcd, L, q, d, b, h, H,Cv,Cforma,Caco):
        if self.fatorxh > self.fatoryh:
            Mdh = 1.4*q*(L^2)/8*self.fatorxh
        else:
            Mdh = 1.4*q*(L^2)/8*self.fatoryh
        if self.fatorxv > self.fatoryv:
            Mdv = 1.4*q*(L^2)/8*self.fatorxv
        else:
            Mdv = 1.4*q*(L^2)/8*self.fatoryv
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
        Tp=Vsd/(self.xp*self.yp)
        self.PAs = (((Ash*4+Asv1*2+Asv2+7*Asw)*L)+0.4*self.xp*self.yp*6)*7800/10000               #Massa de aco
        self.Vc = L*(h/100)*(b/100)*7 + 6*self.yp*self.xp*H/10000 #volume concreto
        self.Aforma = 2*7*(L*(h/100)+L*(b/100))+ 2*6*(H*(self.xp/100)+H*(self.yp/100))
        if xlinhav2>xlimite or dlimite>d or Tp>fcd :
            self.custo_avaliacao=10000000       #Coloca-se valor exorbitante para ser desconsiderado no rankiamento
        else:
            self.custo_avaliacao= self.Vc*Cv+self.Aforma*Cforma+Caco*self.PAs
        
    def crossover(self, outro_individuo):
        corte1 = round(random()  * 5)
        filho1 = outro_individuo.cromossomo[0:corte1] + self.cromossomo[corte1::]#+outro_individuo.cromossomo[corte2::]
        filho2 = self.cromossomo[0:corte1] + outro_individuo.cromossomo[corte1::]#+self.cromossomo[corte2::]
        
        filhos = [Individuo(self.geracao + 1),
                  Individuo(self.geracao + 1)]
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos
    
    def mutacao(self, taxa_mutacao):
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        return self
    
    
    
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []
        
    def inicializa_populacao(self):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo())
        self.melhor_solucao = self.populacao[0]
        
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.custo_avaliacao)
        
    def melhor_individuo(self, individuo):
        if individuo.custo_avaliacao < self.melhor_solucao.custo_avaliacao:
            self.melhor_solucao = individuo
            
    def soma_avaliacoes(self):
        soma = 0
        for i in range(10):
            if self.populacao[i].custo_avaliacao !=10000000:
                soma += self.populacao[i].custo_avaliacao
        return soma
    
    def seleciona_pai(self, soma_avaliacao):
        pizza=list()
        for i in range(10):
            if self.populacao[i].custo_avaliacao !=10000000:
                k=self.populacao[9-i].custo_avaliacao
                proporcao=k/soma_avaliacao
                pizza.append(proporcao)
        pai = -1
        valor_sorteado = random()
        i = 0
        soma=0
        while i < len(pizza) and soma < valor_sorteado:
            soma += pizza[i]
            pai += 1
            i += 1
        return pai
    
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G:%s -> Valor: %s  Xp: %s  Yp: %s" % (self.populacao[0].geracao,
                                                               melhor.custo_avaliacao,
                                                               melhor.xp, melhor.yp))
    
    def resolver(self, taxa_mutacao, numero_geracoes,fyd, fcd, L, q, d, b, h, H,Cc, Cforma,Caco):
        self.inicializa_populacao()
        
        for individuo in self.populacao:
            individuo.avaliacao(fyd, fcd, L, q, d, b, h, H,Cc,Cforma,Caco)
        
        self.ordena_populacao()
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.custo_avaliacao)
        
        self.visualiza_geracao()
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
            
            self.populacao = list(nova_populacao)
            
            for individuo in self.populacao:
                individuo.avaliacao(fyd, fcd, L, q, d, b, h, H,Cc, Cforma,Caco)
            
            self.ordena_populacao()
            
            self.visualiza_geracao()
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.custo_avaliacao)
            self.melhor_individuo(melhor)
        
        print("\nMelhor solução -> G: %s Valor: %s Xp: %s Yp: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.custo_avaliacao,
               self.melhor_solucao.xp,
               self.melhor_solucao.yp))
        
        return self.melhor_solucao
    
if __name__ == '__main__':
    fcd = 3/1.4        #[kN/cm^2] Resitência à tração no concreto de cálculo
    fyd = 50/1.15       #[kN/cm^2] Resitência à tração no aço de cálculo
    L = 6               #[m] Tamanho do vão
    q = 52            #[kN/m] Carregamento
    c = 3               #[cm] Cobrimento
    H = 3               #[m] Pe direito
    h = 50              #[cm] Altura da viga
    b = 20              #[cm] Largura da viga
    d = h-c             #[cm] Altura útil
    Cc = 244            #custo do volume do concreto
    Cforma = 26.04      #custo da area da forma
    Caco = 3.99         #custo do kg do aço
    tamanho_populacao = 20                  #Tamanho da população inicial
    taxa_mutacao = 0.01
    numero_geracoes = 100
    ag = AlgoritmoGenetico(tamanho_populacao)
    resultado = ag.resolver(taxa_mutacao, numero_geracoes,fyd, fcd, L, q, d, b, h, H,Cc, Cforma,Caco )
    plt.plot(ag.lista_solucoes)
    plt.title("Acompanhamento dos valores")
    plt.show()