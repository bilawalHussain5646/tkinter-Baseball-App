# -*- coding: utf-8 -*-
import mysql.connector
import tkinter as tkr
from tkinter import ttk
from tkinter import *


option = 0


master = tkr.Tk()
master.geometry("500x500")
master.title("MLB Players")
main_frame = Frame(master)
main_frame.pack(fill=BOTH, expand=1)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

second_frame = Frame(my_canvas)
my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

third_frame = Frame(my_canvas,width=500,height=500,background="bisque")
my_canvas.create_window((500, 200), window=third_frame,anchor='nw')

def OptionSelected(option, var_):
    cnx = mysql.connector.connect(user='root', database='lahmansbaseballdb', host='127.0.0.1',
                                  password='')  # MySql Connection
    for widget in third_frame.winfo_children():
        widget.destroy()

    my_conn = cnx.cursor()
    if (option == 1):
        var_batter = var_.get().split(', ')
        var_batter[1] = '%' + var_batter[1] + '%'
        Team = str(var_batter[1])



        player : list = []
        e = Label(third_frame, text='Player Stats', relief='flat', anchor='w',)
        e.configure(font=("Arial", 12), fg='#0275d8')
        e.grid(row=0, column=0,)
        ####### end of connection ####
        my_conn.execute(
            "SELECT playerID, teamID, H/AB as 'AVG', (H+BB+HBP)/(AB+BB+HBP+SF) as 'OBP', ((H-2B-3B-HR)+(2B*2)+(3B*3)+(HR*4))/AB as 'SLG',(H+BB+HBP)/(AB+BB+HBP+SF) + ((H-2B-3B-HR)+(2B*2)+(3B*3)+(HR*4))/AB as 'OPS' FROM batting WHERE yearID=2019 && AB>=400 && playerID=(SELECT playerID FROM `people` WHERE CONCAT(nameFirst,' ',nameLast) = '%s' AND playerID IN (select playerID from batting where teamID LIKE '%s'))" % (
            var_batter[0],Team))
        e = Label(third_frame, width=10, text='playerID', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c', fg='#f7f7f7')
        e.grid(row=0, column=1)
        e = Label(third_frame, width=10, text='teamID', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c', fg='#f7f7f7')
        e.grid(row=0, column=2)
        e = Label(third_frame, width=10, text='AVG', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c', fg='#f7f7f7')
        e.grid(row=0, column=3)
        e = Label(third_frame, width=10, text='OBP', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c', fg='#f7f7f7')
        e.grid(row=0, column=4)
        e = Label(third_frame, width=10, text='SLG', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c', fg='#f7f7f7')
        e.grid(row=0, column=5)
        e = Label(third_frame, width=10, text='OPS', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=0, column=6)
        i = 1
        k = 1
        for specific_data in my_conn:
            k = 1
            for j in range(len(specific_data)):
                e1 = Entry(third_frame, width=10, fg='blue')
                e1.grid(row=i, column=k)
                e1.insert(END, specific_data[j])
                player.append(specific_data[j])
                k = k + 1
            i = i + 1
        print("Batter Selected")

        e = Label(third_frame, text='League Stats', relief='flat', anchor='w',)
        e.configure(font=("Arial", 12), fg='#0275d8')
        e.grid(row=4, column=0,pady=(10, 0))
        my_conn.execute(
            "SELECT AVG((H/AB)) as 'LgAVG', AVG((H+BB+HBP)/(AB+BB+HBP+SF)) as 'LgOBP', AVG(((H-2B-3B-HR)+(2B*2)+(3B*3)+(HR*4))/AB) as 'LgSLG' , AVG((H+BB+HBP)/(AB+BB+HBP+SF) + ((H-2B-3B-HR)+(2B*2)+(3B*3)+(HR*4))/AB) as 'LgOPS' FROM batting where yearID=2019;")

        e = Label(third_frame, width=10, text='LgAVG', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=4, column=1,pady=(10, 2))
        e = Label(third_frame, width=10, text='LgOBP', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=4, column=2,pady=(10, 2))
        e = Label(third_frame, width=10, text='LgSLG', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=4, column=3,pady=(10, 2))
        e = Label(third_frame, width=10, text='LgOPS', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=4, column=4,pady=(10, 2))

        i = 5
        k = 1
        league_avg: list = []
        for specific_data in my_conn:
            k = 1
            for j in range(len(specific_data)):
                e1 = Entry(third_frame, width=10, fg='blue')
                e1.grid(row=i, column=k)
                e1.insert(END, specific_data[j])
                league_avg.append(specific_data[j])
                k = k + 1
            i = i + 1


       # check average and player stats

        if (float(player[2]) >= float(league_avg[0]) or float(player[3]) >= float(league_avg[1]) or float(player[4]) >= float(league_avg[2]) or float(player[5]) >= float(league_avg[3])):
            # print average player
            text = 'HE IS AVERAGE PLAYER'
            e = Label(third_frame, text=text, relief='flat', anchor='w', )
            e.configure(font=("Arial", 10), fg='#5cb85c', width=35)
            e.grid(row=7, column=1, pady=(15,0),columnspan=3)
        else:
            text = "HE IS NOT AVERAGE PLAYER"
            e = Label(third_frame, text=text, relief='flat', anchor='w', )
            e.configure(font=("Arial", 10), fg='#d9534f', width=35)
            e.grid(row=7, column=1, pady=(15,0), columnspan=3)


            # print not average player



    # Batter conditions above ---------------------------
    elif (option == 2):

        var_pitcher = var_.get().split(', ')
        print (var_pitcher[1])
        var_pitcher[1] = '%' + var_pitcher[1] + '%'
        Team = str(var_pitcher[1])
        e = Label(third_frame, text='Player Stats', relief='flat', anchor='w', )
        e.configure(font=("Arial", 12), fg='#0275d8')
        e.grid(row=0, column=0, )
        ####### end of connection ####
        my_conn.execute(
            "SELECT playerID, teamID, ERA, (BB+H)/(IPouts*.333) as 'WHIP', SO/BB as 'KtoBB_Ratio' FROM pitching WHERE yearID=2019 && G>=25 && ERA<=5.00 && playerID=(SELECT playerID FROM `people` WHERE CONCAT(nameFirst,' ',nameLast) = '%s' AND playerID IN (select playerID from pitching where teamID LIKE '%s'))" % (
                var_pitcher[0], Team))

        e = Label(third_frame, width=10, text='playerID', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=0, column=1)
        e = Label(third_frame, width=10, text='teamID', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=0, column=2)
        e = Label(third_frame, width=10, text='ERA', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=0, column=3)
        e = Label(third_frame, width=10, text='WHIP', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=0, column=4)
        e = Label(third_frame, width=10, text='KtoBB_Ratio', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=0, column=5)


        i = 1
        k = 1
        player : list = []
        for specific_data in my_conn:
            k = 1
            for j in range(len(specific_data)):
                    e1 = Entry(third_frame, width=10, fg='blue')
                    e1.grid(row=i, column=k)
                    e1.insert(END, specific_data[j])
                    player.append(specific_data[j])
                    k = k + 1
            i = i + 1

        e = Label(third_frame, text='League Stats', relief='flat', anchor='w', )
        e.configure(font=("Arial", 12), fg='#0275d8')
        e.grid(row=4, column=0, pady=(10, 0))

        my_conn.execute(
            "select AVG(ERA) as 'LgERA', AVG((BB+H)/(IPouts*.333)) as 'LgWHIP', AVG(SO/BB) as 'LgK/BB Ratio' from pitching Where yearID=2019;")

        e = Label(third_frame, width=10, text='LgERA', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=4, column=1, pady=(10, 2))
        e = Label(third_frame, width=10, text='LgWHIP', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=4, column=2, pady=(10, 2))
        e = Label(third_frame, width=10, text='LgK/BB Ratio', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',fg='#f7f7f7')
        e.grid(row=4, column=3, pady=(10, 2))

        i = 5
        k = 1
        league_avg: list = []
        for specific_data in my_conn:
            k = 1
            for j in range(len(specific_data)):
                e1 = Entry(third_frame, width=10, fg='blue')
                e1.grid(row=i, column=k)
                e1.insert(END, specific_data[j])
                league_avg.append(specific_data[j])
                k = k + 1
            i = i + 1
        # Average calculated -----

        # check average and player stats
        if player==[]:
            print("NO DATA FOUND")
        else:
            if (float(player[2]) >= float(league_avg[0]) or float(player[3]) >= float(league_avg[1]) or float(player[4]) >= float(league_avg[2])):
                text = 'HE IS AVERAGE PLAYER'
                e = Label(third_frame, text=text, relief='flat', anchor='w', )
                e.configure(font=("Arial", 10), fg='#5cb85c', width=35)
                e.grid(row=7, column=1, pady=(15, 0), columnspan=3)
            else:
                text = "HE IS NOT AVERAGE PLAYER"
                e = Label(third_frame, text=text, relief='flat', anchor='w', )
                e.configure(font=("Arial", 10), fg='#d9534f', width=35)
                e.grid(row=7, column=1, pady=(15, 0), columnspan=3)

                # print not average player


        #-------------------------------
        print("Pitcher Selected")




    # Pitcher Conditions above -----------------------------------
    elif (option == 3):

        var_team = var_.get()


        Team = str(var_team)
        e = Label(third_frame, text='Team Stats', relief='flat', anchor='w', )
        e.configure(font=("Arial", 12), fg='#0275d8')
        e.grid(row=0, column=0)
        ####### end of connection ####
        my_conn.execute(
            "SELECT teamID, W as 'WINS' FROM teams WHERE yearID=2019 && franchID=(select franchID from teamsfranchises where franchName LIKE '%s')" % (
                    Team,))
        e = Label(third_frame, width=10, text='TeamID', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=0, column=1)
        e = Label(third_frame, width=10, text='Wins', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=0, column=2)

        i = 1
        k = 1
        team_ID : list = []
        for specific_data in my_conn:
            k = 1
            for j in range(len(specific_data)):
                e1 = Entry(third_frame, width=10, fg='blue')
                e1.grid(row=i, column=k)
                e1.insert(END, specific_data[j])
                team_ID.append(specific_data[j])

                k = k + 1
            i = i + 1
        teamID = team_ID[0]
        e = Label(third_frame, text='Pitcher AVG', relief='flat', anchor='w', )
        e.configure(font=("Arial", 12), fg='#0275d8')
        e.grid(row=4, column=0, pady=(10, 0))

        my_conn.execute(
            "select AVG(ERA) as 'LgERA', AVG((BB+H)/(IPouts*.333)) as 'LgWHIP', AVG(SO/BB) as 'LgK/BB Ratio' from pitching Where yearID=2019;")

        e = Label(third_frame, width=10, text='LgERA', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=4, column=1, pady=(10, 2))
        e = Label(third_frame, width=10, text='LgWHIP', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=4, column=2, pady=(10, 2))
        e = Label(third_frame, width=10, text='LgK/BB Ratio', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=4, column=3, pady=(10, 2))

        i = 5
        k = 1
        league_avg: list = []
        for specific_data in my_conn:
            k = 1
            for j in range(len(specific_data)):
                e1 = Entry(third_frame, width=10, fg='blue')
                e1.grid(row=i, column=k)
                e1.insert(END, specific_data[j])
                league_avg.append(specific_data[j])
                k = k + 1
            i = i + 1

        # Average calculated -----

        e = Label(third_frame, text='Pitcher Stats', relief='flat', anchor='w', )
        e.configure(font=("Arial", 12), fg='#0275d8')
        e.grid(row=7, column=0)
        my_conn.execute(
            "SELECT playerID, teamID, ERA, (BB+H)/(IPouts*.333) as 'WHIP', SO/BB as 'KtoBB_Ratio' FROM pitching WHERE yearID=2019 && G>=25 && ERA<=5.00 && teamID='%s'" % (
               teamID,))

        e = Label(third_frame, width=10, text='playerID', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=7, column=1, pady=(10, 2))
        e = Label(third_frame, width=10, text='teamID', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=7, column=2, pady=(10, 2))
        e = Label(third_frame, width=10, text='ERA', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=7, column=3, pady=(10, 2))
        e = Label(third_frame, width=10, text='WHIP', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=7, column=4, pady=(10, 2))
        e = Label(third_frame, width=10, text='KtoBB_Ratio', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=7, column=5, pady=(10, 2))


        i = 8
        k = 1
        player: list = []
        for specific_data in my_conn:
            k = 1
            if (float(specific_data[2]) >= float(league_avg[0]) or float(specific_data[3]) >= float(league_avg[1]) or float(
                        specific_data[4]) >= float(league_avg[2])):
                    # print average player
                for j in range(len(specific_data)):
                    e1 = Entry(third_frame, width=10, fg='blue')
                    e1.grid(row=i, column=k)
                    e1.insert(END, specific_data[j])
                    k = k + 1

            i = i + 1

        e = Label(third_frame, text='Batter AVG', relief='flat', anchor='w', )
        e.configure(font=("Arial", 12), fg='#0275d8')
        e.grid(row=23, column=0)
        my_conn.execute(
            "SELECT AVG((H/AB)) as 'LgAVG', AVG((H+BB+HBP)/(AB+BB+HBP+SF)) as 'LgOBP', AVG(((H-2B-3B-HR)+(2B*2)+(3B*3)+(HR*4))/AB) as 'LgSLG' , AVG((H+BB+HBP)/(AB+BB+HBP+SF) + ((H-2B-3B-HR)+(2B*2)+(3B*3)+(HR*4))/AB) as 'LgOPS' FROM batting where yearID=2019;")

        e = Label(third_frame, width=10, text='LgAVG', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=23, column=1, pady=(10, 2))
        e = Label(third_frame, width=10, text='LgOBP', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=23, column=2, pady=(10, 2))
        e = Label(third_frame, width=10, text='LgSLG', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=23, column=3, pady=(10, 2))
        e = Label(third_frame, width=10, text='LgOPS', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=23, column=4, pady=(10, 2))

        i = 24
        k = 1
        league_avg: list = []
        for specific_data in my_conn:
            k = 1
            for j in range(len(specific_data)):
                e1 = Entry(third_frame, width=10, fg='blue')
                e1.grid(row=i, column=k)
                e1.insert(END, specific_data[j])
                league_avg.append(specific_data[j])
                k = k + 1
            i = i + 1

        e = Label(third_frame, text='Batter Stats', relief='flat', anchor='w', )
        e.configure(font=("Arial", 12), fg='#0275d8')
        e.grid(row=27, column=0, )
        ####### end of connection ####
        my_conn.execute(
            "SELECT playerID, teamID, H/AB as 'AVG', (H+BB+HBP)/(AB+BB+HBP+SF) as 'OBP', ((H-2B-3B-HR)+(2B*2)+(3B*3)+(HR*4))/AB as 'SLG',(H+BB+HBP)/(AB+BB+HBP+SF) + ((H-2B-3B-HR)+(2B*2)+(3B*3)+(HR*4))/AB as 'OPS' FROM batting WHERE yearID=2019 && AB>=400 && teamID='%s'" % (
               teamID,))
        e = Label(third_frame, width=10, text='playerID', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=27, column=1, pady=(10, 2))
        e = Label(third_frame, width=10, text='teamID', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=27, column=2, pady=(10, 2))
        e = Label(third_frame, width=10, text='AVG', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=27, column=3, pady=(10, 2))
        e = Label(third_frame, width=10, text='OBP', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=27, column=4, pady=(10, 2))
        e = Label(third_frame, width=10, text='SLG', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=27, column=5, pady=(10, 2))
        e = Label(third_frame, width=10, text='OPS', borderwidth=2, relief='ridge', anchor='w', bg='#292b2c',
                  fg='#f7f7f7')
        e.grid(row=27, column=6, pady=(10, 2))
        i = 28
        k = 1
        for specific_data in my_conn:
            k = 1
            if (float(specific_data[2]) >= float(league_avg[0]) or float(specific_data[3]) >= float(league_avg[1]) or float(specific_data[4]) >= float(league_avg[2]) or float(specific_data[4]) >= float(league_avg[3])):
                # print average player
                for j in range(len(specific_data)):
                    e1 = Entry(third_frame, width=10, fg='blue')
                    e1.grid(row=i, column=k)
                    e1.insert(END, specific_data[j])
                    k = k + 1

            i = i + 1


        print("Team Selected")
    else:
        print("Nothing selected")



b1 = 'Adam Eaton, WAS'
b2 = 'Adam Frazier, PIT'
b3 = 'Adam Jones, ARI'
b4 = 'Albert Pujols, LAA'
b5 = 'Aldaberto Mondessi, KC'
b6 = 'Alex Bregman, HOU'
b7 = 'Alex Gordon, KC'
b8 = 'Amed Rosario, NYM'
b9 = 'Andrew Benintendi, BOS'
b10 = 'Anthony Rendon, WAS'
b11 = 'Anthony Rizzo, CHC'
b12 = 'Austin Meadows, TB'
b13 = 'Avisail Garcia, TB'
b14 = 'Brandon Belt, SF'
b15 = 'Brandon Crawford, SF'
b16 = 'Brandon Drury, TOR'
b17 = 'Brett Gardner, NYY'
b18 = 'Brian Anderson, MIA'
b19 = 'Brian Dozier, WAS'
b20 = 'Brian Goodwin, LAA'
b21 = 'Bryan Reynolds, PIT'
b22 = 'Bryce Harper, PHI'
b23 = 'Buster Posey, SF'
b24 = 'Carlos Santana, CLE'
b25 = 'Cesar Hernandez, PHI'
b26 = 'Charlie Blackmon, COL'
b27 = 'Christian Vazquez, BOS'
b28 = 'Christian Walker, ARI'
b29 = 'Christian Yelich, MIL'
b30 = 'CJ Cron, MIN'
b31 = 'Cody Bellinger, LAD'
b32 = 'Colin Moran, PIT'
b33 = 'Corey Seager, LAD'
b34 = 'Daniel Murphy, COL'
b35 = 'Danny Santana, TEX'
b36 = 'Dansby Swanson, ATL'
b37 = 'David Fletcher, LAA'
b38 = 'David Vogelsong, SEA'
b39 = 'Dexter Fowler, STL'
b40 = 'DJ LeMahieu, NYY'
b41 = 'Domingo Santana, SEA'
b42 = 'Eduardo Escobar, ARI'
b43 = 'Edwin Rosario, MIN'
b44 = 'Eloy Jimenez, CHW'
b45 = 'Elvis Andrus, TEX'
b46 = 'Enrique Hernandez, LAD'
b47 = 'Eric Hosmer, SD'
b48 = 'Eugenio Suarez, CIN'
b49 = 'Evan Longoria, SF'
b50 = 'Francisco Lindor, CLE'
b51 = 'Freddie Freeman, ATL'
b52 = 'Freddy Galvis, TOR'
b53 = 'George Springer, HOU'
b54 = 'Gio Urshela, NYY'
b55 = 'Gleyber Torres, NYY'
b56 = 'Hansel Alberto, BAL'
b57 = 'Harold Ramirez, MIA'
b58 = 'Hunter Dozier, KC'
b59 = 'Hunter Renfroe, SD'
b60 = 'Ian Desmond, COL'
b61 = 'Jackie Bradley Jr., BOS'
b62 = 'James McCann, CHC'
b63 = 'Jarrod Dyson, ARI'
b64 = 'Jason Heyward, CHC'
b65 = 'Jason Kipnis, CLE'
b66 = 'Javier Baez, CHC'
b67 = 'JD Davis, NYM'
b68 = 'JD Martinez, BOS'
b69 = 'Jean Segura, PHI'
b70 = 'Jeff McNeil, NYM'
b71 = 'Ji-Man Choi, TB'
b72 = 'Joc Pederson, LAD'
b73 = 'Joey Votto, CIN'
b74 = 'Jonathan Schoop, MIN'
b75 = 'Jonathan Villar, BAL'
b76 = 'Jorge Alfaro, MIA'
b77 = 'Jorge Polanco, MIN'
b78 = 'Jorge Soler, KC'
b79 = 'Jose Abreu, CHW'
b80 = 'Jose Altuve, HOU'
b81 = 'Jose Iglesias, CIN'
b82 = 'Jose Ramirez, CLE'
b83 = 'Josh Bell, PIT'
b84 = 'Josh Donaldson, ATL'
b85 = 'Josh Reddick, HOU'
b86 = 'JT Realmuto, PHI'
b87 = 'Juan Soto, WAS'
b88 = 'Jurickson Profar, OAK'
b89 = 'Justin Smoak, TOR'
b90 = 'Justin Turner, LAD'
b91 = 'Ketel Marte, ARI'
b92 = 'Kevin Kiermaier, TB'
b93 = 'Kevin Newman, PIT'
b94 = 'Kevin Pillar, SF'
b95 = 'Khris Davis, OAK'
b96 = 'Kole Calhoun, LAA'
b97 = 'Kolten Wong, STL'
b98 = 'Kris Bryant, CHC'
b99 = 'Kyle Schwarber, CHC'
b100 = 'Leury Garcia, CHW'
b101 = 'Lorenzo Cain, MIL'
b102 = 'Luke Voit, NYY'
b103 = 'Mallex Smith, SEA'
b104 = 'Manny Machado, SD'
b105 = 'Marcell Ozuna, STL'
b106 = 'Marcus Semien, OAK'
b107 = 'Mark Canha, OAK'
b108 = 'Marwin Gonzalez, MIN'
b109 = 'Matt Carpenter, STL'
b110 = 'Matt Chapman, OAK'
b111 = 'Matt Olson, OAK'
b112 = 'Max Kepler, MIN'
b113 = 'Max Muncy, LAD'
b114 = 'Michael Brantley, HOU'
b115 = 'Michael Conforto, NYM'
b116 = 'Miguel Cabrera, DET'
b117 = 'Miguel Rojas, MIA'
b118 = 'Mike Moustakas, MIL'
b119 = 'Mike Trout, LAA'
b120 = 'Mookie Betts, BOS'
b121 = 'Nelson Cruz, MIN'
b122 = 'Nick Ahmed, ARI'
b123 = 'Nick Castellanos, DET'
b124 = 'Nick Markakis, ATL'
b125 = 'Nico Goodrum, DET'
b126 = 'Nolan Arenado, COL'
b127 = 'Nomar Mazara, TEX'
b128 = 'Omar Narvaez, SEA'
b129 = 'Orlando Arcia, MIL'
b130 = 'Oscar Mercado, CLE'
b131 = 'Ozzie Albies, ATL'
b132 = 'Paul DeJong, STL'
b133 = 'Paul Goldschmidt, STL'
b134 = 'Pete Alonso, NYM'
b135 = 'Rafael Devers, BOS'
b136 = 'Raimel Tapia, COL'
b137 = 'Ramon Laureano, OAK'
b138 = 'Randall Grichuk, TOR'
b139 = 'Renato Nunez, BAL'
b140 = 'Rhys Hoskins, PHI'
b141 = 'Robbie Grossman, OAK'
b142 = 'Ronald Acuna, ATL'
b143 = 'Rougned Odor, TEX'
b144 = 'Ryan Braun, MIL'
b145 = 'Ryan McMahon, COL'
b146 = 'Scott Kingery, PHI'
b147 = 'Shin-Soo Choo, TEX'
b148 = 'Starling Castro, MIA'
b149 = 'Starling Marte, PIT'
b150 = 'Teoscar Hernandez, TOR'
b151 = 'Tim Anderson, CHW'
b152 = 'Todd Frazier, NYM'
b153 = 'Tommy Pham, TB'
b154 = 'Trea Turner, WAS'
b155 = 'Trevor Story, COL'
b156 = 'Trey Mancini, BAL'
b157 = 'Victor Robles, WAS'
b158 = 'Vladimir Guerrero Jr., TOR'
b159 = 'Whit Merrifield, KC'
b160 = 'Wil Myers, SD'
b161 = 'Willy Adames, TB'
b162 = 'Wilson Ramos, NYM'
b163 = 'Xander Bogaerts, BOS'
b164 = 'Yadier Molina, STL'
b165 = 'Yasmani Grandal, MIL'
b166 = 'Yoan Moncada, CHW'
b167 = 'Yolmer Sanchez, CHW'
b168 = 'Yuli Gurriel, HOU'

var_batter = tkr.StringVar()
set_b = tkr.OptionMenu(second_frame, var_batter, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16,
                       b17, b18, b19, b20, b21, b22, b23, b24, b25, b26, b27, b28, b29, b30, b31, b32, b33, b34, b35,
                       b36, b37, b38, b39, b40, b41, b42, b43, b44, b45, b46, b47, b48, b49, b50, b51, b52, b53, b54,
                       b55, b56, b57, b58, b59, b60, b61, b62, b63, b64, b65, b66, b67, b68, b69, b70, b71, b72, b73,
                       b74, b75, b76, b77, b78, b79, b80, b81, b82, b83, b84, b85, b86, b87, b88, b89, b90, b91, b92,
                       b93, b94, b95, b96, b97, b98, b99, b100, b101, b102, b103, b104, b105, b106, b107, b108, b109,
                       b110, b111, b112, b113, b114, b115, b116, b117, b118, b119, b120, b121, b122, b123, b124, b125,
                       b126, b127, b128, b129, b130, b131, b132, b133, b134, b135, b136, b137, b138, b139, b140, b141,
                       b142, b143, b144, b145, b146, b147, b148, b149, b150, b151, b152, b153, b154, b155, b156, b157,
                       b158, b159, b160, b161, b162, b163, b164, b165, b166, b167, b168)
var_batter.set('Select Batter')
var_batter.trace("w", lambda *args: OptionSelected(1,var_batter))
set_b.configure(font=("Arial", 15),width=20,)
set_b.grid(row=0, column=6, columnspan=4)

p1 = 'Aaron Bummer, CHW'
p2 = 'Aaron Nola, PHI'
p3 = 'Adam Kolarek, LAD'
p4 = 'Adam Morgan, PHI'
p5 = 'Adrian Houser, MIL'
p6 = 'Alex Colome, CHW'
p7 = 'Anthony Bass, SEA'
p8 = 'Anthony DeSclafani, CIN'
p9 = 'Aroldis Chapman, NYY'
p10 = 'Austin Adams, SEA'
p11 = 'Austin Brice, MIA'
p12 = 'Blaine Hardy, DET'
p13 = 'Brad Hand, CLE'
p14 = 'Brandon Brennan, SEA'
p15 = 'Brandon Kintzler, CHC'
p16 = 'Brandon Workman, BOS'
p17 = 'Bryan Yarbrough, TB'
p18 = 'Caleb Smith, MIA'
p19 = 'Cam Bedrosian, LAA'
p20 = 'Carlos Martinez, STL'
p21 = 'Chad Green, NYY'
p22 = 'Charlie Morton, TB'
p23 = 'Chase Anderson, MIL'
p24 = 'Chris Bassitt, OAK'
p25 = 'Chris Martin, TEX'
p26 = 'Chris Paddack, SD'
p27 = 'Chris Sale, BOS'
p28 = 'Clayton Kershaw, LAD'
p29 = 'Colin McHugh, HOU'
p30 = 'Colin Poche, TB'
p31 = 'Craig Stammen, SD'
p32 = 'Diego Castillo, TB'
p33 = 'Domingo German, NYY'
p34 = 'Drew Pomeranz, MIL'
p35 = 'Emilio Pagan, TB'
p36 = 'Felipe Rivero, PIT'
p37 = 'German Marquez, COL'
p38 = 'Gerrit Cole, HOU'
p39 = 'Giovanny Gallegos, STL'
p40 = 'Hansel Robles, LAA'
p41 = 'Hector Neris, PHI'
p42 = 'Hector Rondon, HOU'
p43 = 'Hyun-jin Ryu, LAD'
p44 = 'Jack Flaherty, STL'
p45 = 'Jacob DeGrom, NYM'
p46 = 'Jacob Webb, ATL'
p47 = 'Jake Odorizzi, MIN'
p48 = 'Jared Hughes, PHI'
p49 = 'Jarlin Garcia, MIA'
p50 = 'Javy Guerra, WAS'
p51 = 'JB Wendelken, OAK'
p52 = 'Jerry Blevins, ATL'
p53 = 'Jimmy Cordero, CHW'
p54 = 'Joakim Soria, OAK'
p55 = 'Joe Musgrove, PIT'
p56 = 'Joe Smith, HOU'
p57 = 'Joey Lucchesi, SD'
p58 = 'John Brebbia, STL'
p59 = 'John Means, BAL'
p60 = 'Jordan Hicks, STL'
p61 = 'Jose Berrios, MIN'
p62 = 'Josh Hader, MIL'
p63 = 'Josh Osich, CHW'
p64 = 'Josh Taylor, BOS'
p65 = 'Josh Tomlin, ATL'
p66 = 'Julio Urias, LAD'
p67 = 'Junior Guerra, MIL'
p68 = 'Justin Verlander, HOU'
p69 = 'Ken Giles, TOR'
p70 = 'Kenley Jansen, LAD'
p71 = 'Kenta Maeda, LAD'
p72 = 'Keone Kela, PIT'
p73 = 'Kevin Ginkel, ARI'
p74 = 'Kirby Yates, SD'
p75 = 'Kyle Hendricks, CHC'
p76 = 'Lance Lynn, TEX'
p77 = 'Liam Hendriks, OAK'
p78 = 'Lucas Giolito, CHW'
p79 = 'Luis Castillo, CIN'
p80 = 'Luis Perdomo, SD'
p81 = 'Luke Bard, LAA'
p82 = 'Madison Bumgarner, SF'
p83 = 'Marcus Walden, BOS'
p84 = 'Masahiro Tanaka, NYY'
p85 = 'Matt Bowman, CIN'
p86 = 'Matt Strahm, SD'
p87 = 'Matthew Boyd, DET'
p88 = 'Max Scherzer, WAS'
p89 = 'Michael Feliz, PIT'
p90 = 'Michael Lorenzen, CIN'
p91 = 'Michael Pineda, MIN'
p92 = 'Mike Fiers, OAK'
p93 = 'Mike Minor, TEX'
p94 = 'Mike Soroka, ATL'
p95 = 'Miles Mikolas, STL'
p96 = 'Mychal Givens, BAL'
p97 = 'Nick Wittgren, CLE'
p98 = 'Noah Syndergaard, NYM'
p99 = 'Noe Ramirez, LAA'
p100 = 'Oliver Drake, TB'
p101 = 'Oliver Perez, CLE'
p102 = 'Patrick Corbin, WAS'
p103 = 'Pedro Baez, LAD'
p104 = 'Raisel Iglesias, CIN'
p105 = 'Robert Stephenson, CIN'
p106 = 'Roberto Osuna, HOU'
p107 = 'Roenis Elias, SEA'
p108 = 'Ross Stripling, LAD'
p109 = 'Rowan Wick, CHC'
p110 = 'Ryan Pressley, HOU'
p111 = 'Ryne Harper, MIN'
p112 = 'Ryne Stanek, TB'
p113 = 'Sam Coonrod, SF'
p114 = 'Sam Dyson, SF'
p115 = 'Sam Gaviglio, TOR'
p116 = 'Scott Oberg, COL'
p117 = 'Sergio Romo, MIN'
p118 = 'Seth Lugo, NYM'
p119 = 'Shane Bieber, CLE'
p120 = 'Shane Greene, DET'
p121 = 'Sonny Gray, CIN'
p122 = 'Stefan Crichton, ARI'
p123 = 'Stephen Strasburg, WAS'
p124 = 'Steve Cishek, CHC'
p125 = 'Taylor Rogers, MIN'
p126 = 'Tim Hill, KC'
p127 = 'Tommy Kahnle, NYY'
p128 = 'Tony Watson, SF'
p129 = 'Trevor Gott, SF'
p130 = 'Trevor May, MIN'
p131 = 'Tyler Duffey, MIN'
p132 = 'Tyler Clippard, CLE'
p133 = 'Tyler Webb, STL'
p134 = 'Walker Buehler, LAD'
p135 = 'Wander Suero, WAS'
p136 = 'Will Harris, HOU'
p137 = 'Will Smith, SF'
p138 = 'Yimi Garcia, LAD'
p139 = 'Yoan Lopez, ARI'
p140 = 'Yonny Chirinos, TB'
p141 = 'Yu Darvish, CHC'
p142 = 'Yusmeiro Petit, OAK'
p143 = 'Zach Davies, MIL'
p144 = 'Zach Eflin, PHI'
p145 = 'Zack Britton, NYY'
p146 = 'Zack Littell, MIN'
p147 = 'Zack Wheeler, NYM'

var_pitcher = tkr.StringVar()
set_p = tkr.OptionMenu(second_frame, var_pitcher, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16,
                       p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30, p31, p32, p33, p34, p35,
                       p36, p37, p38, p39, p40, p41, p42, p43, p44, p45, p46, p47, p48, p49, p50, p51, p52, p53, p54,
                       p55, p56, p57, p58, p59, p60, p61, p62, p63, p64, p65, p66, p67, p68, p69, p70, p71, p72, p73,
                       p74, p75, p76, p77, p78, p79, p80, p81, p82, p83, p84, p85, p86, p87, p88, p89, p90, p91, p92,
                       p93, p94, p95, p96, p97, p98, p99, p100, p101, p102, p103, p104, p105, p106, p107, p108, p109,
                       p110, p111, p112, p113, p114, p115, p116, p117, p118, p119, p120, p121, p122, p123, p124, p125,
                       p126, p127, p128, p129, p130, p131, p132, p133, p134, p135, p136, p137, p138, p139, p140, p141,
                       p142, p143, p144, p145, p146, p147)
var_pitcher.set('Select Pitcher')
var_pitcher.trace("w", lambda *args: OptionSelected(2,var_pitcher))
set_p.configure(font=("Arial", 15), width=20)
set_p.grid(row=0, column=10,columnspan=4)

t1 = 'Arizona Diamondbacks'
t2 = 'Atlanta Braves'
t3 = 'Baltimore Orioles'
t4 = 'Boston Red Sox'
t5 = 'Chicago Cubs'
t6 = 'Chicago White Sox'
t7 = 'Cincinnati Reds'
t8 = 'Cleveland Indians'
t9 = 'Colorado Rockies'
t10 = 'Detroit Tigers'
t11 = 'Houston Astros'
t12 = 'Kansas City Royals'
t13 = 'Los Angeles Angels'
t14 = 'Los Angeles Dodgers'
t15 = 'Miami Marlins'
t16 = 'Milwaukee Brewers'
t17 = 'Minnesota Twins'
t18 = 'New York Mets'
t19 = 'New York Yankees'
t20 = 'Oakland Athletics'
t21 = 'Philadelphia Phillies'
t22 = 'Pittsburgh Pirates'
t23 = 'San Diego Padres'
t24 = 'San Francisco Giants'
t25 = 'Seattle Mariners'
t26 = 'St. Louis Cardinals'
t27 = 'Tampa Bay Rays'
t28 = 'Texas Rangers'
t29 = 'Toronto Blue Jays'
t30 = 'Washington Nationals'

var_team = tkr.StringVar()
var_team.set('Select Team')
var_team.trace("w", lambda *args: OptionSelected(3, var_team))
set_team = tkr.OptionMenu(second_frame, var_team, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16,
                          t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29, t30)

set_team.configure(font=("Arial", 15),width=20)  # for fonts
set_team.grid(row=0, column=14,columnspan=4)  # for setting position









cnx = mysql.connector.connect(user='root', database='lahmansbaseballdb', host='127.0.0.1', password='')     # MySql Connection

cursor = cnx.cursor()
bquery = (
    "SELECT playerID, teamID, H/AB as 'AVG', (H+BB+HBP)/(AB+BB+HBP+SF) as 'OBP', ((H-2B-3B-HR)+(2B*2)+(3B*3)+(HR*4))/AB as 'SLG',(H+BB+HBP)/(AB+BB+HBP+SF) + ((H-2B-3B-HR)+(2B*2)+(3B*3)+(HR*4))/AB as 'OPS' FROM batting WHERE yearID=2019 && AB>=400 ORDER BY AVG desc")

cursor.execute(bquery)

e = Label(second_frame, width=10, text='playerID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
e.grid(row=0, column=0)
e = Label(second_frame, width=10, text='teamID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
e.grid(row=0, column=1)
e = Label(second_frame, width=10, text='AVG', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
e.grid(row=0, column=2)
e = Label(second_frame, width=10, text='OBP', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
e.grid(row=0, column=3)
e = Label(second_frame, width=10, text='SLG', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
e.grid(row=0, column=4)
e = Label(second_frame, width=10, text='OPS', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
e.grid(row=0, column=5)

i = 1

for batting in cursor:
    for j in range(len(batting)):
        e1 = Entry(second_frame, width=10, fg='blue')
        e1.grid(row=i, column=j)
        e1.insert(END, batting[j])
    i = i + 1

pquery = (
    "SELECT playerID, teamID, ERA, (BB+H)/(IPouts*.333) as 'WHIP', SO/BB as 'KtoBB_Ratio' FROM pitching WHERE yearID=2019 && G>=25 && ERA<=5.00 ORDER BY ERA")

cursor.execute(pquery)

e = Label(second_frame, width=10, text='playerID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
e.grid(row=170, column=0)
e = Label(second_frame, width=10, text='teamID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
e.grid(row=170, column=1)
e = Label(second_frame, width=10, text='ERA', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
e.grid(row=170, column=2)
e = Label(second_frame, width=10, text='WHIP', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
e.grid(row=170, column=3)
e = Label(second_frame, width=10, text='KtoBB_Ratio', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
e.grid(row=170, column=4)

i = 1
for pitching in cursor:
    for j in range(len(pitching)):
        e2 = Entry(second_frame, width=10, fg='red')
        e2.grid(row=i + 171, column=j)
        e2.insert(END, pitching[j])
    i = i + 1

cursor.close()

cnx.close()

tkr.mainloop()


