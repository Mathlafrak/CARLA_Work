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
    recul = 10.0
    hauteur = 7.0

    vehicle_transform = vehicle.get_transform()
    vehicle_location = vehicle.get_location()
    forward_vector = vehicle_transform.get_forward_vector()
    up_vector = vehicle_transform.get_up_vector()
    
    spectator_location = vehicle_location - forward_vector*recul - up_vector*hauteur
    vehicle_rotation = vehicle.get_transform().rotation

    spectator_rotation = carla.Rotation(pitch = vehicle_rotation.pitch, yaw = vehicle_rotation.yaw, roll = vehicle_rotation.roll)
    new_transform = carla.Transform(spectator_location, spectator_rotation)
    spectator.set_transform(new_transform)


    # print(vehicle_matrix)

    # spectator_transform = vehicle_transform.transform(carla.Location(x= 0.0, y = 0.0, z = recul), vehicle_rotation)
    # spectator.set_transform(spectator_transform)

    # forward_vector = vehicle_transform.get_forward_vector()
    # print(forward_vector)
    
    # right_vector = vehicle_transform.get_right_vector()
    # # print(right_vector)
    # up_vector = vehicle_transform.get_up_vector()
    # # print(up_vector)
    # spectator_vector = carla.Vector3D(x = forward_vector.x -recul)
    # spectator_location = forward_vector.transform(spectator_vector)

    # print("Avant transform", vehicle_transform)
    # vehicle_transform.transform(spectator.get_location())
    # print(vehicle_transform)
    # print("Apres transform", vehicle_transform)
    # camera_transform = carla.Transform(vehicle_transform)
    #spectator_rotation = vehicle.get_transform().rotation
    # camera_local_location = carla.Location(x=-7.0,y=0.0,z=0.0)
    # camera_transform.set_location()
    # camera_transform.transform(camera_local_location)
    # spectator.set_transform(spectator_transform)

   # print(vehicle_transform.get_matrix())
    

    
     #This is still not a local referential fixed on on the vehicle, but a global referential
    # hauteur = 7.0
    # recul = -7.0
    
#     spectator_location = vehicle_location + carla.Vector3D(0,recul , hauteur)

#     vehicle_rotation = vehicle.get_transform().rotation
#     spectator_rotation = carla.Rotation(pitch = vehicle_rotation.pitch -45.0, yaw = vehicle_rotation.yaw, roll = vehicle_rotation.roll)
# #
#     new_transform = carla.Transform(spectator_location, spectator_rotation)

#     spectator.set_transform(new_transform)

    time.sleep(0.01)



  # vehicle.destroy()


if __name__ == '__main__':

  main()
