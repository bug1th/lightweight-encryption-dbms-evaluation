# speck.py
class SpeckCipher:
    def __init__(self, key, rounds=27):
        self.rounds = rounds
        self.key = self.expand_key(key)

    def expand_key(self, key):
        l = []
        k = []
        m = 4  # key size (in 32-bit words)
        for i in range(m - 1):
            l.append((key >> (32 * i)) & 0xFFFFFFFF)
        k.append((key >> (32 * (m - 1))) & 0xFFFFFFFF)
        for i in range(self.rounds - 1):
            l_new = ((k[i] + self.rotate_right(l[i], 8)) & 0xFFFFFFFF) ^ i
            k_new = (self.rotate_left(k[i], 3) ^ l_new) & 0xFFFFFFFF
            l.append(l_new)
            k.append(k_new)
        return k

    def encrypt_block(self, plaintext, key_schedule):
        x = (plaintext >> 32) & 0xFFFFFFFF
        y = plaintext & 0xFFFFFFFF
        for k in key_schedule:
            x = (self.rotate_right(x, 8) + y) & 0xFFFFFFFF
            x ^= k
            y = self.rotate_left(y, 3) ^ x
        return (x << 32) | y

    def decrypt_block(self, ciphertext, key_schedule):
        x = (ciphertext >> 32) & 0xFFFFFFFF
        y = ciphertext & 0xFFFFFFFF
        for k in reversed(key_schedule):
            y = self.rotate_right(y ^ x, 3)
            x = (self.rotate_left((x ^ k), 8) - y) & 0xFFFFFFFF
        return (x << 32) | y

    def encrypt(self, plaintext):
        return self.encrypt_block(plaintext, self.key)

    def decrypt(self, ciphertext):
        return self.decrypt_block(ciphertext, self.key)

    @staticmethod
    def rotate_left(x, r):
        return ((x << r) & 0xFFFFFFFF) | (x >> (32 - r))

    @staticmethod
    def rotate_right(x, r):
        return (x >> r) | ((x << (32 - r)) & 0xFFFFFFFF)
