import tkinter as tk
# from User import *
from functools import partial
from PIL import ImageTk, Image
import sqlite3
import uuid

import requests
from xml.etree import ElementTree

import geopy.distance

from tkinter import ttk
from tkinter import filedialog

import os

import openai
import secret


class FindFriends:
    def __init__(self):

        self.conn = sqlite3.connect("final_test.db")
        self.c = self.conn.cursor()
        # self.runDb() #This Line needs to be uncommented to create another database. After closing code uncomment to run again
                        # but no need to in this case
        self.runApp()

    # Creates Each required Tables
    def runDb(self):
        self.c.execute("""CREATE TABLE users(
                    id text,
                    email text,
                    password text)""")

        self.c.execute("""CREATE TABLE user(
                    id text,
                    name text,
                    age integer,
                    gender text,
                    image text,
                    about text,
                    geo text)""")

        self.c.execute("""CREATE TABLE interests(
                    id text,
                    reading integer ,
                    music integer,
                    memes integer,
                    shopping integer,
                    movies integer,
                    workingOut integer,
                    coffee integer,
                    sports integer,
                    environmentalism integer,
                    meditation integer,
                    photography integer,
                    nightlife integer,
                    anime integer,
                    socialMedia integer,
                    esports integer)""")

        # self.c.execute("""CREATE TABLE seen(
        #             user_id text,
        #             user_id_2 text)""")

        self.c.execute("""CREATE TABLE unseen(
                    user_id text,
                    user_id_2 text)""")

        self.c.execute("""CREATE TABLE potentialFriends(
                    user_id text,
                    user_id_2 text)""")

        self.c.execute("""CREATE TABLE friend(
                    user_id text,
                    user_id_2 text)""")

        self.c.execute("""CREATE TABLE chatlogAI(
                    user_id text,
                    chatlog text)""")




        self.conn.commit()


    #Creates root
    def runApp(self):
        root = tk.Tk()
        root.title("Friends")
        root.geometry("300x500+550+150")
        root.resizable(False, False)
        self.signup_screen(root)

        root.mainloop()

    #Creates Registration Screen
    def signup_screen(self, root):
        login_screen = tk.Frame(root)
        login_screen.pack()

        email = tk.StringVar()
        password = tk.StringVar()

        email_label = tk.Label(login_screen, text="Email: ")
        email_label.pack()
        email_entry = tk.Entry(login_screen, textvariable=email)
        email_entry.pack()

        password_label = tk.Label(login_screen, text="Password: ")
        password_label.pack()
        password_entry = tk.Entry(login_screen, textvariable=password, show="*")
        password_entry.pack()

        args_login = partial(self.signing_in, email, password, login_screen, email_entry, password_entry, root)
        args_signup = partial(self.signing_up, email, password, login_screen, email_entry, password_entry, root)

        submit_login = tk.Button(login_screen, text="Login", command=args_login)
        submit_login.pack()
        submit_signup = tk.Button(login_screen, text="Signup", command=args_signup)
        submit_signup.pack()

    def signing_up(self, x, y, login_frame, email_entry, password_entry, root):
        # Check if email already exists

        self.c.execute("SELECT email from users")
        all_emails = self.c.fetchall()

        email = x.get()
        password = y.get()

        my_boolean = True

        for item in all_emails:
            if email == str(item)[2:-3]:
                print("Email already exists")
                my_boolean = False
                break

        if my_boolean:
            #Create user_id if new user
            user_id = str(uuid.uuid4())

            self.c.execute("INSERT INTO users VALUES (:id,:email,:password)",
                           {"id": user_id, "email": email, "password": password})
            self.conn.commit()



            self.c.execute("SELECT email from users")
            all_emails = self.c.fetchall()

            self.c.execute("INSERT INTO chatlogAI VALUES (:id,:id2)",
                           {'id': user_id, 'id2': ""})

            self.conn.commit()

            login_frame.destroy()

            self.profile_settings_screen(root, user_id, "signup")

        else:
            email_entry.delete(0, len(email))
            password_entry.delete(0, len(password))

        # I am doing main screen first

        # Go to profile settings -> From there to Login screen

    #Creating User Profile
    def profile_check(self, state, name_entry, age_entry, var, about_box, profile, root, user_id, ):
        #You cannot continue unless you write name,age,etc..
        if name_entry.get() == "" or age_entry.get() == "" or var.get() == 0 or about_box.get("1.0", "end") == "\n":
            if name_entry.get() == "":
                name_entry.configure(bg="#F9A8A7")
            if age_entry.get() == "":
                age_entry.configure(bg="#F9A8A7")
            if about_box.get("1.0", "end") == "\n":
                about_box.configure(bg="#F9A8A7")

        else:
            name = name_entry.get()
            age = age_entry.get()
            male_or_female = var.get()
            about_me = about_box.get("1.0", "end")
            profile.destroy()

            profile_page_2 = tk.Frame(root)
            profile_page_2.pack()


            # Go to profile page 2
            interests = tk.Label(profile_page_2, text="Interests", font="bold")
            interests.pack()

            def get_box():
                pass

            #Create 15 ttk.Checkbuttons
            interest1_var = tk.StringVar()
            interest1 = ttk.Checkbutton(profile_page_2,
                                        text='Reading',
                                        variable=interest1_var,
                                        command=get_box,
                                        onvalue=True,
                                        offvalue=False,
                                        )

            interest1.pack()

            interest2_var = tk.StringVar()
            interest2 = ttk.Checkbutton(profile_page_2,
                                        text='Music',
                                        variable=interest2_var,
                                        command=get_box,
                                        onvalue=True,
                                        offvalue=False,
                                        )

            interest2.pack()

            interest3_var = tk.StringVar()
            interest3 = ttk.Checkbutton(profile_page_2,
                                        text='Memes',
                                        variable=interest3_var,
                                        command=get_box,
                                        onvalue=True,
                                        offvalue=False,
                                        )

            interest3.pack()

            interest4_var = tk.StringVar()
            interest4 = ttk.Checkbutton(profile_page_2,
                                        text='Shopping',
                                        variable=interest4_var,
                                        command=get_box,
                                        onvalue=True,
                                        offvalue=False,
                                        )

            interest4.pack()

            interest5_var = tk.StringVar()
            interest5 = ttk.Checkbutton(profile_page_2,
                                        text='Movies',
                                        variable=interest5_var,
                                        command=get_box,
                                        onvalue=True,
                                        offvalue=False,
                                        )

            interest5.pack()

            interest6_var = tk.StringVar()
            interest6 = ttk.Checkbutton(profile_page_2,
                                        text='Working out',
                                        variable=interest6_var,
                                        command=get_box,
                                        onvalue=True,
                                        offvalue=False,
                                        )

            interest6.pack()

            interest7_var = tk.StringVar()
            interest7 = ttk.Checkbutton(profile_page_2,
                                        text='Coffee',
                                        variable=interest7_var,
                                        command=get_box,
                                        onvalue=True,
                                        offvalue=False,
                                        )

            interest7.pack()

            interest8_var = tk.StringVar()
            interest8 = ttk.Checkbutton(profile_page_2,
                                        text='Sports',
                                        variable=interest8_var,
                                        command=get_box,
                                        onvalue=True,
                                        offvalue=False,
                                        )

            interest8.pack()

            interest9_var = tk.StringVar()
            interest9 = ttk.Checkbutton(profile_page_2,
                                        text='Environmentalism',
                                        variable=interest9_var,
                                        command=get_box,
                                        onvalue=True,
                                        offvalue=False,
                                        )

            interest9.pack()

            interest10_var = tk.StringVar()
            interest10 = ttk.Checkbutton(profile_page_2,
                                         text='Meditation',
                                         variable=interest10_var,
                                         command=get_box,
                                         onvalue=True,
                                         offvalue=False,
                                         )

            interest10.pack()

            interest11_var = tk.StringVar()
            interest11 = ttk.Checkbutton(profile_page_2,
                                         text='Photography',
                                         variable=interest11_var,
                                         command=get_box,
                                         onvalue=True,
                                         offvalue=False,
                                         )

            interest11.pack()

            interest12_var = tk.StringVar()
            interest12 = ttk.Checkbutton(profile_page_2,
                                         text='Nightlife',
                                         variable=interest12_var,
                                         command=get_box,
                                         onvalue=True,
                                         offvalue=False,
                                         )

            interest12.pack()

            interest13_var = tk.StringVar()
            interest13 = ttk.Checkbutton(profile_page_2,
                                         text='Anime',
                                         variable=interest13_var,
                                         command=get_box,
                                         onvalue=True,
                                         offvalue=False,
                                         )

            interest13.pack()

            interest14_var = tk.StringVar()
            interest14 = ttk.Checkbutton(profile_page_2,
                                         text='Social-Media',
                                         variable=interest14_var,
                                         command=get_box,
                                         onvalue=True,
                                         offvalue=False,
                                         )

            interest14.pack()

            interest15_var = tk.StringVar()
            interest15 = ttk.Checkbutton(profile_page_2,
                                         text='E-Sports',
                                         variable=interest15_var,
                                         command=get_box,
                                         onvalue=True,
                                         offvalue=False,
                                         )

            interest15.pack()
            interest_obj = ["empty", interest1, interest2, interest3, interest4, interest5, interest6, interest7,
                            interest8,
                            interest9, interest10, interest11, interest12, interest13, interest14, interest15, ]

            # for i in range (1,len(interest_obj)):
            #     interest_obj[i].invoke()
            #     interest_obj[i].invoke()

            warning = tk.Label(profile_page_2, text="(0/5) hobbies selected")

            # If state is login, when profile page 2 gets called, the buttons that were selected in previous session will stil appear selected
            if state == "login":
                self.c.execute("SELECT * FROM interests WHERE id =(:userid)", {'userid': user_id})
                interests_tuple = self.c.fetchone()
                # print("tuple: ", interests_tuple)

                for i in range(1, len(interests_tuple)):
                    if interests_tuple[i] == 1:
                        interest_obj[i].invoke()

            # I prefer partial instead of command = lambda : .
            args_of_submit = partial(self.prep_main, state, root, profile_page_2, warning, name, age, male_or_female,
                                     about_me,
                                     user_id, interest1_var, interest2_var, interest3_var,
                                     interest4_var, interest5_var, interest6_var, interest7_var, interest8_var,
                                     interest9_var, interest10_var, interest11_var, interest12_var, interest13_var,
                                     interest14_var, interest15_var, )
            submit = tk.Button(profile_page_2, text="submit", command=args_of_submit)
            submit.pack()
            warning.pack()

    #Preparing for entering main screen.
    def prep_main(self, state, root, profile, warning, name, age, male_or_female, about_me, user_id, *interests):
        global geodata
        if geodata:
            geodata = str(geodata)
        else:
            geodata = "0"

        global filename

        self.c.execute("SELECT image FROM user WHERE id =:userid",
                           {'userid':user_id})
        x = self.c.fetchone()
        try:
            x = x[0]
            if filename == None:
                filename = "Images\\anonym.png"


            if x != "Images\\anonym.png":
                filename = x
        except:
            if not filename:
                filename = "Images\\anonym.png"


        interests = list(interests)
        for i in range(len(interests)):
            # print("yo", interests[i].get())
            if interests[i].get() == 0 or interests[i].get() == "":
                interests[i] = 0
            else:
                # print("ok", interests[i].get())
                interests[i] = 1
        # print(interests, "##################")
        count = interests.count(1)


        if count < 5:
            warning.configure(text=f"({count}/5) hobbies selected", fg="red")
        else:
            if state == "signup":
                # If signup insert profile settings into relevant tables

                self.c.execute("INSERT INTO user VALUES (:id,:name,:age,:gender,:image,:about,:geodata)",
                               {'id': user_id, 'name': name, 'age': int(age), 'gender': male_or_female,
                                'image': filename,
                                'about': about_me, 'geodata': str(geodata)})

                self.c.execute("""INSERT INTO interests VALUES (:id,:read,:music,:memes,:shopping,:movies,:workingOut,
                               :coffee,:sports,:environment,:meditation,:photography,:nightlife,:anime,
                               :socialMedia,:esports)""",
                               {'id': user_id, 'read': interests[0], 'music': interests[1], 'memes': interests[2],
                                'shopping': interests[3],
                                'movies': interests[4], 'workingOut': interests[5], 'coffee': interests[6],
                                'sports': interests[7],
                                'environment': interests[8], 'meditation': interests[9], 'photography': interests[10],
                                'nightlife': interests[11],
                                'anime': interests[12], 'socialMedia': interests[13], 'esports': interests[14], }
                               )

                self.conn.commit()
            else:
                self.c.execute("""
                        UPDATE user 
                        SET name = :name,age =:age,gender =:gender,image = :image,about =:about,geo =:geo
                        WHERE id = :user_id""",
                               {'name': name, 'age': int(age), 'gender': male_or_female, 'image': filename,
                                'about': about_me, 'geo': geodata, 'user_id': user_id})

                self.c.execute("""
                            UPDATE interests
                            SET reading =:read,music =:music,memes =:memes,shopping =:shopping,movies =:movies,workingOut =:workingOut,
                               coffee =:coffee,sports =:sports,environmentalism =:environment,meditation =:meditation,photography =:photography,nightlife =:nightlife,anime =:anime,
                               socialMedia =:socialMedia,esports =:esports
                            WHERE id =:user_id""",
                               {'read': interests[0], 'music': interests[1], 'memes': interests[2],
                                'shopping': interests[3],
                                'movies': interests[4], 'workingOut': interests[5], 'coffee': interests[6],
                                'sports': interests[7],
                                'environment': interests[8], 'meditation': interests[9], 'photography': interests[10],
                                'nightlife': interests[11],
                                'anime': interests[12], 'socialMedia': interests[13], 'esports': interests[14],
                                'user_id': user_id})
                self.conn.commit()

            profile.destroy()
            self.main_screen(state, root, user_id)

    def profile_settings_screen(self, root, user_id, state):
        #Create profile settings screen
        profile = tk.Frame(root)
        profile.pack()
        row = None

        if state == "login":
            # print("login", user_id)
            self.c.execute("SELECT * FROM user WHERE id =(:userid)", {'userid': user_id})
            row = self.c.fetchone()
            # print(row)

        name = tk.Label(profile, text="Name: ")
        name.pack()

        name_entry = tk.Entry(profile)
        name_entry.pack()

        age = tk.Label(profile, text="Age: ")
        age.pack()
        age_entry = tk.Entry(profile)
        age_entry.pack()

        labelFrame = tk.LabelFrame(profile, text="Gender")
        labelFrame.pack()

        var = tk.IntVar()
        male = tk.Radiobutton(labelFrame, text="Male", variable=var, value=1)
        male.pack()
        female = tk.Radiobutton(labelFrame, text="Female", variable=var, value=2)
        female.pack()

        image = tk.Label(profile, text="Profile Picture")
        image.pack()

        global filename
        filename = None

        def select_file():
            global filename
            filetypes = (
                ("another type of image", "*.jpg"),
                ("a type of image", "*.png")

            )

            filename = filedialog.askopenfilename(
                title="Add image",
                initialdir="Images\Available",
                filetypes=filetypes
            )
            filename = os.path.basename(filename)
            # print("lessgo",filename)
            src = f"Images\Available\{filename}"
            dest = f"Images\Taken\{filename}"

            os.rename(src,dest)

            filename = dest

            # print(dest)


        open_button = ttk.Button(
            profile,
            text="Add image",
            command=select_file
        )
        open_button.pack(expand=True)

        global geodata
        geodata = None

        # Still neeed to how to get random lat and longitude
        geography_button = tk.Button(profile, text="Get Geographic Data", command=self.get_latt_longt)
        geography_button.pack()

        about = tk.Label(profile, text="About me: ")
        about_box = tk.Text(profile, width=35, height=8)

        about.pack()
        about_box.pack()

        # fetchone can return none.
        if row:
            name_entry.insert(0, row[1])
            age_entry.insert(0, row[2])
            if row[3] == "1":
                male.select()
            elif row[3] == "2":
                female.select()
            about_box.insert("1.0", row[5])

        # args_submit = partial(self.profile_check,state, name_entry,
        #                       age_entry, var, filename, about_box, profile, root, user_id)

        submit = tk.Button(profile, text="submit",
                           command=lambda: self.profile_check(state, name_entry, age_entry, var, about_box, profile,
                                                              root, user_id, ))
        submit.pack()

        # Submit only if all the data are provided.

    def authentification(self, email, password):
        #If email and password match return id
        self.c.execute("SELECT id,email,password from users")
        list_of_tuples = self.c.fetchall()
        for user_id, k, v in list_of_tuples:
            if email == k and password == v:
                return user_id

        return False

    def signing_in(self, x, y, login_frame, email_entry, password_entry, root):
        email = x.get()
        password = y.get()

        if self.authentification(email, password):
            user_id = self.authentification(email, password)
            # print(user_id)
            login_frame.destroy()
            self.main_screen("login", root, user_id)
        else:
            email_entry.delete(0, len(email))
            password_entry.delete(0, len(password))
            # Delete Entry data. Try again

        # Go to main_screen

    def main_screen(self, state, root, user_id):
        #EXPLANATION of Friends.py

        # Create unseen table, ,Potential friends,Friends

        # Signup
        # Unseen full,Seen empty, [DONE]

        #  matchmaking algorithm --> [counts number of common interests + some value for distance that looses value as it gets bigger]
        # Run MatchMaking -> Creates a list of all [unseen_id, value] for active user and returns most "valued" unseen id

        # Algorithm

        # Sort list by order value
        # Show first entry to user
        #
        # [Take relevant Data from tables to make a view: Name,age,distance,about,common interests]


        #[DONE]




        #LOGIN/SIGNUP:
            #initially:
                #MainScreen
                #Run Match Making Algorithm -> target id
                # Make a View Page: Image,Name,age,distance,about,common interests
            #Yes:
                #Add to potential friends
                #Remove from unseen
                #Check potential_friend target_id has you as as potential_friend.
                    #Yes:Remove Yourself,targets from potential friends, ADD yourself,targetss to Friends
                    #No: Do Nothing
                    #RUN self.main_screen("login")


            #No:
                #Remove unseen,
                # RUN self.main_screen("login")

        # All values in Friends table show in  Dropdown Menu




        main_frame = tk.Frame(root)
        main_frame.pack()
        print(state,user_id)


        if state == "signup":
            self.c.execute("""SELECT id FROM users""")
            items = self.c.fetchall()
            items_without_user_id = []
            for item in items:
                if item[0] != user_id:
                    items_without_user_id.append(item[0])

            for item in items_without_user_id:
                self.c.execute("""INSERT INTO unseen VALUES (:id,:id_2)""",{'id':user_id,'id_2':item})
                self.c.execute("""INSERT INTO unseen VALUES (:id,:id_2)""",{'id':item,'id_2':user_id})
                #This way unseen database stays updated even when a new user is added

                self.conn.commit()





        target_id = self.match_making_algorithm(user_id) # Could be None if first user
        print("HERE",target_id)
        if target_id:
            logged_in_username = self.get_name(user_id)


            self.c.execute("SELECT * FROM user WHERE id =:id1", {'id1': target_id})
            user_tuple = self.c.fetchone()


            name = user_tuple[1]
            age = user_tuple[2]
            gender = "male" if user_tuple[3]== 1 else "female"
            image_url = user_tuple[4]
            about = user_tuple[5].strip()
            distance = self.get_distance(user_id,target_id)

            print(f"User: {logged_in_username} is currently viewing page of {name}")




             # make View Page

            ##################################################################################################
            # ADD this and much more later to the View Page

            image = Image.open(image_url)
            image = image.resize((300, 385), Image.ANTIALIAS)
            image_object = ImageTk.PhotoImage(image)

            label1 = tk.Label(image=image_object, anchor="center")
            label1.image = image_object
            label1.pack(expand=True, )
            # img = ImageTk.PhotoImage(Image.open("random_image.jpg"))

            action_with_arg1 = partial(self.no_action,user_id,target_id,root,label1,main_frame)
            action_with_arg2 = partial(self.yes_action,user_id,target_id,root,label1,main_frame)

            settings_arg = partial(self.prep_profile, root, user_id, main_frame, label1)

            swipe_left = tk.Button(main_frame, text=" No", command=action_with_arg1)
            swipe_right = tk.Button(main_frame, text=" Yes", command=action_with_arg2)
            settings = tk.Button(main_frame, text="Settings", command=settings_arg)

            swipe_left.pack(side="left")

            swipe_right.pack(side="right")
            settings.pack()
            friends= self.get_friends(user_id)
            friends_args = partial(self.open_friends,root,friends)
            friends_button = tk.Button(main_frame,text = "Friends", command = friends_args)
            friends_button.pack()
            about_args = partial(self.open_about,root,name,age,gender,about,distance)
            about_button = tk.Button(main_frame,text = "About", command = about_args)
            about_button.pack()

            print("Hey",user_id)
            chatbot_args = partial(self.open_chatbot,root,user_id)
            chatbot_button = tk.Button(main_frame,text = "chat-bot", command = chatbot_args)
            chatbot_button.pack()






        else:
            image = Image.open("Images\empty.png")
            image = image.resize((300, 385), Image.ANTIALIAS)
            image_object = ImageTk.PhotoImage(image)

            label1 = tk.Label(image=image_object, anchor="center")
            label1.image = image_object
            label1.pack(expand=True)



    def open_chatbot(self,root,user_id):
        window = tk.Toplevel(root)
        window.title("OpenAI")
        window.geometry("300x500")
        tk.Label(window, text="Chatbot", pady=15, font=("Times New Roman", 20, "underline")).pack()

        text_widget = tk.Text(window, height=10, width=100)
        scroll_bar = tk.Scrollbar(window)
        scroll_bar.pack(side=tk.RIGHT)
        text_widget.pack(side=tk.LEFT)

        chatlog = ""
        self.c.execute("SELECT chatlog FROM chatlogAI WHERE user_id =:id1", {'id1': user_id})
        none_or_tuple = self.c.fetchone()
        print(none_or_tuple)
        if none_or_tuple != None and none_or_tuple != "":
            chatlog = none_or_tuple[0]


        value = tk.StringVar()
        entry = tk.Entry(window,textvariable=value,width = 30)
        entry.place(x=0,y=375)

        send_args = partial(self.send,value,entry,chatlog,text_widget,user_id)
        send = tk.Button(window,text = "send", command = send_args)
        send.place(x=230,y=375)


        # text_widget.insert(tk.END,)


    def openai(self,input):
        openai.api_key = secret.get_key()

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt="The following is a conversation between You and another AI Chatbot. The Chatbot will act liek a very kind,friendly and talkative person" + input,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Chatbot:"]
        )

        reply = response["choices"][0]["text"]

        return reply

    def send(self,entry,entry_obj,chatlog,textwidget,user_id):
        print("####",user_id)
        value = entry.get()

        entry_obj.delete(0,len(value))

        entry = "You: " + value + "\nChatbot: "
        updated_prompt = chatlog + "\n"+entry

        reply = self.openai(updated_prompt)

        updated_chatlog = updated_prompt + reply
        textwidget.insert(tk.END, updated_chatlog)

        print(user_id)
        self.c.execute("""
                                UPDATE chatlogAI 
                                SET chatlog = :chat
                                WHERE user_id = :user_id""",
                       {'user_id': user_id, 'chat': updated_chatlog,})
        self.conn.commit()



    def open_about(self,root,name,age,gender,about,distance):
        window = tk.Toplevel(root)
        window.title("About")
        window.geometry("300x500")
        tk.Label(window, text="About", pady=15, font=("Times New Roman", 20, "underline")).pack()
        tk.Label(window, text="Name: " + name, pady=1, padx=1, font=("Times New Roman", 14,)).pack(anchor="s")
        tk.Label(window, text="Age: " + str(age), pady=1, padx=1, font=("Times New Roman", 14,)).pack(anchor="s")
        tk.Label(window, text="Gender: " + gender, pady=1, padx=1, font=("Times New Roman", 14,)).pack(anchor="s")
        if distance:
            tk.Label(window, text=f"{name} is {distance} km away from you ", pady=1, padx=1, font=("Times New Roman", 14,)).pack(anchor="s")
        else:
            tk.Label(window, text="Location: Data is not provided", pady=1, padx=1, font=("Times New Roman", 14,)).pack(anchor="s")



        text_widget = tk.Text(window, height=10, width=100)
        scroll_bar = tk.Scrollbar(window)
        scroll_bar.pack(side=tk.RIGHT)
        text_widget.pack(side=tk.LEFT)

        text_widget.insert(tk.END,about)

    def open_friends(self,root,friends):
        window = tk.Toplevel(root)
        window.title("Friends")
        window.geometry("300x500")
        tk.Label(window,text="Friends",pady = 15,font = ("Times New Roman",20,"underline")).pack()
        for item in friends:
            tk.Label(window,text = "* "+item,pady = 1, font = ("Times New Roman",14,)).pack(anchor="s")




            ############################################################################################



    def get_name(self,user_id):
        self.c.execute("SELECT name FROM user WHERE id =:id1", {'id1': user_id})
        x = self.c.fetchone()
        return x[0]

    def no_action(self,user_id,target_id,root,label1,main_frame):
        label1.destroy()
        main_frame.destroy()

        self.c.execute("DELETE FROM unseen WHERE user_id =:id and user_id_2 =:id2",{'id':user_id,'id2':target_id})
        self.conn.commit()
        self.main_screen("login",root,user_id)


    def yes_action(self,user_id,target_id,root,label1,main_frame):
        label1.destroy()
        main_frame.destroy()


        self.c.execute("INSERT INTO potentialFriends VALUES (:id,:id2)",
                       {'id': user_id, 'id2': target_id})
        self.conn.commit()

        self.c.execute("DELETE FROM unseen WHERE user_id =:id and user_id_2 =:id2", {'id': user_id, 'id2': target_id})

        self.conn.commit()


        #Check if target has you in PotentialFriends

        self.c.execute("SELECT * FROM potentialFriends WHERE user_id =:id and user_id_2 =:id2",
                       {'id': target_id, 'id2': user_id})
        list_of_tuples = self.c.fetchall()
        # print(list_of_tuples,"yes") # Should either be empty or have 1 entry. If it has more than 1 something went wrong.

        if len(list_of_tuples)>0:
            #Remove Yourself,targets from potential friends, ADD yourself,targetss to Friends
            self.c.execute("DELETE FROM potentialFriends WHERE user_id =:id and user_id_2 =:id2",
                           {'id': user_id, 'id2': target_id})

            self.c.execute("DELETE FROM potentialFriends WHERE user_id =:id and user_id_2 =:id2",
                           {'id': target_id, 'id2': user_id})

            self.c.execute("INSERT INTO friend VALUES (:id,:id2)",
                           {'id': user_id, 'id2': target_id})

            self.c.execute("INSERT INTO friend VALUES (:id,:id2)",
                           {'id': target_id, 'id2': user_id})
            self.conn.commit()




        self.main_screen("login",root,user_id)





    def prep_profile(self, root, user_id, main_screen, label1):
        main_screen.destroy()
        label1.destroy()
        self.profile_settings_screen(root, user_id, "login")

    def get_latt_longt(self):
        global geodata
        response = requests.get("https://api.3geonames.org/?randomland=yes")
        tree = ElementTree.fromstring(response.content)
        x = tree.find("nearest/latt").text
        y = tree.find("nearest/longt").text
        geodata = (x, y)

    #####################################################

    def get_distance(self,user1_id,user2_id):

        self.c.execute("SELECT geo FROM user WHERE id =:id1",{'id1':user1_id})
        id1 = self.c.fetchone()


        self.c.execute("SELECT geo FROM user WHERE id =:id2",{'id2':user2_id})
        id2 = self.c.fetchone()
        # ("('11.99899', '102.37065')",)
        items_1 = id1[0][1:-1].split(",")
        # print(items_1)
        try:

            latt_1 = float(items_1[0][1:-1])
            longt_1 = float(items_1[1][2:-1])
            items_2 = id2[0][1:-1].split(",")

            latt_2 = float(items_2[0][1:-1])
            longt_2 = float(items_2[1][2:-1])

            coordinate_user1 = (latt_1, longt_1)
            coordinate_user2 = (latt_2, longt_2)
            distance = geopy.distance.geodesic(coordinate_user1, coordinate_user2).km


            return round(distance)
        except:
            return None

    def number_of_matches(self, tuple1, tuple2):
        x = list(tuple1)
        y = list(tuple2)

        value = 0
        for i in range(1, len(x)):
            if x[i] == y[i] and x[i] == 1:
                value += 1
        return value

    def value_calculator(self,distance,common_interests):
        dist_count = 0
        if common_interests == 0:
            return 0
        else:
            if not distance:
                distance = 10000 #km
            if distance >= 0 and distance < 1000:
                dist_count = 3
            elif distance >= 1000 and distance <3000:
                dist_count = 2
            elif distance >= 3000 and distance < 5000:
                dist_count = 1
            else:
                dist_count = 0
        return dist_count + common_interests

            #Function with distance and count


    def fetch_interest_tuple(self,user_id):
        self.c.execute("SELECT * FROM interests WHERE id =(:userid)", {'userid': user_id})
        interests_tuple_of_user = self.c.fetchone()
        return interests_tuple_of_user

    def match_making_algorithm(self,user_id):
        #Given a user_id -> use it to make a list of tuples (user_id_of, value)   --> distance -> just need 2 userids -> intersts -> You need
        try:

            interests_tuple_of_user = self.fetch_interest_tuple(user_id)

            self.c.execute("SELECT user_id_2 FROM unseen WHERE user_id =(:id)", {'id': user_id})
            users = self.c.fetchall()
            users_list = []
            for item in users:
                users_list.append(item[0])

            # print(users_list,interests_tuple_of_user)
            match = []
            match_part = [-1,-1]
            for id in users_list:
                match_part[0] = id
                distance = self.get_distance(user_id,id)
                other_tuple = self.fetch_interest_tuple(id)
                count = self.number_of_matches(interests_tuple_of_user, other_tuple)
                value = self.value_calculator(distance,count)
                match_part[1] = value
                match.append(match_part.copy())
            # print(match) #[['7771b049-0bf0-4f24-b167-fbab8f362a0b', 3],...]

            #Sort and get first item
            sorted_match = sorted(match,key = lambda x:x[1],reverse= True)

            # print(sorted_match)
            selected_user = sorted_match[0][0]
            return sorted_match[0][0]
        except:
            return None # Most likely reason first user in Database. Other reason Corrupted database but easy to test

    def get_friends(self,user_id):
        self.c.execute("SELECT user_id_2 FROM friend WHERE user_id =:id",{'id':user_id})
        list_of_id = self.c.fetchall()
        list_of_friends = []

        for item in list_of_id:

            list_of_friends.append(self.get_name(item[0]))
        return list_of_friends









app = FindFriends()
