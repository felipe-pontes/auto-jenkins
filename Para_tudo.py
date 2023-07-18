import subprocess

decisao = input("Digite 1 para parar os containers e 2 para destruir os containers: ")

def comandos(decisao):
    if decisao == '1':
        return 'stop'
    elif decisao == '2':
        return 'rm'
    else:
        print("Decisão inválida.")
        return None

# Obter a lista de IDs dos contêineres em execução
command = ['docker', 'ps', '-q']
result = subprocess.run(command, capture_output=True, text=True)

if result.returncode == 0:
    container_ids = result.stdout.strip().split('\n')
    if container_ids:
        comando = comandos(decisao)
        if comando:
            for container_id in container_ids:
                subprocess.run(['docker', 'stop', container_id])
                command_remove = ['docker', comando, container_id]
                subprocess.run(command_remove)
            print("Todos os contêineres seguiram sua decisao")
    else:
        print("Não há contêineres em execução")
else:
    print("Erro ao obter a lista de contêineres:", result.stderr)
