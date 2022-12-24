import numpy as np
def minimize(f, g, a, b, x0):
    x0 = x0.tolist()

    def alfa(x, g):
        ilutz_small = g(x)[0]
        ilutz_equal = g(x)[1]

        sumi = 0
        if len(ilutz_small) != 0:
            for i in range(0, len(ilutz_small)):
                p = max((ilutz_small[i]), 0)
                sumi = sumi + p
        if len(ilutz_equal) != 0:
            for j in range(0, len(ilutz_equal)):
                sumi = sumi + abs((ilutz_equal[j]))
        return sumi

    def multi_function(lst, z, index, mu2, g, f):  ## the multi_function ##
        j = [0] * len(lst)
        j[index] = z
        x = []
        for i in range(len(lst)):
            p = lst[i] + j[i]
            x.append(p)
        x = np.asarray(x)
        return f(x) + mu2 * alfa(x, g)

    def substion(x, k):  ## checking for the epsilon  ##
        subst = (np.array(x[k]) - np.array(x[k - 1])).tolist()  ## convert to numpy so can make - between arrays ##
        sumi = 0
        for j in subst:
            sumi = sumi + (j ** 2)
            epsilon = sumi ** 0.5
        return epsilon

    def golden_rule(a, b, max_iterations, multi_function, lst, mu2, index, g, f):
        max_it = 40
        fi = 1.618033988
        a = a
        b = b
        lamba = []
        mu = []
        multi_function
        for i in range(max_it):
            if abs(b-a)<0.01:
                break
            lamba.append(b - (1 / fi) * (b - a))  ## append to the lamda list the current lamda##
            mu.append(a + (1 / fi) * (b - a))  ## append to the mu list the current mu ##
            if multi_function(z=lamba[-1], lst=lst, mu2=mu2, index=index, g=g, f=f) < multi_function(z=mu[-1], lst=lst,mu2=mu2,index=index, g=g,f=f):  ## dicide what a and b to take acoording to the decision ##
                a = a
                b = mu[-1]
            if multi_function(z=lamba[-1], lst=lst, mu2=mu2, index=index, g=g, f=f) > multi_function(z=mu[-1], lst=lst,mu2=mu2,index=index, g=g,f=f):
                a = lamba[-1]
                b = b

        return (a + b) / 2  ## return the middel of the spectrom so it will be the dicided point ##

    def axis_method(x0, max_iterations, multi_function, a, b, mu2, g):
        k = 1  ## starting with k =1 ##
        x = [x0]  ## insert to a list the x0s that are also in list- this is list of lists --
        epsilons = []  ## save the epsilons ##
        epsilon = 1000  ## stratig epsilon is infinity ##
        demsions = len(x0)  ## the demnsions (number of vars) are the same as the number of equstions in fs ##
        while (k < 40):
            if epsilon<0.01:
                break
            ## as long as k is smaller then the max iterations ##
            x.append(
                x[k - 1][:])  ## apeend to x in the current place , the last list of x from the previus iteration ##
            for i in range(0, demsions):  ## move on every var in the list ##
                golden = golden_rule(a=a[i], b=b[i], max_iterations=max_iterations, multi_function=multi_function,
                                     lst=x[k], mu2=mu2, index=i, g=g, f=f)
                x[k][i] = (x[k][i] + golden)
            epsilon = substion(x, k)  ## after the loop check the epsilon ##
            k = k + 1  ## up k to k +1 ##
            epsilons.append(epsilon)  ## append the epsilons ##
        return x[-1]

    def penalty(x0, multi_function, a, b, g):
        k = 0
        mu2 = 0.1
        mu2_alfa = 1000
        x = [x0]
        ks = []
        mu2_alfas = []
        mu2s = []
        alfas_lst = []
        fxs = []
        counter = 0
        while (mu2_alfa > 0):
            k = k + 1
            axis = axis_method(x0=x[-1], max_iterations=100, multi_function=multi_function, a=a, b=b, mu2=mu2, g=g)
            x.append(axis)
            alfas = alfa(x[-1], g)
            alfas_lst.append(alfas)
            mu2_alfa = mu2 * alfas
            mu2_alfas.append(mu2_alfa)
            mu2s.append(mu2)
            mu2 = mu2 * 10
            fxs.append(f(np.asarray(x[-1])))
            ks.append(k)
            if k == 100:
                print('no sulotion for the problem')
                break
            print('k =', ks[-1], ' mu= ', mu2s[-1],' x =', np.asarray(x[-1]), " f(x)= ", fxs[-1]," alfa= ", alfas_lst[-1], "mu * alfa= ", mu2_alfas[-1])

        return ks, mu2s, x, alfas_lst, mu2_alfas, fxs


    k, mu2, x, alfas, mu2_alfa, fx = penalty(x0=x0, multi_function=multi_function, a=a, b=b, g=g)
    x0 = np.asarray(x0)
    x=np.asarray(x)
    return x[-1],fx[-1]

