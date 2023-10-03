import random
import time
import carla
import numpy as np 
import math


def main():
 # First of all, we need to create the client that will send the requests
 # to the simulator. Here we'll assume the simulator is accepting
 # requests in the localhost at port 2000.
  client = carla.Client('localhost', 2000)
  client.set_timeout(5.0)
# Once we have a client we can retrieve the world that is currently
# running.
  world = client.load_world('Town04')
#  env = client.get_world()
#  spectator = world.get_spectator()
  blueprint_library = world.get_blueprint_library()
  blueprint = blueprint_library.find('vehicle.carlamotors.carlacola')
  
#  location = carla.Location(0.0, 0.0, 0.0)
#  rotation = carla.Rotation(0.0, 0.0, 0.0)
  
  transform = random.choice(world.get_map().get_spawn_points())

  vehicle = world.spawn_actor(blueprint, transform)
  vehicle.set_autopilot(True)
  #sleep(3)

#  Sticking the spectator to the vehicle
  spectator = world.get_spectator()


#spectator = world.spawn_actor(blueprint, transform, attach_to=my_vehicle)




  while True:
    recul = -10.0
    hauteur = -7.0

    vehicle_transform = vehicle.get_transform()
    vehicle_location = vehicle.get_location()

    spec_local_vec = carla.Vector3D(-10, 0, 5)
    spectator_location = vehicle_transform.transform(carla.Location(spec_local_vec))

    vehicle_rotation = vehicle.get_transform().rotation
    spectator_rotation = carla.Rotation(pitch = vehicle_rotation.pitch, yaw = vehicle_rotation.yaw, roll = vehicle_rotation.roll)

    new_transform = carla.Transform(spectator_location, spectator_rotation)
    spectator.set_transform(new_transform)


    vehicle_matrix = vehicle_transform.get_matrix()
    # for lignes in vehicle_matrix:
    #   print(lignes, "\n")
    up_vector = vehicle_transform.get_up_vector()
    forward_vector = vehicle_transform.get_forward_vector()
    right_vector = vehicle_transform.get_right_vector()

    # print(vehicle_matrix)
    # print("Forward vector", forward_vector, "\n", "Right vector", right_vector  , "\n","Up vector", up_vector)
    pitch = -math.radians(vehicle_rotation.pitch)
    roll = -math.radians(vehicle_rotation.roll)
    yaw = math.radians(vehicle_rotation.yaw)  

    matrice_roll = np.array([[1, 0, 0],[0, math.cos(roll), -math.sin(roll)],[0, math.sin(roll), math.cos(roll)]])
    matrice_pitch = np.array([[math.cos(pitch), 0, math.sin(pitch)],[0, 1, 0],[-math.sin(pitch), 0, math.cos(pitch)]])
    matrice_yaw = np.array([[math.cos(yaw), -math.sin(yaw), 0],[math.sin(yaw), math.cos(yaw), 0],[0, 0, 1]])

    # rotation_matrix = np.dot(matrice_yaw,np.dot(matrice_pitch, matrice_roll))
    rotation_matrix = matrice_yaw @ (matrice_pitch @ matrice_roll)
    # rotation_matrix = matrice_roll @ (matrice_pitch @ matrice_yaw)

    # print("Matrice de rotation : ",rotation_matrix)


    # forward_velocity = forward_vector.get_velocity()
    # up_velocity = up_vector.get_velocity()
    # right_velocity = right_vector.get_velocity()
    velocity = vehicle.get_velocity()
    Vx = velocity.x
    Vy = velocity.y
    Vz = velocity.z
    print("Vx = ",Vx, "Vy = ", Vy, "Vz = ", Vz)
    # print("Forward speed is : ", forward_velocity,"\n", "Up velocity is : ", up_velocity, "\n", "Right velocity is :", right_velocity)


    time.sleep(0.01)



  # vehicle.destroy()


if __name__ == '__main__':

  main()
