import math

def zeroVec(length):
    return [0.0] * length
def normalizeVec(vec):
    magnitude = math.sqrt(sum([item ** 2 for item in vec]))
    return [item / magnitude for item in vec]

def magnitude(vec):
    return math.sqrt(sum([item ** 2 for item in vec]))

def addVec(vec1, vec2):
    return [a + b for a, b in zip(vec1, vec2)]

def subVec(vec1, vec2):
    return [a - b for a, b in zip(vec1, vec2)]

def multiplyVec(vec, constant):
    return [item * constant for item in vec]

def calcDistance(vec1, vec2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(vec1, vec2)]))

def areaTriangle(vec1, vec2, vec3):

    return abs(vec1[0]*(vec2[1]-vec3[1])+vec2[0]*(vec3[1]-vec1[1])+vec3[0]*(vec1[1]-vec2[1]))