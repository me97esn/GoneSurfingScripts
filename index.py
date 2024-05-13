import numpy as np
import matplotlib.pyplot as plt 
from wave_samples import samples

def ifft2(x, y, fourierCoefficients, lenX, lenY):
    ""
    result = 0.0j

    for m in range(lenX):
        for n in range(lenY):
            # if m  <= 8:
                result = result + fourierCoefficients[m][n]*np.exp(2*np.pi*1j*(m*x/lenX + n*y/lenY))/(lenX*lenY)
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
#     for k in range(n):
#         c[t] = c[t] + b[k]*np.exp(2*np.pi*1j*k*t/n)/n
# print(c)

# random_2darray = np.random.randint(5, size=(10, 10))
# print(random_2darray)
# a2 = np.array([[0,1,0], [1, 1.1, 1.2], [1, 1, 1]])
# b2 = np.fft.fftn(random_2darray)

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

# len(result)
# print(result)
# for array in result:
#     print(array)

frequencies = np.fft.fftn(wave_samples)
print(frequencies)
num_of_frequencies = 20
print(len(frequencies))
filtered_frequencies = [frequencies[i] if i < num_of_frequencies or i > 2570 else 0 for i in range(len(frequencies))]
filtered = np.fft.ifftn(filtered_frequencies)

# plotting
x = np.arange(1, len(wave_samples)+1)
plt.title(str(num_of_frequencies) + " of the lowest frequencies and the 21 highest") 
plt.xlabel("X axis") 
plt.ylabel("Y axis") 
ax = plt.gca()
# ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 50])
plt.plot(x, wave_samples, color ="red") 
plt.plot(x, [a  for a in filtered], color ="blue") 
plt.show()
