# 🚀 Projet Ansible d'Apprentissage

Bienvenue dans ce projet Ansible minimaliste mais complet, conçu spécialement pour l'apprentissage des concepts fondamentaux d'Ansible.

## 📋 Table des Matières

- [Vue d'ensemble](#-vue-densemble)
- [Prérequis](#-prérequis)
- [Structure du projet](#-structure-du-projet)
- [Premiers pas](#-premiers-pas)
- [Concepts Ansible expliqués](#-concepts-ansible-expliqués)
- [Commandes utiles](#-commandes-utiles)
- [Dépannage](#-dépannage)
- [Exercices pratiques](#-exercices-pratiques)
- [Prochaines étapes](#-prochaines-étapes)

## 🎯 Vue d'ensemble

Ce projet déploie automatiquement un serveur web Apache avec une page d'accueil personnalisée. Il illustre les bonnes pratiques Ansible tout en restant simple à comprendre.

### Fonctionnalités

- ✅ Installation et configuration automatique d'Apache
- ✅ Page web dynamique avec informations système
- ✅ Configuration adaptative (Ubuntu/Debian et CentOS/RHEL)
- ✅ Gestion des services et handlers
- ✅ Utilisation des templates Jinja2
- ✅ Variables hiérarchisées
- ✅ Tests et validations automatiques

## 🔧 Prérequis

### Sur votre machine de contrôle (là où vous exécutez Ansible)

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ansible python3-pip

# CentOS/RHEL/Fedora
sudo yum install epel-release
sudo yum install ansible python3-pip

# macOS
brew install ansible

# Vérifier l'installation
ansible --version
```

### Sur les serveurs cibles

- Accès SSH configuré
- Utilisateur avec privilèges sudo
- Python installé (généralement présent par défaut)

## 📁 Structure du projet

```
ansible-learning/
├── ansible.cfg          # Configuration Ansible
├── inventory            # Liste des serveurs cibles
├── site.yml            # Playbook principal
├── group_vars/         
│   └── all.yml         # Variables globales
└── roles/
    └── webserver/      # Rôle pour serveur web
        ├── tasks/
        │   └── main.yml       # Tâches principales
        ├── handlers/
        │   └── main.yml       # Handlers (redémarrages)
        ├── templates/
        │   └── index.html.j2  # Template de page web
        └── defaults/
            └── main.yml       # Variables par défaut
```

### Explication de la structure

**📄 `ansible.cfg`** : Configure Ansible pour l'apprentissage (désactive la vérification SSH, etc.)

**📄 `inventory`** : Définit les serveurs sur lesquels travailler

**📄 `site.yml`** : Point d'entrée principal - orchestre tout le déploiement

**📁 `group_vars/`** : Variables qui s'appliquent à des groupes de serveurs

**📁 `roles/`** : Logique réutilisable organisée par composants

## 🚀 Premiers pas

### 1. Clonage et préparation

```bash
# Se placer dans le répertoire du projet
cd ansible-learning

# Vérifier la structure
ls -la
```

### 2. Premier test sur localhost

```bash
# Tester la connectivité
ansible all -m ping

# Résultat attendu :
# localhost | SUCCESS => {
#     \"changed\": false,
#     \"ping\": \"pong\"
# }
```

### 3. Exécution du playbook

```bash
# Exécution complète
ansible-playbook site.yml

# Exécution avec plus de détails
ansible-playbook site.yml -v

# Exécution pas-à-pas (demande confirmation)
ansible-playbook site.yml --step

# Test sans modification (dry-run)
ansible-playbook site.yml --check
```

### 4. Vérification du résultat

```bash
# Tester le serveur web
curl http://localhost

# Ou dans un navigateur
open http://localhost
```

## 📚 Concepts Ansible expliqués

### 🎭 Playbooks

Un **playbook** est comme une recette de cuisine qui décrit :
- Quels serveurs configurer (`hosts`)
- Quelles actions effectuer (`tasks` ou `roles`)
- Dans quel ordre (`pre_tasks`, `roles`, `post_tasks`)

```yaml
- name: \"Installer un serveur web\"
  hosts: webservers
  become: true
  roles:
    - webserver
```

### 📦 Rôles

Un **rôle** est un ensemble cohérent de tâches pour un composant spécifique :

```
roles/webserver/
├── tasks/      # Ce qu'il faut faire
├── handlers/   # Réactions aux changements
├── templates/  # Fichiers à personnaliser
└── defaults/   # Valeurs par défaut
```

### 🔧 Variables

Ansible utilise une hiérarchie de variables (de la plus haute à la plus basse priorité) :

1. **Ligne de commande** : `ansible-playbook -e \"port=8080\"`
2. **Variables de playbook** : `vars:` dans le playbook
3. **Variables de groupe** : `group_vars/webservers.yml`
4. **Variables globales** : `group_vars/all.yml`
5. **Variables par défaut** : `roles/*/defaults/main.yml`

### 🎨 Templates

Les **templates** utilisent Jinja2 pour générer des fichiers dynamiques :

```html
<h1>Serveur: {{ inventory_hostname }}</h1>
<p>IP: {{ ansible_default_ipv4.address }}</p>
```

### 🔄 Handlers

Les **handlers** s'exécutent uniquement quand notifiés et à la fin :

```yaml
# Dans tasks/main.yml
- name: \"Modifier la configuration\"
  template: src=config.j2 dest=/etc/apache2/apache2.conf
  notify: restart apache

# Dans handlers/main.yml
- name: restart apache
  service: name=apache2 state=restarted
```

### 🏷️ Tags

Les **tags** permettent l'exécution sélective :

```bash
# Exécuter seulement les tâches avec le tag \"install\"
ansible-playbook site.yml --tags \"install\"

# Ignorer les tâches avec le tag \"slow\"
ansible-playbook site.yml --skip-tags \"slow\"
```

## 🛠️ Commandes utiles

### Commandes de base

```bash
# Lister tous les serveurs
ansible all --list-hosts

# Tester la connectivité
ansible all -m ping

# Exécuter une commande sur tous les serveurs
ansible all -m command -a \"uptime\"

# Vérifier la syntaxe d'un playbook
ansible-playbook site.yml --syntax-check

# Voir quels serveurs seraient affectés
ansible-playbook site.yml --list-hosts
```

### Commandes de débogage

```bash
# Mode verbeux (plusieurs niveaux possibles)
ansible-playbook site.yml -v     # Basic
ansible-playbook site.yml -vv    # More
ansible-playbook site.yml -vvv   # Debug
ansible-playbook site.yml -vvvv  # Connection debug

# Voir toutes les variables d'un serveur
ansible localhost -m setup

# Voir des variables spécifiques
ansible localhost -m setup -a \"filter=ansible_default_ipv4\"
```

### Commandes avancées

```bash
# Exécuter seulement certaines tâches
ansible-playbook site.yml --tags \"webserver,config\"

# Cibler un serveur spécifique
ansible-playbook site.yml --limit \"localhost\"

# Commencer à partir d'une tâche spécifique
ansible-playbook site.yml --start-at-task=\"Démarrer le service web\"

# Mode différentiel (voir les changements)
ansible-playbook site.yml --diff
```

## 🔍 Dépannage

### Problèmes courants

**❌ Erreur de connexion SSH**
```bash
# Vérifier la connectivité
ansible all -m ping

# Si échec, vérifier la configuration SSH
ssh localhost
```

**❌ Permission denied (sudo)**
```bash
# Vérifier les privilèges sudo
ansible all -m command -a \"sudo whoami\" --become

# Ou modifier l'inventaire pour spécifier l'utilisateur
echo \"localhost ansible_connection=local ansible_user=votre_utilisateur\" > inventory
```

**❌ Service web ne démarre pas**
```bash
# Vérifier manuellement
sudo systemctl status apache2
sudo journalctl -u apache2

# Vérifier les ports
sudo netstat -tlnp | grep :80
```

### Debug pas-à-pas

```bash
# 1. Vérifier la syntaxe
ansible-playbook site.yml --syntax-check

# 2. Voir ce qui serait fait sans le faire
ansible-playbook site.yml --check

# 3. Exécuter avec des détails
ansible-playbook site.yml -vv

# 4. Exécuter étape par étape
ansible-playbook site.yml --step
```

### Logs et diagnostics

```bash
# Logs d'Apache
sudo tail -f /var/log/apache2/error.log
sudo tail -f /var/log/apache2/access.log

# Statut du service
sudo systemctl status apache2

# Vérifier la configuration Apache
sudo apache2ctl configtest
```

## 🎓 Exercices pratiques

### Exercice 1 : Modifier le port

1. Changez le port du serveur web de 80 à 8080
2. Indices : regardez dans `group_vars/all.yml` et `roles/webserver/defaults/main.yml`

### Exercice 2 : Personnaliser la page

1. Modifiez le template `index.html.j2` pour ajouter votre nom
2. Changez la couleur du thème

### Exercice 3 : Ajouter un serveur distant

1. Ajoutez un vrai serveur dans l'inventaire
2. Configurez l'accès SSH
3. Déployez sur ce serveur

### Exercice 4 : Créer de nouvelles variables

1. Ajoutez une variable `company_name` dans `group_vars/all.yml`
2. Utilisez cette variable dans le template

### Exercice 5 : Tags et exécution sélective

1. Ajoutez des tags à certaines tâches
2. Exécutez seulement les tâches d'installation

### Solutions des exercices

<details>
<summary>Solution Exercice 1 (cliquez pour voir)</summary>

```yaml
# Dans group_vars/all.yml
default_http_port: 8080

# Ou en ligne de commande
ansible-playbook site.yml -e \"webserver_port=8080\"
```
</details>

## 🚀 Prochaines étapes

Une fois que vous maîtrisez ce projet, voici comment progresser :

### 1. Ajouter de la complexité

```bash
# Créer des environnements multiples
mkdir -p group_vars/{development,production}

# Ajouter de nouveaux rôles
mkdir -p roles/{database,monitoring}

# Utiliser des inventaires dynamiques
# (AWS, Azure, etc.)
```

### 2. Bonnes pratiques avancées

- **Ansible Vault** : Chiffrement des mots de passe
- **Tests automatisés** : Molecule pour tester les rôles
- **CI/CD** : Intégration avec GitLab/GitHub Actions
- **Collections** : Utilisation des collections Ansible Galaxy

### 3. Ressources pour approfondir

- 📖 [Documentation officielle Ansible](https://docs.ansible.com/)
- 🏪 [Ansible Galaxy](https://galaxy.ansible.com/) - Rôles communautaires
- 🎥 [Ansible YouTube Channel](https://www.youtube.com/ansibleautomation)
- 📚 Livres recommandés :
  - \"Ansible for DevOps\" par Jeff Geerling
  - \"Ansible: Up and Running\" par Lorin Hochstein

### 4. Projets suggérés

1. **Serveur LAMP complet** (Linux + Apache + MySQL + PHP)
2. **Déploiement d'application** (avec base de données et reverse proxy)
3. **Infrastructure monitoring** (avec Prometheus/Grafana)
4. **Déploiement multi-environnement** (dev/staging/prod)

## 🤝 Contribution

Ce projet est éducatif. N'hésitez pas à :

- 🐛 Signaler des bugs
- 💡 Proposer des améliorations
- 📖 Améliorer la documentation
- 🎯 Ajouter des exercices

## 📄 License

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

---

**💡 Conseil** : N'hésitez pas à expérimenter ! Ansible est idempotent, vous pouvez relancer le playbook autant de fois que vous voulez sans risque.

**🎯 Objectif** : Comprendre les concepts, pas mémoriser les commandes. Une fois les concepts acquis, la syntaxe viendra naturellement.

Bon apprentissage avec Ansible ! 🚀