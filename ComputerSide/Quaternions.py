"""A file implementing the quaternion class"""
import sympy as sp
import math

""" A class for describing a quaternion """
class Quaternion:
    def __init__(self, q0=0, q1=0, q2=0, q3=0):
        self.q0 = q0
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3

""" A class for describing a vector """
class Vector:
    def __init__(self, vx=0, vy=0, vz=0):
        self.vx = vx
        self.vy = vy
        self.vz = vz

""" p, q are two quaternions; quaternion product. """
def quaternion_product(p, q):
    p0 = p.q0
    p1 = p.q1
    p2 = p.q2
    p3 = p.q3

    q0 = q.q0
    q1 = q.q1
    q2 = q.q2
    q3 = q.q3

    r0 = p0 * q0 - p1 * q1 - p2 * q2 - p3 * q3
    r1 = p0 * q1 + p1 * q0 + p2 * q3 - p3 * q2
    r2 = p0 * q2 - p1 * q3 + p2 * q0 + p3 * q1
    r3 = p0 * q3 + p1 * q2 - p2 * q1 + p3 * q0

    r = Quaternion(r0, r1, r2, r3)
    return(r)

""" v is a vector """
def minus_vector(v):
    return(Vector(-v.vx, -v.vy, -v.vz))


""" q is a quaternion """
def conjugate_quaternion(q):
    q0 = q.q0
    q1 = q.q1
    q2 = q.q2
    q3 = q.q3

    r = Quaternion(q0, -q1, -q2, -q3)
    return(r)

""" v is a vector """
def transform_vector_to_quaternion(v):
    r = Quaternion(0, v.vx, v.vy, v.vz)
    return(r)

""" q is the quaternion describing the rotation to apply, 
    v is the vector on which to apply the rotation """
def apply_rotation_on_vector(q, v):
    
    quaternion_v = transform_vector_to_quaternion(v)
    transposed_q = conjugate_quaternion(q)

    r = quaternion_product(quaternion_product(q, quaternion_v), transposed_q)
    return(extract_vector_from_quaternion(r))


""" v is a vector """
def print_vector(v):
    print("vx: " + str(v.vx) + " | vy: " + str(v.vy) + " | vz: " + str(v.vz))

""" q is a quaternion """
def print_quaternion(q):
    print("q0: " + str(q.q0) + " | q1: " + str(q.q1) +
          " | q2: " + str(q.q2) + " | q3: " + str(q.q3))

""" q is a quaternion """
def extract_vector_from_quaternion(q):
    q1 = q.q1
    q2 = q.q2
    q3 = q.q3

    v = Vector(q1, q2, q3)
    return(v)

""" w is the vector indicating angular rate in the reference frame of the IMU, 
    all coords in rad/s
    dt is the time interval during which the angular rate is valid"""
def angular_rate_to_quaternion_rotation(w, dt):
    wx = w.vx
    wy = w.vy
    wz = w.vz

    l = (wx**2 + wy**2 + wz**2)**0.5

    dtlo2 = dt * l / 2

    q0 = sp.cos(dtlo2)
    q1 = sp.sin(dtlo2) * wx / l
    q2 = sp.sin(dtlo2) * wy / l
    q3 = sp.sin(dtlo2) * wz / l

    r = Quaternion(q0, q1, q2, q3)
    return(r)


""" q is a unit quaternion """
def angle_axis_from_unit_quaternion(q):
    angle = sp.acos(q.q0) * 2
    sin_angle = sp.sin(angle)
    axis_x = q.q1 / sin_angle
    axis_y = q.q2 / sin_angle
    axis_z = q.q3 / sin_angle

    return(angle, axis_x, axis_y, axis_z)


""" q is a quaternion """
def compute_quaternion_norm(q):
    return((q.q0**2 + q.q1**2 + q.q2**2 + q.q3**2)**0.5)


""" q is a quaternion """
def normalise_quaternion(q):
    l = compute_quaternion_norm(q)
    return(Quaternion(q.q0 / l, q.q1 / l, q.q2 / l, q.q3 / l))


""" v, w are vectors """
def add_vectors(v, w):
    vx = v.vx
    vy = v.vy
    vz = v.vz

    wx = w.vx
    wy = w.vy
    wz = w.vz

    r = Vector(vx + wx, vy + wy, vz + wz)
    return(r)


""" q is a quaternion """
def roll_pitch_yaw(q):
    x, y, z, w = q.q1, q.q2, q.q3, q.q0
    pitch = math.atan2(2 * y * w - 2 * x * z, 1 - 2 * y * y - 2 * z * z)
    roll = math.atan2(2 * x * w - 2 * y * z, 1 - 2 * x * x - 2 * z * z)
    yaw = math.asin(2 * x * y + 2 * z * w)

    return (roll, pitch, yaw)
