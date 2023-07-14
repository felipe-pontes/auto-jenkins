import subprocess

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
result = subprocess.run(['docker', 'exec', '-t', 'jenkins-blueocean', 'cat', '/var/jenkins_home/secrets/initialAdminPassword'], capture_output=True, text=True)

if result.returncode == 0:
    initial_admin_password = result.stdout.strip()
    print("Senha inicial do Jenkins:", initial_admin_password)
else:
    print("Erro ao obter a senha inicial do Jenkins:", result.stderr)
