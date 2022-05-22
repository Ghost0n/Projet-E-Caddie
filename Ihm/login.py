#######################################################################################################################################################################################################
#
#   Fonction login pour assurer l'authentification de l'utilisateur vers l'interface graphique de l'IHM
#
#   Auteur :     CHABIR Yassine, DACHRAOUI Amine, ELKAMEL Sirine
#   Nom du projet : E-CADDIE
#
#   But de la fonction : 
#       Cette fonction a pour objectif de détecter un code à barre quand il passe devant la caméra placé sur le e-caddie et vérifier après si ce produit existe dans la base de données
#       qui contient la liste des produits du supermarché et verifie ensuite l'éligibilité de ce produit, ça veut dire si le produit est trop grand ou il n'est pas de type frais, un son de refus va sortir 
#       pour alerter la caissière que ce produit n'entre pas dans le e-caddie.Dans le cas contraire un son va être génerer pour confirmer l'acceptation de ce produit.
#
#   Entrée :
#       Un username et un mot de passe
#
#   Sortie :
#       Dériger l'utilisateur vers l'interface graphique de l'IHM si le nom d'utilisateur et le mot de passe sont correctes
#       Sinon afficher un message invitant l'itlisateur à ressaisir le nom d'utilisateur et le mot de passe

########################################################################################################################################################################################################

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image
from ihm import DrawingWindow
import sqlite3



conn = sqlite3.connect(r"//home//dachra//Desktop//CHABIR_yassine_DACHRAOUI_amine_groupe_8_caddie-intelligent//donnees10.db")    #connecter la base de données
mycursor = conn.cursor()


class LoginUI(GridLayout):

    def __init__(self,**kwargs):

        super().__init__(**kwargs)                                                                  #Partie graphique du login
        
        self.cols = 1
        self.rows = 10
        Window.size = (800, 600)
        
        image = Image(source='./images/caisse2.jpg',allow_stretch=True,keep_ratio=False)
        Window.add_widget(image)

        self.add_widget(Label(text="LOGIN", font_size='40sp', italic= True, bold=True,color=[170, 170, 0])) 
        self.add_widget(Label(text="Identifiant", font_size='20sp',size_hint=(.2, .2), markup=True,color=[0, 0, 0]))


        self.username = TextInput(multiline=False,write_tab=False, size_hint=(0.01, .2))
        self.username.focus=True
        self.username.pos = (10, 0)
        self.add_widget(self.username)

        self.add_widget(Label(text="Mot de passe",italic=True, font_size='20sp',size_hint=(.5, .2), markup=True ,color=[0, 0, 0]))
        self.password = TextInput(multiline=False,write_tab=False, password=True ,size_hint=(0.5, .2))
        self.add_widget(self.password)

        self.connect = Button(text ="Entrer", color=[0, 0, 0], size_hint=(.1,.2),bold=True, font_size='20sp')
        self.connect.bind(on_press=self.connect_btn)
        self.add_widget(self.connect)


    def on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 36:  
            self.connect_btn(instance)


    def connect_btn(self, instance):
        
        sql = "SELECT * FROM login WHERE username = '%s' AND password = '%s'" % (self.username.text,self.password.text) 
        mycursor.execute(sql)
        if mycursor.fetchone():                                                             #vérifier si le username et le mot de passe sont sont conformes à la base de données
            window_login.stop()
            window = DrawingWindow().run()                                      
                                                                                            
        else:
            print("Invalid Credentials")                                                    #Refuser l'accès à l'interface de l'IHM
            box = BoxLayout(orientation = 'vertical', padding = (10))                       #Afficher un message d'erreur invitant l'utilisateur à saisir une autre fois les informations
            box.add_widget(Label(text ='Identifiant et/ou mot de passe incorrecte(s)'))
            btn1 = Button(text = "Réesayer", size=(100,100))
            box.add_widget(btn1)
            popup = Popup(title='Erreur d identification', title_size= (30),title_align = 'center', content = box,size_hint=(None, None), size=(400, 400), auto_dismiss = True)
            btn1.bind(on_press = popup.dismiss)
            popup.open()


class Login(App):
    def build(self):
        self.title = 'E-CADDE Authentification'
        return LoginUI()

if __name__ == "__main__":
    window_login = Login()
    window_login.run()

conn.close()