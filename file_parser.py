from io import BytesIO

with open("data.1d", "rb") as input:
    
    print(input)
    
    
    output = open("output.csv", "wb")
    #print(output)


    file_like_b = input.read()
    o = file_like_b.decode('ansi')

    file_like = BytesIO(file_like_b)
    output.write(o)
    #output.close()
