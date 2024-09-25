import sys
import random
import json
sys.set_int_max_str_digits(0)

class Encript:
    def __init__(self,file):
        self.file = file

    def converter(self): # Читаем файл и переносим байты в список.
        file = open(self.file,"rb")

        reader = file.read()

        list = []
        for i in reader:
            list.append(i)

        return list

    def function(self): # Основная функция. Создаем Р с помощью двух случайных простых чисел.
        try:
            file = open("simpleInt.txt","r")
            file = file.read().splitlines()

            p = []

            for i in range(len(self.converter())):
                l = []

                for j in range(2):
                    l.append(random.randint(1,69023))

                p.append(int(file[l[0]])*int(file[l[1]]))
        except:
            print("Somthing error.")
            exit(0)

        return p

    def chipertext(self): # Создаем шифротекст. Р умножаем на Сообщение.
        message = self.converter()
        p = self.function()

        c = []

        for i in range(len(message)):
            c.append(message[i]*p[i])

        return c,p

    def stirrer(self): # Смешиваем порядок сообщения.
        c = self.chipertext()

        randint = []
        randval = []
        original = [0] * len(c[0])

        for i in range(len(c[0])):
            randint.append(i)
        random.shuffle(randint)

        for i in range(len(c[0])):
            randval.append(c[0][randint[i]])

        j = 0
        for i in randint:
            original[i] += randval[j]
            j += 1

        return randval,randint,original,c[1]

#New Class -------------------------------------------------------------------------------------------------------------

class Decrypt:
    def __init__(self,file,fkey,fname):
        self.file = file
        self.fkey = fkey
        self.fname = fname

    def efile(self): # Получаем данные из файла данных. Превратим их в список.
        file = open(self.file,"r")
        reader = file.read()
        file.close()

        reader = json.loads(reader)

        return reader

    def filekey(self): # Получаем данные из файла ключей. Превратим их в список.
        file = open(self.fkey,"r")
        reader = file.read()
        file.close()

        reader = json.loads(reader)

        return reader

    def ret(self): # Получим оригинальное зашифрованное сообщение.
        key = self.filekey()
        emess = self.efile()
        originallist = [0]*len(emess)

        for i in range(len(emess)):
            originallist[key[0][i]] += (emess[i])

        return originallist

    def reverse(self): # Поделим оригинальное зашифрованное сообщение на сумму его простых чисел.
        retlist = self.ret()
        p = self.filekey()[1]
        originalmess = []

        for i in range(len(retlist)):
            originalmess.append(int(retlist[i]/p[i]))

        return originalmess

    def compliter(self): # Переведем оригинальное сообщение из 10тичной системы счисления в 16теричню. Запишем его в файл.
        bit = self.reverse()
        b = bytes()

        file = open(self.fname,"wb")

        for i in range(len(bit)):
            b += bit[i].to_bytes()

        file.write(b)
        file.close()



while True:
    mod = input("Input mod [E/D]:    ")
    mod = mod.upper()

    print("If your file not in this directory: input file with path!")
    fname = input("Input file name:    ")

    if mod == "E":
        for i in range(len(fname)): # Получим название файла без его расширения.
            if fname[-i] == ".":
                break

        efile = "E" + fname[:-i] + ".lik"

        cfn = r"KEY.ma"

        print(efile + "is your encrypted file.")

        print(cfn + "is your key file.")

        creator = Encript(fname)
        key = creator.stirrer()

        file = open("E"+fname[:-3]+"lik","w")

        file.write(str(key[0]))
        file.close()

        file = open(cfn,"w")
        file.write("[" + str(key[1]) + "," + str(key[3]) + "]")

    if mod == "D":
        print("If your file not in this directory: input file with path!")
        efile = input("Input encrypted file:    ")
        cfn = input("Input key file:    ")

        decriptor = Decrypt(efile,cfn,fname)
        decriptor.compliter()

    print("Done!")