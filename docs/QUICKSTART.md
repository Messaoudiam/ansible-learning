# 🚀 Guide de Démarrage Rapide

## ✅ Test Réussi !

Félicitations ! Vous venez de tester avec succès Ansible sur votre système. La page web générée automatiquement confirme qu'Ansible fonctionne correctement.

## 🎯 Prochaines Étapes

### Option 1: Serveur Web Simple (Recommandé pour débuter)

Vous avez déjà testé cette option avec succès ! Pour la relancer :

```bash
# Exécuter le playbook de test
ansible-playbook site-local.yml

# Démarrer le serveur web
cd web
python3 -m http.server 8080

# Visiter http://localhost:8080
```

### Option 2: Installation d'Apache (Playbook Complet)

Pour utiliser le playbook complet avec Apache, vous devez résoudre le problème de sudo.

#### Solution A: Mot de passe sudo interactif

```bash
# Demander le mot de passe sudo
ansible-playbook site.yml --ask-become-pass
```

#### Solution B: Configuration sudo sans mot de passe (pour développement)

```bash
# Éditer la configuration sudo (ATTENTION: seulement pour dev/test)
sudo visudo

# Ajouter cette ligne (remplacez 'votreusername' par votre nom d'utilisateur):
votreusername ALL=(ALL) NOPASSWD: ALL

# Puis tester:
ansible-playbook site.yml
```

#### Solution C: Utiliser Homebrew pour installer Apache

```bash
# Sur macOS, installer Apache via Homebrew (sans sudo)
brew install httpd

# Modifier le playbook pour utiliser Homebrew
# (voir section personnalisation ci-dessous)
```

### Option 3: Docker (Alternative)

```bash
# Créer un conteneur Ubuntu pour tester
docker run -d --name ansible-test -p 8080:80 ubuntu:22.04 sleep 3600

# Exécuter le playbook sur le conteneur
# (nécessite configuration Docker + SSH)
```

## 🔧 Personnalisation du Projet

### Modifier le Port

```bash
# Dans group_vars/all.yml
default_http_port: 8080

# Ou en ligne de commande
ansible-playbook site-local.yml -e "web_port=9000"
```

### Ajouter vos Variables

```yaml
# Dans group_vars/all.yml
company_name: "Mon Entreprise"
admin_email: "admin@example.com"
```

### Personnaliser la Page Web

Éditez le fichier `roles/webserver/templates/index.html.j2`

## 🎓 Exercices Pratiques

### Exercice 1: Modifier le Message

1. Ouvrez `group_vars/all.yml`
2. Modifiez `demo_string`
3. Relancez `ansible-playbook site-local.yml`
4. Vérifiez le changement sur http://localhost:8080

### Exercice 2: Ajouter une Variable

1. Ajoutez `mon_nom: "VotreNom"` dans `group_vars/all.yml`
2. Utilisez `{{ mon_nom }}` dans le template HTML
3. Testez le résultat

### Exercice 3: Tags

```bash
# Ajouter des tags dans site-local.yml
- name: "Ma tâche"
  debug: msg="Test"
  tags: [info]

# Exécuter seulement les tâches avec ce tag
ansible-playbook site-local.yml --tags "info"
```

## 🐛 Dépannage

### Erreur "service is not a valid attribute"
✅ **Résolu** - Problème de syntaxe YAML corrigé

### Erreur "sudo password required"
- Utilisez `--ask-become-pass`
- Ou configurez sudo sans mot de passe
- Ou utilisez `site-local.yml` pour les tests

### Erreur "connection refused"
- Vérifiez que le serveur web est démarré
- Vérifiez le port (8080 par défaut pour site-local.yml)
- Testez avec `curl http://localhost:8080`

### Python interpreter warning
Cette alerte est normale et ne pose pas de problème pour l'apprentissage.

## 📚 Ressources

- **Documentation officielle**: https://docs.ansible.com/
- **Ansible Galaxy**: https://galaxy.ansible.com/
- **Communauté**: /r/ansible sur Reddit

## 🎯 Structure Recommandée pour la Suite

```
mes-projets-ansible/
├── 01-webserver-simple/     # Ce projet
├── 02-lamp-stack/           # Prochain: LAMP complet
├── 03-multi-serveurs/       # Puis: plusieurs serveurs
└── 04-production/           # Enfin: configuration production
```

## ✨ Conclusion

Vous avez maintenant :
- ✅ Un projet Ansible fonctionnel
- ✅ Une compréhension des concepts de base
- ✅ Un environnement de test
- ✅ Des exercices pour progresser

**Prochaine étape recommandée** : Faire les exercices du README.md pour solidifier vos connaissances !

---

💡 **Astuce** : Gardez ce projet comme référence. C'est un excellent point de départ pour vos futurs projets Ansible !