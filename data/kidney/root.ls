name : Kidney root branching
iteration : 5
angle : 30
radius : 0.03
width : 1

ignore : +-[]

define : radius : 0.05
define : width : 1
define : angle : 45
define : root_angle : 55

axiom : [F[-(root_angle)A][+(root_angle)B]]

rules : A : F[[+(28)^(30)R][+(28)&(70)G]]
#rules : B : F[[-^(angle)R][-&(angle)G]]

#axiom : [F[-(root_angle)F[+^(angle)R][+&(angle)G]][+(root_angle)F[-^(angle)G][-&(angle)R]]]

symbols : A : F
symbols : B : F