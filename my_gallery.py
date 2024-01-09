import random
import time
import carla
import numpy as np 
import math
import pygame

# []
# class RenderObject(object):
#   def __init__(self, width, height):
#     init_image = np.random.randint(0, 255,(height, width, 3), dtype="uint8")
#     self.surface = pygame.surfarray.make_surface(init_image.swapaxes(0,1))
def callback(imu_data):
  acceleration = imu_data.accelerometer
  gyroscope = imu_data.gyroscope
  orientation = imu_data.compass

  print("Acceleration :", acceleration)
  print("Vitesse angulaire :", gyroscope)
  print("Orientation :", orientation)

# def pygame_callback(data, obj):
#   img = np.reshape(np.copy(data.raw_data), (data.height, data.width, 4))
#   img = img[:,:,:3]
#   img = img[:,:,::-1]
#   obj.surface = pygame.surfarray.make_surface(img.swapaxes(0,1)) 
def main():
 # First of all, we need to create the client that will send the requests
 # to the simulator. Here we'll assume the simulator is accepting
 # requests in the localhost at port 2000.
  client = carla.Client('localhost', 2000)
  client.set_timeout(10.0)
# Once we have a client we can retrieve the world that is currently
# running.
  world = client.load_world('Town04')
  # print(world.get_map().get_spawn_points())
  # a = [0,2,3]
  # print("Hello")
  # print(a)
#  env = client.get_world()
#  spectator = world.get_spectator()
  blueprint_library = world.get_blueprint_library()
  blueprint = blueprint_library.find('vehicle.carlamotors.carlacola')

  
#  location = carla.Location(0.0, 0.0, 0.0)
#  rotation = carla.Rotation(0.0, 0.0, 0.0)
  
  transform = random.choice(world.get_map().get_spawn_points())
  print(transform.location, transform.rotation)
  vehicle = world.spawn_actor(blueprint, transform)
  vehicle.set_autopilot(True)
  #sleep(3)

#  Sticking the spectator to the vehicle
  spectator = world.get_spectator()
  imu_sensor_blueprint = blueprint_library.find('sensor.other.imu')
  imu_sensor_transform = random.choice(world.get_map().get_spawn_points())
  imu_sensor = world.spawn_actor(imu_sensor_blueprint, imu_sensor_transform, attach_to=vehicle)

  # image_w = camera_blueprint.get_attribute('image_size_x')
  # image_h = camera_blueprint.get_attribute('image_size_y')
  # image_w.as_int()
  # image_h.as_int()

  # renderObject = RenderObject(image_w, image_h)


  # pygame.init()
  # gameDisplay = pygame.display.set_mode(((image_w, image_h), pygame.HWSURFACE | pygame.DOUBLEBUF))
  # gameDisplay = pygame.display.set_mode(((0, 0), pygame.HWSURFACE | pygame.DOUBLEBUF))
#spectator = world.spawn_actor(blueprint, transform, attach_to=my_vehicle)




  while True:
    # world.tick()
    # gameDisplay.blit(renderObject.surface, (0,0))
    # pygame.display.flip()
    
    recul = -10.0
    hauteur = -7.0

    vehicle_transform = vehicle.get_transform()
    vehicle_location = vehicle.get_location()
    vehicle_rotation = vehicle.get_transform().rotation

    imu_sensor_location = imu_sensor.get_location()
    imu_sensor_rotation = imu_sensor.get_transform().rotation
    spec_local_vec = carla.Vector3D(-10, 0, 5)
    imu_sensor_location = vehicle_transform.transform(carla.Location(spec_local_vec))

    imu_sensor.listen(lambda imu_data: callback(imu_data))
    # imu_sensor_rotation = carla.Rotation(pitch = vehicle_rotation.pitch, yaw = vehicle_rotation.yaw, roll = vehicle_rotation.roll)

    # new_transform = carla.Transform(imu_sensor_location, imu_sensor_rotation)
    # imu_sensor.set_transform(new_transform)
    # print("Vehicle location : ", vehicle_location, vehicle_rotation, "\n", "Camera location : ", imu_sensor_location, imu_sensor_rotation)


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
    rotation_matrix = matrice_yaw.dot(matrice_pitch.dot(matrice_roll))
    # rotation_matrix = matrice_roll @ (matrice_pitch @ matrice_yaw)

    # print("Matrice de rotation : ",rotation_matrix)


    # forward_velocity = forward_vector.get_velocity()
    # up_velocity = up_vector.get_velocity()
    # right_velocity = right_vector.get_velocity()
    velocity = vehicle.get_velocity()
    Vx = velocity.x
    Vy = velocity.y
    Vz = velocity.z
    #print("Vx = ",Vx, "Vy = ", Vy, "Vz = ", Vz)
    # print("Forward speed is : ", forward_velocity,"\n", "Up velocity is : ", up_velocity, "\n", "Right velocity is :", right_velocity)


    time.sleep(0.01)

    # camera = world.spawn_actor(camera_blueprint, camera_transform, attach_to=vehicle)

    # camera.listen(lambda image : rgb_callback(image, renderObject))

    # gameDisplay.fill((0,0,0))
    # gameDisplay.blit(renderObject.surface, (0,0))
    # pygame.display.flip()
  




  # vehicle.destroy()
# def rgb_callback(image, data_dict):
#   data_dict['rgb_image'] = np.reshape(np.copy(image.raw_data), (image.height, image.width, 4)) 

if __name__ == '__main__':

  main()
