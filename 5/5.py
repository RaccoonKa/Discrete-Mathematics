import numpy as np


class CyclicCode:
    def __init__(self, n, k, generator_poly):
        self.n = n
        self.k = k
        self.r = n - k
        self.generator_poly = generator_poly
        self.g = [int(bit) for bit in generator_poly]
        self.g_degree = len(self.g) - 1
        self.G = self.build_systematic_generator_matrix()
        self.codewords = self.generate_all_codewords()
        self.d_min = self.calculate_min_distance()

    def poly_div(self, dividend, divisor):
        dividend = np.array(dividend, dtype=int)
        divisor = np.array(divisor, dtype=int)
        dividend = np.trim_zeros(dividend, 'f')
        divisor = np.trim_zeros(divisor, 'f')

        if len(dividend) < len(divisor):
            return dividend.copy()

        remainder = dividend.copy()
        for i in range(len(dividend) - len(divisor) + 1):
            if remainder[i] == 1:
                remainder[i:i + len(divisor)] ^= divisor

        remainder = np.trim_zeros(remainder, 'f')
        return remainder

    def build_systematic_generator_matrix(self):
        I_k = np.eye(self.k, dtype=int)
        C = []

        for i in range(self.k):
            x_power = np.zeros(self.k, dtype=int)
            x_power[i] = 1
            shifted = np.concatenate([x_power, np.zeros(self.r, dtype=int)])
            remainder = self.poly_div(shifted, self.g)
            if len(remainder) < self.r:
                remainder = np.concatenate([np.zeros(self.r - len(remainder), dtype=int), remainder])
            C.append(remainder)

        C = np.array(C, dtype=int)
        G = np.hstack([I_k, C])
        return G

    def encode(self, message):
        if len(message) != self.k:
            raise ValueError(f"Длина сообщения должна быть {self.k} бит")

        remainder = self.poly_div(np.concatenate([message, np.zeros(self.r, dtype=int)]), self.g)
        if len(remainder) < self.r:
            remainder = np.concatenate([np.zeros(self.r - len(remainder), dtype=int), remainder])
        return np.concatenate([message, remainder])

    def generate_all_codewords(self):
        codewords = []
        for i in range(2**self.k):
            message = np.array([int(bit) for bit in np.binary_repr(i, width=self.k)], dtype=int)
            codeword = self.encode(message)
            codewords.append(codeword)
        return codewords

    def calculate_min_distance(self):
        min_distance = self.n  # Инициализируем максимально возможным значением

        for i in range(len(self.codewords)):
            for j in range(i + 1, len(self.codewords)):
                distance = np.sum(self.codewords[i] != self.codewords[j])
                if distance < min_distance:
                    min_distance = distance

        return min_distance

    def decode(self, received):
        if len(received) != self.n:
            raise ValueError(f"Длина принятого слова должна быть {self.n} бит")

        remainder = self.poly_div(received, self.g)
        error_detected = np.any(remainder != 0)
        return error_detected, remainder

    def get_capabilities(self):
        detect = self.d_min - 1
        correct = (self.d_min - 1) // 2
        return detect, correct

    def generate_error_examples(self):
        message = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=int)
        codeword = self.encode(message)

        print("\n3. Примеры, иллюстрирующие свойства кода:")

        # Пример 1: Обнаружение одиночной ошибки
        error1 = np.zeros(self.n, dtype=int)
        error1[5] = 1
        received1 = (codeword + error1) % 2
        detected1, _ = self.decode(received1)
        print(f"\nПример 1: Обнаружение одиночной ошибки")
        print(f"Кодовое слово: {codeword}")
        print(f"Вектор ошибки: {error1}")
        print(f"Принятое слово: {received1}")
        print(f"Ошибка обнаружена: {detected1}")

        # Пример 2: Обнаружение двух ошибок
        error2 = np.zeros(self.n, dtype=int)
        error2[5] = 1
        error2[10] = 1
        received2 = (codeword + error2) % 2
        detected2, _ = self.decode(received2)
        print(f"\nПример 2: Обнаружение двух ошибок")
        print(f"Кодовое слово: {codeword}")
        print(f"Вектор ошибки: {error2}")
        print(f"Принятое слово: {received2}")
        print(f"Ошибка обнаружена: {detected2}")
        print("Код может исправить такую ошибку, так как количество ошибок ≤ t")

        # Пример 3: Ошибка, которую можно обнаружить, но не исправить
        t = (self.d_min - 1) // 2
        error_count = t + 1
        error3 = np.zeros(self.n, dtype=int)
        for i in range(error_count):
            error3[i*2] = 1
        received3 = (codeword + error3) % 2
        detected3, _ = self.decode(received3)
        print(f"\nПример 3: Ошибка, которую можно обнаружить, но не исправить")
        print(f"Кодовое слово: {codeword}")
        print(f"Вектор ошибки: {error3}")
        print(f"Принятое слово: {received3}")
        print(f"Ошибка обнаружена: {detected3}")

        return error3


n = 23  # общее число элементов
k = 12  # число информационных элементов
generator_poly = '11000110101'  # порождающий многочлен (11 бит)
code = CyclicCode(n, k, generator_poly)

print("1. Порождающая матрица G:")
print(code.G)

print("\nФрагмент множества кодовых слов (первые 5):")
for i in range(min(5, len(code.codewords))):
    print(f"Сообщение {i}: {code.codewords[i]}")

d_min = code.d_min
detect, correct = code.get_capabilities()
print(f"\n2. Характеристики кода:")
print(f"Минимальное расстояние кода: d_min = {d_min}")
print(f"Кратность гарантированно обнаруживаемых ошибок: {detect}")
print(f"Кратность гарантированно исправляемых ошибок: {correct}")

# 3. Примеры иллюстрирующие свойства кода и 4. Вектор ошибки
error_example = code.generate_error_examples()

print("\n4. Конкретный вектор ошибки, который код может обнаружить, но не может исправить:")
print(error_example)
