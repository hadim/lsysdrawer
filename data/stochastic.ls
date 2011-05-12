# define some variable
define : test : 0.6

# ignore symbols in case of context sensitive
ignore : +-

name : Stochastic behaviour
iteration : 4
angle : 22.5
ratio : 1

axiom : F

rules : p1 : F : 0.33 : F[+F]F[-F]F
rules : p2 : F : 0.33 : F[+F]F
rules : p3 : F : 0.34 : F[-F]F

symbols : F : F
symbols : B : F
