import csv

valid_data_codes = ['0', '1', '4', '5', 'C', 'M']
def ExtractValueFromTwoValueSection(section_name, name, section):
    # print (section)
    split_section = section.split(',')
    if section_name != name or len(split_section) != 2 or split_section[1] not in valid_data_codes or split_section[1] == '+9999' or split_section[1] == '99999':
        return (' ', False)
    value = float(int(split_section[0]))/10.0
    # print(value)
    return (value, True)

def GetWindDirection(section_name, name, section):
    # print(section)
    split_section = section.split(',')
    if section_name != name or len(split_section) != 5 or split_section[1] not in valid_data_codes:
        return (' ', False)
    angle = int(split_section[0])
    # print(angle)
    return (angle, True)

def GetWindSpeed(section_name, name, section):
    # print(section)
    split_section = section.split(',')
    if section_name != name or len(split_section) != 5 or split_section[4] not in valid_data_codes:
        return (' ', False)
    speed = float(int(split_section[3]))/10.0
    # print(speed)
    return (speed, True)

def GetPercipitation(section_name, name, section):
    # print(section)
    split_section = section.split(',')
    if section_name != name or len(split_section) != 4 or split_section[3] not in valid_data_codes:
        return (' ', False)
    depth = float(int(split_section[1])) / 10.0
    return (depth, True)

def GetSkyCoverage(section_name, name, section):
    # print(section)
    split_section = section.split(',')
    if section_name != name or len(split_section) != 6 or split_section[1] not in valid_data_codes or split_section[0] == "99" :
        return (' ', False)
    if split_section[0] == "00":
        return (0.0, True)
    if split_section[0] == "01":
        return (0.1, True)
    if split_section[0] == "02":
        return (0.25, True)
    if split_section[0] == "03":
        return (0.4, True)
    if split_section[0] == "04":
        return (0.5, True)
    if split_section[0] == "05":
        return (0.6, True)
    if split_section[0] == "06":
        return (0.75, True)
    if split_section[0] == "07":
        return (0.95, True)
    if split_section[0] == "08":
        return (1.0, True)
    return (' ', False)


