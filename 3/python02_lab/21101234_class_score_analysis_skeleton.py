def read_data(filename):
    # TODO) Read `filename` as a list of integer numbers
    data = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            if not line.startswith('#'):
                midScore, finalScore = int(line.split(',')[0].strip()), int(line.split(',')[1].strip())
                data.append([midScore, finalScore])
        #print(data)
    return data

def calc_weighted_average(data_2d, weight):
    # TODO) Calculate the weighted averages of each row of `data_2d`
    average = []
    for row in data_2d:
        average.append(row[0]*weight[0] + row[1]*weight[1])
    #print(average)
    return average

def cal_mean(data):
    s = 0
    for i in data:
        s += i
    return s/len(data)
def analyze_data(data_1d):
    # TODO) Derive summary of the given `data_1d`
    # Note) Please don't use NumPy and other libraries. Do it yourself.
    mean = cal_mean(data_1d) 
    v = [ (x-mean)**2 for x in data_1d]
    var = cal_mean(v)
    median_idx = int(len(data_1d)/2)
    median = sorted(data_1d)[median_idx]
    return mean, var, median, min(data_1d), max(data_1d)

if __name__ == '__main__':
    data = read_data('data/class_score_en.csv')
    if data and len(data[0]) == 2: # Check 'data' is valid
        average = calc_weighted_average(data, [40/125, 60/100])

        # Write the analysis report as a markdown file
        with open('class_score_analysis.md', 'w') as report:
            report.write('### Individual Score\n\n')
            report.write('| Midterm | Final | Average |\n')
            report.write('| ------- | ----- | ----- |\n')
            for ((m_score, f_score), a_score) in zip(data, average):
                report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')
            report.write('\n\n\n')

            report.write('### Examination Analysis\n')
            data_columns = {
                'Midterm': [m_score for m_score, _ in data],
                'Final'  : [f_score for _, f_score in data],
                'Average': average }
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f'* {name}\n')
                report.write(f'  * Mean: **{mean:.3f}**\n')
                report.write(f'  * Variance: {var:.3f}\n')
                report.write(f'  * Median: **{median:.3f}**\n')
                report.write(f'  * Min/Max: ({min_:.3f}, {max_:.3f})\n')