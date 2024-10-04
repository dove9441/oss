import matplotlib.pyplot as plt
from collections import Counter

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('./data/class_score_kr.csv')
    class_en = read_data('./data/class_score_en.csv')
    # 창 크기 설정
    plt.rcParams["figure.figsize"] = (6,8)

    # TODO) Prepare midterm, final, and total scores
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [40/125*midterm + 60/100*final for (midterm, final) in class_kr]
    midterm_en, final_en = zip(*class_en)
    total_en = [40/125*midterm + 60/100*final for (midterm, final) in class_en]
    fig = plt.figure()
    # TODO) Plot midterm/final scores as points
    scplot = fig.add_subplot(2,1,1)
    scplot.scatter(midterm_kr, final_kr, s=8, c='red', marker='o', label='Korean')
    scplot.scatter(midterm_en, final_en, s=40, c='blue', marker='+', label='English')
    scplot.set_xlabel('Midterm scores')
    scplot.set_ylabel('Final scores')
    scplot.set_xlim(0, )
    scplot.set_ylim(0,100)
    scplot.grid()
    scplot.legend(loc='upper left')
    # TODO) Plot total scores as a histogram
    hiplot = fig.add_subplot(2,1,2)
    hiplot.hist(total_kr, bins=20, color='red', label='Korean', range=(0,100), alpha=0.8)
    hiplot.hist(total_en, bins=20, color='blue', label='English', range=(0,100), alpha=0.3)
    hiplot.set_xlim(0,100)
    hiplot.set_xlabel('Total scores')
    hiplot.set_ylabel('The number of students')
    hiplot.legend(loc='upper left') 
    plt.show()