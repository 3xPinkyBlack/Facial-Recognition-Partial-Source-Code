import os

i = 1
while i <= 100:
    os.rename("..\\FalsePhoto\\User.1163." + str(i) + ".png", str(i) + ".png")
    i = i + 1
