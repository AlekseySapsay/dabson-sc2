import World 

def main():
  while True:
    #Pick the right action
    agent = World.player
    max_act, max_val = max_Q(agent)
    (agent, a, r, agent_updated) = do_action(max_act)

    #Update Q
    max_act, max_val = max_Q(agent_updated)

    #Start game
    World.start_game()
    print 'Success! Score: ', max_val