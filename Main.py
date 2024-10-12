from Statistics import *
from Solution_Visu import *
plot_MainG()

plot_odd_G()
plot_min_weight_K()
plot_min_weight()

# Call the function to save stats to a text file
save_stats_to_file("stats.txt")
Retracing_Gcpp()
Sequence_Gcpp()
Generating_Frames()
Animating_Gcpp(png_directory, gif_directory + 'cpp_route_animation.gif', fps=3)
