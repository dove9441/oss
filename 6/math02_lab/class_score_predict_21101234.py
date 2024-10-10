import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    midterm_range = np.array([0, 125])
    final_range = np.array([0, 100])

    # Load score data
    class_kr = np.loadtxt('./data/class_score_kr.csv', delimiter=',')# shape : (51,2)
    class_en = np.loadtxt('./data/class_score_en.csv', delimiter=',')# shape : (43,2)
    data = np.vstack((class_kr, class_en)) #shape : (94,2)

    # Estimate a line, final = slope * midterm + y_intercept
    #print(class_kr.shape, class_en.shape, data.shape)
    X = data[:, 0] # 중간고사 점수만, shape : (94, )
    y = data[:, 1] # 기말고사 점수만 shape : (94, )
    A = np.vstack((X, np.ones(X.shape))).T
    b = y

    line = np.linalg.pinv(A) @ b # TODO) Please find the best [slope, y_intercept] from 'data'
    # line.shape : (2, ) (1차원이다)
    #print(X.shape, y.shape, A.shape, line.shape, np.linalg.pinv(A).shape)
    # Predict scores
    final = lambda midterm: line[0] * midterm + line[1]
    while True:
        try:
            given = input('Q) Please input your midterm score (Enter or -1: exit)? ')
            if given == '' or float(given) < 0:
                break
            print(f'A) Your final score is expected to {final(float(given)):.3f}.')
        except Exception as ex:
            print(f'Cannot answer the question. (message: {ex})')
            break

    # Plot scores and the estimated line
    plt.figure()
    plt.plot(data[:,0], data[:,1], 'r.', label='The given data')
    plt.plot(midterm_range, final(midterm_range), 'b-', label='Prediction')
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.xlim(midterm_range)
    plt.ylim(final_range)
    plt.grid()
    plt.legend()
    plt.show()
