import matplotlib.pyplot as plt
from IPython import display
from constantes import *

plt.ion()
plt.figure(figsize=(5, 4))
font_size = 7

def displayScores(scores, moyenne, record, glissante=0):
    plt.clf()
    plt.title(f'Entrainement : gamma:{GAMMA_DISCOUNT_RATE}, lr:{VITESSE_APPRENTISSAGE}, hidden:{HIDDEN_SIZE}, epsilon:{EPSILON_NB_GAMES}', fontsize=font_size)
    plt.xlabel('Nombre d\'essais', fontsize=font_size)
    plt.ylabel('Score', fontsize=font_size)
    plt.plot(scores, color="green", linewidth=1)
    plt.plot(moyenne, color="blue", linewidth=1)
    plt.axhline(y=record, color="red", linestyle="--", linewidth=0.5)
    plt.text(len(scores)-1, record, str(record), fontsize=font_size)

    plt.legend(["Scores", f"Moyenne glissante ({glissante})", "Record"], loc='upper left', fontsize=font_size)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]), fontsize=font_size)
    plt.text(len(moyenne)-1, moyenne[-1], str(round(moyenne[-1], 2)), fontsize=font_size)
    
    # On affiche que des valeurs entières, et s'il y en a trop on wrap
    plt.xticks(fontsize=font_size)
    y_min, y_max = plt.ylim()
    if y_max < 10:
        plt.yticks(range(int(y_min), int(y_max)+1), fontsize=font_size)
    else:
        plt.yticks(range(int(y_min), int(y_max)+1, int((y_max-y_min)/10)), fontsize=font_size)
    
    plt.show(block=False)
    plt.pause(.1)