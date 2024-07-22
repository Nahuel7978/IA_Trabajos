from controller import  Supervisor

class SupervisorClass():

    def __init__(self):
        self.supervisor = Supervisor()
        self.robot_node = Supervisor().getFromDef("principal_robot")
        if self.robot_node is None:
            print("Error: No se encontró el nodo del robot con el DEF especificado.")
        self.timestep = int(self.supervisor.getBasicTimeStep())
        self.translation_field = self.robot_node.getField("translation")