from random import random
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
import numpy as np
import warnings
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

warnings.filterwarnings('ignore')

class Individuo():
    def __init__(self, features, geracao=0):
        self.r2 = 0
        self.geracao = geracao
        self.cromossomo = []
        for i in range(features):
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
    
    def avaliacao(self,X,y,features,modelo):
        k = X.shape[0]
        index = range(k)
        X_new = pd.DataFrame(index=index)
        for i in range(features):
            if self.cromossomo[i]=='1':
                X_new = X_new.join(df_train.iloc[:,i])
        X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.2, random_state=42)
        modelo = make_pipeline(StandardScaler(),SVR(C=80, gamma= 0.036,kernel = 'rbf'))
        modelo.fit(X_train,y_train)
        y_test_predict = modelo.predict(X_test)
        score = mean_squared_error(y_test,y_test_predict)
        scores = 10 - np.sqrt(score)
        self.r2 = scores
        print(self.r2)
    
    def crossover(self, features, outro_individuo):
        corte = round(random()  * len(self.cromossomo))
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        filhos = [Individuo(features, self.geracao + 1),
                  Individuo(features, self.geracao + 1)]
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos
    
    def mutacao(self, taxa_mutacao):
        #print("Antes %s " % self.cromossomo)
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        #print("Depois %s " % self.cromossomo)
        return self

class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []
    
    def inicializa_populacao(self, features):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(features))
        self.melhor_solucao = self.populacao[0]
        
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao, key = lambda populacao: populacao.r2, reverse=True)
        
    def melhor_individuo(self, individuo):
        if individuo.r2 > self.melhor_solucao.r2:
            self.melhor_solucao = individuo
            
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
           soma += individuo.r2
        return soma
    
    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].r2
            pai += 1
            i += 1
        return pai
    
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G:%s -> R2: %s Cromossomo: %s" % (self.populacao[0].geracao,
                                                 melhor.r2,
                                                 melhor.cromossomo))
    
    def resolver(self, features, X, y, taxa_mutacao, numero_geracoes,modelo):
        self.inicializa_populacao(features)
        
        for individuo in self.populacao:
            individuo.avaliacao(X,y,features,modelo)
        
        self.ordena_populacao()
        y=self
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.r2)
        
        self.visualiza_geracao()
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(features, self.populacao[pai2])
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
            
            self.populacao = list(nova_populacao)
            
            for individuo in self.populacao:
                individuo.avaliacao(X,y,features,modelo)
            
            self.ordena_populacao()
            
            self.visualiza_geracao()
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)
            self.melhor_individuo(melhor)
        
        print("\nMelhor solução -> G: %s R2: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.r2,
               self.melhor_solucao.cromossomo))
        
        return self.melhor_solucao.cromossomo
    
if __name__ == '__main__':
    
    
    df_train = pd.read_csv('df_per_no_train.csv')
    df_holdout = pd.read_csv('df_per_no_holdout.csv')
    
    X_t = df_train.drop(['TOP SPEED [min]', 'Unnamed: 0','After'], axis=1)
    y_t = df_train.drop(['Unnamed: 0', 'Total poids chargeKg]',
                        'Total poids charge combustible [Kg]',
                        'Total composant charge M +F + C + fines [Kg]', 'Total humide [Kg]',
                        'Densite de chargement [t/m3]',
                        'Permeabilite avant allumage [Nm3/m2/mn]', 'Humidite sur sec [%/sec]',
                        'FE total [Kg]', 'CaO [Kg]', 'SiO2 [Kg]',
                        'Al2O3 [Kg]', 'MN [Kg]', 'TiO2 [Kg]', 'H20 HYD [Kg]', 'Fe++ [Kg]',
                        'Graphite [Kg]', 'Charbon [Kg]', 'Carbone [Kg]', 'H2O SA [Kg]',
                        'H2O DI [Kg]', 'H2O ADD [Kg]', 'Numerical Serie',
                        'Mailles > 2,5mm  Poids [Kg]', 'Mailles < 1,25mm   Poids [Kg]',
                        'Mailles > 2,5mm  %', 'Mailles < 1,25mm    %',
                        'Fines de retour chargees %', 'Total poids charge %','After'], axis=1)
    
    limite = 10
    tamanho_populacao = 20
    taxa_mutacao = 0.01
    numero_geracoes = 100
    ag = AlgoritmoGenetico(tamanho_populacao)
    features = X_t.shape[1]
    pipe_svr = make_pipeline(StandardScaler(),SVR(C=80, gamma= 0.036,kernel = 'rbf'))
    
    resultado = ag.resolver(features, X_t, y_t, taxa_mutacao, numero_geracoes,pipe_svr)

    plt.plot(ag.lista_solucoes)
    plt.title("Acompanhamento dos valores")
    plt.show() 
coluna=[]
k=['1', '1', '1', '0', '0', '1', '0', '1', '1', '0', '1', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '1', '0', '1', '0', '0']
for i in range(len(k)):
    if k[i]=='1':
        coluna.append(i)
X_g = X_t.iloc[:,coluna]
pipe_svr = make_pipeline(StandardScaler(),SVR(C=80, gamma= 0.036,kernel = 'rbf'))

scores_svr = cross_val_score(estimator = pipe_svr, X=X_g, y=y_t, cv=10, n_jobs = -1,scoring = 'neg_mean_squared_error')

print('CV R2: %.3f +/- %.3f' % (np.mean(np.sqrt(-scores_svr)), np.std(np.sqrt(-scores_svr))))