if __name__ == '__main__':
    base_directory = r"C:\Users\yczohar\Desktop\weather_underground_data"

    filename = []
    outfile = []
    dateTime_index = []                        #"DATE"
    temperature_index = []                     #"TMP"
    dew_point_index = []                       #"DEW"
    humidity_index = []                        #"DEW"
    wind_direction_index = []                  #"WND"
    wind_speed_index = []                      #"WND"
    wind_gust_index = []                       #"OC1"
    pressure_index = []                        #"SLP"
    percipitation_depth_index = []             #"AA1", "AA2", "AA3"
    sky_coverage_index = []                    # "GA1", "GA2", "GA3", "GA4"

    filename.append(base_directory + r"/2006.csv")
    outfile.append(base_directory + r"/2006_extracted.csv")
    dateTime_index.append(1)
    temperature_index.append(13)
    dew_point_index.append(14)
    humidity_index.append(14)
    wind_direction_index.append(10)
    wind_speed_index.append(10)
    wind_gust_index.append(40)
    pressure_index.append(15)
    percipitation_depth_index.append([16, 17, 18])
    sky_coverage_index.append([25, 26, 27, 28])

    filename.append(base_directory + r"/2007.csv")
    outfile.append(base_directory + r"/2007_extracted.csv")
    dateTime_index.append(1)
    temperature_index.append(13)
    dew_point_index.append(14)
    humidity_index.append(14)
    wind_direction_index.append(10)
    wind_speed_index.append(10)
    wind_gust_index.append(41)
    pressure_index.append(15)
    percipitation_depth_index.append([16, 17, 18])
    sky_coverage_index.append([25, 26, 27, 28])

    filename.append(base_directory + r"/2008.csv")
    outfile.append(base_directory + r"/2008_extracted.csv")
    dateTime_index.append(1)
    temperature_index.append(13)
    dew_point_index.append(14)
    humidity_index.append(14)
    wind_direction_index.append(10)
    wind_speed_index.append(10)
    wind_gust_index.append(40)
    pressure_index.append(15)
    percipitation_depth_index.append([16, 17, 18])
    sky_coverage_index.append([26, 27 ,28 ,29])

    filename.append(base_directory + r"/2009.csv")
    outfile.append(base_directory + r"/2009_extracted.csv")
    dateTime_index.append(1)
    temperature_index.append(13)
    dew_point_index.append(14)
    humidity_index.append(14)
    wind_direction_index.append(10)
    wind_speed_index.append(10)
    wind_gust_index.append(40)
    pressure_index.append(15)
    percipitation_depth_index.append([16, 17, 18])
    sky_coverage_index.append([25, 26, 27, 28])

    header = "Time,Temperature,Dew_Point,Wind_Direction,Wind_Speed,Wind_Gust_Speed,Pressure,Sky_Coverage\n"

    for i in range(len(filename)):
        with open(filename[i], newline='') as csvfile:
            lines = csv.reader(csvfile, delimiter=',', quotechar='"')
            is_first_line = True
            first_line = ""
            out_lines = []

            for l in lines:
                if is_first_line:
                    is_first_line = False
                    first_line = l
                    out_lines.append(header)
                else:
                    single_line = ""
                    single_line += l[dateTime_index[i]] + ","

                    #temperature
                    (temperature, is_okay) = ExtractValueFromTwoValueSection(first_line[temperature_index[i]], "TMP", l[temperature_index[i]])
                    if not is_okay:
                        pass #print("ERROR temperature ", l[temperature_index[i]], l[dateTime_index[i]])
                    single_line += str(temperature) + ","

                    #dew point
                    (dew, is_okay) = ExtractValueFromTwoValueSection(first_line[dew_point_index[i]], "DEW", l[dew_point_index[i]])
                    if not is_okay:
                        pass #print("ERROR dew ", l[dew_point_index[i]], l[dateTime_index[i]])
                    single_line += str(dew) + ","

                    #Wind_Direction
                    (wind_direction, is_okay) = GetWindDirection(first_line[wind_direction_index[i]], "WND", l[wind_direction_index[i]])
                    if not is_okay:
                        pass #print("ERROR wind direction ", l[wind_direction_index[i]], l[dateTime_index[i]])
                    single_line += str(wind_direction) + ","

                    #Wind_Speed
                    (wind_speed, is_okay) = GetWindSpeed(first_line[wind_speed_index[i]], "WND", l[wind_speed_index[i]])
                    if not is_okay:
                        pass #print("ERROR wind speed ", l[wind_speed_index[i]], l[dateTime_index[i]])
                    single_line += str(wind_speed) + ","

                    #Wind_Gust_Speed
                    (wind_gust_speed, is_okay) = ExtractValueFromTwoValueSection(first_line[wind_gust_index[i]], "OC1", l[wind_gust_index[i]])
                    if not is_okay:
                        wind_gust_speed = 0.0
                    single_line += str(wind_gust_speed) + ","

                    #Pressure
                    (pressure, is_okay) = ExtractValueFromTwoValueSection(first_line[pressure_index[i]], "SLP", l[pressure_index[i]])
                    if not is_okay:
                        pass #print("ERROR pressure ", l[pressure_index[i]], l[dateTime_index[i]])
                    single_line += str(pressure) + ","

                    #sky coverage
                    (coverage_0, is_okay_0) = GetSkyCoverage(first_line[sky_coverage_index[i][0]], "GA1", l[sky_coverage_index[i][0]])
                    (coverage_1, is_okay_1) = GetSkyCoverage(first_line[sky_coverage_index[i][1]], "GA2", l[sky_coverage_index[i][1]])
                    (coverage_2, is_okay_2) = GetSkyCoverage(first_line[sky_coverage_index[i][2]], "GA3", l[sky_coverage_index[i][2]])
                    (coverage_3, is_okay_3) = GetSkyCoverage(first_line[sky_coverage_index[i][3]], "GA4", l[sky_coverage_index[i][3]])

                    coverage_sum = 0.0
                    coverage_num = 0.0
                    if is_okay_0:
                        coverage_sum += coverage_0
                        coverage_num += 1
                    if is_okay_1:
                        coverage_sum += coverage_1
                        coverage_num += 1
                    if is_okay_2:
                        coverage_sum += coverage_2
                        coverage_num += 1
                    if is_okay_3:
                        coverage_sum += coverage_3
                        coverage_num += 1

                    coverage_mean = ' '
                    if coverage_num > 0:
                        coverage_mean = coverage_sum / coverage_num

                    single_line += str(coverage_mean) + "\n"

                    out_lines.append(single_line)

            with open(outfile[i], 'w') as f:
                f.writelines(out_lines)

                    # #Percipitation
                    # (percipitation_depth_0, is_okay_0) = GetPercipitation(first_line[percipitation_depth_index[i][0]], "AA1", l[percipitation_depth_index[i][0]], prev_percp_AA1)
                    # (percipitation_depth_1, is_okay_1) = GetPercipitation(first_line[percipitation_depth_index[i][1]], "AA2", l[percipitation_depth_index[i][1]], prev_percp_AA2)
                    # (percipitation_depth_2, is_okay_2) = GetPercipitation(first_line[percipitation_depth_index[i][2]], "AA3", l[percipitation_depth_index[i][2]], prev_percp_AA3)
                    # if ((is_okay_2 and percipitation_depth_2 >= 6) and (is_okay_1 and percipitation_depth_1 >= 6) and (is_okay_0 and percipitation_depth_0 >= 6)):
                    #     print(l[dateTime_index[i]])
                    #     print(l[percipitation_depth_index[i][0]])
                    #     print(l[percipitation_depth_index[i][1]])
                    #     print(l[percipitation_depth_index[i][2]])
                    #     a = 0
                    # percp =  (percipitation_depth_0 + percipitation_depth_1 + percipitation_depth_2)/3
                    # if not is_okay:
                    #     continue
                    # single_line += str(percp) + "\n"

                    # out_lines.append(single_line)
