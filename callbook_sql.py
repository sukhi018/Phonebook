import sqlite3 as sq

# regex module,tkinter
'''
regex for phone number (9|8|7|6)\d{9}+
regex for name - \w+[a-z A-Z]\s*\w*[a-z A-Z]
regex for phone groups - \w{1,20}+ 
regex for username \w+[a-z A-Z]\w{0,5}*[0-9 - \.] 
regex for password \w+

'''



new=sq.connect('phonebook_db.db')
point=new.cursor()


login_details='''CREATE TABLE if not exists Login ( User_id varchar(15) NOT NULL ,Password varchar(20) NOT NULL,PRIMARY KEY(User_id));'''
point.execute(login_details)
phone_book='''CREATE TABLE IF NOT exists PHONEBOOK (User_id varchar(15) NOT NULL,NAME text(20),PHONE number(10),ADDRESS varchar(100), phone_groups text(20));'''
point.execute(phone_book)
recycle_bin='''CREATE TABLE IF NOT exists Recycle (User_id varchar(15) NOT NULL,NAME text(20),PHONE number(10),ADDRESS varchar(100), phone_groups text(20));'''
point.execute(recycle_bin)

class mainpage():
	def create():
		print('{:.^20s}'.format('|Sign Up|'))
		print('Username -> ',end='')
		username=input()
		print('Password -> ',end='')
		password=input()
		q='''INSERT INTO Login VALUES (?,?);'''
		try:
			point.execute(q,(username,password))
			new.commit()
			print('Account Created !!')
			mainpage.page()
		except Exception as e:
			print(e)
			print('Username Already Taken')
			mainpage.log_in()
		
	def log_in():
		print('{:.^20s}'.format('|Login|'))
		print('Enter Username -> ',end='')
		username=input()
		print('Enter Password -> ',end='')
		password=input()
		q='''SELECT * FROM Login where User_id=(?) AND Password=(?) ;'''
		point.execute(q,(username,password))
		k=point.fetchall()
		if len(k)==1:mainpage.option(username)
		else:
			print('Either Password or Username is Incorrect!')
			mainpage.page()

	def ex_it():
		exit()


	def edit(k,name):
		print('Want to change Name\nEnter Y or N',end=' ')
		q='''SELECT * FROM Phonebook where User_id=(?) AND NAME=(?) ;'''
		point.execute(q,(K,P))
		k=point.fetchall()
		if len(k)==1:
			if input()=='Y':
				print('\nEnter New Name:. ',end=' ')
				p=input()
				q=''' UPDATE PHONEBOOK SET NAME=(?) WHERE NAME=(?) AND User_id =(?);'''
				point.execute(q,(p,name,k))
				new.commit()
				print('\nName changed')
				name=p
				print('Want to change Number\nEnter Y or N')
				if input()=='Y':
						print('Enter Number:. ',end='')
						num=input()	
						q=''' UPDATE PHONEBOOK SET PHONE=(?) WHERE NAME=(?) AND User_id=(?);'''
						point.execute(q,(num,name,k))
						new.commit()
						print('Number changed')

			print('Want to change Address\nEnter Y or N',end=' ')
			if input()=='Y':
				print('\nEnter Address:. ',end=' ')
				add=input()
				q=''' UPDATE PHONEBOOK SET ADDRESS=(?) WHERE User_Id=(?) AND Name=(?) ;'''
				point.execute(q,(add,k,name))
				new.commit()
				print('Address changed')


			print('Want to change Group\nEnter Y or N',end=' ')
			if input()=='Y':
				print('Enter group:.',end='')
				group1=input()
				q=''' UPDATE PHONEBOOK SET phone_groups = ? WHERE User_Id=(?) AND Name=(?) ;'''
				point.execute(q,(group1,k,name))
				new.commit()
				print('Group changed')
				mainpage.option(k)	
		else:
			print('\nNo contact Found')
			mainpage.page()	

	def option(k):
		print('{:.^20s} \n\n1 -> New Contact\n2 -> Search Contact \n3 -> Delete Contact \n4 -> Restore Deleted\n5 -> All contacts\n6 -> Log Out '.format('|Contacts|'))
		p=int(input())


		if p==1:
			print('Enter Name -> ',end='')
			name=input()[:20]
			print('Enter Number -> ',end='')
			num=int(input()[:10])
			print('Enter Address -> ',end='')
			add=input()[:25]
			print('Group -> ',end='')
			_group_=input()[:15]
			q='''INSERT INTO PHONEBOOK VALUES (?,?,?,?,?);'''
			point.execute(q,(k,name,num,add,_group_))
			new.commit()
			mainpage.option(k)

		elif p==2:
			print('Enter Name -> ',end='')
			name=input()[:20]
			q=''' Select * from PHONEBOOK where NAME=(?) AND User_id=(?);'''
			point.execute(q,(name,k))
			l=point.fetchall()
			if len(l)==1:
				for x in l:print(*x[1:])
				print('1 -> Exit')
				edit_del=input()
				if edit_del=='1':mainpage.option(k)
				else:mainpage.option(k)
			else:
				print('No Contact found !!')
				mainpage.option(k)

		elif p==3:
			print('Enter Name -> ',end='')
			name=input()[:20]
			infor='''SELECT * from PHONEBOOK WHERE NAME =(?) AND User_id=(?);'''
			point.execute(infor,(name,k))
			info=point.fetchall()
			if len(info)==1:
				q=''' DELETE  from PHONEBOOK where User_id=(?) AND NAME=(?);'''
				point.execute(q,(k,name))
				new.commit()
				rec='''INSERT INTO Recycle  VALUES((?),(?),(?),(?),(?));'''
				for x in info:
					point.execute(rec,(k,x[1],x[2],x[3],x[4]))
				new.commit()
				print('Deleted {} from contacts'.format(name))
				mainpage.option(k)
			else:
				print('NO contact Found!')
				mainpage.option(k)

		elif p==4:
			print('Enter Name -> ',end=' ')
			name=input()[:20]
			mainpage.restore(k,name)

		elif p==5:
			q=''' SELECT * FROM PHONEBOOK WHERE User_id=(?);'''
			point.execute(q,(k,))
			l1=point.fetchall()
			q=''' SELECT COUNT(NAME) FROM PHONEBOOK WHERE User_id=(?);'''
			point.execute(q,(k,))
			l=point.fetchall()
			print('{:.^20s}'.format('|Total Contacts -> {}|'.format(l[0][0])))
			for x in l1:print(*x[1:])
			mainpage.option(k)


		elif p==6:
			print('Logged Out Successfuly')
			mainpage.page()

		else:
			print('Not a Valid Option!!')
			mainpage.option(k)


	def page():
		print('{:.^20s} \n\n1 -> SIGN UP \n2 -> LOGIN \n3 -> EXIT '.format('|ContactsFolio|'))
		p=int(input())
		if p==1:mainpage.create()
		elif p==2:mainpage.log_in()	
		elif p==3:mainpage.ex_it()		
		else:
			print('Not a Valid Option!!')
			page()
	

	def restore(k,name):
		info='''SELECT * from Recycle;'''
		point.execute(info)
		info='''SELECT * from Recycle WHERE  NAME =(?) AND User_id=(?);'''
		point.execute(info,(name,k))
		info=point.fetchall()
		if info !=[]:
			q=''' DELETE  from PHONEBOOK where User_id=(?) AND NAME=(?);'''
			point.execute(q,(k,name))
			new.commit()
			rest_ore='''INSERT INTO PHONEBOOK VALUES((?),(?),(?),(?),(?));'''
			for x in info:
				point.execute(rest_ore,(k,x[1],x[2],x[3],x[4]))
			new.commit()
			print('Restored {} back to Contacts {} !!'.format(name,k))
			mainpage.option(k)
		else:
			print('No Contacts Found !!')
			mainpage.option(k)

mainpage.page()


