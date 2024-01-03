
def HighScoresFunc(newScore, newName):

    mylist = []

    #turns file into mylist-------------

    try:
        file = open("high_scores.txt" , "r") # open file
    
    except FileNotFoundError:
        file = open("high_scores.txt", "x") # if no file, create file and set to read
        file = open("high_scores.txt", "r")
        print("No score file found, score file created in game directory")
        
    finally:
        for line in file:
            mylist.append(line.strip().split(":"))
        
        file.close() # converting test file strings into a 2 dimensional list 
    
    
    # getting score and name-----------------
    
    score = newScore
    name = newName

        
    print("\nYour Score:\n"+(name)+"  "+str(score)+"\n")
    
    NameAndScore = [name, score]
    
    #adding name and score in correct place in full mylist
    
    Added = False
    if len(mylist) == 0:
        mylist.append(NameAndScore) # if list empty, then add to list
        Added = True
    else:
        count2 = 0
        for item in mylist: # adding above the item if greater, and continuing the loop if not.
            if score > int(item[1]):
                mylist.insert(count2, NameAndScore) # if score greater, insert in mylist then break
                Added = True
                break
            elif score <= int(item[1]):
                count2 += 1
                
    if Added == False: # if not greater than enything on the list, add to the end
        mylist.append(NameAndScore)
        
    
    # changing mylist into back into a formatted txt file... name:score 
    file = open("high_scores.txt", "w")   
    for item in mylist:
        nameAndScore_string = item[0] + ":" + str(item[1])
        file.writelines(nameAndScore_string)
        file.writelines("\n")
        
    
    file.close()

    return mylist[:12]