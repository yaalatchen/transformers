import csv

def GetDate(date_slashes, time):
    date_seperated = date_slashes.split('/')
    full_time = time
    if len(time) == 7:
        full_time = "0"+full_time
    new_date = date_seperated[2]+"-"+date_seperated[1]+"-"+date_seperated[0]+"T"+full_time
    return new_date

def GetTemperature(fahrenheit_temperature_string):
    if fahrenheit_temperature_string == ' ' or fahrenheit_temperature_string == '':
        return ' '
    fahrenheit_temperature = float(fahrenheit_temperature_string.split(' ')[0].split('Â')[0])
    celsius_temperature = (float(fahrenheit_temperature)-32)*5/9
    return celsius_temperature

def GetDirectionAngle(direction_string):
    if direction_string == ' ' or direction_string == '':
        return ' '
    direction_string = direction_string.lower()
    if direction_string == "n":
        return 360
    if direction_string.count("n") == 2 and direction_string.count("e") == 1:
        return 22.5
    if direction_string.count("n") == 1 and direction_string.count("e") == 1:
        return 45
    if direction_string.count("n") == 1 and direction_string.count("e") == 2:
        return 67.5
    if direction_string == "e":
        return 90
    if direction_string.count("s") == 1 and direction_string.count("e") == 2:
        return 112.5
    if direction_string.count("s") == 1 and direction_string.count("e") == 1:
        return 135
    if direction_string.count("s") == 2 and direction_string.count("e") == 1:
        return 157.5
    if direction_string == "s":
        return 180
    if direction_string.count("s") == 2 and direction_string.count("w") == 1:
        return 202.5
    if direction_string.count("s") == 1 and direction_string.count("w") == 1:
        return 225
    if direction_string.count("s") == 1 and direction_string.count("w") == 2:
        return 247.5
    if direction_string == "w":
        return 270
    if direction_string.count("n") == 1 and direction_string.count("w") == 2:
        return 292.5
    if direction_string.count("n") == 1 and direction_string.count("w") == 1:
        return 315
    if direction_string.count("n") == 2 and direction_string.count("w") == 1:
        return 337.5
    return ' '

def GetSpeed(speed_mph_string):
    if speed_mph_string == ' ' or speed_mph_string == '':
        return ' '
    speed_mph = float(speed_mph_string.split(' ')[0].split('Â')[0])
    speed_mps = speed_mph*0.447
    return speed_mps

def GetSkyCoverage(string_coverage):
    if string_coverage == ' ' or string_coverage == '':
        return ' '
    string_coverage = string_coverage.lower()
    if string_coverage.count("fair"):
        return 0.05
    if string_coverage.count("partly") == 1:
        return 0.32
    if string_coverage.count("mostly") == 1:
        return 0.55
    if string_coverage == "cloudy":
        return 0.87
    return ' '

def GetPressure(pressure_inch_string):
    if pressure_inch_string == ' ' or pressure_inch_string == '':
        return ' '
    pressure_inch = float(pressure_inch_string.split(' ')[0].split('Â')[0])
    pressure_hectopascal = pressure_inch*33.8639
    return pressure_hectopascal


if __name__ == "__main__":
    file_2010 = r"C:\Users\yczohar\Desktop\weather_underground_data\2010.csv"
    outfile_2010 = r"C:\Users\yczohar\Desktop\weather_underground_data\2010_extracted.csv"

    with open(file_2010, newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')

        header = "Time,Temperature,Dew_Point,Wind_Direction,Wind_Speed,Wind_Gust_Speed,Pressure,Sky_Coverage\n"

        is_first_line = True
        out_lines = []
        for l in lines:
            if is_first_line:
                is_first_line = False
                first_line = l
                out_lines.append(header)
            else:
                #data
                date = GetDate(l[0], l[1])
                temp = GetTemperature(l[2])
                dew = GetTemperature(l[3])
                wind_direction = GetDirectionAngle(l[5])
                wind_speed = GetSpeed(l[6])
                gust_speed = GetSpeed(l[7])
                pressure = GetPressure(l[8])
                sky_coverage = GetSkyCoverage(l[10])

                single_line = date + "," + str(temp) + "," + str(dew) + "," + str(wind_direction) + "," \
                               + str(wind_speed) + "," + str(gust_speed) + "," + str(pressure) + "," + str(sky_coverage) + "\n"
                out_lines.append(single_line)

        with open(outfile_2010, 'w') as f:
            f.writelines(out_lines)

