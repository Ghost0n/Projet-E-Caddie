#######################################################################################################################################################################################################
#
#   Interface graphique de l'IHM
#
#   Auteur :     BOUZEYEN Ghassen, CHABIR Yassine, DACHRAOUI Amine
#   Nom du projet : E-CADDIE
#
#   But de la fonction : 
#   Le but de ce code est d'afficher sur une interface graphique bien claire et lisible, l'état des caisses en temps réél, le stockage du e-caddie, et son état de batterie.
#
#
#
#   Entrée :
#       le poids stocké dans le e-caddie, l'état des caisses...
#
#   Sortie :
#       Afficher les données reçus comme des variables sur une interface graphique
#       

########################################################################################################################################################################################################




import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import Int16
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from time import sleep
import random
from kivy.clock import Clock
 

 
class MyRelativeLayout(RelativeLayout):
    def build(self):
        image = Image(source='./images/Supermarche2.jpg',allow_stretch=True,keep_ratio=False)   
        self.add_widget(image)
        self.orientation='vertical'
        self.spacing=20
        self.Un_Label()
        self.Un_Slider()
        self.variables_ross()

      
    def change_slider_value(self,x):
        self.slider.value = round(x * 33)


    def Un_Slider(self):                                                                                       #Mise en place d'un Slider qui indique la localisation du caddie
        self.slider = Slider(min = 0, max = 100)
        self.slider.size_hint=(0.5,0.15)
        self.slider.pos_hint={'x': 0.25, 'center_y': .5}
        self.slider.value = 0
        self.add_widget(self.slider)


    def Un_Label(self):
        #On cree des labels avec toutes ses proprietes:
        self.Label1=Label(text="SYSTEME DE CONTROLE DE E-CADDIE",   pos_hint={'x': -0.0     , 'y': 0.35},       color=[0, 0, 255])  
        self.Label2=Label(text="Caisse 1",                          pos_hint={'x': -0.406   , 'y': -0.3},       color=[0, 0, 255])
        self.Label3=Label(text="Caisse 2",                          pos_hint={'x': 0        , 'y': -0.3},       color=[0, 0, 255])
        self.Label4=Label(text="Caisse 3",                          pos_hint={'x': 0.406    , 'y': -0.3},       color=[0, 0, 255])
        self.Label5=Label(text="Batterie",                          pos_hint={'x': -0.352   , 'y': 0.16},       color=[0, 0, 255])
        self.Label6=Label(text="Stockage",                          pos_hint={'x': 0.338    , 'y': 0.16},       color=[0, 0, 255])
        
        self.Label7=Label(text="Park",                              pos_hint={'x': -0.23, 'center_y': .56},     color=[0, 0, 255])
        self.Label8=Label(text="1",                                 pos_hint={'x': -0.08, 'center_y': .56},     color=[0, 0, 255])
        self.Label9=Label(text="2",                                 pos_hint={'x': 0.073, 'center_y': .56},     color=[0, 0, 255])
        self.Label10=Label(text="3",                                pos_hint={'x': 0.226, 'center_y': .56},     color=[0, 0, 255])
        self.Label11=Label(text="|",                                pos_hint={'x': -0.23, 'center_y': .53},     color=[0, 0, 255])
        self.Label12=Label(text="|",                                pos_hint={'x': -0.08, 'center_y': .53},     color=[0, 0, 255])
        self.Label13=Label(text="|",                                pos_hint={'x': 0.073, 'center_y': .53},     color=[0, 0, 255])
        self.Label14=Label(text="|",                                pos_hint={'x': 0.226, 'center_y': .53},     color=[0, 0, 255])
       
        liste = self.variables_ross()   
        self.Label15=Label(text=str(liste[1]),                      pos_hint={'x': -0.357, 'y': 0.114},          color=[250, 10, 10])   
        self.Label16=Label(text=str(liste[0]),                      pos_hint={'x':  0.333, 'y': 0.114},          color=[250, 10, 10])
        
        #On les ajoute au layout principal:
        self.add_widget(self.Label1)
        self.add_widget(self.Label2)
        self.add_widget(self.Label3)
        self.add_widget(self.Label4)
        self.add_widget(self.Label5)
        self.add_widget(self.Label6)
        self.add_widget(self.Label7)
        self.add_widget(self.Label8)
        self.add_widget(self.Label9)
        self.add_widget(self.Label10)
        self.add_widget(self.Label11)
        self.add_widget(self.Label12)
        self.add_widget(self.Label13)
        self.add_widget(self.Label14)
        self.add_widget(self.Label15)
        self.add_widget(self.Label16)        
    

    def variables_ross(self):
        batteriev = random.randint(0,100)               #Valeur batterie qu'on attend de ROS
        stockagev = random.randint(0,100)               #Valeur stockage qu'on attend de ROS
        var_ros= [batteriev, stockagev]             
        return var_ros 


    def change_etat_caisse(self,etat):                  #Fonction pour afficher les caisses qui sont en attente
        for i in range(1,len(etat)):
            xi = (i-2)*0.406                                
            jaune = Image(source='./images/jaune.jpg',allow_stretch=False,keep_ratio=True,pos_hint={'x': xi, 'y': -0.374})
            gris  = Image(source='./images/gris.jpg' ,allow_stretch=False,keep_ratio=True,pos_hint={'x': xi, 'y': -0.374})
            if etat[i]==1:
                  
                self.add_widget(jaune)
            else:
                self.add_widget(gris)

    
 
