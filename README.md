# Keylogger Python

Un keylogger simple en Python qui capture les frappes clavier et les envoie périodiquement par email ou les sauvegarde dans un fichier local.

---

## Fonctionnalités

* Capture des frappes clavier en temps réel.
* Gestion des touches spéciales (espace, entrée, tabulation, etc.).
* Envoi automatique des logs par email via SMTP.
* Option de sauvegarde locale dans un fichier texte.
* Configuration simple avec choix du mode de rapport.
* Timer intégré pour envoyer ou enregistrer les logs à intervalle régulier.

---

## Prérequis

* Python 3.x
* Bibliothèque `keyboard` (à installer via pip)

  ```bash
  pip install keyboard
  ```
* Accès à un serveur SMTP (Gmail, Outlook, Yahoo, etc.) pour l’envoi par email.

---

## Usage

1. **Lancer le script :**

   ```bash
   sudo /chemin/absolu/vers/.venv/bin/python keylogger.py
   ```

2. **Configurer le mode de rapport :**
   Choisir entre `email` ou `file`.

3. **Si mode email :**

   * Entrer votre adresse email.
   * Entrer votre mot de passe (le mot de passe ne s'affichera pas).
   * Choisir votre fournisseur (gmail, outlook, yahoo...).

4. **Le keylogger démarre et capture les frappes clavier.**

   * Les logs sont envoyés ou sauvegardés toutes les N secondes (configurable dans le script).

5. **Arrêter le keylogger :**

   * Utiliser CTRL+C dans le terminal.

---

## Remarques importantes

* Ce projet est à but éducatif uniquement.
* Utiliser ce keylogger uniquement sur des machines où vous avez l’autorisation explicite.
* La collecte de données à l’insu d’un utilisateur est illégale dans de nombreux pays.

---

## Personnalisation

* Modifier l’intervalle d’envoi dans la création de l’objet `Keylogger` (paramètre `interval` en secondes).
* Ajouter ou modifier les touches spéciales dans le dictionnaire `special_keys` dans la méthode `callback`.

---

## Licence

Projet open-source libre, à modifier et utiliser selon vos besoins.

---