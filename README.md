# gs25-2-Cybersecurity

Demo de uma API em Flask que ilustra vulnerabilidades comuns e suas correções. O objetivo do projeto é servir como material didático para entender vulnerabilidades reais (e.g., injeção SQL, controle de acesso, desserialização insegura e injeção de comandos) e comparar implementações vulneráveis com implementações seguras.

## Como executar
Requisitos:
- Python 3.8+
- pip

Instalar dependências:
```bash
pip install flask
```

Executar:
```bash
python main.py
```

## Endpoints e explicação
- /sql-injection-vulnerable
  - Demonstra injeção SQL construindo consultas via formatação de string.
  - Risco: execução de consultas arbitrárias no banco (exfiltração, alteração de dados).
- /sql-injection-safe
  - Usa queries parametrizadas (placeholders) para evitar injeção.
  - Recomendação: sempre usar queries parametrizadas / ORM.
---
- /acesso-vulneravel
  - Controle de acesso baseado em parâmetro de query ("role"), fácil de manipular.
  - Risco: usuário consegue escalar privilégios apenas alterando parâmetros.
- /acesso-seguro
  - Verifica token no cabeçalho (exemplo simples). Atenção: implementação de exemplo retorna "ok" — em produção valide tokens corretamente e aplique autorização apropriada.
---
- /deserializacao-vulneravel (POST)
  - Recebe payload pickled e desserializa com pickle.loads.
  - Risco: execução remota de código via objetos maliciosos.
- /deserializacao-segura (POST)
  - Usa json.loads para desserializar dados de forma segura.
  - Recomendação: nunca desserialize formatos binários inseguros de origem não confiável.
---
- /comando-vulneravel
  - Executa comandos passados pelo usuário com subprocess.check_output e shell=True.
  - Risco: execução de comandos arbitrários no sistema.
- /comando-seguro
  - Lista de comandos permitidos e execução restrita (exemplo). Em produção, evite executar comandos do sistema ou use mecanismos de autorização e validação rigorosa.


## Membro
- Bruno Caputo - RM558303
