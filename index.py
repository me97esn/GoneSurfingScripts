import numpy as np
import matplotlib.pyplot as plt 
from wave_samples import samples, samples2d

def ifft2(x, y, fourierCoefficients, lenX, lenY):
    result = 0.0j

    for m in range(lenX):
        for n in range(lenY):
            print("m: ", m, "n: ", n, "lenX:", lenX, "lenY:", lenY)

            print()
            fourierCoefficient = fourierCoefficients[m][n]
            result = result + fourierCoefficient*np.exp(2*np.pi*1j*(m*x/lenX + n*y/lenY))/(lenX*lenY)
    return result.real


def ifft(t, fourierCoefficients):
    ""
    n = len(fourierCoefficients)
    result = 0.0j
    for m in range(n):
        result = result + fourierCoefficients[m]*np.exp(2*np.pi*1j*m*t/n)/n
    return result.real



# print(ifft(0, b))
# print(ifft(1, b))
# print(ifft(2, b))

# fill an array with zero imaginary numbers
# c = np.linspace(0, n-1, num=n)*1.0j
# for t in range(n):
#     c[t] = 0.0
#     for k in range(n)]m
#         c[t] = c[t] + b[k]*np.exp(2*np.pi*1j*k*t/n)/n
# print(c)

random_2darray = np.random.randint(5, size=(10, 10))
# print(random_2darray)
# a2 = np.array([[0,1,0], [1, 1.1, 1.2], [1, 1, 1]])
b2 = np.fft.fftn(random_2darray)

# print("-----------------")
# print("Original 2d array\n",random_2darray)
# # print("Fouriere transformed 2d array:\n",b2)
# # print(ifft2(1, 1, b2))
# print('-----------------')
# print(random_2darray.shape[0])
# print("0,:" ,ifft2(0, 0, b2,random_2darray.shape[0], random_2darray.shape[1]), ", should be: ", random_2darray[0][0])
# print("8,6:" ,ifft2(8, 6, b2,random_2darray.shape[0], random_2darray.shape[1]), ", should be: ", random_2darray[8][6])
# print("9,5:" ,ifft2(9, 5, b2,random_2darray.shape[0], random_2darray.shape[1]), ", should be: ", random_2darray[9][5])
# print("9,9:" ,ifft2(9, 9, b2,random_2darray.shape[0], random_2darray.shape[1]), ", should be: ", random_2darray[9][9])
# print()
# result = [[(ifft2(i, j, b2, random_2darray.shape[0], random_2darray.shape[1])) for i in range(random_2darray[0].size )] for j in range(random_2darray.size)]

wave_samples = samples()
wave_samples_2d = samples2d()

frequencies = np.fft.fftn(wave_samples)
frequencies_2d = np.fft.fftn(wave_samples_2d)
num_of_frequencies = 20
filtered_frequencies = [frequencies[i] if i < num_of_frequencies or i > 2570 else 0 for i in range(len(frequencies))]
# Use numpy ifftn
result_using_numpy_iiiftn = np.fft.ifftn(filtered_frequencies)
# use my own ifftn
# result_using_my_iiiftn = ifft2(8, 6, b2,random_2darray.shape[0], random_2darray.shape[1]), ", should be: ", random_2darray[8][6])

# result_using_my_iiiftn = [ifft2(i, 0, filtered_frequencies, len(wave_samples), 1) for i in range(len(wave_samples))]


print("9,0:" ,ifft2(9, 0, frequencies_2d,len(frequencies_2d[0])-1, 1), ", should be: ", wave_samples_2d[9][0])

# plotting
x = np.arange(1, len(wave_samples)+1)
# plt.title(str(num_of_frequencies) + " of the lowest frequencies and the 21 highest") 
# plt.xlabel("X axis") 
# plt.ylabel("Y axis") 
# ax = plt.gca()
# # ax.set_xlim([xmin, xmax])
# ax.set_ylim([0, 50])
# plt.plot(x, wave_samples, color ="red") 
# # plt.plot(x, [a  for a in result_using_my_iiiftn ], color ="blue") 
# plt.plot(x, [a  for a in result_using_numpy_iiiftn], color ="blue") 
# plt.show()
