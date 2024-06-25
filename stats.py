import matplotlib.pyplot as plt

plt.switch_backend('TkAgg')

plt.ion()

def plot(scores, mean_scores):
    plt.figure(1)
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.pause(0.001)  # Add a pause to update the plot
    plt.show(block=False)  # Ensure the plot shows in a separate window without blocking
