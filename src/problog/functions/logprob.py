from dotenv import load_dotenv

load_dotenv()

custom_colors = ['#FF7074', '#FFA756', '#7ad151', '#43bf71',
    '#22a884', '#21908c', '#2a788e', '#345f8d',
    '#414487', '#482575', '#440154']

def get_colors():
    return custom_colors

colors = get_colors()

# Output of Colors:
# ['#FF7074', '#FFA756', '#7ad151', '#43bf71',
#     '#22a884', '#21908c', '#2a788e', '#345f8d',
#     '#414487', '#482575', '#440154']
