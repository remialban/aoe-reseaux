import random
import time

def generate_id():
    # Récupérer la date actuelle
    current_time = time.localtime()
    
    # Format de la date (YYYYMMDD)
    date_part = time.strftime("%Y%m%d", current_time)
    
    # Récupérer les secondes écoulées dans la minute
    seconds_in_minute = current_time.tm_sec
    
    # Générer un nombre aléatoire de 10 chiffres
    random_part = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    
    # Combiner toutes les parties
    id_generated = f"{date_part}{seconds_in_minute:02d}{random_part}"
    
    return int(id_generated)

# Exemple d'utilisation
generated_id = generate_id()
print(generated_id)
