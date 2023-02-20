# 1) Write a function that returns a float corresponding to the volume of a sphere: 
def get_sphere_volume(radius):
    "Calculates volume of a sphere given the radius"
    return (4/3)*3.14*radius**3


# 2) Write a function that calculates and returns an integer corresponding to the factorial of an integer (n):
    # a) Using recursivity
def recursive_factorial(n):
    "Calculates factorial of a given value n (using recursivity)"
    if n == 0:
        return 1
    else:
        return n * recursive_factorial(n-1)

    # b) Without recursivity
def factorial(n):
    "Calculates factorial of a given value n"
    fact = 1
    i=1
    if n >= 0:
        while 0 < i <= n:
            fact = fact * i
            i+=1
    return fact


# 3) Write a function for counting up numbers from 0 to n, showing the count up in thescreen. If parameter odd is set to True, prints only odd numbers:
    # a) Using recursivity
def recursive_count_up(n, odd=False, i=0):
    if i > n:
        return
    if odd and i % 2 == 0:
        recursive_count_up(n, odd, i+1)
    else:
        print(i)
        recursive_count_up(n, odd, i+1)
        
    # b) Without recursivity
def count_up(n,odd = False):
    i = 1
    while i <= n: 
      if odd and i % 2 != 0:
        print(i)
        i+=2
      elif not odd:
        print(i)
        i+=1
        

# 4) Find and solve the bugs in the following function:
# def get_final_price(discount_percentage=10, price):
#     """ Return the final price after applying the discount percentage """
#     return ((price+price) * percentage) / 100

# We have several bugs here:
# - The argument with default value needs to be after ones without default values
# - Function uses percentage instead of discount_percentage
# - The function doubles the price, which makes no sense
# - It is also calculating the discount itself, not the final price
# Then, a corrected function would be:
def get_final_price(price, discount_percentage=10):
    """Return the final price after applying the discount percentage"""
    return (price * (100 - discount_percentage)) / 100

