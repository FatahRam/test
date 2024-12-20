from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import User, jeu_de_reference, piece_standard, piece_exemplaire, exemplaire, pret, fussion_historique
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import random

import requests
import warnings
import json

# Create your views here.

def register(request): # Une vue de creation de compte pour les clients
    msg=None
    if request.method =='POST':
        usernamee = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            msg = "Les deux mot de passe doivent etre identiques"
            return render(request, 'ludothequeapp/register.html', {'msg':msg})
        if len(password1)<8:
            msg = "Le mot de passe doit contenir obligatiore 8 caracteres"
            return render(request, 'ludothequeapp/register.html', {'msg':msg})
        if User.objects.filter(username=usernamee).exists():
            msg = "Ce Pseudi exist déja, Veuillez choisir un autre pseudo"
            return render(request, 'ludothequeapp/register.html', {'msg':msg})
        if User.objects.filter(email=email).exists():
            msg = "Ce mail exist déja, Veuillez choisir un autre mail"
            return render(request, 'ludothequeapp/register.html', {'msg':msg})
        print(usernamee, email, phone, password1, password2)
        user = User.objects.create_user(username=usernamee,email=email,phone_nbr=phone,password=password1)
        return render(request, 'ludothequeapp/connexion.html')
    return render(request, 'ludothequeapp/register.html', {'msg':msg})

def connexion(request): #Une vue de connexion
    msg = None
    a = exemplaire.objects.all()
    p=1
    for c in a:
        e = piece_exemplaire.objects.filter(ex_id=c.id)
        j = piece_standard.objects.filter(jeu_id=c.jeu_id)
        for h in j:
            if h.essentiel == True:
                print(c.jeu_id)
                print(h.id)
                e = piece_exemplaire.objects.filter(ex_id=c.id, pis_id=h.id).first()
                if e.presente == True and p != 0:
                    p=1
                else:
                    p=0
        if p==1:
            c.jouable=True
            c.save()
        else:
            c.jouable=False
            c.save()
    if request.method =='POST':
        usernamee = request.POST['username']
        passworde = request.POST['password']
        user = authenticate(request, username=usernamee, password=passworde)
        print(usernamee,passworde)
        print(user)
        if not usernamee or not passworde:
            msg='Veuillez saisir les champs svp'
            return render(request, 'ludothequeapp/connexion.html',{'msg':msg})
            #return render (request, 'registration/password_change_form.html')
        
        if user is not None:
            login(request, user)
            if user.is_staff==True:
                request.session['user_id'] = user.id
                request.session['is_staff'] = user.is_staff
                request.session['username'] = user.username
                request.session['email'] = user.email
                request.session['phone'] = user.phone_nbr
                a = exemplaire.objects.filter(jouable=True, dispo=False)
                return render(request, 'ludothequeapp/home1.html', {'a':a})
            request.session['user_id'] = user.id
            request.session['is_staff'] = user.is_staff
            request.session['username'] = user.username
            request.session['email'] = user.email
            request.session['phone'] = user.phone_nbr
            t = jeu_de_reference.objects.all()
            return render(request, 'ludothequeapp/home.html', {'id':request.session.get('user_id'), 'username':request.session.get('username'), 'email':request.session.get('email'), 'first': request.session.get('first'), 'jdr':t})
        else:
            msg ="Utilisateur n'existe pas"
            return render(request, 'ludothequeapp/connexion.html', {'msg':msg})
    return render(request, 'ludothequeapp/connexion.html',{'msg':msg})


@login_required
def home(request):
    a = exemplaire.objects.all()
    p=1
    for c in a: #Parcourir tous les exemplaire
        e = piece_exemplaire.objects.filter(ex_id=c.id)
        j = piece_standard.objects.filter(jeu_id=c.jeu_id)
        for h in j: # Parcourir tous les pieces standard d'un jeu de reference d'un exemplaire c in a
            if h.essentiel == True: #verification si la piece standard est essentiel 
                e = piece_exemplaire.objects.filter(ex_id=c.id, pis_id=h.id).first() # Recuperer la piece exemplaire qui est essentiel,
                if e.presente == True and p != 0: #verification est ce que la piece exemplaire essentiel est presente
                    p=1
                else:
                    p=0
        if p==1: # Si tous les pieces standard essentiel sont presentes mettes l'exemplaire jouable c in a
            c.jouable=True
            c.save()
        else: # Sinon mettre l'exemplaire pas jouable
            c.jouable=False
            c.save()
    t = jeu_de_reference.objects.all()
    return render(request, 'ludothequeapp/home.html', {'jdr':t})


