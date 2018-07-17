import sc2
from sc2 import run_game, maps, Race, Difficulty, position, Result
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, \
 CYBERNETICSCORE, STALKER, STARGATE, VOIDRAY, ROBOTICSFACILITY, OBSERVER
import random
import cv2
import numpy as np
import time
import keras

HEADLESS = False #when true, will not render visualisation window

# os.environ["SC2PATH"] = 'C:/starcraft/path/goes/here'
# ~165 iterations per minute #self.f = open("gamedata.txt", "w+")
class DabsonBot(sc2.BotAI):
  def __init__(self, use_model=False):
    self.ITERATIONS_PER_MINUTE = 165
    self.MAX_WORKERS = 64
    self.RECOMENDED_WORKERS_PER_NEXUS = 16
    self.decimalTime = 0 #in decimal minutes (e 1.5 = 1minute 30seconds)
    self.do_something_after = 0
    self.train_data = []
    self.use_model = use_model
    if self.use_model:
      print("using model")
      self.model = keras.models.load_model("trained_model/BasicCNN-30-epochs-0.0001-LR-4.2")

  def on_end(self, game_result):
    print('--- on_end() called ---')
    print(game_result)

    if game_result == Result.Victory:
      np.save("train_data/{}.npy".format(str(int(time.time()))), np.array(self.train_data))

  async def on_step(self, iteration):
    self.iteration = iteration
    self.decimalTime = self.iteration / self.ITERATIONS_PER_MINUTE
    await self.scout()
    await self.distribute_workers()
    await self.build_workers()
    await self.build_pylons()
    await self.build_assimilators()
    await self.expand()
    await self.offensive_force_buildings()
    await self.build_offensive_force()
    await self.intel()
    await self.attack()

  async def scout(self):
    if len(self.units(OBSERVER)) > 0:
      scout = self.units(OBSERVER)[0]
      if scout.is_idle:
        enemy_location = self.enemy_start_locations[0]
        move_to = self.random_location_variance(enemy_location)
        print(move_to)
        await self.do(scout.move(move_to))
    else:
      for rf in self.units(ROBOTICSFACILITY).ready.noqueue: 
        if self.can_afford(OBSERVER) and self.supply_left > 0:
          await self.do(rf.train(OBSERVER))    

  def random_location_variance(self, enemy_start_location):
    x = enemy_start_location[0] * self.randDelta(.2) #this doesnt make sense, variance should not change based on random start location
    y = enemy_start_location[1] * self.randDelta(.2)
    x = self.bound(x, 0, self.game_info.map_size[0])
    y = self.bound(y, 0, self.game_info.map_size[1])
    go_to = position.Point2(position.Pointlike((x,y)))
    return go_to

  def randDelta(self, magnitude): #pop pop 
    return 1 + random.uniform(-magnitude, magnitude)

  def bound(self, val, minVal, maxVal ):
    if val < minVal:
      return minVal
    if val > maxVal:
      return maxVal
    return val

  async def intel(self):
    game_data = np.zeros((self.game_info.map_size[1], self.game_info.map_size[0], 3), np.uint8)
    draw_dict = {       #size #color #strokeFill #draw from largest to smallest good idea
      NEXUS:            [15, (  0, 255,   0),  1],
      STARGATE:         [ 5, (255,   0,   0), -1],
      PYLON:            [ 3, ( 20, 235,   0), -1],
      GATEWAY:          [ 3, (200, 100,   0), -1],
      CYBERNETICSCORE:  [ 3, (150, 150,   0), -1],
      VOIDRAY:          [ 3, (255, 100,   0), -1],
      OBSERVER:         [ 3, (255, 255, 255), -1],
      ASSIMILATOR:      [ 2, ( 55, 200,   0), -1],
      PROBE:            [ 1, ( 55, 200,   0), -1],
    }

    for unit_type in draw_dict:
      for unit in self.units(unit_type).ready:
        pos = unit.position 
        u = draw_dict[unit_type]
        cv2.circle(game_data, (int(pos[0]), int(pos[1])), u[0], u[1], u[2]) #-1 for solid fill, no stroke

    main_base_names = ["nexus", "commandcenter", "hatchery"]
    for enemy_building in self.known_enemy_structures:
      pos = enemy_building.position
      if enemy_building.name.lower() not in main_base_names:
        cv2.circle(game_data, (int(pos[0]), int(pos[1])), 15, (0, 0, 255), -1)

    for enemy_unit in self.known_enemy_units:
      if not enemy_unit.is_structure:
        worker_names = ["probe", "scv", "drone"]

        #if that unit is a worker 
        pos = enemy_unit.position 
        if enemy_unit.name.lower() in worker_names: 
          cv2.circle(game_data, (int(pos[0]), int(pos[1])), 1, (55, 0, 155), -1)
        else: 
          cv2.circle(game_data, (int(pos[0]), int(pos[1])), 3, (50, 0, 215), -1)

    for obs in self.units(OBSERVER).ready:
      pos = obs.position 
      cv2.circle(game_data, (int(pos[0]), int(pos[1])), 1, (255, 255, 255), -1)

    line_max = 50
    mineral_ratio = self.minerals / 1500
    if mineral_ratio > 1.0:
      mineral_ratio = 1.0

    vespene_ratio = self.vespene / 1500 
    if vespene_ratio > 1.0:
      vespene_ratio = 1.0 

    population_ratio = self.supply_left / self.supply_cap 
    if population_ratio > 1.0:
      population_ratio = 1.0 

    plausible_supply = self.supply_cap / 200.0
    military_weight = len(self.units(VOIDRAY)) / (self.supply_cap - self.supply_left)
    if military_weight > 1.0:
      military_weight = 1.0

    #draw each line as a sideways column graph
    cv2.line(game_data, (0, 19), (int(line_max * military_weight) , 19), (250, 250, 200), 3) # worker/supply ratio
    cv2.line(game_data, (0, 15), (int(line_max * plausible_supply), 15), (220, 200, 200), 3) # plausible supply (supply/200)
    cv2.line(game_data, (0, 11), (int(line_max * population_ratio), 11), (150, 150, 150), 3) # population ratio (supply_left/supply)
    cv2.line(game_data, (0,  7), (int(line_max * vespene_ratio)   ,  7), (210, 200,   0), 3) # gas /1500
    cv2.line(game_data, (0,  3), (int(line_max * mineral_ratio)   ,  3), (  0, 255,  25), 3) # minerals minerals/1500

    # flip horizontally to make our final fix in numpyMatrix -> visual represent
    self.flipped = cv2.flip(game_data, 0)

    if not HEADLESS:
      resized = cv2.resize(self.flipped, dsize=None, fx=2, fy=2)
      cv2.imshow('Intel', resized)
      cv2.waitKey(1)

  async def build_workers(self):
    workerCount = len(self.units(PROBE)) 
    nexusCount = len(self.units(NEXUS))
    harvestCapacity = nexusCount * self.RECOMENDED_WORKERS_PER_NEXUS 

    if workerCount < harvestCapacity and workerCount < self.MAX_WORKERS:
      for nexus in self.units(NEXUS).ready.noqueue:
        if self.can_afford(PROBE):
          await self.do(nexus.train(PROBE))

  async def build_pylons(self):
    if self.supply_left < 5 and not self.already_pending(PYLON):
      nexuses = self.units(NEXUS).ready
      if nexuses.exists:
        if self.can_afford(PYLON):
          await self.build(PYLON, near=nexuses.first)

  async def build_assimilators(self):
    for nexus in self.units(NEXUS).ready:
      vespenes = self.state.vespene_geyser.closer_than(15.0, nexus)
      for vespene in vespenes:
        if not self.can_afford(ASSIMILATOR):
          break
        worker = self.select_build_worker(vespene.position) #grab the closest worker to the position 
        if worker is None:
          break
        if not self.units(ASSIMILATOR).closer_than(1.0, vespene).exists: #if no assimilator exists, make one 
          await self.do( worker.build(ASSIMILATOR, vespene) )

  async def expand(self):
    if self.units(NEXUS).amount < self.decimalTime and self.can_afford(NEXUS):
      await self.expand_now()

  async def offensive_force_buildings(self):
    #print(self.decimalTime) #test the time
    if self.units(PYLON).ready.exists:
      pylon = self.units(PYLON).ready.random

      if self.units(GATEWAY).ready.exists and not self.units(CYBERNETICSCORE):
        if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
          await self.build(CYBERNETICSCORE, near=pylon)

      elif len(self.units(GATEWAY)) < 1:
        if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
          await self.build(GATEWAY, near=pylon)
      
      if self.isReadyForRoboticsFacility():
        await self.build(ROBOTICSFACILITY, near=pylon)

      if self.isReadyForStargate():
        await self.build(STARGATE, near=pylon)

  def isCyberReady(self):
    return self.units(CYBERNETICSCORE).ready.exists

  def isReadyForRoboticsFacility(self):
    noRFyet = len(self.units(ROBOTICSFACILITY)) < 1
    isRFAffordable = self.can_afford(ROBOTICSFACILITY)
    isRFNotPending = not self.already_pending(ROBOTICSFACILITY)
    return self.isCyberReady() and noRFyet and isRFAffordable and isRFNotPending

  def isReadyForStargate(self):
    isStargateUndercap = len(self.units(STARGATE)) < self.decimalTime
    isStargateAffordable = self.can_afford(STARGATE) 
    isStargateNotPending = not self.already_pending(STARGATE)
    return self.isCyberReady() and isStargateUndercap and isStargateAffordable and isStargateNotPending

  async def build_offensive_force(self):
    for sg in self.units(STARGATE).ready.noqueue:
      if self.can_afford(VOIDRAY) and self.supply_left > 0:
        await self.do(sg.train(VOIDRAY))

  def find_target(self, state):
    if len(self.known_enemy_units) > 0:
      return random.choice(self.known_enemy_units)
    elif len(self.known_enemy_structures) > 0:
      return random.choice(self.known_enemy_structures)
    else:
      return self.enemy_start_locations[0]

  async def attack(self):
    if len(self.units(VOIDRAY).idle) > 0:
      target = False 
      if self.iteration > self.do_something_after:

        if self.use_model: #use model, pass in a list of things to be predicted
          prediction = self.model.predict([self.flipped.reshape([-1,176,200,3])])
          choice = np.argmax(prediction[0])
          choice_dict = {0: "No Attack!",
                         1: "Attack close to our nexus!",
                         2: "Attack Enemy Structure!",
                         3: "Attack Eneemy Start!"}
          print("Choice #{}:{}".format(choice, choice_dict[choice]))
        else:
          choice = random.randrange(0,4)

        if choice == 0: # no attack 
          wait = random.randrange(20, 165)
          self.do_something_after = self.iteration + wait 

        elif choice == 1: # attack_unit_closest_nexus 
          if len(self.known_enemy_units) > 0:
            target = self.known_enemy_units.closest_to(random.choice(self.units(NEXUS)))

        elif choice == 3: # attack enemy structures
          if len(self.known_enemy_structures) > 0:
            target = random.choice(self.known_enemy_structures)

        if target:
          for vr in self.units(VOIDRAY).idle:
            await self.do(vr.attack(target))

        y = np.zeros(4)
        y[choice] = 1
        #print(y)
        self.train_data.append([y,self.flipped])

      print(len(self.train_data))

run_game(
  maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, DabsonBot(use_model=True)),
    Computer(Race.Terran, Difficulty.Medium)
  ], realtime=False)