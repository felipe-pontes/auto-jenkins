import subprocess
import os
import requests

# Variáveis para login com o GitHub
email = "seu email"
username = 'seu usuario git'
token_pessoal=  'seu token pessoal do git'

#Abre o docker desktop
comando_windows = 'start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"'
subprocess.run(comando_windows, shell=True)

# Shortcut para os comandos do Docker
command = ['docker', 'exec', '-t', 'jenkins-blueocean']

# Criar a rede Docker
subprocess.run(['docker', 'network', 'create', 'jenkins'])

# Baixar a imagem do Jenkins
subprocess.run(['docker', 'pull', 'jenkins/jenkins'])

# Iniciar o contêiner Docker do Jenkins com docker:dind
subprocess.run(['docker', 'run', '--name', 'jenkins-docker', '--rm', '--detach', '--privileged', '--network', 'jenkins', '--network-alias', 'docker', '--env', 'DOCKER_TLS_CERTDIR=/certs', '--volume', 'jenkins-docker-certs:/certs/client', '--volume', 'jenkins-data:/var/jenkins_home', '--publish', '2376:2376', 'docker:dind'])

# Construir a imagem personalizada do Jenkins
subprocess.run(['docker', 'build', '-t', 'myjenkins-blueocean:2.401.2-1', '.'])

# Iniciar o contêiner Jenkins-blueocean
subprocess.run(['docker', 'run', '--name', 'jenkins-blueocean', '--restart=on-failure', '--detach', '--network', 'jenkins', '--env', 'DOCKER_HOST=tcp://docker:2376', '--env', 'DOCKER_CERT_PATH=/certs/client', '--env', 'DOCKER_TLS_VERIFY=1', '--volume', 'jenkins-data:/var/jenkins_home', '--volume', 'jenkins-docker-certs:/certs/client:ro', '--publish', '8080:8080', '--publish', '50000:50000', 'myjenkins-blueocean:2.401.2-1'])

# Obter a senha inicial do Jenkins
result = subprocess.run(command + ['cat', '/var/jenkins_home/secrets/initialAdminPassword'], capture_output=True, text=True)

# Processo para a chave SSH
key_file = '/root/.ssh/id_rsa'
subprocess.run(command + ['ssh-keygen', '-t', 'rsa', '-b', '4096', '-C', email, '-f', key_file, '-P', ''])
chavessh = subprocess.run(command + ['cat', '/root/.ssh/id_rsa.pub'], capture_output=True, text=True).stdout.strip()
print("A chave SSH:", chavessh)

# Configurar a chave SSH no GitHub usando a API do GitHub
github_api_url = 'https://api.github.com/user/keys'
ssh_key = subprocess.run(command + ['cat', '/root/.ssh/id_rsa.pub'], capture_output=True, text=True).stdout.strip()
headers = {
    'Authorization': 'token {}'.format(token_pessoal),
    'Accept': 'application/vnd.github.v3+json'
}
data = {
    'title': 'Jenkins SSH Key',
    'key': ssh_key
}
response = requests.post(github_api_url, headers=headers, json=data)

# Verificar se o registro da chave SSH foi bem-sucedido
if response.status_code == 201:
    print("Chave SSH registrada com sucesso no GitHub!")
else:
    print("Erro ao registrar a chave SSH no GitHub:", response.text)

# Continuar com o restante do código
if result.returncode == 0:
    initial_admin_password = result.stdout.strip()
    print("Senha inicial do Jenkins:", initial_admin_password)
else:
    print("Erro ao obter a senha inicial do Jenkins:", result.stderr)
