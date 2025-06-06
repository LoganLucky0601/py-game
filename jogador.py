# jogador.py

from entidade import Entidade
from arma import Arma

class Jogador(Entidade):
    """
    Representa o jogador controlado pelo usuário no jogo.
    Herda da classe base `Entidade`, adicionando atributos específicos do jogador
    como nome e a capacidade de equipar e usar armas.
    """
    def __init__(self, nome_jogador: str, vida_inicial: int, posicao_inicial: tuple[int, int, int]):
        """
        Inicializa uma nova instância de Jogador.

        Args:
            nome_jogador (str): O nome do jogador. Não pode ser uma string vazia.
            vida_inicial (int): A quantidade inicial de pontos de vida do jogador.
                                Herda as validações de `Entidade`.
            posicao_inicial (tuple[int, int, int]): A posição (x, y, z) inicial do jogador.
                                                    Herda as validações de `Entidade`.

        Raises:
            ValueError: Se `nome_jogador` for vazio.
                        Outras ValueErrors podem ser levantadas pela classe `Entidade`.
        """
        super().__init__(vida_inicial, posicao_inicial) # Chama o construtor da classe base Entidade

        if not isinstance(nome_jogador, str) or not nome_jogador.strip():
            raise ValueError("Nome do jogador não pode ser vazio.")

        self.nome_jogador: str = nome_jogador.strip()
        self.arma_equipada: Arma | None = None  # O jogador começa desarmado. Tipo é Arma ou None.

    def equipar_arma(self, arma_para_equipar: Arma) -> None:
        """
        Equipa o jogador com a arma fornecida.
        Se o jogador já tiver uma arma, ela é substituída pela nova.

        Args:
            arma_para_equipar (Arma): A instância da classe `Arma` a ser equipada.

        Raises:
            TypeError: Se `arma_para_equipar` não for uma instância de `Arma`.
        """
        if not isinstance(arma_para_equipar, Arma):
            raise TypeError("Só é possível equipar um objeto do tipo Arma.")

        self.arma_equipada = arma_para_equipar
        print(f"{self.nome_jogador} equipou {self.arma_equipada.nome_arma}.")

    def atacar_alvo(self, alvo: Entidade) -> None:
        """
        Permite ao jogador atacar uma entidade alvo usando sua arma equipada.

        O ataque só ocorre se:
        - O jogador estiver vivo.
        - O jogador tiver uma arma equipada.
        - O alvo estiver vivo.

        Se o ataque for bem-sucedido (arma causou dano), o dano é aplicado ao alvo.
        Mensagens são impressas no console para indicar o resultado da tentativa de ataque.

        Args:
            alvo (Entidade): A entidade que o jogador tentará atacar.

        Raises:
            TypeError: Se o `alvo` não for uma instância de `Entidade`.
        """
        if not isinstance(alvo, Entidade):
            raise TypeError("O alvo do ataque deve ser uma Entidade.")

        # Verifica se o jogador pode atacar
        if not self.esta_vivo():
            print(f"{self.nome_jogador} não pode atacar, pois está morto.")
            return

        if not self.arma_equipada:
            print(f"{self.nome_jogador} está desarmado e não pode atacar!")
            return

        # Verifica se o alvo pode ser atacado
        if not alvo.esta_vivo():
            # Usamos alvo.__class__.__name__ para obter o nome da classe específica (ex: Zumbi)
            print(f"O alvo {alvo.__class__.__name__} já está morto. {self.nome_jogador} não pode atacar.")
            return

        # Se todas as condições forem atendidas, o jogador tenta o ataque.
        print(f"{self.nome_jogador} tenta atacar {alvo.__class__.__name__} com {self.arma_equipada.nome_arma}.")
        dano_causado = self.arma_equipada.atacar() # O método atacar da Arma pode retornar 0 (ex: sem munição)

        if dano_causado > 0:
            alvo.receber_dano(dano_causado)
        # Se dano_causado for 0, a arma já imprimiu a mensagem (ex: "sem munição")

    def __str__(self) -> str:
        """
        Retorna uma representação textual do jogador, incluindo nome, vida, posição e arma equipada.

        Returns:
            str: Uma string formatada com os detalhes do jogador.
        """
        status_arma = self.arma_equipada.nome_arma if self.arma_equipada else "Desarmado"
        return (f"Jogador(Nome: {self.nome_jogador}, Vida: {self.vida}/{self.vida_maxima}, "
                f"Posição: {self.posicao}, Arma: {status_arma})")

