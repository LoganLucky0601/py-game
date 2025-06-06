# zumbi.py

from entidade import Entidade
# A importação de 'jogador' é necessária para a anotação de tipo (type hint)
# no método 'atacar_jogador'. Usar 'import jogador' em vez de 'from jogador import Jogador'
# ajuda a evitar potenciais problemas de importação circular se o módulo 'jogador'
# também precisar importar algo de 'zumbi' no futuro (embora não seja o caso atualmente).
# A anotação de tipo 'jogador.Jogador' é uma forward reference e é resolvida em tempo de execução.
import jogador

class Zumbi(Entidade):
    """
    Representa um inimigo do tipo Zumbi no jogo.
    Herda da classe base `Entidade` e adiciona comportamentos específicos
    de zumbis, como tipo e a capacidade de atacar jogadores.
    """
    def __init__(self, vida_inicial: int, posicao_inicial: tuple[int, int, int], tipo_zumbi: str = "Comum"):
        """
        Inicializa uma nova instância de Zumbi.

        Args:
            vida_inicial (int): A quantidade inicial de pontos de vida do zumbi.
                                Herda as validações de `Entidade`.
            posicao_inicial (tuple[int, int, int]): A posição (x, y, z) inicial do zumbi.
                                                    Herda as validações de `Entidade`.
            tipo_zumbi (str, optional): Uma string que define a variante do zumbi
                                        (ex: "Comum", "Rápido", "Tanque").
                                        Afeta atributos como o dano de ataque.
                                        Defaults to "Comum".

        Raises:
            ValueError: Se `tipo_zumbi` for uma string vazia.
                        Outras ValueErrors podem ser levantadas pela classe `Entidade`.
        """
        super().__init__(vida_inicial, posicao_inicial) # Chama o construtor da classe base

        if not isinstance(tipo_zumbi, str) or not tipo_zumbi.strip():
            raise ValueError("Tipo do zumbi não pode ser vazio.")

        self.tipo_zumbi: str = tipo_zumbi.strip()
        self.dano_ataque: int = 10  # Dano base padrão para um zumbi "Comum"

        # Ajustar atributos com base no tipo de zumbi.
        # Esta é uma lógica simples de exemplo; poderia ser mais complexa.
        if self.tipo_zumbi == "Rápido":
            self.dano_ataque = 8  # Zumbis rápidos podem ser mais fracos, mas talvez mais ágeis (não implementado)
        elif self.tipo_zumbi == "Tanque":
            self.dano_ataque = 15 # Zumbis tanque causam mais dano e geralmente têm mais vida (passada no construtor)

    def perambular(self) -> None:
        """
        Simula o comportamento de perambulação (movimento) do zumbi no ambiente.
        Para fins de exemplo, altera ligeiramente a posição X do zumbi.
        Em um jogo real, isso envolveria uma lógica de IA mais sofisticada
        (ex: pathfinding, detecção de jogador).
        """
        # Movimento simples e determinístico para teste baseado no hash da posição atual.
        # Isso garante que o movimento seja o mesmo se a posição for a mesma,
        # mas introduz alguma variação.
        # Alterna entre adicionar 1 ou -1 à coordenada x.
        offset = -1 if hash(self.posicao) % 2 == 0 else 1
        nova_pos_x = self.posicao[0] + offset
        self.posicao = (nova_pos_x, self.posicao[1], self.posicao[2])
        print(f"Zumbi {self.tipo_zumbi} ({self.object_id()}) perambula para {self.posicao}.")

    def atacar_jogador(self, alvo_jogador: 'jogador.Jogador') -> None:
        """
        Permite ao zumbi atacar uma instância de Jogador.

        O ataque só ocorre se:
        - O zumbi estiver vivo.
        - O jogador alvo estiver vivo.

        Se o ataque for bem-sucedido, o dano do zumbi é aplicado ao jogador.
        Mensagens são impressas no console para indicar o resultado da tentativa de ataque.

        Args:
            alvo_jogador (jogador.Jogador): A instância do jogador a ser atacada.
                                            A anotação de tipo é uma string para evitar
                                            importação circular no nível do módulo se Jogador
                                            também importasse Zumbi.

        Raises:
            TypeError: Se `alvo_jogador` não for uma instância de `jogador.Jogador`.
        """
        # Validação do tipo do alvo usando o módulo jogador importado.
        if not isinstance(alvo_jogador, jogador.Jogador):
            raise TypeError("Zumbi só pode atacar um objeto do tipo Jogador.")

        # Verifica se o zumbi pode atacar
        if not self.esta_vivo():
            print(f"Zumbi ({self.tipo_zumbi}, ID: {self.object_id()}) não pode atacar, pois está morto.")
            return

        # Verifica se o jogador alvo pode ser atacado
        if not alvo_jogador.esta_vivo():
            print(f"Zumbi ({self.tipo_zumbi}, ID: {self.object_id()}) não pode atacar {alvo_jogador.nome_jogador}, pois ele já está morto.")
            return

        # Se todas as condições forem atendidas, o zumbi ataca.
        print(f"Zumbi ({self.tipo_zumbi}, ID: {self.object_id()}) ataca {alvo_jogador.nome_jogador} causando {self.dano_ataque} de dano!")
        alvo_jogador.receber_dano(self.dano_ataque)

    def __str__(self) -> str:
        """
        Retorna uma representação textual do zumbi, incluindo tipo, vida, posição e dano de ataque.

        Returns:
            str: Uma string formatada com os detalhes do zumbi.
        """
        return (f"Zumbi(Tipo: {self.tipo_zumbi}, Vida: {self.vida}/{self.vida_maxima}, "
                f"Posição: {self.posicao}, Dano: {self.dano_ataque}, ID: {self.object_id()})")

    def object_id(self) -> str:
        """Retorna os últimos 4 dígitos do id do objeto para fácil identificação."""
        return str(id(self))[-4:]


