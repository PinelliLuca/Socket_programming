import socket
import sys
import os
import re

HOST = '127.0.0.1'
PORT = 8080

#processo di decadimento audioattivo di conway:Se si trovano n cifre adiacenti uguali ad x, al loro posto si sostituisce nx
def decadimento_audioattivo(seed,niterations):
    #inizializzo la stringa di partenza
    stringa=str(seed)
    for i in range(niterations):
        #inizializzo la stringa di output
        stringa_output=''
        #inizializzo la variabile che conta le occorrenze
        occorrenze=0
        #inizializzo la variabile che contiene il carattere da controllare
        carattere=stringa[0]
        for j in range(len(stringa)):
            #se il carattere è uguale al precedente, incremento il contatore delle occorrenze
            if(stringa[j]==carattere):
                occorrenze+=1
            #se il carattere è diverso dal precedente, scrivo il numero di occorrenze e il carattere
            else:
                stringa_output+=str(occorrenze)+carattere+'\r\n'
                #aggiorno il carattere
                carattere=stringa[j]
                #aggiorno il contatore delle occorrenze
                occorrenze=1
        #scrivo l'ultima occorrenza
        stringa_output+=str(occorrenze)+carattere
        #aggiorno la stringa di partenza
        stringa=stringa_output
    #stampo la stringa finale
    print(stringa_output)
    return stringa_output
   
        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        pid = os.fork()
        if pid == 0:  # This is the child process
            data = conn.recv(1024)
            print('Here is the message: %s'% data.decode('utf-8'))
            if(not data):
                print('errore parametri')
                break
            elif not re.match(r'^\d+,\d+$',data.decode('utf-8')):
                print('errore parametri')
                break
            else:
                data=data.decode('utf-8').split(',')
                seed=int(data[0])
                niterations=int(data[1])
                decadimento_audioattivo(seed,niterations)

            conn.close()
            os._exit(0)  # Child process ends here
        else:  # This is the parent process
            conn.close()