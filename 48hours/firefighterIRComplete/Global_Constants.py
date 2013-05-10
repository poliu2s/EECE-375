# Wait for user to input which candles we're attacking.
CANDLES_TO_ATTACK = 0 # 0 for black, 1 for white
NUMBER_OF_WHITE_CANDLES = 4 # These should be 4 and 4. 
NUMBER_OF_BLACK_CANDLES = 5
IMAGE_BASENAME = "picture"
IMAGE_EXT = ".jpg"

n_global = 144
m_global = 144
dx_global = [1, 1, 0, -1, -1, -1, 0, 1]
dy_global = [0, 1, 1, 1, 0, -1, -1, -1]
dirs_global = 8
map_global = []
step_global = 30.48 / (n_global/12) # (30.48cm/ft) / (nodes/ft) = cm/node