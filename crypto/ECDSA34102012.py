"""
Формирование и проверка цифрровой подписи согласно ГОСТ 34.10-2012
"""

import secrets 
import hashlib

# Функции нахождения обратного числа в поле по модулю с помощью расширенного алгоритма Евклида
def ext_euclidean(a, b):
    t = u = 1
    s = v = 0
    while b:
        a, (q, b) = b, divmod(a, b)
        u, s = s, u - q * s
        v, t = t, v - q * t
    return a, u, v

def inverse_mod(k,p):
    gcd,x,y = ext_euclidean(k,p)
    assert (k*x + p*y) % p == gcd
    if gcd != 1:
        raise ValueError
    else:
        return x % p

class Curve:
    def __init__(self,p,a,b,m,q,P):
        self.p = p 
        self.a = a
        self.b = b
        self.m = m
        self.q = q
        self.P = P 
    # Проверка принадлежности точки кривой
    def on_curve(self, point):
        if point is None:  # None - нулевая точка
            return True
        x,y = point
        return (y**2 - x**3 - self.a*x - self.b) % self.p == 0

    # Нахождение обратной точки (по сложению)
    def negative_point(self,point):
        assert self.on_curve(point)
        if point is None:
            return None
        x,y = point
        res = (x, -y % self.p)
        assert self.on_curve(res)
        return res

    # Операция сложения точек эллиптической кривой
    def p_add(self,p1,p2):
        assert self.on_curve(p1)
        assert self.on_curve(p2)
        if p1 is None:
            return p2
        if p2 is None:
            return p1
        x1,y1 = p1
        x2,y2 = p2
    
        if x1 == x2 and y1 != y2:
            return None
        if x1 == x2:
            m = (3*(x1**2) + self.a)*inverse_mod(2*y1,self.p)
        else:
            m = (y1 - y2)*inverse_mod(x1 - x2,self.p)
        x = (m**2 - x1 - x2) % self.p
        y = -(y1 + m*(x-x1)) % self.p
        assert self.on_curve((x,y))
        return (x,y)

    # Операция умножения точек
    def p_mul(self,k,p):
        def binary(n):
            while n:
                yield n & 1
                n = n >> 1 
        assert self.on_curve(p)
        if k % self.q == 0 or p == None:
            return None
        if k < 0:
            return self.p_mul(-k,self.negative_point(p))
        res = None
        add = p
        for b in binary(k):
            if b == 1:
                res = self.p_add(res,add)
            add = self.p_add(add,add)
        assert self.on_curve(res)
        return res
    
class Scheme:
    def __init__(self,d,Q,curve):
        self.d = d # private key
        self.Q = Q # public key
        self.curve = curve

    def hash_message(self, msg):
        if (self.curve.q > 2**254 and self.curve.q < 2**256):
            h = hashlib.sha256
        elif (self.curve.q > 2**508 and self.curve.q < 2**512):
            h = hashlib.sha512
        msg_hash = h(msg).digest()
        e = int.from_bytes(msg_hash,'big')
        z = e >> (e.bit_length() - self.curve.q.bit_length())
        assert z.bit_length() <= self.curve.q.bit_length()
        return z

    def sign_message(self, msg):
        z = self.hash_message(msg)
        r = 0
        s = 0
        while not r or not s:
            k = secrets.randbelow(self.curve.q)
            C = self.curve.p_mul(k,self.curve.P) # C = kP
            x,y = C
            r = x % self.curve.q
            s = (inverse_mod(k, self.curve.q)*(z + r * self.d)) % self.curve.q
        return (r,s)

    # Функция проверки подписи
    def verify_message(self,msg, signature):
        z = self.hash_message(msg)
        r,s = signature
        v = inverse_mod(s,self.curve.q)
        z1 = (z*v) % self.curve.q
        z2 = (r*v) % self.curve.q
        x, y = self.curve.p_add(self.curve.p_mul(z1, self.curve.P),self.curve.p_mul(z2, self.Q))
        if r == (x % self.curve.q):
            return 'Подпись корректна.'
        else:
            return 'Подпись неверна :['

