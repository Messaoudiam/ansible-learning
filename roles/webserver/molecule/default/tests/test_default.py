"""
Tests de validation pour le rôle webserver avec testinfra.
Ces tests vérifient que le rôle webserver a correctement configuré le serveur.
"""

import os
import pytest
import testinfra.utils.ansible_runner


# Obtenir les hosts à tester depuis Ansible
testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


class TestWebserver:
    """Tests pour le rôle webserver."""
    
    def test_webserver_package_installed(self, host):
        """Vérifier que le package Apache est installé."""
        # Déterminer le nom du package selon l'OS
        if host.system_info.distribution.lower() in ['ubuntu', 'debian']:
            package_name = 'apache2'
        else:  # CentOS/RHEL
            package_name = 'httpd'
            
        package = host.package(package_name)
        assert package.is_installed, f"Le package {package_name} devrait être installé"
    
    def test_webserver_service_running(self, host):
        """Vérifier que le service Apache est démarré et activé."""
        # Déterminer le nom du service selon l'OS
        if host.system_info.distribution.lower() in ['ubuntu', 'debian']:
            service_name = 'apache2'
        else:  # CentOS/RHEL
            service_name = 'httpd'
            
        service = host.service(service_name)
        assert service.is_running, f"Le service {service_name} devrait être démarré"
        assert service.is_enabled, f"Le service {service_name} devrait être activé"
    
    def test_webserver_port_listening(self, host):
        """Vérifier que le serveur écoute sur le port 80."""
        assert host.socket("tcp://0.0.0.0:80").is_listening, \
            "Le serveur devrait écouter sur le port 80"
    
    def test_document_root_exists(self, host):
        """Vérifier que le répertoire DocumentRoot existe."""
        doc_root = host.file("/var/www/html")
        assert doc_root.exists, "Le répertoire DocumentRoot devrait exister"
        assert doc_root.is_directory, "DocumentRoot devrait être un répertoire"
    
    def test_index_file_exists(self, host):
        """Vérifier que le fichier index.html existe."""
        index_file = host.file("/var/www/html/index.html")
        assert index_file.exists, "Le fichier index.html devrait exister"
        assert index_file.is_file, "index.html devrait être un fichier"
        
        # Vérifier les permissions
        assert index_file.mode == 0o644, "index.html devrait avoir les permissions 644"
    
    def test_index_file_content(self, host):
        """Vérifier le contenu du fichier index.html."""
        index_file = host.file("/var/www/html/index.html")
        content = index_file.content_string
        
        # Vérifier que le contenu contient des éléments attendus
        assert "<!DOCTYPE html>" in content, "Le fichier devrait contenir une déclaration DOCTYPE"
        assert "<html" in content, "Le fichier devrait contenir une balise HTML"
        assert "Serveur Web Ansible" in content or "Apache" in content, \
            "Le fichier devrait contenir un titre approprié"
    
    def test_info_file_exists(self, host):
        """Vérifier que le fichier info.html existe."""
        info_file = host.file("/var/www/html/info.html")
        assert info_file.exists, "Le fichier info.html devrait exister"
        assert info_file.is_file, "info.html devrait être un fichier"
    
    def test_webserver_user_exists(self, host):
        """Vérifier que l'utilisateur web existe."""
        if host.system_info.distribution.lower() in ['ubuntu', 'debian']:
            user_name = 'www-data'
        else:  # CentOS/RHEL
            user_name = 'www-data'  # Créé par notre playbook
            
        user = host.user(user_name)
        assert user.exists, f"L'utilisateur {user_name} devrait exister"
    
    def test_http_response(self, host):
        """Tester la réponse HTTP du serveur."""
        # Utiliser curl pour tester la réponse HTTP
        cmd = host.run("curl -s -o /dev/null -w '%{http_code}' http://localhost/")
        assert cmd.succeeded, "La commande curl devrait réussir"
        assert cmd.stdout.strip() == "200", "Le serveur devrait retourner un code 200"
    
    def test_logs_directory_exists(self, host):
        """Vérifier que les répertoires de logs existent."""
        if host.system_info.distribution.lower() in ['ubuntu', 'debian']:
            log_dir = "/var/log/apache2"
        else:  # CentOS/RHEL
            log_dir = "/var/log/httpd"
            
        logs = host.file(log_dir)
        assert logs.exists, f"Le répertoire de logs {log_dir} devrait exister"
        assert logs.is_directory, f"{log_dir} devrait être un répertoire"


class TestWebserverSecurity:
    """Tests de sécurité pour le webserver."""
    
    def test_webserver_not_root(self, host):
        """Vérifier que le serveur ne s'exécute pas en tant que root."""
        # Déterminer le nom du service selon l'OS
        if host.system_info.distribution.lower() in ['ubuntu', 'debian']:
            service_name = 'apache2'
            expected_user = 'www-data'
        else:  # CentOS/RHEL
            service_name = 'httpd'
            expected_user = 'apache'
            
        # Vérifier que le processus ne s'exécute pas en tant que root
        processes = host.process.filter(comm=service_name)
        for process in processes:
            if process.pid != 1:  # Ignorer le processus init
                assert process.user != 'root', \
                    f"Le processus {service_name} ne devrait pas s'exécuter en tant que root"


@pytest.mark.parametrize("url_path", ["/", "/info.html"])
def test_webserver_pages_accessible(host, url_path):
    """Tester que les pages principales sont accessibles."""
    cmd = host.run(f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost{url_path}")
    assert cmd.succeeded, f"La commande curl pour {url_path} devrait réussir"
    assert cmd.stdout.strip() == "200", f"La page {url_path} devrait retourner un code 200"