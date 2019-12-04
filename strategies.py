from math import sin, cos, pi


def straight(v, a, g, t):
    return (v*0.5*cos(a/180*pi))/2, -(v*0.5*sin(a/180*pi))/2

def oblique(v, a, g, t):
    return (v*0.5*cos(a/180*pi))/2, -(v*0.5*sin(a/180*pi) - g*t)/2

def ballistic(v, a, g, t):
    return (v*0.5/1.4*cos(a/180*pi))/2, -(v*0.5/1.4*sin(a/180*pi) - g/1.4*t)/2

__all__ = [
    "straight",
    "oblique",
    "ballistic",
]
