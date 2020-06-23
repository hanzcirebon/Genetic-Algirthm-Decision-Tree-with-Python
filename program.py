# Genetic Algorithm Decision Tree
import numpy
import random

# decode from rules into binary
def Decode(datalist):
    chromosome = []

    # suhu 3 bit
    if (datalist[0] == 'rendah'):
        chromosome.extend([1, 0, 0])
    elif (datalist[0] == 'normal'):
        chromosome.extend([0, 1, 0])
    elif (datalist[0] == 'tinggi'):
        chromosome.extend([0, 0, 1])

    # waktu 4 bit
    if (datalist[1] == 'pagi'):
        chromosome.extend([1, 0, 0, 0])
    elif (datalist[1] == 'siang'):
        chromosome.extend([0, 1, 0, 0])
    elif (datalist[1] == 'sore'):
        chromosome.extend([0, 0, 1, 0])
    elif (datalist[1] == 'malam'):
        chromosome.extend([0, 0, 0, 1])

    # kondisi langit 4 bit
    if (datalist[2] == 'cerah'):
        chromosome.extend([1, 0, 0, 0])
    elif (datalist[2] == 'berawan'):
        chromosome.extend([0, 1, 0, 0])
    elif (datalist[2] == 'rintik'):
        chromosome.extend([0, 0, 1, 0])
    elif (datalist[2] == 'hujan'):
        chromosome.extend([0, 0, 0, 1])

    # kelembapan 3 bit
    if (datalist[3] == 'rendah'):
        chromosome.extend([1, 0, 0])
    elif (datalist[3] == 'normal'):
        chromosome.extend([0, 1, 0])
    elif (datalist[3] == 'tinggi'):
        chromosome.extend([0, 0, 1])

    # terbang/tidak 1 bit
    if isTrain:
        if (datalist[4] == 'tidak'):
            chromosome.extend([0])
        else:
            chromosome.extend([1])

    # data total 15 bit
    return chromosome

# bikin populasi random dengan banyak populasi sebanyak popSize
def createPopulation():
    random = []
    a = 0
    while a < popSize:
        # ini buat check banyak rule tiap chromosome. min 1 rule , max 3 rule
        checker = numpy.random.randint(1,5)
        # bikin array data random, dengan isi 0/1
        data = numpy.random.randint(2,size = popLength * checker)
        arrcheck = numpy.array_split(data,checker)
        valid = True
        j = 0

        # nge check kalo di dalam array random apakah salah 1 persyaratannya adalah kosong, ex: suhu = [0,0,0]
        # kalo suhu = [0,0,0], maka chromosome nya salah dan akan di random lagi
        while j < checker and valid:

            # array suhu bit ke 1-3
            suhu = arrcheck[j][0:3]
            # array waktu bit ke 4-7
            waktu = arrcheck[j][3:7]
            #array cuaca bit ke 8-11
            cuaca = arrcheck[j][7:11]
            #array kelembapan bit ke 12-14
            kelembapan = arrcheck[j][11:14]

            # nge check kalo suhu nya [0,0,0]
            if (not any(suhu)):
                valid = False
            # nge check kalo waktu nya [0,0,0,0]
            elif (not any(waktu)):
                valid = False
            # nge check kalo cuaca nya [0,0,0,0]
            elif (not any(cuaca)):
                valid = False
            # nge check kalo kelembapan nya [0,0,0]
            elif (not any(kelembapan)):
                valid = False
            
            j = j + 1

        # kalo data nya valid, maka di masukan ke dalam array, otherwise random ulang sampai data valid
        if valid:
            random.append(data)
            a = a + 1

    return random