@login_required
def home1(request):
    r = request.session.get('is_staff')
    if r:
        a = exemplaire.objects.filter(jouable=True, dispo=False)
        return render(request, 'ludothequeapp/home1.html', {'a':a})
    else:
        t = jeu_de_reference.objects.all()
        return render(request, 'ludothequeapp/home.html', {'id':request.session.get('user_id'), 'username':request.session.get('username'), 'email':request.session.get('email'), 'first': request.session.get('first'), 'jdr':t})

@login_required
def fus(request):
    s = request.session.get('is_staff')
    if s:
        pass
    else:
        t = jeu_de_reference.objects.all()
        return render(request, 'ludothequeapp/home.html', {'id':request.session.get('user_id'), 'username':request.session.get('username'), 'email':request.session.get('email'), 'first': request.session.get('first'), 'jdr':t})
    
    a = exemplaire.objects.all()
    if request.method =='POST':
        ex1 = request.POST['ex1']
        ex2 = request.POST['ex2']
        b = piece_exemplaire.objects.filter(ex_id=ex1, presente=False)
        c = piece_exemplaire.objects.filter(ex_id=ex2, presente=True)
        t1 = exemplaire.objects.get(id=ex1)
        t2 = exemplaire.objects.get(id=ex2)
        m=0
        for j in b:
            for k in c:
                if j.pis_id == k.pis_id:
                    j.presente=True
                    k.presente=False
                    j.save()
                    k.save()
                    m=m+1
        r = fussion_historique(id_user_id=request.session.get('user_id'), ex1=t1, ex2=t2, total=m)
        r.save()
        msg=f"Nombre de piéces fussionner est : {m}"
        return render(request, 'ludothequeapp/fus.html', {'a':a, 'msg':msg})
    return render(request, 'ludothequeapp/fus.html', {'a':a})


def home2(request):
    t = jeu_de_reference.objects.all()
    return render(request, 'ludothequeapp/home2.html', {'jdr':t})


@login_required
def show(request, idl): # Une vue permet de voir tous les pieces standard d'un jeu de reference donner
    request.session['jdr_id'] = idl
    idd = request.session.get('jdr_id')
    nbr1 = piece_standard.objects.filter(jeu_id=idl)
    
    return render(request, 'ludothequeapp/show.html', {'nbr':nbr1})


@login_required
def show1(request, idl): #Une vue permet de recuperer tous les exemplaires d'un jeu de reference donner
    request.session['jdr_id'] = idl
    idd = request.session.get('jdr_id')
    n = jeu_de_reference.objects.get(id=idl)
    name = n.nom
    nbr1 = exemplaire.objects.filter(jeu_id=idl)
    
    return render(request, 'ludothequeapp/show1.html', {'nbr':nbr1, 'name':name})

@login_required
def show2(request, idl): # Une vue permet de recuperer tous les pieces d'un exemplaires donner
    request.session['exp_id'] = idl
    nbr1 = piece_exemplaire.objects.filter(ex_id=idl)
    return render(request, 'ludothequeapp/show2.html',{'nbr':nbr1})

@login_required
def pre(request, idl): #Une vue permet pour un client de prete un jeu
    request.session['ex_id'] = idl
    if request.method =='POST':
        date = request.POST['date'] #L'utilisateur saisir la date de retour sur le formulaire
        a = exemplaire.objects.get(id=idl)
        a.dispo = False # faire le champ dispo False Pour dire que n'est pas disponible a preter
        a.save()
        b = pret(id_user_id=request.session.get('user_id'), ex_id=request.session.get('ex_id'), date_retour=date)
        b.save()
        msg="L'xemplaire est bien prété veuillez venez pour le recuperer"
        return render (request, 'ludothequeapp/show1.html', {'msg':msg})
    return render(request,'ludothequeapp/pre.html', {'id':idl})

@login_required
def pre1(request, idl): # Une vue permet de remetre l'exemplaire dispo soit apres le retour apres le pret soit par l'administrateur pour des reseaux interne
    a = exemplaire.objects.get(id=idl)
    a.dispo=True
    a.save()
    a = exemplaire.objects.filter(jouable=True, dispo=False)
    return render(request, 'ludothequeapp/home1.html', {'a':a})

@login_required
def his(request, idl): # Une vue permet de voir tous l'historique des prets d'un exemplaire donner
    a = pret.objects.filter(ex_id=idl)
    return render(request, 'ludothequeapp/his.html', {'a':a})

@login_required
def vis(request, idl): #Une vue permet de recuperer tous les exemplaire incomplet d'un jeu de reference donner
    a = exemplaire.objects.filter(jeu_id=idl, jouable=False)
    return render(request,'ludothequeapp/vis.html', {'a':a})


@login_required
def deconnexion(request):
    logout(request)
    return redirect('connexion')
