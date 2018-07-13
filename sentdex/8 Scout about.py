import sc2
from sc2 import run_game, maps, Race, Difficulty, position
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, \
 CYBERNETICSCORE, STALKER, STARGATE, VOIDRAY, ROBOTICSFACILITY, OBSERVER
import random
import cv2
import numpy as np

# ~165 iterations per minute 
class DabsonBot(sc2.BotAI):
  def __init__(self):
    self.ITERATIONS_PER_MINUTE = 165
    self.MAX_WORKERS = 64
    self.RECOMENDED_WORKERS_PER_NEXUS = 16
    self.iteration = 0
    self.time = 0 #in decimal minutes (e 1.5 = 1minute 30seconds)
    #self.f = open("gamedata.txt", "w+")

  async def on_step(self, iteration):
    self.iteration = iteration
    self.time = self.iteration / self.ITERATIONS_PER_MINUTE
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
    x = enemy_start_location[0] * self.randDelta(.2)
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

    main_base_names = ["nexus", "supplydepot", "hatchery"]
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

    # flip horizontally to make our final fix in numpyMatrix -> visual represent
    flipped = cv2.flip(game_data, 0)
    resized = cv2.resize(flipped, dsize=None, fx=2, fy=2)
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
    if self.units(NEXUS).amount < 3 and self.can_afford(NEXUS):
      await self.expand_now()

  async def offensive_force_buildings(self):
    #print(self.time) #test the time
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
    isStargateUndercap = len(self.units(STARGATE)) < self.time
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
    # {UNIT: [n to fight, n to defend]}
    aggressive_units = {VOIDRAY: [8, 3]}

    for UNIT in aggressive_units:
      unitCount = self.units(UNIT).amount
      offenceCount = aggressive_units[UNIT][0]
      defenceCount = aggressive_units[UNIT][1]
      idleUnits = self.units(UNIT).idle

      if unitCount > offenceCount and unitCount > defenceCount:
        for s in idleUnits:
          await self.do(s.attack(self.find_target(self.state)))
      elif unitCount > defenceCount and len(self.known_enemy_units) > 0: 
        for s in idleUnits:
          await self.do(s.attack(random.choice(self.known_enemy_units))) 


run_game(
  maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, DabsonBot()),
    Computer(Race.Terran, Difficulty.Hard)
  ], realtime=False)