class DrawingWindow(App):
    def build(self):                                            #Layout
        self.layout = MyRelativeLayout()
        self.layout.build()
        self.pos_caddie = [0.0,0.0]
        self.etat_caisses = [0,0,0,0]
        self.etat_batterie = 100
        self.stockage = 0
        self.current_i = 0
        rospy.init_node('IHM',anonymous=True)                   #Lancement noeud ROS
        Clock.schedule_interval(self.update, 0.5)               #Rafraichir l'interface en temps réel 
        return self.layout


    def refresh_pos_caddie(self,data):
        self.pos_caddie[0] = round(data.data[0], 2)             #Indiquer la position du caddie en temps réel
        self.pos_caddie[1] = round(data.data[1], 2)
        

    def refresh_etat_caisses(self,data):                        #Indiquer l'etat  des caisses en temps réel
        self.etat_caisses[1]= data.data[1]
        self.etat_caisses[2] = data.data[2]
        self.etat_caisses[3] = data.data[3]

    def refresh_batterie(self,data):                            #Fonction prête pour la recupération de l'état de batterie 
        self.etat_batterie = data.data


    def refresh_stockage(self,data):                            #Fonction prête pour la recupération de l'état du stockage 
        self.stockage = data.data


    def update(self, *args):
        rospy.Subscriber('pos_caddie',Float32MultiArray,self.refresh_pos_caddie)                #Recuperer la position du caddie via le ROS
        rospy.Subscriber('etat_caisse',Int16MultiArray,self.refresh_etat_caisses)               #Recuperer l'état des caisses via le ROS
        #rospy.Subscriber('batterie',Int16,self.refresh_batterie)                               #A recuperer 
        #rospy.Subscriber('stockage',Int16,self.refresh_stockage)                               #A recuperer

        lista = self.layout.variables_ross()
        self.layout.remove_widget(self.layout.Label15)
        self.layout.remove_widget(self.layout.Label16)

        self.layout.Label15= Label(text=str(lista[1]),       pos_hint={'x': -0.357, 'y': 0.114},          color=[250, 10, 10])
        self.layout.Label16= Label(text=str(lista[0]),       pos_hint={'x':  0.333, 'y': 0.114},          color=[250, 10, 10])
        
        self.layout.add_widget(self.layout.Label15)
        self.layout.add_widget(self.layout.Label16)
        
        self.layout.change_slider_value(self.pos_caddie[0])                                     #Afficher la position du caddie dans le slider
        self.layout.change_etat_caisse (self.etat_caisses)                                      #Afficher l'état des caisses sur l'IHM


        
        self.current_i = 1
        if self.current_i == 0:
            Clock.unschedule(self.update)                                                       #Rafraichir les données