# return array dari Fitness sesuai dengan initPopulation
# cara mendapatkan Fitness dengan metode maximize the accuracy
def createFitness(population):
    
    Fitness = []

    # looping buat nyari semua hasil terbang / tidak nya
    for i in range (len(population)):
        
        # ngitung error
        errCount = 0
        # di cari rule nya ada berapa
        rules = len(population[i])/popLength

        # nge looping buat nyari nilai fitness nya
        for j in range (len(data_latih)):
            
            #boolean buat nge check error
            isError = False
            checker = 0
            #looping buat rule nya, kalo error dia nambah error count, kalo bener lanjut aje
            while checker != rules and not isError:
                
                #buat check suhu (bit 1-3)
                suhu_population = numpy.array(population[i][(checker*15)+0:(checker*15)+3])
                suhu_data_latih = numpy.array(data_latih[j][0:3])
                suhu = suhu_population * suhu_data_latih

                #buat check waktu (bit 4-7)
                waktu_population = numpy.array(population[i][(checker*15)+3:(checker*15)+7])
                waktu_data_latih = numpy.array(data_latih[j][3:7])
                waktu = waktu_population * waktu_data_latih

                #buat check kondisi langit (cuaca) (bit 8-11)
                cuaca_population = numpy.array(population[i][(checker*15)+7:(checker*15)+11])
                cuaca_data_latih = numpy.array(data_latih[j][7:11])
                cuaca = cuaca_population * cuaca_data_latih

                #buat check kelembapan (bit 12-14)
                kelembapan_population = numpy.array(population[i][(checker*15)+11:(checker*15)+14])
                kelembapan_data_latih = numpy.array(data_latih[j][11:14])
                kelembapan = kelembapan_population * kelembapan_data_latih

                #buat check result (bit 14)
                result_population = numpy.array(population[i][(checker*15)+14])
                result_data_latih = numpy.array(data_latih[j][14])
                result = bool(result_population == result_data_latih)

                # kalo semua memenuhi
                if any(suhu) and any(waktu) and any(cuaca) and any(kelembapan) or result:
                    checker += 1
                    continue
                
                isError = True

                # endwhile checker >= rules or isError
            
            if isError:
                errCount += 1

            # kalo error di antara suhu/waktu/cuaca/kelembapan/result
            
            # endfor j >= len(data_latih)
        
        # ngitung fitness metode maximize accuracy = (ndata - error) / ndata
        currFitness = (len(data_latih) - errCount)/len(data_latih)
        Fitness.extend([currFitness])

        # endfor i >= len(data_latih)
    
    return Fitness

# mendapatkan 2 parent dengan cara tournament selection, nge return 2 chromosome parent
def findParent():
    parent = []
    for i in range(total_parent):
        #BO3 take 1
        hoki1,hoki2,hoki3 = -1,-1,-1
        while True:
            if hoki1 == -1:
                hoki1 = random.randrange(10)

            if hoki2 == hoki1 or hoki2 == -1:
                hoki2 = random.randrange(10)
            
            if hoki3 == hoki2 or hoki3 == hoki1 or hoki3 == -1:
                hoki3 = random.randrange(10)
                break
        
        if arrFitness[hoki1] > arrFitness[hoki2] and arrFitness[hoki1] > arrFitness[hoki3]:
            parent.append(initPopulation[hoki1])
        elif arrFitness[hoki2] > arrFitness[hoki3]:
            parent.append(initPopulation[hoki2])
        else:
            parent.append(initPopulation[hoki3])

    return parent

