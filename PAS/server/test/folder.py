import os


folder = '../images/video/1'

for filename in os.walk(folder):
        print(filename)