from decimal import Decimal

class Amount:
    def __init__(self, value):
        if isinstance(value, (float, int, str)):
            value = Decimal(str(value))
            self.whole = int(value)
            self.fraction = int((value - self.whole) * 100)
        elif isinstance(value, Decimal):
            self.whole = int(value)
            self.fraction = int((value - self.whole) * 100)
        else:
            raise ValueError("Invalid type for Amount")

    def __str__(self):
        return f"{self.whole}.{str(self.fraction).zfill(2)}"

    def __add__(self, other):
        if not isinstance(other, Amount):
            raise ValueError("Can only add Amount to Amount")
        
        new_whole = self.whole + other.whole
        new_fraction = self.fraction + other.fraction
        
        if new_fraction >= 100:
            new_whole += new_fraction // 100
            new_fraction = new_fraction % 100
        
        return Amount(f"{new_whole}.{str(new_fraction).zfill(2)}")

    def __sub__(self, other):
        if not isinstance(other, Amount):
            raise ValueError("Can only subtract Amount from Amount")
        
        new_whole = self.whole - other.whole
        new_fraction = self.fraction - other.fraction
        
        if new_fraction < 0:
            new_whole -= 1
            new_fraction += 100
        
        return Amount(f"{new_whole}.{str(new_fraction).zfill(2)}")

    def __mul__(self, other):
        if not isinstance(other, (Decimal, float, int)):
            raise ValueError("Can only multiply Amount by a number")
        
        total_amount = Decimal(f"{self.whole}.{str(self.fraction).zfill(2)}") * Decimal(str(other))
        return Amount(total_amount)

    def __truediv__(self, other):
        if not isinstance(other, (Decimal, float, int)):
            raise ValueError("Can only divide Amount by a number")
        
        total_amount = Decimal(f"{self.whole}.{str(self.fraction).zfill(2)}") / Decimal(str(other))
        return Amount(total_amount)

    def __eq__(self, other):
        return self.whole == other.whole and self.fraction == other.fraction

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.whole == self.whole:
            return self.fraction < other.fraction
        return self.whole < other.whole

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)
