*Automação de Configurações no Windows 11*

Este projeto é um script em Python que automatiza funções de configuração no Windows 11, ajudando a agilizar parte de um processo de trabalho.
O executável é gerado com Pyllancer, permitindo rodar diretamente no sistema sem precisar do Python instalado.

*Funcionalidades automatizadas*

- Instala alguns softwares padrão

- Desabilita o UAC

- Habilita a Conexão com Área de Trabalho Remota

- Altera configurações de desempenho do computador

- Configura o Windows Update para atualização automática

- Habilita o Cliente Telnet e suporte a SMB

- Altera regras de Firewall

- Ajusta as configurações de energia

- Altera o nome do computador

- Cria um ponto de restauração do sistema

*Requisitos*

- Windows 11

- Python 3.11.9+ (apenas se quiser rodar o código-fonte ao invés do executável)

*Observações*

- O script deve ser executado com permissões de administrador.

- A lógica de instalação dos softwares padrão busca pelos softwares presentes no dicionário 'softwares_dict' em uma pasta chamada 'instaladores'. Por padrão, o script vai apenas informar que não encontrou o caminho especificado do executável.  