# crossover
def crossover():
    crossrand = numpy.random.uniform(low=0,high=1)

    if (crossrand <= propCrossover):

        possible_points = []
        # ambil point dulu dari parent ke 1
        ap1 = 0
        bp1 = 0
        while ap1 == bp1:
            ap1 = numpy.random.randint(len(newParent[0]))
            bp1 = numpy.random.randint(len(newParent[0]))
        
        if(ap1 > bp1):
            point1 = [bp1,ap1]
            range1 = ap1-bp1
        else:
            point1 = [ap1,bp1]
            range1 = bp1-ap1

        # ambil point dulu dari parent ke 2
        ap2 = 0
        bp2 = 0
        while ap2 == bp2:
            ap2 = numpy.random.randint(len(newParent[1]))
            bp2 = numpy.random.randint(len(newParent[1]))
        
        if(ap2 > bp2):
            point2 = [bp2,ap2]
            range2 = ap2-bp2
        else:
            point2 = [ap2,bp2]
            range2 = bp2-ap2
        
        # pilih yang range nya paling gede
        if range1 > range2:
            possible_points.append(point1)
            range = range1
        else:
            possible_points.append(point2)
            newParent[0],newParent[1] = newParent[1],newParent[0]
            range = range2
        
        # ambil sisa nya
        # sebelah kiri
        ruleborder = len(newParent[0]) // 15

        # cari gap yang kecil nya
        gap = possible_points[0][1]-ruleborder*15

        # bikin gap seminim mungkin selama ruleborder > 1
        i = ruleborder
        while gap < 0:
            if i > 1:
                gap += 15
                i -= 1
            else:
                break

        # cek panjang range parent 1 >= 1 rule
        if ruleborder >= 1 and gap > 0:
            
            # cek gap kiri
            gap_kiri = possible_points[0][0] + gap
            #print ('kiri : ',gap_kiri)
            # cek di parent ke 2
            if gap_kiri < len(newParent[1]):
                possible_points.append([possible_points[0][0],gap_kiri])

            #cek gap kanan
            gap_kanan = possible_points[0][1] - gap
            #print ('kanan : ',gap_kanan)
            # cek di parent ke 2
            if gap_kanan > 0:
                possible_points.append([gap_kanan,possible_points[0][1]])

        #print('possible points : ',possible_points)

        # select random number for possible crossover
        number = numpy.random.randint(len(possible_points))
        #print('number : ',number)
        
        #print('sebelum : ',newParent[0],' , ',newParent[1])
        #print('panjang : ',len(newParent[0]),' , ',len(newParent[1]))

        # tengah biasa
        if number == 0:
            if possible_points[0][1] > len(newParent[1]):
                multiply = possible_points[0][1] // 15
                #print('multiply', multiply)
                # generate new length
                k = 0
                while k < multiply:
                    newParent[1] = numpy.concatenate((newParent[1],newParent[1]),axis=None)
                    k += 1
            
            swap = numpy.array(newParent[1][possible_points[0][0]:possible_points[0][1]])
            #print ('swap1 : ', swap)
            newParent[1][possible_points[0][0]:possible_points[0][1]] = newParent[0][possible_points[0][0]:possible_points[0][1]]
            #print ('swap2 : ', swap)
            newParent[0][possible_points[0][0]:possible_points[0][1]] = swap

        elif number == 1:
            if possible_points[0][1] > len(newParent[1]):
                multiply = possible_points[0][1] // 15
                #print('multiply', multiply)
                # generate new length
                k = 0
                while k < multiply:
                    newParent[1] = numpy.concatenate((newParent[1],newParent[1]),axis=None)
                    k += 1

            bigswap = numpy.array(newParent[0][possible_points[0][0]:possible_points[0][1]])
            smallswap = numpy.array(newParent[1][possible_points[1][0]:possible_points[1][1]])
            #print('bigswap : ',bigswap)
            newParent[0][possible_points[1][0]:possible_points[1][1]] = smallswap
            #print('parent : ',newParent[1][possible_points[0][0]:possible_points[0][1]])
            newParent[1][possible_points[0][0]:possible_points[0][1]] = bigswap

            if len(newParent[1]) % 15 > 0 and len(newParent[1]) // 15 > 0:
                newLen = len(newParent[1]) // 15
                for z in range(newLen*15):
                    newParent[1][z] = newParent[1][z]

        else:
            if possible_points[0][1] > len(newParent[1]):
                multiply = possible_points[0][1] // 15
                #print('multiply', multiply)
                # generate new length
                k = 0
                while k < multiply:
                    newParent[1] = numpy.concatenate((newParent[1],newParent[1]),axis=None)
                    k += 1

            bigswap = numpy.array(newParent[0][possible_points[0][0]:possible_points[0][1]])
            smallswap = numpy.array(newParent[1][possible_points[2][0]:possible_points[2][1]])
            #print('bigswap : ',bigswap)
            newParent[0][possible_points[2][0]:possible_points[2][1]] = smallswap
            newParent[1][possible_points[0][0]:possible_points[0][1]] = bigswap

            if len(newParent[1]) % 15 > 0 and len(newParent[1]) // 15 > 0:
                newLen = len(newParent[1]) // 15
                for z in range(newLen*15):
                    newParent[1][z] = newParent[1][z]

def mutate():
    for i in range(len(newParent)):
        rand = numpy.random.uniform(low=0,high=1)
        if rand < propMutation :
            datarand = numpy.random.randint(2, size=len(newParent[i]))
            for j in range(len(newParent[i])):
                if datarand[j] == newParent[i][j]:
                    if (newParent[i][j] == 1):
                        newParent[i][j] = 0
                    else:
                        newParent[i][j] = 1
            
    return newParent

def steadyState(childs):
    for c in range (len(childs)):
        newPopGan = min(arrFitness)
        newPopGanIdx = arrFitness.index(min(arrFitness))
        #print(newPopGanIdx)
        initPopulation[newPopGanIdx] = childs[c]

    return initPopulation

