#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int16MultiArray

#check box state from etat_caisse topic 
#and assign 0 if the state is 0 in the array gathered from the topic
#class server structure

class server:
    def __init__(self):
        self.etats_caisses = [0,0,0]

    #def handler(self,data):
        #print(data.data)
        #self.etats_caisses = [etat for etat in data.data]


    def caisses(self):
        message.data=[0,0,0]
        try:
            appel = int(input("Numero de caisse: "))

            if appel == 1:
                #self.etats_caisses[0] = 1
                message.data[0] = 1
                print("Caisse numéro 1 appelle le e_caddie...")
            elif appel == 2:
                #self.etats_caisses[1] = 1
                message.data[1] = 1
                print("Caisse numéro 2 appelle le e_caddie...")
            elif appel == 3:
                #self.etats_caisses[2] = 1
                message.data[2] = 1
                print("Caisse numéro 3 appelle le e_caddie...")
            elif appel == 99:
                quit()
            else:
                print("Caisse {} n'existe pas!".format(appel))

        except Exception as e: 
            print("Ce n'est pas un numéro de caisse, réessayer")
            pass
        
        #message.data = [etat for etat in self.etats_caisses]

        
        pub.publish(message)
    
if __name__=="__main__":
    server=server()
    rospy.init_node('caisses',anonymous = True)
    pub = rospy.Publisher('appels_caisses', Int16MultiArray, queue_size=1)
    message = Int16MultiArray()
    
    while True:
        #rospy.Subscriber('etat_caisse', Int16MultiArray, server.handler)
        server.caisses()
        
    #rospy.spin()