def sanity_check(curve, scheme):
    assert(4*(curve.a**3) + 27*(curve.b**2) % curve.p != 0) 
    assert(curve.m % curve.q == 0)
    assert((curve.q > 2**254 and curve.q < 2**256) or (curve.q > 2**508 and curve.q < 2**512))
    assert(curve.p_mul(curve.q, curve.P) is None)
    assert(0 < scheme.d < curve.q)
    assert(curve.p_mul(scheme.d, curve.P) == scheme.Q)
    assert(curve.m!=curve.p)
    if (curve.q > 2**254 and curve.q < 2**256):
        B = 31
    elif (curve.q > 2**508 and curve.q < 2**512):
        B = 131
    for t in range(1, B+1):
        assert(curve.p**t % curve.q != 1)
    return True

# Пример 1
p1 = 0x8000000000000000000000000000000000000000000000000000000000000431
a1 = 7
b1 = 0x5FBFF498AA938CE739B8E022FBAFEF40563F6E6A3472FC2A514C0CE9DAE23B7E
m1 = 0x8000000000000000000000000000000150FE8A1892976154C59CFC193ACCF5B3
q1 = 0x8000000000000000000000000000000150FE8A1892976154C59CFC193ACCF5B3
P1 = (2,0x8E2A8A0E65147D4BD6316030E16D19C85C97F0A9CA267122B96ABBCEA7E8FC8)
d1 = 0x7A929ADE789BB9BE10ED359DD39A72C11B60961F49397EEE1D19CE9891EC3B28
Q1 = (0x7F2B49E270DB6D90D8595BEC458B50C58585BA1D4E9B788F6689DBD8E56FD80B,0x26F1B489D6701DD185C8413A977B3CBBAF64D1C593D26627DFFB101A87FF77DA)

# Пример 2
p2 = 0x4531ACD1FE0023C7550D267B6B2FEE80922B14B2FFB90F04D4EB7C09B5D2D15DF1D852741AF4704A0458047E80E4546D35B8336FAC224DD81664BBF528BE6373
a2 = 7
b2 = 0x1CFF0806A31116DA29D8CFA54E57EB748BC5F377E49400FDD788B649ECA1AC4361834013B2AD7322480A89CA58E0CF74BC9E540C2ADD6897FAD0A3084F302ADC
m2 = 0x4531ACD1FE0023C7550D267B6B2FEE80922B14B2FFB90F04D4EB7C09B5D2D15DA82F2D7ECB1DBAC719905C5EECC423F1D86E25EDBE23C595D644AAF187E6E6DF
q2 = 0x4531ACD1FE0023C7550D267B6B2FEE80922B14B2FFB90F04D4EB7C09B5D2D15DA82F2D7ECB1DBAC719905C5EECC423F1D86E25EDBE23C595D644AAF187E6E6DF
P2 = (0x24D19CC64572EE30F396BF6EBBFD7A6C5213B3B3D7057CC825F91093A68CD762FD60611262CD838DC6B60AA7EEE804E28BC849977FAC33B4B530F1B120248A9A,0x2BB312A43BD2CE6E0D020613C857ACDDCFBF061E91E5F2C3F32447C259F39B2C83AB156D77F1496BF7EB3351E1EE4E43DC1A18B91B24640B6DBB92CB1ADD371E)
d2 = 0xBA6048AADAE241BA40936D47756D7C93091A0E8514669700EE7508E508B102072E8123B2200A0563322DAD2827E2714A2636B7BFD18AADFC62967821FA18DD4
Q2 = (0x115DC5BC96760C7B48598D8AB9E740D4C4A85A65BE33C1815B5C320C854621DD5A515856D13314AF69BC5B924C8B4DDFF75C45415C1D9DD9DD33612CD530EFE1,0x37C7C90CD40B0F5621DC3AC1B751CFA0E2634FA0503B3D52639F5D7FB72AFD61EA199441D943FFE7F0C70A2759A3CDB84C114E1F9339FDF27F35ECA93677BEEC)

curve1 = Curve(p1,a1,b1,m1,q1,P1)
scheme1 = Scheme(d1,Q1,curve1)
curve2 = Curve(p2,a2,b2,m2,q2,P2)
scheme2 = Scheme(d2,Q2,curve2)

sanity_check(curve1,scheme1)
sanity_check(curve2,scheme2)

msg = bytes("R136a1",'utf-8')
sig1 = scheme1.sign_message(msg)
res1 = scheme1.verify_message(msg,sig1)
sig2 = scheme2.sign_message(msg)
res2 = scheme2.verify_message(msg,sig2)
print(res1)
print(res2)
