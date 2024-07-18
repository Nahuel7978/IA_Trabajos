
from pyswip import Prolog

class Meetings():
    def __init__(self,profesor,day,hour,minutes) -> None:
        self.profesor=profesor
        self.day=day
        self.hour=hour
        if(minutes==None):
            self.minutes=0
        else:
            self.minutes=minutes

    def run(self):
        if(self.day==None):
            print("Que dia te parece")
        else:
            prolog = Prolog()
            prolog.consult("reglas_nahuel.pl")
            
            if(self.profesor):
                consult = next(prolog.query("horario_ocupado_profesor("+str(self.day)+", X)"))
            else:
                consult= next(prolog.query("horario_ocupado_alumno("+str(self.day)+", X)"))
            print(consult)
            consult_reuniones = next(prolog.query("reunion("+str(self.day)+", X)"))
            reuniones_previas = list(consult_reuniones["X"])
            result=list(consult["X"])
            print(result)
            print(reuniones_previas)
            if(self.hour ==None):
                self.offer_schedules(result)
            else:
                self.confirm_meet(result,self.hour,self.minutes)

    def confirm_meet(self,Lista_horarios,hour,minutes):
        if(minutes==None):
            minutes=0;
        i=0
        reunion = True
        while((i<len(Lista_horarios))):
            sub_lista = Lista_horarios[i]
            print(sub_lista)
            if((hour>=int(sub_lista[0]))&(hour<=int(sub_lista[1]))):
                reunion=False
            else:
                if((hour==int(sub_lista[0])-1)&(minutes>40)):
                    reunion=False
            i+=1            

        if(reunion):
            print("Buenisimo, nos vemos ahi entonces.")
            #Aquí hacer un assert de reunion(llamar otro metodo)
        else:
            print("uy, justo ese horario se me complica")
            self.offer_schedules(Lista_horarios)


    def offer_schedules(self,Lista_horarios):
        print("OFFER_SCHEDULES")
        #Ofrecer la hora más cerca de la solicitada
        #Si es la hora es NONE, mostrar la primer desocupada
        #Si no es NONE, ofrecer una hora y CAMBIAR el Slot
        ###Qué pasa con los slots cuando uso el checkpoint o cambio de store??




reunion = Meetings(True,'martes',18,0)
reunion.run()

