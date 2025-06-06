# main.py
# Arquivo principal para orquestrar a simulação do mini jogo de combate.

# Importações das classes definidas nos outros módulos do projeto.
from jogador import Jogador
from zumbi import Zumbi
from arma import Arma
from entidade import Entidade # Importada para type hinting na lista de participantes.

def exibir_status_geral(participantes: list[Entidade]) -> None:
    """
    Imprime o status atual de todos os participantes da simulação.
    Um participante é qualquer objeto que herda da classe Entidade.

    Args:
        participantes (list[Entidade]): Uma lista contendo instâncias de Entidade (ou suas subclasses).
    """
    print("\n" + "="*40) # Linha separadora para melhor visualização
    print("STATUS ATUAL DE TODOS OS PARTICIPANTES:")
    if not participantes:
        print("Nenhum participante na simulação.")
    else:
        for p in participantes:
            # O método __str__ de cada classe (Jogador, Zumbi) será chamado aqui.
            print(p)
    print("="*40 + "\n")

def main() -> None:
    """
    Função principal que executa a simulação do jogo de combate.
    Cria armas, um jogador, vários zumbis e simula uma série de interações
    de combate entre eles, imprimindo o resultado de cada ação.
    """
    print("🚀 Iniciando a simulação do mini jogo de combate! 🚀")

    # --- ETAPA 1: CRIAÇÃO DAS ARMAS ---
    # Armas são objetos que podem ser equipados por jogadores para causar dano.
    print("\n--- ⚔️  Etapa 1: Criando Armas ---")
    espada_longa = Arma(nome_arma="Espada Longa", dano=18) # Arma branca, munição infinita por padrão
    arco_curto = Arma(nome_arma="Arco Curto", dano=12, municao_inicial=20) # Arma com munição finita
    cajado_magico = Arma(nome_arma="Cajado Mágico", dano=22, municao_inicial=-1) # Magia, munição infinita
    print(f"   Arma criada: {espada_longa}")
    print(f"   Arma criada: {arco_curto}")
    print(f"   Arma criada: {cajado_magico}")

    # --- ETAPA 2: CRIAÇÃO DO JOGADOR ---
    # O jogador é a entidade controlada pelo usuário (nesta simulação, suas ações são pré-definidas).
    print("\n--- 🦸‍♀️ Etapa 2: Criando Jogador ---")
    heroina = Jogador(nome_jogador="Lyra", vida_inicial=120, posicao_inicial=(0, 0, 1))
    print(f"   Jogador criado: {heroina}")

    # --- ETAPA 3: CRIAÇÃO DOS ZUMBIS ---
    # Zumbis são os inimigos na simulação. Eles têm diferentes tipos e atributos.
    print("\n--- 🧟 Etapa 3: Criando Zumbis ---")
    zumbi_comum1 = Zumbi(vida_inicial=40, posicao_inicial=(10, 5, 0), tipo_zumbi="Comum")
    zumbi_corredor = Zumbi(vida_inicial=30, posicao_inicial=(12, 8, 0), tipo_zumbi="Rápido") # Menos vida, dano específico
    zumbi_bruto = Zumbi(vida_inicial=70, posicao_inicial=(15, 3, 0), tipo_zumbi="Tanque")  # Mais vida, mais dano
    print(f"   Zumbi criado: {zumbi_comum1}")
    print(f"   Zumbi criado: {zumbi_corredor}")
    print(f"   Zumbi criado: {zumbi_bruto}")

    # Lista de todos os participantes para fácil visualização do status geral.
    participantes: list[Entidade] = [heroina, zumbi_comum1, zumbi_corredor, zumbi_bruto]
    exibir_status_geral(participantes)

    # --- ETAPA 4: SIMULAÇÃO DAS INTERAÇÕES DE COMBATE ---
    print("\n--- 🔥 Etapa 4: Iniciando Sequência de Combate ---")

    # Cenário 1: Lyra vs. Zumbi Comum
    print("\n--- Cenário 1: Lyra enfrenta Zumbi Comum ---")
    heroina.equipar_arma(espada_longa) # Lyra equipa a Espada Longa
    exibir_status_geral(participantes)
    if zumbi_comum1.esta_vivo() and heroina.esta_vivo():
        print(f"Lyra (Vida: {heroina.vida}) ataca Zumbi Comum (Vida: {zumbi_comum1.vida})")
        heroina.atacar_alvo(zumbi_comum1) # Zumbi Comum: 40 HP - 18 Dano = 22 HP
    exibir_status_geral(participantes)

    # Zumbi comum revida se ainda estiver vivo
    if zumbi_comum1.esta_vivo() and heroina.esta_vivo():
        print(f"Zumbi Comum (Vida: {zumbi_comum1.vida}) revida contra Lyra (Vida: {heroina.vida})")
        zumbi_comum1.atacar_jogador(heroina) # Lyra: 120 HP - 10 Dano = 110 HP
    exibir_status_geral(participantes)

    # Cenário 2: Lyra vs. Zumbi Corredor
    print("\n--- Cenário 2: Lyra enfrenta Zumbi Corredor ---")
    heroina.equipar_arma(arco_curto) # Lyra muda para o Arco Curto
    exibir_status_geral(participantes)
    # Lyra ataca o Zumbi Corredor (30 HP) múltiplas vezes
    print(f"Lyra (Vida: {heroina.vida}) se prepara para atacar Zumbi Corredor (Vida: {zumbi_corredor.vida}) com {arco_curto.nome_arma}.")
    for i in range(3): # Tenta atacar até 3 vezes ou até o zumbi morrer
        if zumbi_corredor.esta_vivo() and heroina.esta_vivo():
            print(f"   Ataque {i+1} de Lyra...")
            heroina.atacar_alvo(zumbi_corredor) # 1º: 30-12=18 HP; 2º: 18-12=6 HP; 3º: 6-12=0 HP
            if not zumbi_corredor.esta_vivo():
                print(f"   Zumbi Corredor foi derrotado no ataque {i+1}!")
                break
        else:
            break # Sai do loop se Lyra ou o zumbi morrerem antes
    exibir_status_geral(participantes)

    # Zumbi corredor tenta atacar (mas provavelmente já estará morto)
    if zumbi_corredor.esta_vivo() and heroina.esta_vivo():
        print(f"Zumbi Corredor (Vida: {zumbi_corredor.vida}) tenta atacar Lyra (Vida: {heroina.vida})")
        zumbi_corredor.atacar_jogador(heroina)
    else:
        if not zumbi_corredor.esta_vivo():
            print(f"Zumbi {zumbi_corredor.tipo_zumbi} (ID: {zumbi_corredor.object_id()}) não pode atacar pois já foi derrotado.")
    exibir_status_geral(participantes)

    # Cenário 3: Zumbi Bruto (Tanque) ataca Lyra
    print("\n--- Cenário 3: Zumbi Bruto (Tanque) ataca Lyra ---")
    if zumbi_bruto.esta_vivo() and heroina.esta_vivo():
        print(f"Zumbi Bruto (Vida: {zumbi_bruto.vida}) ataca Lyra (Vida: {heroina.vida})")
        zumbi_bruto.atacar_jogador(heroina) # Lyra: 110 HP - 15 Dano = 95 HP
    exibir_status_geral(participantes)

    # Cenário 4: Lyra vs. Zumbi Bruto (Tanque) - Combate prolongado
    print("\n--- Cenário 4: Lyra usa Cajado Mágico contra Zumbi Bruto ---")
    heroina.equipar_arma(cajado_magico) # Lyra equipa o Cajado Mágico
    exibir_status_geral(participantes)

    rounds_contra_bruto = 0
    max_rounds = 5 # Limite para evitar loop infinito caso algo dê errado na lógica de dano/vida
    print(f"Lyra (Vida: {heroina.vida}) inicia combate contra Zumbi Bruto (Vida: {zumbi_bruto.vida}) com {cajado_magico.nome_arma}.")
    # Loop de combate: continua enquanto ambos estiverem vivos e dentro do limite de rounds.
    while zumbi_bruto.esta_vivo() and heroina.esta_vivo() and rounds_contra_bruto < max_rounds:
        rounds_contra_bruto += 1
        print(f"\n   --- Round {rounds_contra_bruto} contra Zumbi Bruto ---")

        # Ação do Jogador
        heroina.atacar_alvo(zumbi_bruto) # Cajado: 22 Dano
                                         # Zumbi Bruto: 70 -> 48 -> 26 -> 4 -> 0 (morre no 4º round)

        # Ação do Zumbi (só ataca se ainda estiver vivo após o ataque de Lyra)
        if zumbi_bruto.esta_vivo() and heroina.esta_vivo(): # Verifica vida da heroína também
            zumbi_bruto.atacar_jogador(heroina) # Zumbi Bruto: 15 Dano
                                                # Lyra: 95 -> 80 -> 65 -> 50

        exibir_status_geral(participantes) # Mostra status ao final de cada sub-round

        # Condições de término do combate
        if not heroina.esta_vivo():
            print(f"悲 {heroina.nome_jogador} foi derrotada no round {rounds_contra_bruto}! 悲")
            break
        if not zumbi_bruto.esta_vivo():
            print(f"🎉 Zumbi Bruto foi derrotado por {heroina.nome_jogador} no round {rounds_contra_bruto}! 🎉")
            break
        if rounds_contra_bruto >= max_rounds:
            print(f"Combate contra Zumbi Bruto atingiu o limite de {max_rounds} rounds.")
            break

    # --- FIM DA SIMULAÇÃO ---
    print("\n--- 🏁 Fim da Simulação 🏁 ---")
    if heroina.esta_vivo():
        print(f"🏆 {heroina.nome_jogador} sobreviveu ao encontro com {heroina.vida}/{heroina.vida_maxima} HP! 🏆")
    else:
        print(f"💀 {heroina.nome_jogador} não sobreviveu... 💀")

    print("\n--- Status Final dos Zumbis ---")
    for zumbi in [zumbi_comum1, zumbi_corredor, zumbi_bruto]:
        estado = f"Derrotado (Vida: {zumbi.vida})" if not zumbi.esta_vivo() else f"Vivo (Vida: {zumbi.vida})"
        print(f"- Zumbi {zumbi.tipo_zumbi} (ID: {zumbi.object_id()}): {estado}")


if __name__ == "__main__":
    # Este bloco é executado quando o script main.py é rodado diretamente.
    try:
        main()  # Chama a função principal que executa a simulação.
    except ImportError as e:
        # Tratamento de erro caso algum dos módulos do jogo não seja encontrado.
        print(f"ERRO DE IMPORTAÇÃO em main.py: {e}")
        print("Por favor, certifique-se de que os arquivos 'entidade.py', 'arma.py', "
              "'jogador.py', e 'zumbi.py' estão no mesmo diretório que 'main.py' "
              "ou acessíveis no PYTHONPATH.")
    except Exception as e:
        # Tratamento de erro para qualquer outra exceção inesperada durante a simulação.
        print(f"OCORREU UM ERRO INESPERADO DURANTE A EXECUÇÃO DE MAIN.PY: {e}")
        # Para depuração, pode ser útil imprimir o traceback completo:
        # import traceback
        # traceback.print_exc()
