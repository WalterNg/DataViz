import matplotlib

color_tableau = []
tab_colors = list(matplotlib.colors.TABLEAU_COLORS.keys())
for color in tab_colors:
    color_tableau.append(color[4:])

color_css = []
css_colors = list(matplotlib.colors.CSS4_COLORS.keys())
for color in css_colors:
    color_css.append(color)

color_list = color_tableau + color_css
