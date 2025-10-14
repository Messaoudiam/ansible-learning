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
├── ansible.cfg                    # Configuration Ansible
├── README.md                      # Ce fichier - documentation principale
├── CLAUDE.md                      # Instructions pour Claude Code
├── inventories/                   # Inventaires multi-environnements
│   ├── production                 # Serveurs de production (localhost)
│   ├── staging                    # Serveurs de staging
│   └── docker                     # Conteneurs Docker pour tests
├── playbooks/                     # Playbooks organisés
│   ├── site.yml                   # Playbook principal (point d'entrée)
│   ├── site-local.yml             # Version sans sudo pour tests locaux
│   ├── site-docker.yml            # Déploiement sur conteneurs Docker
│   ├── demo-tags.yml              # Démonstration des tags Ansible
│   ├── docker-test.yml            # Tests avec Docker
│   └── test-suite.yml             # Suite de tests complète
├── group_vars/                    # Variables par groupe
│   ├── all.yml                    # Variables globales
│   └── webservers.yml             # Variables spécifiques aux serveurs web
├── roles/                         # Rôles réutilisables
│   └── webserver/                 # Rôle de serveur web Apache
│       ├── tasks/
│       │   └── main.yml           # Tâches principales
│       ├── handlers/
│       │   └── main.yml           # Handlers (redémarrages)
│       ├── templates/
│       │   └── index.html.j2      # Template de page web Jinja2
│       ├── defaults/
│       │   └── main.yml           # Variables par défaut
│       └── molecule/              # Tests Molecule (Docker)
│           ├── default/
│           │   ├── molecule.yml   # Configuration Molecule
│           │   └── converge.yml   # Scénario de test
│           └── Dockerfile.j2      # Template pour conteneurs de test
├── tests/                         # Tests Ansible natifs
│   ├── test-webserver.yml         # Tests du rôle webserver complet
│   └── test-webserver-local.yml   # Tests locaux sans sudo
└── docs/                          # Documentation complémentaire
    ├── QUICKSTART.md              # Démarrage rapide
    ├── GUIDE-TESTS.md             # Guide des tests
    ├── LECON-2-DOCKER-MULTI-OS.md # Leçon sur Docker et multi-OS
    ├── MACOS-VS-LINUX.md          # Différences macOS/Linux
    └── RECAPITULATIF-COMPLET.md   # Récapitulatif complet du projet
```

### Explication de la structure

**📄 `ansible.cfg`** : Configure Ansible pour l'apprentissage (désactive la vérification SSH, etc.)

**📁 `inventories/`** : Différents inventaires pour production, staging et tests Docker

**📁 `playbooks/`** : Playbooks organisés par usage (principal, tests, démonstrations)
- `site.yml` : Point d'entrée principal - orchestre tout le déploiement

**📁 `group_vars/`** : Variables qui s'appliquent à des groupes de serveurs
- `all.yml` : Variables pour tous les serveurs
- `webservers.yml` : Variables spécifiques au groupe webservers

**📁 `roles/`** : Logique réutilisable organisée par composants

**📁 `tests/`** : Tests Ansible natifs (recommandés pour l'apprentissage)

**📁 `docs/`** : Documentation complémentaire et guides détaillés

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
# Exécution complète (nécessite sudo)
ansible-playbook playbooks/site.yml

# Version locale sans sudo (recommandée pour débuter)
ansible-playbook playbooks/site-local.yml

# Exécution avec plus de détails
ansible-playbook playbooks/site.yml -v

# Exécution pas-à-pas (demande confirmation)
ansible-playbook playbooks/site.yml --step

# Test sans modification (dry-run)
ansible-playbook playbooks/site.yml --check

# Démonstration des tags
ansible-playbook playbooks/demo-tags.yml
```

### 4. Exécution des tests

```bash
# Tests locaux sans sudo (recommandé pour débuter)
ansible-playbook tests/test-webserver-local.yml

# Tests complets du webserver (nécessite Apache installé)
ansible-playbook tests/test-webserver.yml

# Suite de tests complète (performance, sécurité)
ansible-playbook playbooks/test-suite.yml

# Tests Molecule avec Docker (avancé)
cd roles/webserver && molecule test
```

### 5. Vérification du résultat

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
ansible-playbook playbooks/site.yml --tags \"install\"

# Ignorer les tâches avec le tag \"slow\"
ansible-playbook playbooks/site.yml --skip-tags \"slow\"
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
ansible-playbook playbooks/site.yml --syntax-check

# Voir quels serveurs seraient affectés
ansible-playbook playbooks/site.yml --list-hosts
```

### Commandes de débogage

```bash
# Mode verbeux (plusieurs niveaux possibles)
ansible-playbook playbooks/site.yml -v     # Basic
ansible-playbook playbooks/site.yml -vv    # More
ansible-playbook playbooks/site.yml -vvv   # Debug
ansible-playbook playbooks/site.yml -vvvv  # Connection debug

# Voir toutes les variables d'un serveur
ansible localhost -m setup

# Voir des variables spécifiques
ansible localhost -m setup -a \"filter=ansible_default_ipv4\"
```

### Commandes avancées

```bash
# Exécuter seulement certaines tâches
ansible-playbook playbooks/site.yml --tags \"webserver,config\"

# Cibler un serveur spécifique
ansible-playbook playbooks/site.yml --limit \"localhost\"

# Commencer à partir d'une tâche spécifique
ansible-playbook playbooks/site.yml --start-at-task=\"Démarrer le service web\"

# Mode différentiel (voir les changements)
ansible-playbook playbooks/site.yml --diff
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
ansible-playbook playbooks/site.yml --syntax-check

# 2. Voir ce qui serait fait sans le faire
ansible-playbook playbooks/site.yml --check

# 3. Exécuter avec des détails
ansible-playbook playbooks/site.yml -vv

# 4. Exécuter étape par étape
ansible-playbook playbooks/site.yml --step
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
ansible-playbook playbooks/site.yml -e \"webserver_port=8080\"
```
</details>

## 📖 Documentation complémentaire

Ce projet contient une documentation exhaustive dans le répertoire `docs/` :

- **[QUICKSTART.md](docs/QUICKSTART.md)** : Guide de démarrage rapide pour commencer immédiatement
- **[GUIDE-TESTS.md](docs/GUIDE-TESTS.md)** : Guide complet sur les tests (natifs et Molecule)
- **[LECON-2-DOCKER-MULTI-OS.md](docs/LECON-2-DOCKER-MULTI-OS.md)** : Leçon sur Docker et tests multi-OS
- **[MACOS-VS-LINUX.md](docs/MACOS-VS-LINUX.md)** : Différences entre macOS et Linux pour Ansible
- **[RECAPITULATIF-COMPLET.md](docs/RECAPITULATIF-COMPLET.md)** : Récapitulatif complet du projet

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