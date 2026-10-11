# Máquina de estados de recebimento

**Estágio: experimental / em teste. Demonstração parcial sanitizada, não pronta para produção.**

Módulo extraído de um fluxo de recebimento: leitura, mapeamento, plano, confirmação, envio simulado, validação e recuperação. O exemplo percorre os estados e imprime histórico em JSON.

## Estágio
Demonstração local de um módulo existente, com dados sintéticos. Não é uma cópia completa do sistema operacional nem um produto pronto para produção.

## Executar
Python 3.10 ou superior. Sem dependências externas. Dentro desta pasta:

```sh
python demo.py
python -m unittest -v
```

## Arquitetura e limites
Não recebe mercadoria nem acessa serviço externo. A máquina original admite PLAN_READY → SENDING, e force() ignora a validação de transição registrando forced=True. Portanto não é uma barreira de autorização ou mecanismo de segurança. A interface desktop e os adaptadores reais estão excluídos.

Nenhum acesso à rede, configuração operacional, histórico Git, base de dados ou artefato binário é distribuído. Exemplos e testes foram escritos para esta demonstração. Nenhuma licença de redistribuição foi presumida; o responsável deve definir a licença antes de promover reutilização de terceiros.
