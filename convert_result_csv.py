import pandas as pd

def convert_result_csv(filename,output):
    df = pd.read_csv(filename, delimiter=',', low_memory=False)
    df['Previous model'] = df['Model'].shift(1)
    order = [0, 8, 1, 2, 3, 4, 5, 6, 7]  # setting column's order
    df = df[[df.columns[i] for i in order]]
    df.to_csv(output)

if __name__ == '__main__':
    convert_result_csv('./Results/2104_Testing_wTC_20_N2dataset/All_models.txt',
                       './Results/2104_Testing_wTC_20_N2dataset/All_models.csv')