import sc2
from sc2 import run_game, maps, Race, Difficulty 
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, \
 CYBERNETICSCORE, STALKER, STARGATE, VOIDRAY
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
    await self.distribute_workers()
    await self.build_workers()
    await self.build_pylons()
    await self.build_assimilators()
    await self.expand()
    await self.offensive_force_buildings()
    await self.build_offensive_force()
    await self.intel()
    await self.attack()

  async def intel(self):
    game_data = np.zeros((self.game_info.map_size[1], self.game_info.map_size[0], 3), np.uint8)
    draw_dict = {       #size #color #draw from largest to smallest good idea
      NEXUS:            [15, (  0, 255, 0),  1],
      STARGATE:         [ 5, (255,   0, 0), -1],
      PYLON:            [ 3, ( 20, 235, 0), -1],
      GATEWAY:          [ 3, (200, 100, 0), -1],
      CYBERNETICSCORE:  [ 3, (150, 150, 0), -1],
      VOIDRAY:          [ 3, (255, 100, 0), -1],
      ASSIMILATOR:      [ 2, ( 55, 200, 0), -1],
      PROBE:            [ 1, ( 55, 200, 0), -1],
    }

    for unit_type in draw_dict:
      for unit in self.units(unit_type).ready:
        pos = unit.position 
        u = draw_dict[unit_type]
        cv2.circle(game_data, (int(pos[0]), int(pos[1])), u[0], u[1], u[2]) #-1 for solid fill, no stroke

    # for nexus in self.units(NEXUS):
    #   nex_pos = nexus.position
    #   cv2.circle(game_data, (int(nex_pos[0]), int(nex_pos[1])), 10, (0, 255, 0), -1) #data, coord coord, px_size, color, line_width(-1 for no stroke)

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

      isStargateUndercap = len(self.units(STARGATE)) < self.time
      isStargateAffordable = self.can_afford(STARGATE) 
      isStargateNotPending = not self.already_pending(STARGATE)
      isStargateReady = isStargateUndercap and isStargateAffordable and isStargateNotPending
      isCyberReady = self.units(CYBERNETICSCORE).ready.exists
      if isCyberReady and isStargateReady:
        await self.build(STARGATE, near=pylon)

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