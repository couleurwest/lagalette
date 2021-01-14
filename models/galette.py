# -*- coding:utf-8 -*-
import turtle

from PIL import Image
from dreamtools import tools
from dreamtools.cfgmng import CFGBases

import resource


class CPart:
    indice = 0
    ANGLE = 60
    COLOR_ENABLE = '#E1991A'
    COLOR_TAKEN = "#F2aa2b"

    def __init__(self, indice, user=None):
        self.indice = indice
        self.user = user

    @property
    def state(self):
        return self.user

    def draw(self):
        turtle.speed(0)
        turtle.up()
        turtle.goto(0, 0)
        turtle.down()
        angle = (self.indice - 1) * 60

        turtle.begin_fill()
        turtle.color("#f7e7b2")
        turtle.seth(angle)
        turtle.fd(300)
        turtle.seth(angle + 120)
        turtle.color('#ce9d00')
        turtle.pensize(3)
        turtle.fd(300)
        turtle.color('#f7e7b2')
        turtle.pensize(1)
        turtle.seth(angle + 240)
        turtle.fd(300)
        turtle.color(CPart.COLOR_ENABLE if self.user else CPart.COLOR_TAKEN)
        turtle.end_fill()

        style = ('Courier', 20, 'italic')

        turtle.up()
        turtle.goto(0, 0)
        turtle.seth(angle + 30)
        turtle.fd(300)
        turtle.down()
        turtle.color('#5b4600')
        turtle.write(self.user or self.indice, font=style, align='center')


class CGalette:
    GALETTES = []
    parts = []
    ENCOURS = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def state_user(user):
        data = CFGBases.loadingbyref('participants', user) or {}
        data = {'count': len(data), 'participations': data}
        return data

    @staticmethod
    def participation():
        return CFGBases.loadingbyref('galettes') or []

    @staticmethod
    def newuser(user):
        fiche_user = CGalette.state_user(user)

        if fiche_user['count'] >= 3:
            return fiche_user

        CGalette.loading()
        indice = 0
        CGalette.ENCOURS = 0

        for galette in CGalette.GALETTES:
            participants = galette.participants

            if len(participants) >= 6 and participants.get(user) != 0:
                indice += 1
                continue
            elif user not in participants or participants.get(user) == 0:
                break
            indice += 1

        CGalette.ENCOURS = indice

        if 0 < len(CGalette.GALETTES) <= indice:
            galette = CGalette(
                participants={user: 0},
                feve=tools.aleatoire(6, 1),
                numero=CGalette.ENCOURS)
            CGalette.GALETTES.append(galette)

        CGalette.save()
        return fiche_user

    @staticmethod
    def save():
        data = []
        for galette in CGalette.GALETTES:
            data.append(galette.__dict__)
        resource.savingbyref(data, 'galettes')

    @staticmethod
    def loading():
        data = CFGBases.loadingbyref('galettes') or []
        CGalette.GALETTES = []

        for g in data:
            CGalette.GALETTES.append(CGalette(**g))

    @staticmethod
    def newtirage(user, choix):
        """
        Enregistrement du tirage d'une part par un participant
        :param str user: Nom du participant
        :param int choix: indice de la part choisis
        :return: L'état de l'enregistrement
        """

        # recupération de la liste des participants
        participants = CFGBases.loadingbyref('participants') or {}
        if user not in participants:
            participants[user] = []

        participations = participants[user]

        # Traitement de la participation 3 partiticpation max
        if len(participations) < 3:
            # Enregistrement particpants / participation
            participations.append({'galette': CGalette.ENCOURS, 'part': int(choix)})
            resource.savingbyref(participants, 'participants')

            # Enregistrement galettes / participant
            CGalette.loading()
            galettes = CGalette.GALETTES
            galette = galettes[CGalette.ENCOURS]
            participants = galette.participants
            participants[user] = choix
            CGalette.save()

            return True
        return False

    @staticmethod
    def newgalette():
        indice = CGalette.ENCOURS
        galette = CGalette.GALETTES[indice]
        participants = galette.participants

        dir_image = resource.get_resource_path('images')
        nameimage = f'galette{indice}.png'
        pathimage = f'{dir_image}/{nameimage}'

        ts = turtle.getscreen()
        ts.clear()
        turtle.hideturtle()
        turtle.speed(0)

        for ii in range(1, 7):
            u = None
            for participant, part in participants.items():
                if ii == int(part):
                    u = participant

            part = CPart(indice=ii, user=u)
            part.draw()

        CGalette.deco()

        image_eps = f"{nameimage[:-3]}eps"
        ts.getcanvas().postscript(file=image_eps)
        im = Image.open(image_eps)

        fig = im.convert('RGBA')
        fig.save(pathimage)

        return nameimage, participants.values()

    @staticmethod
    def deco():
        turtle.speed(0)
        turtle.pensize(2)
        turtle.color('#ffc200')
        turtle.up()

        turtle.goto(260, -20)
        turtle.seth(120)
        turtle.down()
        turtle.fd(300)

        turtle.up()
        turtle.goto(255, -40)
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
        turtle.color('#a07a00')
        for angle in range(0, 360, 60):
            turtle.seth(angle)
            turtle.fd(300)
            turtle.seth(angle + 120)
            turtle.fd(300)
            turtle.seth(angle + 240)
            turtle.fd(300)
