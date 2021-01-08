# -*- coding:utf-8 -*-
import turtle

from PIL import Image
from dreamtools import tools
from dreamtools.cfgmng import CFGBases
from dreamtools.logmng import CTracker

from models import savingbyref


class CPart:
    indice = 0
    ANGLE = 60
    COLOR_ENABLE = '#E1991A'
    COLOR_TAKEN = "#F2aa2b"
    def __init__(self, indice, user=None):
        self.__dict__.update({"indice": indice, 'user':user})

    @property
    def state(self):
        return (self.user)

    def draw(self):
        turtle.hideturtle()
        turtle.speed(20)
        turtle.up()
        turtle.goto(0,0)
        turtle.down()
        angle =( self.indice-1) * 60

        turtle.begin_fill()
        turtle.color(CPart.COLOR_ENABLE if self.user else CPart.COLOR_TAKEN)
        turtle.seth(angle)
        turtle.fd(300)
        turtle.seth(angle + 120)
        turtle.fd(300)
        turtle.seth(angle + 240)
        turtle.fd(300)
        turtle.color('#E1991A')
        turtle.end_fill()

        style = ('Courier', 30, 'italic')

        turtle.up()
        turtle.goto(0, 0)
        turtle.seth(angle+30)
        turtle.fd(300)
        turtle.down()
        turtle.color('black')
        turtle.write(self.user or self.indice,font=style, align='center')


class CGalette :
    GALETTES = []
    parts = []
    ENCOURS=None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def lesfeves ():
        data = CFGBases.loadingbyref('galettes') or []
        gagnant = []
        for g in data:
            feve = int(g.get('feve'))
            for pa in g.get('participants'):
                if feve in pa.values():
                    gagnant.append(pa.get('name'))
        return gagnant

    @classmethod
    def newuser (cls,user):
        turtle.clearscreen()

        data = CFGBases.loadingbyref('galettes') or []
        CGalette.GALETTES = []

        for g in data:
            CGalette.GALETTES.append(CGalette(**g))

        i = 0
        indice = 0
        CGalette.ENCOURS = 0
        next = False

        for galette in  CGalette.GALETTES:
            participants = galette.participants

            if len(participants) >= 6:
                continue

            for participant in participants:
                next = (user in participant.values())
                if next:
                    i+=1
                    if i >= 3:
                        return None
                    break

            if next:
                indice+=1
                continue
            break

        CGalette.ENCOURS = indice

        try:
            galette = CGalette.GALETTES[CGalette.ENCOURS]
            galette.participants.append({'name': user, 'part': 0})
        except:
            rest = CTracker.fntracker(CGalette.newgalette, '')
            CGalette.GALETTES[CGalette.ENCOURS] = galette = CGalette(
                participants=[{'name': user, 'part': 0}],
                feve=tools.aleatoire(6,1),
                image = rest.data,
                numero = CGalette.ENCOURS)

        return galette.image or (5, 'galette0.png')

    @classmethod
    def newtirage (cls, user, choix):
        turtle.clearscreen()

        galette = CGalette.GALETTES[CGalette.ENCOURS]
        participants = galette.participants

        for participant in participants:
            if choix in participant.values():
                return None

        for ii in range(1, 7):
            u = None
            for participant in participants:
                if ii == choix and participant.get('name') == user:
                    participant['part'] = choix
                    u = user
                    break
                elif ii ==  participant.get('part'):
                    u = participant.get('name')

            part = CPart(indice=ii, user=u)
            part.draw()
        CGalette.deco()

        data = []
        for galette in CGalette.GALETTES:
            data.append(galette.__dict__)
        savingbyref(data, 'galettes')

        turtle.getscreen()
        turtle.getcanvas().postscript(file=f"galette{CGalette.ENCOURS}.eps")
        image_eps = 'duck.eps'
        im = Image.open(image_eps)

        image_png = f'galette{CGalette.ENCOURS}.png'
        im.save(image_png)
        fig = im.convert('RGBA')
        fig.save(f'static/{image_png}')




    @classmethod
    def newgalette (cls):


        for ii in range(1,7):
            part = CPart(ii)
            cls.parts.append(part)
            part.draw()
        CGalette.deco()

        ts = turtle.getscreen()
        turtle.getcanvas().postscript(file=f"galette{CGalette.ENCOURS}.eps")
        image_eps = 'duck.eps'
        im = Image.open(image_eps)

        image_png = f'galette{CGalette.ENCOURS}.png'
        im.save(image_png)
        fig = im.convert('RGBA')
        fig.save(f'static/{image_png}')

        return image_png


    @staticmethod
    def deco():
        turtle.color('yellow')
        turtle.up()

        turtle.goto(260, -20)
        turtle.seth(120)
        turtle.down()
        turtle.fd(300)

        turtle.up()
        turtle.goto(255, -40)
        turtle.seth(120)
        turtle.down()
        turtle.fd(330)

        turtle.up()
        turtle.goto(200, -120)
        turtle.down()
        turtle.fd(430)

        turtle.up()
        turtle.goto(195, -140)
        turtle.down()
        turtle.fd(450)

        turtle.up()
        turtle.goto(140, -220)
        turtle.down()
        turtle.fd(550)

        turtle.up()
        turtle.goto(135, -240)
        turtle.down()
        turtle.fd(570)

        turtle.up()
        turtle.goto(60, -240)
        turtle.down()
        turtle.fd(480)

        turtle.up()
        turtle.goto(40, -240)
        turtle.down()
        turtle.fd(450)

        turtle.up()
        turtle.goto(-10, -240)
        turtle.down()
        turtle.fd(380)

        turtle.up()
        turtle.goto(-25, -240)
        turtle.down()
        turtle.fd(360)

        # -------------

        turtle.up()
        turtle.goto(-260, -20)
        turtle.seth(60)
        turtle.down()
        turtle.fd(300)

        turtle.up()
        turtle.goto(-255, -40)
        turtle.down()
        turtle.fd(330)

        turtle.up()
        turtle.goto(-200, -120)
        turtle.down()
        turtle.fd(430)

        turtle.up()
        turtle.goto(-195, -140)
        turtle.down()
        turtle.fd(450)

        turtle.up()
        turtle.goto(-140, -220)
        turtle.down()
        turtle.fd(550)

        turtle.up()
        turtle.goto(-135, -240)
        turtle.down()
        turtle.fd(570)

        turtle.up()
        turtle.goto(-60, -240)
        turtle.down()
        turtle.fd(480)

        turtle.up()
        turtle.goto(-40, -240)
        turtle.down()
        turtle.fd(460)

        turtle.up()
        turtle.goto(10, -240)
        turtle.down()
        turtle.fd(400)

        turtle.up()
        turtle.goto(25, -240)
        turtle.down()
        turtle.fd(380)
        turtle.up()

        turtle.goto(2, 2)
        turtle.down()
        turtle.pensize(2)
        for angle in range(0, 360, 60):
            turtle.color('#654f29')
            turtle.seth(angle)
            turtle.fd(300)
            turtle.seth(angle + 120)
            turtle.fd(300)
            turtle.seth(angle + 240)
            turtle.fd(300)


