import numpy as np

def _check_input(initial_state_probability, transition_matrix, emission_matrix, num_states, num_observations): #provjera parametra
    if len(initial_state_probability) != num_states:
        print("Error: Number of States does not match provided Initial State Probabilities")
        return False 

    if len(transition_matrix) != num_states:
        print("Error: Number of States does not match provided Transition Matrix")
        return False

    for i in range(len(transition_matrix)):
        if len(transition_matrix[i]) != num_states:
            print("Error: Number of States does not match provided Transition Matrix Row: " + str(i))
            return False

    if len(emission_matrix) != num_states:
        print("Error: Number of States does not match provided Emission Matrix")
        return False

    for i in range(len(emission_matrix)):
        if len(emission_matrix[i]) != num_observations:
            print("Error: Observation Space does not match provided Emission Matrix Row: " + str(i))
            return False
    return True

def generate_observations(initial_state_probability, transition_matrix, emission_matrix, num_samples=300, state_space=None, observation_space=None, seed=None):
   
    if state_space == None:
        state_space = [i for i in range(len(initial_state_probability))]

    if observation_space == None:
        observation_space = [i for i in range(len(emission_matrix[0]))]

    num_states = len(state_space)
    num_observations = len(observation_space)

    if not _check_input(initial_state_probability, transition_matrix, emission_matrix, num_states, num_observations):
        return None, None

    # Set Seed if one exists
    np.random.seed(seed)

    # Setup Index Lookup for States
    state_to_index = dict()
    for i in range(len(state_space)):
        state_to_index[state_space[i]] = i
    
    # Setup Index Lookup for Observations
    obs_to_index = dict()
    for i in range(len(observation_space)):
        obs_to_index[observation_space[i]] = i

    # Find Initial State
    state = np.random.choice(state_space, 1, p=initial_state_probability)[0]
    observation = np.random.choice(observation_space, 1, p=emission_matrix[state_to_index[state]])[0]

    # Initialize Returns
    states_return = [state]
    obs_return = [observation]

    # Generate the Observations
    for _ in range(num_samples-1):
        state = np.random.choice(state_space, 1, p=transition_matrix[state_to_index[state]])[0]
        observation = np.random.choice(observation_space, 1, p=emission_matrix[state_to_index[state]])[0]

        states_return.append(state)
        obs_return.append(observation)

    return states_return, obs_return

def print_result(observed, actual, max_length=100):

    # Chop it into chunks
    obs_chunks = [observed[i:i+max_length] for i in range (0, len(observed), max_length)]
    act_chunks = [actual[i:i+max_length] for i in range (0, len(actual), max_length)]

    # Print out the chunks of max_length
    for i in range(1):
        print(f'{"Rolls":8}: {obs_chunks[i]}')
        print(f'{"Actual":8}: {act_chunks[i]}')
        print("")

