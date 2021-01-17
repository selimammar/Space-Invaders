##Python 3.7

##Space Invader

##18/12/2020

##Selim Ammar   Reda Laborieux

##ToDo: Développement d'un jeu : Space invaders


from tkinter import *
from random import choice

class Alien:
    def __init__(self, posx, posy,canvas,tir,image,height,width,coeur):
        self.positionX = posx
        self.positionY = posy
        self.canvas = canvas
        self.tir=tir
        self.image=image
        self.width=width
        self.height=height
        self.coeur=coeur

class Player:
    def __init__(self, vie, posx, posy,score,canvas,tir,tirchoisi,tirCanvas,level,vitesse):
        self.positionX = posx
        self.positionY = posy
        self.canvas=canvas
        self.vie=vie
        self.score=score
        self.tir=tir
        self.tirCanvas=tirCanvas
        self.level=level
        self.choix=tirchoisi
        self.vitesse=vitesse

class Tir:
    def __init__(self,nom,vitesse,image,width,height,color):
        self.nom=nom
        self.vitesse=vitesse
        self.image=image
        self.width=width
        self.height=height
        self.color=color


def AlienPosition(aliens):
    for i in aliens:
        alien=canvas.create_image(i.positionX,i.positionY,image=i.image,anchor='nw')
        i.canvas=alien
        if i.coeur!=None:
            coeur = canvas.create_rectangle(i.positionX + 111, i.positionY + 80, i.positionX + 150, i.positionY + 115, fill='red')
            i.coeur = coeur

