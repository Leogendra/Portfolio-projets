import matplotlib.pyplot as plt
from IPython import display


plt.ion()
plt.figure(figsize=(5, 4))
font_size = 8

def displayScores(scores, moyenne):
    plt.clf()
    plt.title('Entrainement...', fontsize=font_size)
    plt.xlabel('Nombre d\'essais', fontsize=font_size)
    plt.ylabel('Score', fontsize=font_size)
    plt.plot(scores, color="green")
    plt.plot(moyenne, color="blue")
    plt.legend(["Scores", "Moyenne"], loc='upper left', fontsize=font_size)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]), fontsize=font_size)
    plt.text(len(moyenne)-1, moyenne[-1], str(round(moyenne[-1], 2)), fontsize=font_size)
    
    # On affiche que des valeurs entières, et si il y en a trop on wrap
    y_min, y_max = plt.ylim()
    if y_max < 10:
        plt.yticks(range(int(y_min), int(y_max)+1), fontsize=font_size)
    else:
        plt.yticks(range(int(y_min), int(y_max)+1, int((y_max-y_min)/10)), fontsize=font_size)
    
    plt.show(block=False)
    plt.pause(.1)