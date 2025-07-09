#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Este script lista todos os projetos em uma organização do Azure DevOps
e, para cada projeto, lista todos os seus repositórios Git.

Pré-requisitos:
1. Python 3 instalado.
2. CLI do Azure instalada (`az`).
3. Extensão `azure-devops` instalada (`az extension add --name azure-devops`).
4. Estar logado na CLI do Azure (`az login`) e na organização do DevOps.
"""

import subprocess
import json
import sys

def run_az_command(command):
    """Executa um comando da CLI do Azure e retorna a saída como JSON."""
    try:
        # Executa o comando. 'check=True' lança uma exceção se o comando falhar.
        # 'text=True' decodifica stdout/stderr como texto.
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        # Se não houver saída, retorna uma lista vazia
        if not result.stdout:
            return []
        # Converte a saída JSON em um objeto Python
        return json.loads(result.stdout)
    except FileNotFoundError:
        print("Erro: O comando 'az' não foi encontrado. A CLI do Azure está instalada e no seu PATH?", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {' '.join(command)}", file=sys.stderr)
        print(f"Mensagem de erro: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Erro: Não foi possível decodificar a saída JSON do comando: {' '.join(command)}", file=sys.stderr)
        sys.exit(1)

def main():
    """Função principal para listar projetos e repositórios."""
    print("Buscando a lista de projetos...")
    
    # Comando para listar todos os projetos
    projects_command = ["az", "devops", "project", "list"]
    projects_data = run_az_command(projects_command)
    
    # A resposta da API geralmente vem dentro de uma chave 'value'
    project_list = projects_data.get('value', [])

    if not project_list:
        print("Nenhum projeto encontrado na organização.")
        return

    print("=====================================================")

    # Itera sobre cada projeto encontrado
    for project in project_list:
        project_name = project['name']
        print(f"\nProjeto: {project_name}")
        print("-------------------------------------------------")
        
        # Comando para listar os repositórios de um projeto específico
        repos_command = ["az", "repos", "list", "--project", project_name]
        repo_list = run_az_command(repos_command)
        
        if not repo_list:
            print("  Nenhum repositório encontrado neste projeto.")
        else:
            # Itera sobre cada repositório e exibe suas informações
            for repo in repo_list:
                repo_name = repo['name']
                repo_url = repo['remoteUrl']
                print(f"  - Repositório: {repo_name}")
                print(f"    URL: {repo_url}")

if __name__ == "__main__":
    main()