def VaisseauPostion(player):
    vaisseau = canvas.create_image(w//2,h-133,image=image_vaisseau,anchor='nw')
    player.canvas=vaisseau

def Menu(player,label):
    global life
    for i in range(player.vie):
        coeur=canvas.create_image(w-30-i*30, 0, image=image_coeur, anchor='nw')
        life.append(coeur)
    label.place(x=w-30-i*30,y=10,anchor='e')
    score.config(text='score : '+ str(player.score),bg='black',fg='white',font='bold' )

def tirAlien(aliens):
    global proba
    if len(aliens)>0:
        flag=choice(proba)
        alien=choice(aliens)
        if flag and not pause:
            x=alien.positionX+alien.width//2
            y=alien.positionY+alien.height
            tir = canvas.create_rectangle(x,y,x+3,y+20,fill='yellow')
            animationTirAlien(tir,y)
        if not pause:
            window.after(500,tirAlien,aliens)

def animationTirAlien(tir,y):
    y = y + 20
    if 0<y<h-200:
        canvas.move(tir,0,50)
        window.after(50,animationTirAlien,tir,y)
    elif h>y>=h-200 :

        if  ContactAlien():
            canvas.move(tir, 0, 20)
            window.after(20, animationTirAlien, tir,  y)
        else:
            canvas.delete(window,tir)
    else:
        canvas.delete(window,tir)

def ContactAlien():
    global player,label
    cord=canvas.coords(player.canvas)
    coord_rect = cord+[cord[0]+130,cord[1]+200]
    items = canvas.find_overlapping(*coord_rect)
    if len(items)>=2:
        canvas.delete(items[1])
        player.vie-=1
        if player.vie>0:
            for coeur in life:
                canvas.move(coeur,30,0)
        else:
            GameOver()
        return False
    return True

def Pause(event):
    global pause
    pause = not pause
    allienMoveR()
    move()
    tirAlien(aliens)
    if  pause:
        txt='level :'+str(player.level)
        Level.config(text=txt)
        HowToPlay.config(text='Commande:\n ''appuyer sur "P" pour commencer \n''→ ou ← pour se deplacer \n''[Space] pour tirer',font=('bold',30),fg='white')
        HowToPlay.place(x=w//2,y=h//2,anchor='center')
        Level.place(x=w//2,y=h//2-300,anchor='center')
    else:
        Level.place(x=w+100,y=-100)
        HowToPlay.place(x=w+1000,y=-1000)

def allienMoveR():
    global aliens,dx
    BigX=0
    y=0
    if not pause:
        for alien in aliens:
            if alien.positionX>BigX:
                BigX=alien.positionX+alien.width
                y=alien.positionY
        if BigX+dx<w:
            for alien in aliens:
                alien.positionX+=dx
                canvas.move(alien.canvas,dx,0)
                if alien.coeur!=None:
                    canvas.move(alien.coeur,dx,0)
            window.after(100,allienMoveR)
        else :
            if y<=h-170:
                for alien in aliens:
                    alien.positionY+=20

                    alien.positionX += dx
                    canvas.move(alien.canvas,dx,20)
                    if alien.coeur != None:
                        canvas.move(alien.coeur, dx, 20)
                allienMoveL()
            else:
                player.vie=0
                GameOver()

def allienMoveL():
    global aliens,dx
    LowX=w
    y=0
    if not pause:
        for alien in aliens:
            if alien.positionX<LowX:
                LowX=alien.positionX
                y=alien.positionY

        if LowX-dx>0:
            for alien in aliens:
                alien.positionX-=dx
                canvas.move(alien.canvas,-dx,0)
                if alien.coeur != None:
                    canvas.move(alien.coeur, -dx, 0)
            window.after(100,allienMoveL)
        else :
            if y<=h-170:
                for alien in aliens:
                    alien.positionY += 20
                    alien.positionX -= dx

                    canvas.move(alien.canvas, -dx, 20)
                    if alien.coeur != None:
                        canvas.move(alien.coeur, -dx, 20)
                allienMoveR()
            else:
                player.vie=0
                GameOver()

def move():
    global player
    if not pause:
        dx=player.vitesse

        if direction=='R' and player.positionX+137+10<w:
            player.positionX+=dx
            canvas.move(player.canvas,dx,0)

        elif direction=='L' and player.positionX>9:
            player.positionX-=dx
            canvas.move(player.canvas, -dx, 0)
        window.after(50, move)

def GameOver():
    Pause(None)
    HowToPlay.config(text='Game Over \n'
                          'press P to restart',fg='red',font=('bold',40))
    DestroyAll(None)
    Restart()

def Restart():
    global aliens, player, dx
    A1 = Alien(0, 40, None, None,image_alien,37,52,None)
    A2 = Alien(70, 40, None, None,image_alien,37,52,None)
    A3 = Alien(140, 40, None, None,image_alien,37,52,None)
    A4 = Alien(210, 40, None, None,image_alien,37,52,None)
    A5 = Alien(280, 40, None, None,image_alien,37,52,None)
    aliens = [A1, A2, A3, A4, A5]
    player.level=1
    player.vie=3
    dx=20
    player.score=0
    player.vitesse=10
    Tir1.height=10
    Tir1.width=3
    Tir1.vitesse=-20
    Menu(player,label)
    AlienPosition(aliens)

def tir(event):
    global player
    bullet=Tirs[player.choix]
    x=bullet.width
    y=bullet.height
    if player.tir==None and not pause:
        if bullet.nom=='normal':
            player.tir=[player.positionX+58,player.positionY-bullet.height]
            tir = canvas.create_rectangle(player.tir[0],player.tir[1],player.tir[0]+x,player.tir[1]+y,fill=bullet.color)
            player.tirCanvas=tir
        animation()

def changDirection(event):
    global direction
    if event.keysym == 'Right' and player.positionX+117 < w:
        direction='R'
    elif event.keysym == 'Left' and player.positionX > 0:
        direction='L'

def arret(event):
    global direction
    if event.keysym == 'Right':
        direction = None
    elif event.keysym == 'Left':
        direction = None

def OnMotion(event):
    deltax = event.x
    deltay = event.y
    print(deltax,deltay)

def DestroyAll(event):
    global aliens
    for i in aliens:
        canvas.delete(window,i.canvas)
        if i.coeur!=None:
            canvas.delete(window,i.coeur)

def animation():
    global player
    PosTy = player.tir[1]
    bullet = Tirs[player.choix]
    if PosTy> 0 and player.tir != None :
        canvas.move(player.tirCanvas,0,bullet.vitesse)
        if Hit(aliens):
            window.after(40, animation)
            player.tir[1] += bullet.vitesse
    if PosTy < 10:
        canvas.delete(window,player.tirCanvas)
        player.tir = None

def Hit(aliens):
    global dx,player
    bullet=Tirs[player.choix]
    tir = player.tirCanvas
    coord_rect = canvas.coords(tir)
    items = canvas.find_overlapping(*coord_rect)
    X = bullet.width
    Y = bullet.height
    tir=[player.tir[0],player.tir[0]+X,player.tir[1],player.tir[1]+Y]
    canvas.delete(window, tir)
    if len(aliens)>0:
        if len(items)>=2:
            for alien in aliens:
                if alien.coeur==None:
                    if alien.canvas==items[0]:
                        DestroyAll(None)
                        aliens.remove(alien)
                        WIN()
                        AlienPosition(aliens)
                        player.tir=None
                        canvas.delete(window,player.tirCanvas)
                        dx+=5
                        player.score+=25
                        Menu(player,label)
                        return False
                else:
                    if alien.coeur == items[1] or alien.coeur==items[0]:
                        DestroyAll(None)
                        aliens.remove(alien)
                        WIN()
                        AlienPosition(aliens)
                        player.tir = None
                        canvas.delete(window, player.tirCanvas)
                        dx += 5
                        player.score += 200
                        Menu(player, label)
                        return False
                    elif len(items)==2 and items[0]==alien.canvas:
                        canvas.delete(window, player.tirCanvas)
                        player.tir=None

                        A1 = Alien(0, 40, None, None, image_alien, 37, 52, None)
                        A2 = Alien(70, 40, None, None, image_alien, 37, 52, None)
                        A3 = Alien(140, 40, None, None, image_alien, 37, 52, None)
                        A4 = Alien(210, 40, None, None, image_alien, 37, 52, None)
                        A5 = Alien(280, 40, None, None, image_alien, 37, 52, None)
                        aliens += [A1, A2, A3, A4, A5]
                        DestroyAll(None)
                        AlienPosition(aliens)
        return True
    else:
        WIN()

def WIN():
    if len(aliens)==0:
        player.level+=1
        Pause(None)
        HowToPlay.config(text='YOU WIN \n'
                              'press P to go for next level ',fg='red',font=('bold',40))
        NextLevel()

def NextLevel():
    global aliens,player,dx
    dx=20
    nb_ligne=player.level%5
    A1 = Alien(0, 40, None, None,image_alien,37,52,None)
    A2 = Alien(70, 40, None, None,image_alien,37,52,None)
    A3 = Alien(140, 40, None, None,image_alien,37,52,None)
    A4 = Alien(210, 40, None, None,image_alien,37,52,None)
    A5 = Alien(280, 40, None, None,image_alien,37,52,None)
    aliens=[A1,A2,A3,A4,A5]
    newaliens=[]
    for j in range(nb_ligne):
        for i in aliens :
            alien=Alien(i.positionX,i.positionY+j*40,None,None,image_alien,37,52,None)
            newaliens.append(alien)
    player.vie+=1
    dx=20+5*(player.level-1)
    aliens=newaliens
    AlienPosition(aliens)

direction = None
proba=[1,0,0,0,0]
dx=20
pause = 0
life=[]
window = Tk()

## images
image_vaisseau = PhotoImage(file='111%.gif')
image_alien = PhotoImage(file='alien3.gif')
image_coeur = PhotoImage(file='coeur.gif')

## taille de l'ecran
w = window.winfo_screenwidth()
h = window.winfo_screenheight()
window.overrideredirect(1)
window.geometry("%dx%d+0+0" % (w, h))
window.title('SpaceInvader')
window['bg']='black'
canvas= Canvas(width=w, height=h, bg='black', highlightthickness=0)
canvas.pack()

## les alliens
A1=Alien(70,40,None,None,image_alien,37,52,None)
A2=Alien(140,40,None,None,image_alien,37,52,None)
A3=Alien(210,40,None,None,image_alien,37,52,None)
A4=Alien(280,40,None,None,image_alien,37,52,None)
A5=Alien(350,40,None,None,image_alien,37,52,None)
aliens=[A1,A2,A3,A4,A5]
AlienPosition(aliens)

##Tir
Tir1=Tir('normal',-20,None,3,20,'yellow')
Tir2=Tir('double',-20,None,3,20,'red')
Tir3=Tir('boule',-20,None,8,8,'blue')
Tirs=[Tir1,Tir2,Tir3]

## vaisseau
player=Player(3,w//2,h-132,0,None,None,0,None,1,10)
VaisseauPostion(player)
score=Label(text='score : '+ str(player.score),bg='black',fg='white',font='bold' )
score.place(x=0,y=0)
label=Label(text='[ESC] to quit | [P] pause',bg='black',fg='white',font='bold')
Menu(player,label)

##menu pause
Level=Label(text='',font=('Bold',40),bg='black',fg='white')
Level.place(y=100,x=w//2,anchor='center')
HowToPlay=Label(text='',font=('Bold',20),bg='black', fg='white')
HowToPlay.place(y=h//2,x=w//2,anchor='center')
changDirection

##debut
Pause(None)
allienMoveR()
move()

window.bind("<Escape>", exit)
window.bind('<KeyPress-p>',Pause)
window.bind('<KeyPress-space>',tir)
window.bind("<KeyPress>",)
window.bind("<KeyRelease>",arret)
window.bind("<ButtonPress-1>", OnMotion)
window.mainloop()

