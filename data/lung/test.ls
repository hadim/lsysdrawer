ignore : +-[]

define : radius : 0.05
define : width : 1
define : angle : 35
define : ortho_angle : 60
define : planar_angle : 60

name : Whole kidney test
iteration : 2
angle : 35
radius : 0.05
width : 1

axiom : [C][-(120)D][+(120)E]

patterns : planar : [F[-F[+(planar_angle)][-(planar_angle)G]][+F[+(planar_angle)R][-(planar_angle)G]]]
patterns : ortho : [F[-F[+^(ortho_angle)R][+&(ortho_angle)G]][+F[-^(ortho_angle)^R][-&(ortho_angle)G]]]
patterns : branching : [F[+(90)B][&(90)B]]

rules : C : &(45)'planar'
rules : D : 'planar'
rules : E : 'ortho'

symbols : C : F
symbols : D : F
symbols : E : F
