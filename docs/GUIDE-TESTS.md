# 🧪 Guide Complet des Tests Ansible

Ce guide explique comment utiliser les différents systèmes de tests mis en place dans ce projet d'apprentissage Ansible.

## 📋 Table des Matières

- [Vue d'ensemble](#-vue-densemble)
- [Tests Ansible Natifs](#-tests-ansible-natifs)
- [Tests avec Molecule](#-tests-avec-molecule)
- [Comparaison des Approches](#-comparaison-des-approches)
- [Commandes Utiles](#-commandes-utiles)

## 🎯 Vue d'ensemble

Ce projet propose **deux approches** pour tester vos rôles Ansible :

1. **Tests Ansible Natifs** : Simple, idéal pour l'apprentissage
2. **Tests avec Molecule** : Professionnel, utilisé en entreprise

## 🏗️ Tests Ansible Natifs

### Avantages
- ✅ **Simple à comprendre** - Utilise uniquement Ansible
- ✅ **Rapide à mettre en place** - Pas de dépendances externes
- ✅ **Idéal pour l'apprentissage** - Concepts Ansible purs
- ✅ **Tests immédiats** - Fonctionne avec localhost

### Structure des fichiers
```
tests/
└── test-webserver.yml          # Tests spécifiques au rôle webserver
playbooks/
└── test-suite.yml              # Suite complète de tests
```

### Utilisation

#### Tests rapides du rôle webserver
```bash
# Exécuter les tests du rôle webserver
ansible-playbook tests/test-webserver.yml

# Tests avec plus de détails
ansible-playbook tests/test-webserver.yml -v

# Tests après déploiement
ansible-playbook site.yml && ansible-playbook tests/test-webserver.yml
```

#### Suite complète de tests
```bash
# Exécuter tous les tests (recommandé)
ansible-playbook playbooks/test-suite.yml

# Tests avec verbosité maximale
ansible-playbook playbooks/test-suite.yml -vvv

# Tests sur un serveur spécifique
ansible-playbook playbooks/test-suite.yml --limit "localhost"
```

### Types de tests inclus

#### 🔍 **Tests Fonctionnels**
- Installation des packages
- État des services (démarré/activé)
- Ports en écoute
- Présence des fichiers
- Contenu HTML valide

#### ⚡ **Tests de Performance**
- Temps de réponse HTTP
- Métriques de connexion
- Vitesse de transfert

#### 🔒 **Tests de Sécurité**
- Processus non-root
- Permissions des fichiers
- Accès aux répertoires sensibles

#### 📈 **Tests de Monitoring**
- Présence des logs
- Vérification des erreurs récentes

#### 🔄 **Tests de Récupération**
- Redémarrage du service
- Récupération après panne

### Exemple de sortie
```
✅ Test 1: Package Apache installé
✅ Test 2: Service Apache démarré/activé
✅ Test 3: Port 80 en écoute
✅ Test 4: Fichiers web présents
✅ Test 5: Contenu HTML valide
✅ Test 6: Réponse HTTP correcte
✅ Test 7: Page info.html accessible
✅ Test 8: Permissions correctes

🎉 TOUS LES TESTS ONT RÉUSSI !
```

## 🐳 Tests avec Molecule

### Avantages
- ✅ **Standard industriel** - Utilisé en entreprise
- ✅ **Tests multi-OS** - Ubuntu, CentOS automatiquement
- ✅ **Isolation complète** - Conteneurs Docker
- ✅ **Tests avancés** - avec testinfra/pytest
- ✅ **CI/CD Ready** - Intégration facile

### Structure des fichiers
```
roles/webserver/molecule/
├── default/
│   ├── molecule.yml            # Configuration Molecule
│   ├── converge.yml           # Playbook de test
│   └── tests/
│       └── test_default.py    # Tests testinfra
└── Dockerfile.j2              # Template Docker
```

### Prérequis
```bash
# Installation sur macOS
brew install molecule

# Démarrer Docker Desktop
# Ou installer Docker avec: brew install docker

# Vérifier l'installation
molecule --version
docker --version
```

### Utilisation

#### Tests complets avec Molecule
```bash
# Aller dans le répertoire du rôle
cd roles/webserver

# Exécuter tous les tests
molecule test

# Tests étape par étape
molecule create          # Créer les conteneurs
molecule converge        # Appliquer le rôle
molecule verify          # Exécuter les tests
molecule destroy         # Nettoyer
```

#### Tests de développement
```bash
# Tests rapides (sans destruction)
molecule converge
molecule verify

# Debug - Se connecter au conteneur
molecule login --host ubuntu-instance
molecule login --host centos-instance
```

### Configuration avancée

#### molecule.yml - Configuration principale
- **Plateformes** : Ubuntu 22.04 et CentOS Stream 9
- **Driver** : Docker pour l'isolation
- **Provisioner** : Ansible avec variables par OS
- **Verifier** : testinfra pour tests Python

#### Tests testinfra (test_default.py)
```python
def test_webserver_package_installed(host):
    """Vérifier que le package Apache est installé."""
    # Tests automatiques selon l'OS

def test_webserver_service_running(host):
    """Vérifier que le service Apache fonctionne."""
    # Validation du service

def test_http_response(host):
    """Tester la réponse HTTP."""
    # Tests de connectivité
```

## ⚖️ Comparaison des Approches

| Critère | Tests Natifs | Molecule |
|---------|--------------|----------|
| **Simplicité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Rapidité setup** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Multi-OS** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Isolation** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Tests avancés** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Standard industrie** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Apprentissage** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🛠️ Commandes Utiles

### Tests Ansible Natifs
```bash
# Test après chaque modification
ansible-playbook site.yml && ansible-playbook tests/test-webserver.yml

# Debug en cas d'échec
ansible-playbook tests/test-webserver.yml -vvv

# Tester seulement certains aspects
ansible-playbook tests/test-webserver.yml --tags "validation"
```

### Tests Molecule
```bash
# Cycle complet de test
molecule test

# Tests de développement
molecule converge && molecule verify

# Nettoyer après les tests
molecule cleanup
molecule destroy

# Lister les instances
molecule list
```

### Debugging
```bash
# Tests manuels après déploiement
curl http://localhost/
curl http://localhost/info.html

# Vérifier les services
sudo systemctl status apache2  # Ubuntu
sudo systemctl status httpd    # CentOS

# Logs en temps réel
sudo tail -f /var/log/apache2/error.log
sudo journalctl -u apache2 -f
```

## 📚 Exercices Pratiques

### Exercice 1 : Modifier et tester
1. Modifiez le template `index.html.j2`
2. Redéployez avec `ansible-playbook site.yml`
3. Testez avec `ansible-playbook tests/test-webserver.yml`

### Exercice 2 : Ajouter un test
1. Ajoutez un nouveau test dans `test-webserver.yml`
2. Exemple : vérifier la présence d'un fichier CSS
3. Testez votre nouveau test

### Exercice 3 : Molecule multi-OS
1. Démarrez Docker Desktop
2. Lancez `molecule test` pour tester sur Ubuntu ET CentOS
3. Observez les différences entre les OS

### Exercice 4 : Test de régression
1. Cassez volontairement quelque chose (ex: arrêter Apache)
2. Lancez les tests pour voir les erreurs
3. Réparez et vérifiez que tout redevient vert

## 🚀 Bonnes Pratiques

### Pour l'apprentissage
- ✅ Commencez par les **tests natifs**
- ✅ Testez après **chaque modification**
- ✅ Lisez les **messages d'erreur** attentivement
- ✅ Utilisez **-v** pour plus de détails

### Pour la production
- ✅ Utilisez **Molecule** pour la validation
- ✅ Testez sur **plusieurs OS**
- ✅ Intégrez les tests dans **CI/CD**
- ✅ Documentez vos **tests métier**

### Tests défensifs
- ✅ Testez les **cas d'erreur**
- ✅ Vérifiez la **sécurité basique**
- ✅ Testez la **récupération après panne**
- ✅ Validez les **performances minimales**

## 🎯 Résumé

1. **Tests Natifs** = Parfait pour apprendre et débuter
2. **Molecule** = Standard professionnel pour la production
3. **Les deux approches se complètent** selon le contexte
4. **Testez souvent** pour détecter les problèmes rapidement

---

💡 **Conseil** : Commencez par maîtriser les tests natifs, puis progressez vers Molecule quand vous serez à l'aise avec Ansible.

🎯 **Objectif** : Développer une culture du test dans vos projets Ansible !