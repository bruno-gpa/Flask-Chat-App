# Flask-SocketIO Chat Application

## Ferramentas utilizadas
- Flask
- Flask SocketIO
- Sqlite3
- Python
- HTML
- CSS
- JavaScript

## Funcionamento (update)
A aplicação agora suporta até 10000 salas de chat. Entrando com um nome qualquer você será colocado em uma sala aleatória, mas também pode escolher entrar em uma sala específica digitando o código de 4 dígitos. Apenas usuários dentro da mesma sala podem conversar entre si. Todas as mensagens enviadas são armazenadas em uma tabela específica para o usuário e podem ser acessadas no histórico de mensagens. A opção de deletar dados apaga todos os registros do usuário.

## Próximos objetivos
- [x] Criação de salas de chat separadas;
- [x] Separação do JavaScript em outro arquivo;
- [ ] Avisos para erros de login.

## Avisos
Não há identificação de usuário. Se o nome escolhido já estiver sendo utilizado, o servidor não saberá diferenciar os dois clientes.
