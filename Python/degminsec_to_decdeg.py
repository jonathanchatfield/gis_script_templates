import re
# One minute => 1' = (1/60)°
# One second => 1" = (1/3600)°

# Prompt for Degrees, minutes, and seconds (without symbols)

to_convert = (input("Enter Degrees, Minutes, and Seconds, separated by a space:"))

def conversion_to_dd(to_convert):
    # This uses regex to split on the characters between []
    split_result = re.split(r'[°\'\" ]', to_convert)
    # Remove empty strings from the result
    split_result = [item for item in split_result if item]
        # Convert to floats
    split_result = [float(item) for item in split_result]
    # Convert degrees, minutes, seconds to decimal degrees
    # degrees + (minutes/60) + (seconds/3600)
    if len(split_result) >= 1:
        degrees = split_result[0]
        minutes = split_result[1] / 60 if len(split_result) > 1 else 0
        seconds = split_result[2] / 3600 if len(split_result) > 2 else 0
        result = degrees + minutes + seconds
        return result
    
# print the result, rounded to 6 decimals for precision     
print(f"{conversion_to_dd(to_convert):6f}")



