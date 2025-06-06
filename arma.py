# arma.py

class Arma:
    """
    Representa uma arma no jogo que pode ser equipada e utilizada por entidades
    para causar dano.
    """
    def __init__(self, nome_arma: str, dano: int, municao_inicial: int = -1):
        """
        Inicializa uma nova instância de Arma.

        Args:
            nome_arma (str): O nome descritivo da arma (ex: "Espada Longa", "Pistola Laser").
                             Não pode ser uma string vazia.
            dano (int): A quantidade de dano base que esta arma causa por ataque.
                        Deve ser um inteiro positivo.
            municao_inicial (int, optional): A quantidade inicial de munição para a arma.
                                             Um valor de -1 indica munição infinita (padrão para
                                             armas brancas ou armas mágicas básicas).
                                             Para armas com munição finita, deve ser um inteiro
                                             não negativo. Defaults to -1.

        Raises:
            ValueError: Se `nome_arma` for vazio.
            ValueError: Se `dano` não for um inteiro positivo.
            ValueError: Se `municao_inicial` não for um inteiro.
        """
        if not isinstance(nome_arma, str) or not nome_arma.strip(): # Verifica se o nome não é vazio ou só espaços
            raise ValueError("Nome da arma não pode ser vazio.")
        if not isinstance(dano, int) or dano <= 0:
            raise ValueError("Dano da arma deve ser um inteiro positivo.")
        if not isinstance(municao_inicial, int): # Permite municao_inicial ser 0
            raise ValueError("Munição inicial deve ser um inteiro.")

        self.nome_arma: str = nome_arma.strip()
        self.dano: int = dano
        self.municao: int = municao_inicial
        # Atributo booleano para fácil verificação de munição infinita
        self.tem_municao_infinita: bool = (municao_inicial == -1)

    def atacar(self) -> int:
        """
        Realiza uma tentativa de ataque com a arma.

        Se a arma tiver munição finita e estiver sem munição, o ataque falha (0 de dano).
        Caso contrário, o ataque é bem-sucedido e retorna o dano base da arma.
        Imprime uma mensagem indicando o ataque ou a falha por falta de munição.

        Nota: A lógica de decremento de munição está presente, mas comentada.
              Descomente as linhas relevantes para ativar o gasto de munição.

        Returns:
            int: A quantidade de dano causada pelo ataque (0 se sem munição e não infinita).
        """
        # Verifica se a arma tem munição finita e se acabou
        if not self.tem_municao_infinita and self.municao == 0:
            print(f"{self.nome_arma} está sem munição!")
            return 0  # Retorna 0 de dano se não houver munição

        # Lógica de gasto de munição (descomente para ativar)
        # if not self.tem_municao_infinita:
        #     self.municao -= 1
        #     print(f"{self.nome_arma} disparou! Munição restante: {self.municao}")

        print(f"{self.nome_arma} ataca causando {self.dano} de dano.")
        return self.dano

    def __str__(self) -> str:
        """
        Retorna uma representação textual da arma, incluindo nome, dano e munição.

        Returns:
            str: Uma string formatada com os detalhes da arma.
        """
        municao_str = "Infinita" if self.tem_municao_infinita else str(self.municao)
        return f"Arma(Nome: {self.nome_arma}, Dano: {self.dano}, Munição: {municao_str})"

if __name__ == '__main__':
    # Bloco de teste para a classe Arma.
    # Demonstra a criação de diferentes tipos de armas e a simulação de ataques.
    print("--- Testando a Classe Arma ---")
    try:
        # Arma com munição infinita (branca/mágica)
        print("\nCriando uma Espada Curta (munição infinita):")
        espada = Arma(nome_arma="Espada Curta ", dano=15) # Testar com espaço no nome
        print(espada)
        espada.atacar()

        print("-" * 20)

        # Arma com munição finita
        print("\nCriando uma Pistola 9mm (munição finita):")
        pistola = Arma(nome_arma="Pistola 9mm", dano=25, municao_inicial=12)
        print(pistola)
        print("Primeiro ataque com pistola:")
        pistola.atacar()
        print("Segundo ataque com pistola (munição ainda não está sendo gasta no código atual):")
        pistola.atacar()

        # Simular gasto de munição para testar a condição de "sem munição"
        print("\nSimulando gasto total de munição da pistola...")
        pistola.municao = 0
        # pistola.tem_municao_infinita = False # Garantir que não é infinita para este teste
        print(f"Estado da pistola após zerar munição: {pistola}")
        print("Tentando atacar com pistola sem munição:")
        pistola.atacar() # Deve imprimir que está sem munição e retornar 0 dano

        # Testes de erro (descomente para verificar as validações)
        # print("\n--- Testando Criações Inválidas de Arma ---")
        # try:
        #     print("Testando nome de arma vazio...")
        #     arma_nome_vazio = Arma(nome_arma=" ", dano=10)
        # except ValueError as e_nome:
        #     print(f"Erro esperado (nome): {e_nome}")

        # try:
        #     print("\nTestando dano não positivo...")
        #     arma_dano_invalido = Arma(nome_arma="Faca Cega", dano=0)
        # except ValueError as e_dano:
        #     print(f"Erro esperado (dano): {e_dano}")

        # try:
        #     print("\nTestando tipo de munição inválido...")
        #     arma_municao_invalida = Arma(nome_arma="Besta", dano=18, municao_inicial="muita") # type: ignore
        # except ValueError as e_municao:
        #     print(f"Erro esperado (munição): {e_municao}")

    except ValueError as e:
        print(f"Erro geral de valor durante o teste da Arma: {e}")
    except Exception as e_geral:
        print(f"Um erro inesperado ocorreu nos testes da Arma: {e_geral}")
    finally:
        print("\n--- Fim dos Testes da Classe Arma ---")