if __name__ == '__main__':
    # Bloco de teste para a classe Zumbi e suas interações.
    # É importante que entidade.py e jogador.py estejam no mesmo diretório ou
    # acessíveis via PYTHONPATH para que as importações funcionem.
    print("--- Testando a Classe Zumbi ---")

    # Importação local de Jogador para o teste, minimizando o escopo da importação direta.
    from jogador import Jogador

    try:
        # 1. Criar diferentes tipos de zumbis
        print("\n1. Criando zumbis de teste...")
        zumbi_comum = Zumbi(vida_inicial=50, posicao_inicial=(10, 10, 0), tipo_zumbi=" Comum ") # Teste com espaços
        print(f"   Zumbi criado: {zumbi_comum}") # Deve mostrar tipo "Comum"
        zumbi_comum.perambular() # Testar movimento

        zumbi_tanque = Zumbi(vida_inicial=100, posicao_inicial=(12, 10, 0), tipo_zumbi="Tanque")
        print(f"   Zumbi criado: {zumbi_tanque}")

        zumbi_rapido = Zumbi(vida_inicial=30, posicao_inicial=(11, 11, 0), tipo_zumbi="Rápido")
        print(f"   Zumbi criado: {zumbi_rapido}")


        # 2. Criar um jogador para ser atacado
        print("\n2. Criando jogador 'Herói Teste'...")
        heroi_teste = Jogador(nome_jogador="Herói Teste", vida_inicial=100, posicao_inicial=(0,0,0))
        print(f"   Jogador criado: {heroi_teste}")

        # 3. Zumbis atacam o jogador
        print("\n3. Zumbis atacam o 'Herói Teste'...")
        if zumbi_comum.esta_vivo():
            print(f"   {zumbi_comum.tipo_zumbi} (ID: {zumbi_comum.object_id()}) vai atacar...")
            zumbi_comum.atacar_jogador(heroi_teste)
        print(f"   Estado do jogador após ataque do Comum: {heroi_teste}") # Esperado: 100 - 10 = 90 HP

        if zumbi_tanque.esta_vivo():
            print(f"   {zumbi_tanque.tipo_zumbi} (ID: {zumbi_tanque.object_id()}) vai atacar...")
            zumbi_tanque.atacar_jogador(heroi_teste)
        print(f"   Estado do jogador após ataque do Tanque: {heroi_teste}") # Esperado: 90 - 15 = 75 HP

        if zumbi_rapido.esta_vivo():
            print(f"   {zumbi_rapido.tipo_zumbi} (ID: {zumbi_rapido.object_id()}) vai atacar...")
            zumbi_rapido.atacar_jogador(heroi_teste)
        print(f"   Estado do jogador após ataque do Rápido: {heroi_teste}") # Esperado: 75 - 8 = 67 HP
        print(f"   Jogador está vivo? {heroi_teste.esta_vivo()}") # Esperado: True

        # 4. Zumbi morto tenta atacar
        print("\n4. Zumbi Comum recebe dano letal e tenta atacar...")
        zumbi_comum.receber_dano(200) # Mata o zumbi comum
        print(f"   Zumbi Comum está vivo? {zumbi_comum.esta_vivo()}") # Esperado: False
        zumbi_comum.atacar_jogador(heroi_teste) # Deve imprimir que não pode atacar

        # 5. Zumbi ataca jogador morto
        print("\n5. Zumbi Tanque tenta atacar 'Herói Teste' após ele ser derrotado...")
        heroi_teste.receber_dano(1000) # Mata o herói
        print(f"   'Herói Teste' está vivo? {heroi_teste.esta_vivo()}") # Esperado: False
        if zumbi_tanque.esta_vivo():
            zumbi_tanque.atacar_jogador(heroi_teste) # Deve imprimir que o jogador já está morto

        # Testes de erro (descomente para verificar)
        # print("\n--- Testando Criações Inválidas de Zumbi ---")
        # try:
        #     print("Testando tipo de zumbi vazio...")
        #     zumbi_tipo_vazio = Zumbi(vida_inicial=10, posicao_inicial=(0,0,0), tipo_zumbi="  ")
        # except ValueError as e_tipo:
        #     print(f"Erro esperado (tipo zumbi): {e_tipo}")

    except (ValueError, TypeError) as e:
        print(f"ERRO DURANTE O TESTE DO ZUMBI: {e}")
    except ImportError:
        # Este erro pode ocorrer se jogador.py ou entidade.py não forem encontrados.
        print("ERRO DE IMPORTAÇÃO: Certifique-se de que entidade.py e jogador.py estão no mesmo diretório ou no PYTHONPATH.")
    except Exception as e_geral:
        print(f"UM ERRO INESPERADO OCORREU NOS TESTES DO ZUMBI: {e_geral}")
    finally:
        print("\n--- Fim dos Testes da Classe Zumbi ---")