def validate(data_uji):
    
    rule = len(final_data)/15

    isTerbang = False
    #boolean buat nge check error
    checker = 0
    #looping buat rule nya, kalo error dia nambah error count, kalo bener lanjut aje
    while checker < rule and not isTerbang:
        
        #buat check suhu (bit 1-3)
        suhu_final_data = numpy.array(final_data[(checker*15)+0:(checker*15)+3])
        suhu_data_latih = numpy.array(data_uji[0:3])
        #print('suhu :',suhu_final_data)
        #print('suhu :',suhu_data_latih)
        suhu = suhu_final_data * suhu_data_latih
        #print('suhu ====:',suhu)
        #print(any(suhu))


        #buat check waktu (bit 4-7)
        waktu_final_data = numpy.array(final_data[(checker*15)+3:(checker*15)+7])
        waktu_data_latih = numpy.array(data_uji[3:7])
        #print('waktu :',waktu_final_data)
        #print('waktu :',waktu_final_data)
        waktu = waktu_final_data * waktu_data_latih
        #print('waktu ====:',waktu)
        #print(any(waktu))

        #buat check kondisi langit (cuaca) (bit 8-11)
        cuaca_final_data = numpy.array(final_data[(checker*15)+7:(checker*15)+11])
        cuaca_data_latih = numpy.array(data_uji[7:11])
        #print('cuaca :',cuaca_final_data)
        #print('cuaca :',cuaca_data_latih)
        cuaca = cuaca_final_data * cuaca_data_latih
        #print('cuaca ====:',cuaca)
        #print(any(cuaca))

        #buat check kelembapan (bit 12-14)
        kelembapan_final_data = numpy.array(final_data[(checker*15)+11:(checker*15)+14])
        kelembapan_data_latih = numpy.array(data_uji[11:14])
        #print('kelembapan :',kelembapan_final_data)
        #print('kelembapan :',kelembapan_data_latih)
        kelembapan = kelembapan_final_data * kelembapan_data_latih
        #print('kelembapan ====:',kelembapan)
        #print(any(kelembapan))

        # kalo salah 1 tidak memenuhi, maka dia salah
        valid = any(suhu) and any(waktu) and any(cuaca) and any(kelembapan)
        print('suhu :',any(suhu),' waktu :',any(waktu),' cuaca :',any(cuaca),' kelembapan :',any(kelembapan))
        print('validity = ',valid)
        if not valid:
            checker += 1
            continue

        isTerbang=True

        # endwhile checker >= rules or isError

    if isTerbang:
        return 1
    else:
        return 0
        

# mulai program disini
read = open('data_latih_opsi_1.csv')
# data dari data_latih csv
data_latih = []
isTrain = True
for line in read:
    datalist = []
    line = line.strip('\n')
    datalist = line.split(',')
    data_latih.append(Decode(datalist))

read.close

# banyak populasi nya
popSize = 30
# panjang chromosome random
popLength = 15
# probabilitas mutasi
propMutation = 0.05
# probabilitas crossover
propCrossover = 0.2
# total generasi
generation = 50
# total parent
total_parent = 2

# populasi awal
initPopulation = createPopulation()
print(initPopulation)
for mage in range(generation):
    arrFitness = createFitness(initPopulation)
    print('=============================================================')
    print('generasi ke :', mage)
    print('all fitness :', arrFitness)
    print('best fitness :',max(arrFitness), 'index ke : ', arrFitness.index(max(arrFitness)))
    print('kromosom : ', initPopulation[arrFitness.index(max(arrFitness))])
    newParent = findParent()
    # print(initPopulation)
    crossover()
    child = mutate()
    initPopulation = steadyState(child)

print('')
print('')
print('=============================================================')
print('best fitness akhir :', max(arrFitness))
final_data = initPopulation[arrFitness.index(max(arrFitness))]
print('data final akhir :', final_data)

read = open ('data_uji_opsi_1.csv')
isTrain = False
data_latih = []
for line in read:
    datalist = []
    line = line.strip('\n')
    line = line.lower()
    datalist = line.split(',')
    data_latih.append(Decode(datalist))

read.close

print('')
print('')
print('=============================================================')
print('Data Uji test, see the txt file "hasil.txt" for the best experience')
print('')
f = open("hasil.txt", "w")
for i in range( 0 , len(data_latih)):
    Answer = validate(data_latih[i])
    f.write(str(Answer)+"\n")

f.close()