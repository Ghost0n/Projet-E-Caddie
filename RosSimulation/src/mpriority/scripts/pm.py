#!/usr/bin/env python3
import time
import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Int16MultiArray
from math import dist
from operator import attrgetter


class caddie:
    def __init__(self):
        self.pos = [0.0,0.0]
        self.dest = [0.0,0.0]

class caisse:
    def __init__(self,ID,pos):
        self.ID = ID
        self.pos = pos
        self.wait = 0.0
        #1 si la caisse attend le caddie 0 sinon
        self.state = 0
        self.start_time = 0.0
        

    def start_timer(self):
        self.start_time = time.time()
    
    # refresh wait time caisse
    def get_timer(self):
        self.wait = self.start_time - time.time()
        return self.wait

e_caddie = caddie()
c1 = caisse(1,[1.0,0.0])
c2 = caisse(2,[2.0,0.0])
c3 = caisse(3,[3.0,0.0])
caisses = [c1,c2,c3]
#file de caisses en attente organisé par ordre chnronologique d'appels
destinations = []
#temps d'attente maximum à partir de son appel à l'e_caddie avant de le forcer à y visiter
max_delay =  120

#calcul de distance euclidienne entre deux points
def distance (pos1,pos2):
    return dist(pos1,pos2)

# Renvoyer 0 s'il n'y a pas une caisse qui dépasse le temps maximal d'attente
# si non renvoyer le numéro de caisse avec le temps d'attente maximal  
def max_wait_caisse():
    if (max([caisse.get_timer(c) for c in destinations]) < max_delay):
        return 0
    else:
        c = destinations,attrgetter('wait')
        return c.ID

class server:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def publish(self,msg):
        self.x = msg.pos[0]
        self.y = msg.pos[1]
        dest.data = [self.x,self.y]
        print("Envoie des coordonées de la caisse numéro {} : X:{:0.2f} Y:{:0.2f}".format(msg.ID,self.x,self.y))
        pub1.publish(dest)


    def publish_states(self):
        states.data = [x.state for x in caisses]
        pub2.publish(states)

    # refresh e_caddie_pos
    def update_caddie(self,data):
        e_caddie.pos[0] = data.data[0]
        e_caddie.pos[1] = data.data[1]
        #print("caddy coordinate: ",e_caddie.pos)

    # refresh destinations
    def update_caisses(self,data):
        tmp = destinations
        #print("old destinations: ",[x.ID for x in tmp])
        for i in range(len(data.data)):
            if (data.data[i] == 1) & (i+1 not in [x.ID for x in destinations]):
                destinations.append(caisses[i])
                caisses[i-1].state = 1
        #print("new destinations: ",[x.ID for x in destinations])
        main()


def main(): 
    while len(destinations):
        t = 1  #variable booléenne pour indiquer si la caisse en destination est desservie ou pas encore
        try:
            for i in range(1,len(destinations)):
                #test de distance: si une caisse qui a appelle le e_caddie est sur son chemin il peut la visiter avant  
                test_distance = int((distance(destinations[i].pos,e_caddie.pos)) < distance(destinations[0].pos,e_caddie.pos)) & int(distance(destinations[i].pos,destinations[0].pos) < distance(destinations[0].pos,e_caddie.pos))
                test_max_wait = max_wait_caisse()
                if  test_distance & (test_max_wait == 0) :
                    
                    print("Alerte d'optimisation: destination plus proche trouvée!")
                    print("Caisse numéro {} reportéé ".format(destinations[0].ID))
                    server.publish(destinations[i])
                    caisses[i].state = 0
                    server.publish_states()
                    while t:
                        if distance(e_caddie.pos,destinations[i].pos) == 0.0:
                            destinations.pop(i)
                            # refresh state caisse
                            t = 0
                    break
                elif test_max_wait:
                    #e_caddie.pos = destinations[test_max_wait]   #publish the destination
                    print("Alerte: temps d'attente maximal écoulé !")
                    server.publish(destinations[test_max_wait])
                    caisses[test_max_wait].state = 0
                    server.publish_states()
                    while t:
                        if distance(e_caddie.pos,destinations[test_max_wait].pos) == 0.0:
                            destinations.pop(test_max_wait)
                            t = 0
                    
                    break    
        except Exception as e:
            print(e)
  

        #après avoir desservie ou pas des caisses qui attendent depuis longtemps ou des caisses sur notre chemin en procède à traiter
        # la première caisse en ordre chronologique 
        #e_caddie.pos = destinations[0]    #publish destination
        server.publish(destinations[0])
        caisses[0].state = 0
        server.publish_states()
        while t:
            if distance(e_caddie.pos,destinations[0].pos) == 0.0:
                destinations.pop(0)
                t = 0
        

if __name__ == "__main__":
    server = server()

    rospy.init_node('mpriority',anonymous = True)
    
    pub1 = rospy.Publisher('destination_caddie',Float32MultiArray, queue_size= 1)

    pub2 = rospy.Publisher('etat_caisse',Int16MultiArray, queue_size= 1)
    
    rospy.Subscriber('appels_caisses',Int16MultiArray,server.update_caisses)
    
    rospy.Subscriber('pos_caddie',Float32MultiArray,server.update_caddie)
    
    dest = Float32MultiArray()
    
    states = Int16MultiArray()

    rospy.spin()

