#!/usr/bin/env bash

# Defina a URL da sua organização
ORGANIZATION_URL="https://dev.azure.com/your-organization"

# Faça login no Azure DevOps
az devops login --organization "$ORGANIZATION_URL"

# Lista de projetos - Eu listei meus projetos com o comando:
# $ az devops project list --output table
projects=(
    "my project 1 ", "my project 2 "
)

# Redireciona a saída para o arquivo list-repos.yaml
{
    echo "Projeto | Nome do Repositório"
    echo "---------------------------"
    for project in "${projects[@]}"; do
        # Comando para listar repositórios de um projeto específico
        repo_names=$(az repos list --project "$project" --output table | awk '{print $2}' | tail -n +3) # Remove cabeçalho

        if [ -z "$repo_names" ]; then
            echo "$project | Nenhum repositório encontrado."
        else
            while read -r repo_name; do
                echo "$project | $repo_name" # botei para sair PROJETO | NOME_DO_REPO
            done <<< "$repo_names"
        fi
    done
} > list-repos.yaml

echo "A lista de repositórios foi salva em list-repos.yaml." #usei .yaml como extensao por opcao.
