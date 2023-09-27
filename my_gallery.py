import random
import time
import carla


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

    vehicle_matrix = vehicle_transform.get_matrix()
    for lignes in vehicle_matrix:
      print(lignes, "\n")
    up_vector = vehicle_transform.get_up_vector()
    forward_vector = vehicle_transform.get_forward_vector()
    right_vector = vehicle_transform.get_right_vector()

    # print(vehicle_matrix)
    print("Forward vector", forward_vector, "\n", "Right vector", right_vector  , "\n","Up vector", up_vector)
    #Dans la matrice de rotation, la première colonne correspond au vecteur forward, la deuxième le vecteur right, et la troisème le vecteur up 

    spec_local_vec = carla.Vector3D(-10, 0, 5)
    spectator_location = vehicle_transform.transform(carla.Location(spec_local_vec))

    vehicle_rotation = vehicle.get_transform().rotation
    spectator_rotation = carla.Rotation(pitch = vehicle_rotation.pitch, yaw = vehicle_rotation.yaw, roll = vehicle_rotation.roll)

    new_transform = carla.Transform(spectator_location, spectator_rotation)
    spectator.set_transform(new_transform)

    time.sleep(0.01)



  # vehicle.destroy()


if __name__ == '__main__':

  main()
