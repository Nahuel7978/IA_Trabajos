"""my_controller_rosbot controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, Receiver
from QLearning.HROSbot import * 

# create the Robot instance.
robot = Robot()
# get the time step of the current world. 
timestep = int(robot.getBasicTimeStep())
receiver = robot.getDevice('Receiver')
receiver.enable(32)

rosbot = HROSbot(robot)


"""
rosbot.giroDerecha()
rosbot.avanzar(1,5.0)
rosbot.avanzar(1,5.0)
rosbot.avanzar(1,5.0)
rosbot.avanzar(1,5.0)
rosbot.avanzar(1,5.0)
rosbot.giroIzquierda()
rosbot.avanzar(1,5.0)

"""



# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    if receiver.getQueueLength() > 0:
        message = receiver.getString()
        # Procesar la señal para determinar la dirección
        print(f"Received signal: {message}")
        print("Fuerza: ",receiver.getSignalStrength())
        print("Direccion: ", receiver.getEmitterDirection())
        
        receiver.nextPacket()
    else:
        print("NAti")
    
    rosbot.avanzar(1,5.0)
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
  #  pass

# Enter here exit cleanup code.
