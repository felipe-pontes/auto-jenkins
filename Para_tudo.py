import subprocess

# Obter a lista de IDs dos contêineres em execução
command = ['docker', 'ps', '-q']
result = subprocess.run(command, capture_output=True, text=True)

if result.returncode == 0:
    container_ids = result.stdout.strip().split('\n')
    if container_ids:
        # Parar cada contêiner individualmente
        for container_id in container_ids:
            command_stop = ['docker', 'stop', container_id]
            subprocess.run(command_stop)
        print("Todos os contêineres foram parados.")
    else:
        print("Não há contêineres em execução para parar.")
else:
    print("Erro ao obter a lista de contêineres:", result.stderr)
