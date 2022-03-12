import numpy as np


class DataGenerator:
    #--------------------------------------------#
    # function definition $$$$

    x_init = 1e-5
    iterations = 20000

    aL = 1.5
    aR = -1.2
    aM1 = 1.75
    aM2 = 1.25
    aM3 = -1.5

    mL = 1.503
    mR = -0.1
    mM1 = -0.25
    mM2 = 0.25
    mM3 = 3.9

    fL  = lambda self, x: self.aL * x + self.mL
    fR  = lambda self, x: self.aR * x + self.mR
    fM1 = lambda self, x: self.aM1 * x + self.mM1
    fM2 = lambda self, x: self.aM2 * x + self.mM2
    fM3 = lambda self, x: self.aM3 * x + self.mM3

    def f(self, x):
        if x < -1: 
            return self.fL(x)
        elif x < 0: 
            return self.fM1(x)
        elif x < 1: 
            return self.fM2(x)
        elif x < 2: 
            return self.fM3(x)
        else: 
            return self.fR(x)

    # critical points definition $$$$

    # location of the critical points (x, y)
    def criticalpoints(self):
        critpoints = [[-1, self.fL(-1)], 
                      [-1, self.fM1(-1)], 
                      [0, self.fM1(0)],
                      [0, self.fM2(0)],
                      [1, self.fM2(1)],
                      [1, self.fM3(1)],
                      [2, self.fM3(2)],
                      [2, self.fR(2)]]
        return critpoints

    # initial iterations for critical points
    cp_iterations = [0]*8  

    
    #--------------------------------------------#
    # Data generation 

    def f_data(self, x_range):
        y = np.empty(len(x_range))
        i = 0
        for x in x_range:
            y[i] = self.f(x)
            i += 1
        return y


    def gen_orbit(self, x_init=x_init, iterations=iterations):
        result = np.empty(iterations)
        x = x_init
        for i in range(iterations):
            x = self.f(x)
            result[i] = x
        return result


    def convert_cobweb_data(self, y, x_init=x_init, transient=False):
        """ convert to the cobweb data fromat """
        px=[x_init, x_init]
        py=[x_init, y[0]]
        
        for i in range(0,len(y)-1):
            px.append(y[i])
            px.append(y[i])
            py.append(y[i])
            py.append(y[i+1])

        # skip (some) transient steps (quarter)
        if not transient:
            px = px[len(px)//4:]
            py = py[len(py)//4:]

        return px, py

    
    def cobweb(self, x_init=x_init, iterations=iterations, transient=False):
        orbit = self.gen_orbit(x_init, iterations)
        return self.convert_cobweb_data(orbit, x_init, transient)


    def criticalpoints_cobwebs(self, iterations=None):
        # iterations is a list specifying the number of iterations for each critical point
        if iterations is None:
            iterations = self.cp_iterations
        else:
            self.cp_iterations = iterations

        cobwebs = []
        critpoints = self.criticalpoints()

        for i in range(len(iterations)):
            if iterations[i] <= -1:
                cobwebs.append([None, None])
            elif iterations[i] == 0:
                cobwebs.append(critpoints[i])
            else:
                x, y = critpoints[i]
                px, py = self.cobweb(x_init=y, iterations=iterations[i], transient=True)
                cobwebs.append([[x] + px, [y] + py])

        return cobwebs

