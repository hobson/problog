import tastymap as tm
from dotenv import load_dotenv

load_dotenv()
COLORMAP = "viridis_r"
NUM_COLORS = 11 


def get_colors():
    tmap = tm.cook_tmap(COLORMAP, reverse=False, num_colors=NUM_COLORS, name='Token probability', value=1)
    colors = tmap.to_model("hex")
    return colors

# Output of Colors: 
# ['#fde725','#bcdf27','#7ad151','#43bf71',
# '#22a884','#21908c','#2a788e','#345f8d',
# '#414487','#482575','#440154']