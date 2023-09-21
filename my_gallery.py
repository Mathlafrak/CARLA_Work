import random
import time
import carla


def main():
 # First of all, we need to create the client that will send the requests
 # to the simulator. Here we'll assume the simulator is accepting
 # requests in the localhost at port 2000.
  client = carla.Client('localhost', 2000)
  client.set_timeout(2.0)
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
#Ne fonctionne pas car spectator est un actor spécifique (pas de blueprint)


  while True:

    vehicle_location = vehicle.get_location()
    hauteur = 10.0
    spectator_location = vehicle_location + carla.Vector3D(0, 0, hauteur)

    vehicle_rotation = vehicle.get_transform().rotation
    spectator_rotation = carla.Rotation(pitch = vehicle_rotation.pitch -90.0, yaw = vehicle_rotation.yaw, roll = vehicle_rotation.roll)

    new_transform = carla.Transform(spectator_location, spectator_rotation)

    spectator.set_transform(new_transform)

    time.sleep(0.01)



  # vehicle.destroy()


if __name__ == '__main__':

  main()
