# entidade.py

class Entidade:
    """
    Classe base para todas as entidades interativas dentro do jogo,
    como jogadores, inimigos, NPCs, etc. Define atributos e comportamentos
    fundamentais como vida, posição e a capacidade de receber dano.
    """
    def __init__(self, vida_inicial: int, posicao_inicial: tuple[int, int, int]):
        """
        Inicializa uma nova instância de Entidade.

        Args:
            vida_inicial (int): A quantidade inicial e máxima de pontos de vida da entidade.
                                Deve ser um inteiro positivo.
            posicao_inicial (tuple[int, int, int]): Uma tupla representando as coordenadas (x, y, z)
                                                    iniciais da entidade no mundo do jogo.
                                                    Todos os valores devem ser inteiros.

        Raises:
            ValueError: Se `vida_inicial` não for um inteiro positivo.
            ValueError: Se `posicao_inicial` não for uma tupla de três inteiros.
        """
        # Validação da vida inicial
        if not isinstance(vida_inicial, int) or vida_inicial <= 0:
            raise ValueError("Vida inicial deve ser um inteiro positivo.")

        # Validação da posição inicial
        if not (isinstance(posicao_inicial, tuple) and len(posicao_inicial) == 3 and
                all(isinstance(coord, int) for coord in posicao_inicial)):
            raise ValueError("Posição inicial deve ser uma tupla de três inteiros (x, y, z).")

        self.vida: int = vida_inicial
        self.vida_maxima: int = vida_inicial  # A vida máxima é igual à vida inicial no momento da criação
        self.posicao: tuple[int, int, int] = posicao_inicial

    def receber_dano(self, quantidade_dano: int) -> None:
        """
        Aplica dano à entidade, reduzindo seus pontos de vida.
        A vida da entidade não pode ser reduzida abaixo de zero.
        Imprime uma mensagem indicando o dano recebido e a vida restante.

        Args:
            quantidade_dano (int): A quantidade de dano a ser aplicada.
                                   Deve ser um inteiro não negativo.

        Raises:
            ValueError: Se `quantidade_dano` não for um inteiro não negativo.
        """
        # Validação da quantidade de dano
        if not isinstance(quantidade_dano, int) or quantidade_dano < 0:
            raise ValueError("Quantidade de dano deve ser um inteiro não negativo.")

        self.vida -= quantidade_dano
        if self.vida < 0:
            self.vida = 0  # Garante que a vida não se torne negativa

        # Feedback visual sobre o dano no console para fins de log/debug
        print(f"{self.__class__.__name__} recebeu {quantidade_dano} de dano. Vida restante: {self.vida}")

    def esta_vivo(self) -> bool:
        """
        Verifica se a entidade ainda possui pontos de vida.

        Returns:
            bool: True se a vida da entidade for maior que zero, False caso contrário.
        """
        return self.vida > 0

    def __str__(self) -> str:
        """
        Retorna uma representação textual concisa do estado atual da entidade.
        Útil para debugging e logs.

        Returns:
            str: Uma string formatada mostrando nome da classe, vida atual/máxima e posição.
        """
        return f"{self.__class__.__name__}(Vida: {self.vida}/{self.vida_maxima}, Posição: {self.posicao})"

if __name__ == '__main__':
    # Bloco de teste para a classe Entidade.
    # Demonstra a criação de uma entidade, aplicação de dano, verificação de status e tratamento de erros.
    print("--- Testando a Classe Entidade ---")
    try:
        # Criação de uma entidade válida
        entidade_teste = Entidade(vida_inicial=100, posicao_inicial=(0, 0, 0))
        print(f"Entidade criada: {entidade_teste}")

        # Teste de recebimento de dano
        print("\nAplicando 30 de dano...")
        entidade_teste.receber_dano(30)
        print(f"Está vivo? {entidade_teste.esta_vivo()}")
        print(f"Estado atual: {entidade_teste}")

        # Teste de dano letal
        print("\nAplicando 80 de dano (dano letal)...")
        entidade_teste.receber_dano(80) # Vida restante deve ser 0
        print(f"Está vivo? {entidade_teste.esta_vivo()}") # Deve ser False
        print(f"Estado atual: {entidade_teste}")

        # Testes de erro (descomente as seções abaixo para verificar as validações)

        # print("\n--- Testando Criações Inválidas ---")
        # try:
        #     print("Testando criação com vida inicial negativa...")
        #     entidade_errada_vida = Entidade(vida_inicial=-10, posicao_inicial=(0,0,0))
        #     print(f"Entidade com vida errada: {entidade_errada_vida}") # Não deve chegar aqui
        # except ValueError as e_vida:
        #     print(f"Erro esperado capturado (vida): {e_vida}")

        # try:
        #     print("\nTestando criação com posição inicial inválida (número incorreto de coordenadas)...")
        #     entidade_errada_pos_len = Entidade(vida_inicial=10, posicao_inicial=(0,0))
        #     print(f"Entidade com posição errada (len): {entidade_errada_pos_len}") # Não deve chegar aqui
        # except ValueError as e_pos_len:
        #     print(f"Erro esperado capturado (posição len): {e_pos_len}")

        # try:
        #     print("\nTestando criação com posição inicial inválida (tipo de coordenada incorreto)...")
        #     entidade_errada_pos_type = Entidade(vida_inicial=10, posicao_inicial=(0,'a',0))
        #     print(f"Entidade com posição errada (type): {entidade_errada_pos_type}") # Não deve chegar aqui
        # except ValueError as e_pos_type:
        #     print(f"Erro esperado capturado (posição type): {e_pos_type}")

        # print("\n--- Testando Dano Inválido ---")
        # try:
        #     print("Testando aplicação de dano negativo...")
        #     entidade_teste.receber_dano(-10) # Dano não pode ser negativo
        #     print("Dano negativo aplicado.") # Não deve chegar aqui
        # except ValueError as e_dano:
        #     print(f"Erro esperado capturado (dano): {e_dano}")

    except ValueError as e:
        # Captura de outros ValueErrors que podem não ter sido especificamente tratados acima
        print(f"Erro geral de valor durante o teste: {e}")
    except Exception as e_geral:
        # Captura de quaisquer outras exceções inesperadas
        print(f"Um erro inesperado ocorreu: {e_geral}")
    finally:
        print("\n--- Fim dos Testes da Classe Entidade ---")