if __name__ == '__main__':
    # Bloco de teste para a classe Jogador e suas interações.
    print("--- Testando a Classe Jogador ---")
    try:
        # 1. Criar armas para serem usadas nos testes
        print("\n1. Criando armas de teste...")
        machado = Arma(nome_arma="Machado de Guerra", dano=20)
        shotgun = Arma(nome_arma="Escopeta de Combate", dano=50, municao_inicial=8)
        print(f"   Arma criada: {machado}")
        print(f"   Arma criada: {shotgun}")

        # 2. Criar um jogador
        print("\n2. Criando jogador 'Herói'...")
        player1 = Jogador(nome_jogador=" Herói ", vida_inicial=150, posicao_inicial=(1, 2, 3)) # Nome com espaços
        print(f"   Jogador criado: {player1}") # Deve mostrar nome "Herói" (sem espaços extras)

        # 3. Equipar uma arma
        print("\n3. 'Herói' equipa o Machado...")
        player1.equipar_arma(machado)
        print(f"   Estado do jogador: {player1}")

        # 4. Criar um alvo para teste
        print("\n4. Criando entidade 'Alvo Teste'...")
        # Usamos a classe base Entidade para um alvo genérico neste teste.
        # Em um jogo completo, este poderia ser uma instância de Zumbi ou outra subclasse de Entidade.
        alvo_teste = Entidade(vida_inicial=80, posicao_inicial=(5, 5, 5))
        print(f"   Alvo criado: {alvo_teste}")

        # 5. Jogador ataca o alvo
        print("\n5. 'Herói' ataca 'Alvo Teste' com Machado...")
        player1.atacar_alvo(alvo_teste)
        print(f"   Estado do alvo após 1º ataque: {alvo_teste}") # Esperado: 80 - 20 = 60 de vida

        # 6. Jogador muda de arma e ataca novamente
        print("\n6. 'Herói' equipa a Escopeta e ataca 'Alvo Teste' novamente...")
        player1.equipar_arma(shotgun)
        player1.atacar_alvo(alvo_teste) # Alvo tem 60 de vida, Escopeta tira 50.
        print(f"   Estado do alvo após 2º ataque: {alvo_teste}") # Esperado: 60 - 50 = 10 de vida
        print(f"   Alvo está vivo? {alvo_teste.esta_vivo()}") # Esperado: True

        # 7. Ataque final para derrotar o alvo
        print("\n7. 'Herói' ataca 'Alvo Teste' uma última vez com a Escopeta...")
        player1.atacar_alvo(alvo_teste) # Alvo tem 10 de vida.
        print(f"   Estado do alvo após 3º ataque: {alvo_teste}") # Esperado: 10 - 50 = 0 de vida (não negativo)
        print(f"   Alvo está vivo? {alvo_teste.esta_vivo()}") # Esperado: False

        # 8. Tentar atacar alvo já morto
        print("\n8. 'Herói' tenta atacar 'Alvo Teste' (já morto)...")
        player1.atacar_alvo(alvo_teste) # Deve imprimir que o alvo já está morto.

        # 9. Testar jogador desarmado tentando atacar
        print("\n9. Criando jogador 'Desavisado' (desarmado)...")
        player_desarmado = Jogador("Desavisado", 100, (0,0,0))
        print(f"   Jogador criado: {player_desarmado}")
        print("   'Desavisado' tenta atacar 'Alvo Teste'...")
        player_desarmado.atacar_alvo(alvo_teste) # Deve imprimir que está desarmado.

        # 10. Testar jogador morto tentando atacar
        print("\n10. 'Herói' recebe dano letal...")
        player1.receber_dano(200) # Vida do Herói vai a 0
        print(f"    Estado do 'Herói': {player1}")
        print("    'Herói' (morto) tenta atacar 'Alvo Teste'...")
        player1.atacar_alvo(alvo_teste) # Deve imprimir que o Herói não pode atacar.

    except (ValueError, TypeError) as e:
        print(f"ERRO DURANTE O TESTE DO JOGADOR: {e}")
    except Exception as e_geral:
        print(f"UM ERRO INESPERADO OCORREU NOS TESTES DO JOGADOR: {e_geral}")
    finally:
        print("\n--- Fim dos Testes da Classe Jogador ---")
