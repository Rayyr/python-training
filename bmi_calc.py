import sys

# weight validation
def check_weight(w):
    if w < 0:
        return False
    return True

# height validation
def check_height(h):
    if h <= 0:
        return False
    return True

def calculate_bmi(weight, height):
    return weight / (height * height)

# CLI function
def calcBMI():
    weight = int(input("Enter your weight in kilograms: "))
    if not check_weight(weight):
        print("Weight must be >= 0!")
        sys.exit()

    height = int(input("Enter your height in meters: "))
    if not check_height(height):
        print("Height must be > 0!")
        sys.exit()

    bmi = calculate_bmi(weight, height)
    print("BMI =", bmi)


def test_weight_valid():
    assert check_weight(70) == True

def test_weight_invalid():
    assert check_weight(-100) == False

def test_height_valid():
    assert check_height(1.75) == True

def test_height_zero():
    assert check_height(0) == False

def test_height_negative():
    assert check_height(-10) == False

 

# Only run when executed directly
if __name__ == "__main__":
    calcBMI()