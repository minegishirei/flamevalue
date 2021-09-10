import numpy as np

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import random
import time


print("import numpy")


def function_quadratic(x):
    #予測したい関数
    y = 2*x -10
    return y

def sigmoid(x):
    return 1 / (1 + np.exp(-x))    


def sigmoid_grad(x):
    return (1.0 - sigmoid(x)) * sigmoid(x)

def softmax(x):
    x = x - np.max(x, axis=-1, keepdims=True)   # オーバーフロー対策
    return np.exp(x) / np.sum(np.exp(x), axis=-1, keepdims=True)



#学習用データ
#x_list = np.array([2,1,4,6,10,30,18,391,391,139,19,4,6,910,90])
x_list = np.array([random.randint(0,10) for i in range(0,10000)])
y_list = function_quadratic(x_list)



print(x_list)
print(y_list)



#各種パラメーター
learning_rate = 0.1
hidden_size = 50
output_size = 100
input_size = 1
weight_init_std = 1


params = {}
params['W1'] = weight_init_std * np.random.randn(input_size, hidden_size)
params['b1'] = np.zeros(hidden_size)
params['W2'] = weight_init_std * np.random.randn(hidden_size, hidden_size)
params['b2'] = np.zeros(hidden_size)
params['W3'] = weight_init_std * np.random.randn(hidden_size, output_size)
params['b3'] = np.zeros(output_size)


for i_1 in range(0,10):
    for i in range(0, len(x_list)):
        x = x_list[i]
        t = y_list[i]

        W1, W2, W3 = params['W1'], params['W2'], params['W3']
        b1, b2, b3 = params['b1'], params['b2'], params['b3']

        grads = {}
        
        # forward
        a1 = np.dot(x, W1) + b1
        z1 = a1
        #z1 = sigmoid(a1)
        
        a2 = np.dot(z1, W2) + b2
        z2 = a2
        #y = softmax(a2)

        a3 = np.dot(z2, W3) + b3
        y = a3


        # backward
        dy = (y - t) 
        grads['W3'] = np.dot(z1.T, dy)
        grads['b3'] = np.sum(dy, axis=0)

        dz2 = np.dot(dy, W3.T)
        da2 = dz2
        grads['W2'] = np.dot(z2.T, da2)
        grads['b2'] = np.sum(da2, axis=0)
        
        dz1 = np.dot(dy, W2.T)
        #da1 = sigmoid_grad(a1) * dz1
        da1 = dz1
        grads['W1'] = np.dot(x.T, da1)
        grads['b1'] = np.sum(da1, axis=0)


        # パラメータの更新
        for key in ('W1', 'b1', 'W2', 'b2', 'W3', 'b3'):
            params[key] -= learning_rate * grads[key]
        
        print("x : ", x)
        #print("y : ", y)
        #print("t : ", t)
        print("deff : ", t - y[0][0])
        #print(grads)


        








