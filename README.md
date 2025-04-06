# Aige of EmpAIre

**Concernant le fichier c_client_optimized.c**
Ce programme en C est le fruit d’un assemblage. Il met en place un système de communication bidirectionnel entre un processus Python local et un réseau local via UDP.
1. Réception depuis Python et mise en mémoire (par Mathis Chauviere)
2. Récupération en mémoire et broadcast sur les interfaces réseau ( par Soufiane Benamar)
3. Réception réseau et mise en mémoire ( par Charles Bel)
4. Récupération depuis la mémoire et renvoi à Python ( par Selma Ben Salah)

# Installation guide

**Step 1: Clone the project**
```
git clone https://github.com/remialban/aige-of-empire.git
```
Instead of using HTTPS, you can clone the project using SSH:
```
git clone git@github.com:remialban/aige-of-empire.git
```
**Step 2: Go to project directory**
```
cd aige-of-empaire
```
**Step 3: Create a virtual environment**

We recommand to create a virtual environment to avoid conflicts with packages already installed.
```
python -m venv .venv
```
**Step 4: Activate the virtual environement**

On a Linux system:
```
source .venv/bin/activate
```
On a Windows system:
```
.\.venv\bin\activate
```
**Step 5: Install packages**
```
pip install -r requirements.txt
```
# Run the game
To run the game, you must activate the virtual environment if it is not already the case:
```
source .venv/bin/activate
```
You can finally start the game by running the ```main.py``` file:
```
python3 main.py
```
