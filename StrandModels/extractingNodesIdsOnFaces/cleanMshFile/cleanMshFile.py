a_file = open("cylinder.msh", "r")
lines = a_file.readlines()
a_file.close()

nlines = len(lines)
i = 0
lineToDel = []
while i < nlines:
    if "$PhysicalNames" in lines[i]:
        while not "$EndPhysicalNames" in lines[i]:
            lineToDel.append(i)
            i += 1
        lineToDel.append(i)
        break
    i+=1

for l in lineToDel:
    print(lines[l])

del lines[lineToDel[0]:lineToDel[-1]]

new_file = open("cylinderCleaned.msh", "w+")
for line in lines:
    new_file.write(line)

new_file.close()
